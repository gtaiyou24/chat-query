import abc

from modules.scraper.domain.model.page import URL, Page


class BrowseAdapter(abc.ABC):
    @abc.abstractmethod
    def fetch(self, url: URL) -> Page:
        pass
