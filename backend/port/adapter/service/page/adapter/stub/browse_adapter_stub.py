from http import HTTPStatus
from typing import override

import requests

from modules.scraper.domain.model.html import HTML
from modules.scraper.domain.model.page import URL, Page
from port.adapter.service.page.adapter import BrowseAdapter


class BrowseAdapterStub(BrowseAdapter):
    @override
    def fetch(self, url: URL) -> Page:
        response = requests.get(url.value)
        return Page(url, HTTPStatus(response.status_code), HTML(response.text))
