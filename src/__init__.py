import asyncio

from contextlib import asynccontextmanager
from fastapi import FastAPI

from .routes import include_all_routes
from .scheduler import scheduler


@asynccontextmanager
async def lifespan(_):
    scheduler.start()
    yield
    scheduler.shutdown()


def create_app() -> FastAPI:
    app = FastAPI(lifespan=lifespan)
    include_all_routes(app)

    return app
