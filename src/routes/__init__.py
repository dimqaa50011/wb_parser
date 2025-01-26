from fastapi import FastAPI

from .v1 import router as router_v1


def include_all_routes(app: FastAPI):
    app.include_router(router_v1)
