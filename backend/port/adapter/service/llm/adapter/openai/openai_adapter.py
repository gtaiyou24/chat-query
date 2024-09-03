from typing import override

from openai import OpenAI

from modules.analytics.domain.model.llm import Messages, Message
from port.adapter.service.llm.adapter import LLMAdapter


class OpenAIAdapter(LLMAdapter):
    def __init__(self, api_key: str, model_name: str):
        self.__client = OpenAI(api_key=api_key)
        self.__model_name = model_name

    @override
    def chat(self, messages: Messages) -> Messages:
        response = self.__client.chat.completions.create(
            model=self.__model_name,
            messages=[{"role": m.role.value, "content": m.content} for m in messages.list],
            response_format={"type": "text"},
            temperature=0
        )
        content: str = response.choices[0].message.content
        return messages.replay(Message.Role.ASSISTANT(content))
