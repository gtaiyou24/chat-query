from typing import override

from injector import singleton, inject

from modules.scraper.domain.model.page import PageService, URL, Page
from port.adapter.service.page.adapter import BrowseAdapter


@singleton
class PageServiceImpl(PageService):
    @inject
    def __init__(self, browse_adapter: BrowseAdapter):
        self.__browse_adapter = browse_adapter

    @override
    def fetch(self, url: URL) -> Page:
        return self.__browse_adapter.fetch(url)
