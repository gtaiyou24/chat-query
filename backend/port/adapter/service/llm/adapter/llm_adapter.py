import abc

from modules.analytics.domain.model.llm import Messages


class LLMAdapter(abc.ABC):
    @abc.abstractmethod
    def chat(self, messages: Messages) -> Messages:
        pass
