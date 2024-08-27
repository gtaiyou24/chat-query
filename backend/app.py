import os
from contextlib import asynccontextmanager

from di import DIContainer, DI
from dotenv import load_dotenv
from fastapi.exceptions import RequestValidationError
from slf4py import create_logger
from fastapi import FastAPI, Request
from fastapi.encoders import jsonable_encoder
from sqlalchemy import create_engine, Engine
from starlette import status
from starlette.middleware.cors import CORSMiddleware
from starlette.responses import JSONResponse

from exception import SystemException
from modules.authority.domain.model.mail import SendMailService
from modules.authority.domain.model.session import SessionRepository
from modules.authority.domain.model.tenant import TenantRepository
from modules.authority.domain.model.tenant.project import ProjectRepository
from modules.authority.domain.model.user import UserRepository, EncryptionService
from modules.common.application import UnitOfWork
from port.adapter.persistence.repository.inmem import InMemSessionRepository, InMemTenantRepository, \
    InMemUserRepository, InMemProjectRepository, InMemUnitOfWork
from port.adapter.persistence.repository.mysql import DataBase, MySQLUnitOfWork
from port.adapter.persistence.repository.mysql.project import MySQLProjectRepository
from port.adapter.persistence.repository.mysql.session import MySQLSessionRepository
from port.adapter.persistence.repository.mysql.tenant import MySQLTenantRepository
from port.adapter.persistence.repository.mysql.user import MySQLUserRepository
from port.adapter.resource.auth import AuthResource
from port.adapter.resource.health import HealthResource
from port.adapter.resource.tenant.member import MemberResource
from port.adapter.resource.tenant.tenant_resource import TenantResource
from port.adapter.resource.user import UserResource
from port.adapter.service.mail import SendMailServiceImpl
from port.adapter.service.mail.adapter import MailDeliveryAdapter
from port.adapter.service.mail.adapter.gmail import GmailAdapter
from port.adapter.service.mail.adapter.mailhog import MailHogAdapter
from port.adapter.service.mail.adapter.sendgrid import SendGridAdapter
from port.adapter.service.mail.adapter.stub import MailDeliveryAdapterStub
from port.adapter.service.user import EncryptionServiceImpl


@asynccontextmanager
async def lifespan(app: FastAPI):
    """API 起動前と終了後に実行する処理を記載する"""
    load_dotenv(os.path.join(os.path.dirname(__file__), '.env'))

    if "MySQL" in os.getenv("DI_PROFILE_ACTIVES", []):
        engine = create_engine(os.getenv("DATABASE_URL"), echo=os.getenv("SLF4PY_LOG_LEVEL", "DEBUG") == "DEBUG")
        DIContainer.instance().register(DI.of(Engine, {}, engine))
        DataBase.metadata.create_all(bind=engine)

    DIContainer.instance().register(
        # Persistence
        DI.of(UnitOfWork, {"MySQL": MySQLUnitOfWork}, InMemUnitOfWork),
        DI.of(ProjectRepository, {"MySQL": MySQLProjectRepository}, InMemProjectRepository),
        DI.of(SessionRepository, {"MySQL": MySQLSessionRepository}, InMemSessionRepository),
        DI.of(TenantRepository, {"MySQL": MySQLTenantRepository}, InMemTenantRepository),
        DI.of(UserRepository, {"MySQL": MySQLUserRepository}, InMemUserRepository),
        # Service
        DI.of(SendMailService, {}, SendMailServiceImpl),
        DI.of(EncryptionService, {}, EncryptionServiceImpl),
        # Adapter
        DI.of(
            MailDeliveryAdapter,
            {"SendGrid": SendGridAdapter, "MailHog": MailHogAdapter, "Gmail": GmailAdapter},
            MailDeliveryAdapterStub
        ),
    )
    yield
    # 終了後


app = FastAPI(title="Analytics GPT", root_path=os.getenv("OPENAPI_PREFIX"), lifespan=lifespan)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(AuthResource().router)
app.include_router(HealthResource().router)
app.include_router(TenantResource().router)
app.include_router(MemberResource().router)
app.include_router(UserResource().router)


@app.exception_handler(SystemException)
async def system_exception_handler(request: Request, exception: SystemException):
    exception.logging()
    return JSONResponse(
        status_code=exception.error_code.http_status,
        content=jsonable_encoder(
            {
                "type": exception.error_code.name,
                "title": exception.error_code.message,
                "status": exception.error_code.http_status,
                "instance": str(request.url),
            }
        ),
    )


@app.exception_handler(ValueError)
async def value_error_handler(request: Request, error: ValueError):
    logger = create_logger()
    logger.error(error)
    return JSONResponse(
        status_code=400,
        content=jsonable_encoder(
            {"type": "CLIENT_2001", "title": "不正なリクエストです", "status": 400, "instance": str(request.url)}
        )
    )


@app.exception_handler(AssertionError)
async def assertion_error_handler(request: Request, error: AssertionError):
    logger = create_logger()
    logger.error(error)
    return JSONResponse(
        status_code=400,
        content=jsonable_encoder(
            {"type": "CLIENT_2002", "title": "不正なリクエストです", "status": 400, "instance": str(request.url)}
        ),
    )


@app.exception_handler(RequestValidationError)
async def request_validation_error_handler(request: Request, error: RequestValidationError):
    logger = create_logger()
    logger.error(error)
    return JSONResponse(content={}, status_code=status.HTTP_422_UNPROCESSABLE_ENTITY)


@app.exception_handler(Exception)
async def exception_handler(request: Request, error: Exception):
    logger = create_logger()
    logger.error(error)
    return JSONResponse(
        status_code=500,
        content=jsonable_encoder(
            {"type": "CLIENT_1000", "title": "エラーが発生しました", "status": 500, "instance": str(request.url)}
        ),
    )
