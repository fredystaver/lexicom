from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from uvicorn import run

from task_1.core.redis import setup_redis_connection, close_redis_connection
from task_1.router import router
from task_1.core.settings import get_settings, Settings


def main() -> None:
    settings = get_settings()
    run(
        app=create_app(settings=settings),
        host=settings.api.host,
        port=settings.api.port,
    )


def create_app(settings: Settings) -> FastAPI:
    app = FastAPI(title=settings.api.title)

    app.add_middleware(
        CORSMiddleware,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.state.settings = settings

    app.add_event_handler(
        event_type="startup", func=setup_redis_connection(app=app, settings=settings.redis)
    )
    app.add_event_handler(
        event_type="startup", func=close_redis_connection(app=app)
    )

    app.include_router(router=router)

    return app
