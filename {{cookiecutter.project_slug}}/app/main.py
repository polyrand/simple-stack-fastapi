import time


from app.resources import client
from app.api.api_v1.api import api_router
from app.db import database, init_db
from app.config import settings
from app.views.router import views_router


import sentry_sdk
from sentry_sdk.integrations.asgi import SentryAsgiMiddleware

from fastapi import FastAPI, Request
from starlette.middleware.cors import CORSMiddleware

app = FastAPI(
    title=settings.PROJECT_NAME, openapi_url=f"{settings.API_V1_STR}/openapi.json"
)

sentry_sdk.init(dsn=settings.SENTRY_DSN)
app.add_middleware(SentryAsgiMiddleware)

# Set all CORS enabled origins
if settings.BACKEND_CORS_ORIGINS:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )


@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    return response


app.include_router(views_router)
app.include_router(api_router, prefix=settings.API_V1_STR)


@app.on_event("startup")
async def startup():

    # connect first
    await database.connect()

    # now we can init
    init_db()


@app.on_event("shutdown")
async def shutdown():
    # close httpx client
    await client.aclose()

    # disconnect db
    await database.disconnect()
