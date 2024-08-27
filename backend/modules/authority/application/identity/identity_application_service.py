from __future__ import annotations

import os

from injector import singleton, inject

from exception import SystemException, ErrorCode
from modules.authority.application.identity.command import ProvisionTenantCommand, AuthenticateUserCommand, \
    RefreshCommand, RevokeCommand, ForgotPasswordCommand, ResetPasswordCommand
from modules.authority.application.identity.dpo import TenantDpo, SessionDpo, UserDpo
from modules.authority.application.identity.subscriber import UserProvisionedSubscriber, PasswordForgotSubscriber
from modules.authority.domain.model.mail import SendMailService
from modules.authority.domain.model.session import SessionRepository
from modules.authority.domain.model.tenant import Tenant, TenantRepository
from modules.authority.domain.model.tenant.project import ProjectRepository
from modules.authority.domain.model.user import User, UserRepository, EmailAddress, Token
from modules.common.application import transactional
from modules.common.domain.model import DomainEventPublisher


@singleton
class IdentityApplicationService:
    @inject
    def __init__(self,
                 project_repository: ProjectRepository,
                 send_mail_service: SendMailService,
                 session_repository: SessionRepository,
                 tenant_repository: TenantRepository,
                 user_repository: UserRepository):
        self.project_repository = project_repository
        self.send_mail_service = send_mail_service
        self.session_repository = session_repository
        self.tenant_repository = tenant_repository
        self.user_repository = user_repository

    @transactional
    def provision_tenant(self, command: ProvisionTenantCommand) -> TenantDpo:
        """テナントを登録

        テナントを登録する際に以下の情報も登録する。

        - ユーザー : 認証/認可の単位となる概念であり、サービスを利用する実体。
                    テナント登録時にテナントの管理者として、登録する。
        - プロジェクト : テナントはいくつかのプロジェクトを管理することができる。
                       会社の場合は、各部署ごとにプロジェクトを作成し、操作する。
                       テナント登録時は、’No Project’というプロジェクトを登録し、ユーザーはそのプロジェクト以下で操作する。

        また、ユーザーが登録されたときに、メアド検証メールを送信する。
        """
        # サブスクライバを登録
        DomainEventPublisher.instance().subscribe(UserProvisionedSubscriber())

        # テナントを作成
        tenant_id = self.tenant_repository.next_identity()
        tenant = Tenant.provision(tenant_id, command.tenant.name)

        # ユーザーを新規作成
        user_id = self.user_repository.next_identity()
        user = User.provision(
            user_id,
            command.user.username,
            EmailAddress(command.user.email_address),
            command.user.plain_password
        )

        # ユーザーをテナントに管理者として追加
        tenant.register_admin_member(user)
        # プロジェクトを作成
        project_id = self.project_repository.next_identity()
        project = tenant.create_project(project_id, 'Default Project')

        self.user_repository.add(user)
        self.tenant_repository.add(tenant)
        self.project_repository.add(project)
        return TenantDpo(tenant)

    @transactional
    def verify_email(self, verification_token: str) -> None:
        """メアド検証トークン指定でユーザーを有効化し、セッションを発行する"""
        user = self.user_repository.user_with_token(verification_token)
        if user is None or user.token_with(verification_token).has_expired():
            raise SystemException(ErrorCode.VALID_TOKEN_DOES_NOT_EXISTS, f"{verification_token}は無効なトークンです。")

        user.verified()
        self.user_repository.add(user)

    def user_with_token(self, value: str) -> UserDpo:
        session = self.session_repository.session_with_token(value)
        if session is None or session.token_with(value).has_expired():
            raise SystemException(ErrorCode.SESSION_DOES_NOT_FOUND, f"トークン {value} に該当するセッションが見つかりません。")

        user = self.user_repository.get(session.user_id)
        tenants = self.tenant_repository.tenants_with_user_id(user.id)
        return UserDpo(user, tenants)

    @transactional
    def authenticate(self, command: AuthenticateUserCommand) -> SessionDpo:
        """ユーザー認証し、セッションを発行する"""
        email_address = EmailAddress(command.email_address)
        user = self.user_repository.user_with_email_address(email_address)

        # 該当ユーザーが存在するか、パスワードは一致しているか
        if user is None or not user.verify_password(command.password):
            raise SystemException(ErrorCode.LOGIN_BAD_CREDENTIALS,
                                  f"メールアドレス {email_address.text} のユーザーが見つかりませんでした。")

        # メールアドレス検証が終わっていない場合は、確認メールを再送信する
        if not user.is_verified():
            user.generate(Token.Type.VERIFICATION)
            self.user_repository.add(user)
            raise SystemException(ErrorCode.USER_IS_NOT_VERIFIED, "メールアドレスの検証が完了していません。確認メールを送信しました。")

        session = user.login(self.session_repository.next_identity())
        self.session_repository.save(session)

        return SessionDpo(session)

    @transactional
    def refresh(self, command: RefreshCommand) -> SessionDpo:
        """セッションを更新する"""
        session = self.session_repository.session_with_token(command.refresh_token)
        if session is None or session.token_with(command.refresh_token).has_expired():
            raise SystemException(ErrorCode.SESSION_DOES_NOT_FOUND, f'{command.refresh_token} は無効なリフレッシュトークンです。')

        session.refresh(command.refresh_token)
        self.session_repository.save(session)

        return SessionDpo(session)

    @transactional
    def revoke(self, command: RevokeCommand) -> None:
        """セッションを削除して、ログアウトする"""
        session = self.session_repository.session_with_token(command.token)
        if session is None or session.token_with(command.token).has_expired():
            raise SystemException(ErrorCode.SESSION_DOES_NOT_FOUND, f'{command.token} は無効なリフレッシュトークンです。')

        self.session_repository.remove(session)

    def user_with_session(self, token: str) -> UserDpo | None:
        """セッションのトークン指定でユーザー情報を取得"""
        session = self.session_repository.session_with_token(token)
        if session is None or session.token_with(token).has_expired():
            return None

        user = self.user_repository.get(session.user_id)
        tenants = self.tenant_repository.tenants_with_user_id(session.user_id)
        return UserDpo(user, tenants)

    @transactional
    def forgot_password(self, command: ForgotPasswordCommand) -> None:
        email_address = EmailAddress(command.email_address)
        user = self.user_repository.user_with_email_address(email_address)
        if user is None:
            raise SystemException(
                ErrorCode.USER_DOES_NOT_FOUND,
                f"{email_address.text} に紐づくユーザーが見つからなかったため、パスワードリセットメールを送信できませんでした。",
            )

        # サブスクライバを登録
        DomainEventPublisher.instance().subscribe(PasswordForgotSubscriber())

        user.generate(Token.Type.PASSWORD_RESET)
        self.user_repository.add(user)

    @transactional
    def reset_password(self, command: ResetPasswordCommand) -> None:
        """新しく設定したパスワードとパスワードリセットトークン指定で新しいパスワードに変更する"""
        user = self.user_repository.user_with_token(command.reset_token)
        if user is None or user.token_with(command.reset_token).has_expired():
            raise SystemException(
                ErrorCode.VALID_TOKEN_DOES_NOT_EXISTS,
                f"指定したトークン {command.reset_token} は無効なのでパスワードをリセットできません。",
            )

        user.reset_password(command.password, command.reset_token)
        self.user_repository.add(user)
