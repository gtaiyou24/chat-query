from typing import override

from openai import OpenAI

from modules.scraper.domain.model.llm import Messages, LLMService, Prompt
from port.adapter.service.llm.adapter import LLMAdapter


class OpenAIAdapter(LLMAdapter):
    def __init__(self, api_key: str, model_name: str):
        self.__client = OpenAI(api_key=api_key)
        self.__model_name = model_name

    @override
    def chat(self, messages: Messages, format: LLMService.Format) -> Messages:
        response = self.__client.chat.completions.create(
            model=self.__model_name,
            messages=[{"role": prompt.role.value, "content": prompt.content} for prompt in messages.prompts],
            response_format={"type": "json_object"}
        )
        content: str = response.choices[0].message.content
        messages = messages.append(Prompt.Role.ASSISTANT.make(content))
        return messages
