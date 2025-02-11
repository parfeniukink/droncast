from typing import Iterable

from fastapi import APIRouter, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware import _MiddlewareFactory

from src import http
from src.config import settings
from src.infrastructure import middleware


def asgi_app_factory(
    *_,
    rest_routers: Iterable[APIRouter],
    middlewares: Iterable[tuple[_MiddlewareFactory, dict]] | None = None,
    **kwargs,
) -> FastAPI:
    # initialize the base fastapi application
    app = FastAPI(**kwargs)

    # include rest api routers
    for router in rest_routers:
        app.include_router(router)

    # define middlewares using fastapi hook
    if middlewares is not None:
        for middleware_class, options in middlewares:
            app.add_middleware(middleware_class, **options)

    return app


app: FastAPI = asgi_app_factory(
    debug=settings.debug,
    rest_routers=(http.resources.router,),
    middlewares=(
        (CORSMiddleware, middleware.FASTAPI_CORS_MIDDLEWARE_OPTIONS),
    ),
    exception_handlers=(),
)
