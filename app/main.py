from contextlib import asynccontextmanager

from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from app.api.api import api_router
from app.core.settings import settings
from app.utils.logger import make_logger

logger = make_logger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    yield


app = FastAPI()


try:
    app = FastAPI(
        title="reporter",
        openapi_url=f"{settings.API_V1_STR}/openapi.json",
        # lifespan=lifespan,
    )
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.include_router(api_router, prefix=settings.API_V1_STR)

    host, port = "0.0.0.0", 8000
    logger.info(f"Success to run server. {host}:{port}")
except Exception as e:
    logger.error(e)
