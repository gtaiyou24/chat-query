from fastapi import APIRouter

from port.adapter.resource import APIResource


class HealthResource(APIResource):
    def __init__(self):
        self.router = APIRouter(prefix="/health", tags=["Common"])
        self.router.add_api_route("/check", self.check, methods=["GET"])

    def check(self) -> dict:
        return {"health": True}
