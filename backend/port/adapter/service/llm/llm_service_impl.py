from typing import override, Literal

from injector import inject

from modules.scraper.domain.model.llm import LLMService, Messages
from port.adapter.service.llm.adapter import LLMAdapter


class LLMServiceImpl(LLMService):
    @inject
    def __init__(self, llm_adapter: LLMAdapter):
        self.__llm_adapter = llm_adapter

    @override
    def chat(self, messages: Messages, format_: Literal['json', 'text'] = 'text') -> Messages:
        return self.__llm_adapter.chat(messages, LLMService.Format.value_of(format_))
