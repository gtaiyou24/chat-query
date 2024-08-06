import abc

from modules.scraper.domain.model.llm import Messages, LLMService


class LLMAdapter(abc.ABC):
    @abc.abstractmethod
    def chat(self, messages: Messages, format: LLMService.Format) -> Messages:
        pass
