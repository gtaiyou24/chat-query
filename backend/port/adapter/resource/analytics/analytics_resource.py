from di import DIContainer
from fastapi import APIRouter, Depends

from modules.analytics.application import ChatApplicationService
from modules.authority.application.identity.dpo import UserDpo
from port.adapter.resource import APIResource
from port.adapter.resource.analytics.request import ChatRequest
from port.adapter.resource.analytics.response import ChatResponse, DataSetResponse
from port.adapter.resource.dependency import get_current_active_user


class AnalyticsResource(APIResource):
    router = APIRouter(prefix="/analytics", tags=["分析"])

    def __init__(self):
        self.__chat_application_service = None
        self.router.add_api_route("/chat", self.chat, methods=["POST"], response_model=ChatResponse, name="チャット")
        self.router.add_api_route("/dataset", self.dataset, methods=["POST"], response_model=DataSetResponse, name="データセット取得")

    @property
    def chat_application_service(self) -> ChatApplicationService:
        self.__chat_application_service = (
            self.__chat_application_service or DIContainer.instance().resolve(ChatApplicationService)
        )
        return self.__chat_application_service

    def chat(self, request: ChatRequest, current_user: UserDpo = Depends(get_current_active_user)) -> ChatResponse:
        messages = [{message.role: message.content} for message in request.messages]
        reply = self.chat_application_service.chat(messages)
        return ChatResponse([])

    def dataset(self, request: ChatRequest) -> DataSetResponse:
        dpo = self.chat_application_service.dataset(request.messages[-1].content)
        return DataSetResponse.from_(dpo)
