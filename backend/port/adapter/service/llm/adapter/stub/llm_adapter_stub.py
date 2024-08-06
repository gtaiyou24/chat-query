from typing import override

from modules.scraper.domain.model.llm import LLMService, Messages, Prompt
from port.adapter.service.llm.adapter import LLMAdapter


class LLMAdapterStub(LLMAdapter):
    @override
    def chat(self, messages: Messages, format: LLMService.Format) -> Messages:
        prompt = Prompt.Role.ASSISTANT.make('stub content')
        return messages.append(prompt)
