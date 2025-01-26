from contextlib import asynccontextmanager

from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from apscheduler.schedulers.background import BackgroundScheduler

from app.api.api import api_router
from app.core.settings import settings
from app.utils.logger import make_logger

app = FastAPI()
logger = make_logger(__name__)
scheduler = BackgroundScheduler()

def batch_job():
    print("Batch job started...")
    time.sleep(5)  # 실제로 뭔가 오래 걸리는 작업이라고 가정
    print("Batch job finished!")


@asynccontextmanager
async def lifespan(app: FastAPI):
    scheduler.add_job(batch_job, "cron", hour=3, minute=0)  # 매일 새벽 3시에 실행
    scheduler.start()
    yield


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
