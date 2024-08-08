from di import DIContainer
from fastapi import HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer

from modules.authority.application.identity import IdentityApplicationService
from modules.authority.application.identity.dpo import UserDpo

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")


async def get_current_user(token: str = Depends(oauth2_scheme)) -> UserDpo:
    application_service = DIContainer.instance().resolve(IdentityApplicationService)
    return application_service.user_with_token(token)


async def get_current_active_user(current_user: UserDpo = Depends(get_current_user)) -> UserDpo:
    if not current_user.user.is_verified():
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user
