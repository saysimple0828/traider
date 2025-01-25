from abc import ABC, abstractmethod
from datetime import timedelta
from typing import Any

import boto3
from botocore.client import Config
from minio import Minio

from app.core.settings import settings
from app.utils.logger import make_logger

AWS_S3 = "s3"
logger = make_logger(__name__)


class CloudStorage(ABC):
    @abstractmethod
    def get_keys_from_bucket(self, bucket_name: str, key_prefix: str):
        pass

    def get_object(self, bucket_name: str, key: str):
        pass


# AWS와 호환되기 때문에,
class MinioStorage(CloudStorage, ABC):
    def __init__(self):
        self.aws_s3_client = boto3.client(
            "s3",
            endpoint_url=settings.s3_endpoint_url,
            aws_access_key_id=settings.s3_access_key,
            aws_secret_access_key=settings.s3_secret_key,
            config=Config(signature_version="s3v4"),
            region_name="ap-northeast-2",
            verify=False,
        )

    # 특정 path의 하위 s3 key를 모두 가지고 온다.
    # 주의 : AWS S3의 key의 경우, 맨 앞에 /가 붙지 않는다.
    #       ex) a/b/c/d/e .....
    def get_keys_from_bucket(self, bucket_name: str, key_prefix: str = ""):
        s3_response = self.aws_s3_client.list_objects_v2(
            Bucket=bucket_name,
            Prefix=key_prefix,
        )

        # 조건에 맞는 return이 없을 때, Contents가 뜨지 않으므로, KeyCount로 판단한다.
        if s3_response.get("KeyCount") == 0:
            return []

        s3_object_key = [
            s3_object_metadata.get("Key")
            for s3_object_metadata in s3_response.get("Contents")
        ]

        return s3_object_key

    def get_object(self, bucket_name: str, key: str) -> Any:
        s3_object = self.aws_s3_client.get_object(Bucket=bucket_name, Key=key)
        s3_object_binary_data = s3_object["Body"].read()
        return s3_object_binary_data

    def put_object(self, bucket_name: str, key: str, data: bytes):
        result = self.aws_s3_client.put_object(
            Bucket=bucket_name, Key=key, Body=data, ContentType="binary/octet-stream"
        )

        return result

    def get_presigned_url(self, bucket_name: str, key: str) -> str:
        """프론트에서 업로드 할 수 있는 URL 생성

        Args:
            bucket_name (str): 버킷 네임
            key (str): 업로드 할 파일 경로

        Returns:
            dict: S3Object
        """
        result = self.aws_s3_client.generate_presigned_url(
            "put_object",
            Params={
                "Bucket": bucket_name,
                "Key": key,
            },
            ExpiresIn=3600,
            HttpMethod="PUT",
        )

        return result

    def delete_object(self, bucket_name: str, key: str):
        result = self.aws_s3_client.delete_object(Bucket=bucket_name, Key=key)
        return result
