from fastapi import APIRouter

from app.utils.s3_utils import MinioStorage
from app.utils.logger import make_logger

router = APIRouter(prefix="/s3")

logger = make_logger(__name__)


@router.get("/get_presigned_url")
async def get_presigned_url(
    bucket_name: str,
    key: str,
) -> str:
    minio = MinioStorage()
    presigned_url = minio.get_presigned_url(bucket_name=bucket_name, key=key)

    return presigned_url


@router.delete("/delete_object")
async def delete_object(
    bucket_name: str,
    key: str,
):
    minio = MinioStorage()
    deleted_obj = minio.delete_object(bucket_name=bucket_name, key=key)

    return deleted_obj
