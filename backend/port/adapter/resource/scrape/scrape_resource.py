from di import DIContainer
from fastapi import APIRouter

from modules.scraper.application.scrape import ScrapeApplicationService
from port.adapter.resource import APIResource
from port.adapter.resource.scrape.request import ScrapeRequest


class ScrapeResource(APIResource):
    router = APIRouter(prefix="/scrape")

    def __init__(self):
        self.__scrape_application_service = None
        self.router.add_api_route("/", self.scrape, methods=["POST"], response_model=dict, name="スクレイピング")

    @property
    def scrape_application_service(self) -> ScrapeApplicationService:
        self.__scrape_application_service = (
            self.__scrape_application_service or DIContainer.instance().resolve(ScrapeApplicationService)
        )
        return self.__scrape_application_service

    def scrape(self, request: ScrapeRequest) -> dict:
        """スクレイピング"""
        return self.scrape_application_service.scrape(request.url, request.html, request.json_schema)
