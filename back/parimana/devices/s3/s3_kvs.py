from pathlib import Path
from typing import Optional

import boto3
from botocore.exceptions import ClientError

from parimana.io.kvs import Storage
from parimana.io.message import mprint


class S3Storage(Storage):
    def __init__(self, bucket, prefix: str = ""):
        self.s3client = boto3.client("s3")
        self.bucket = bucket
        self.prefix = prefix

    def exists(self, key: str) -> bool:
        try:
            self.s3client.head_object(Bucket=self.bucket, Key=self._get_key(key))
            return True

        except ClientError as e:
            if e.response["Error"]["Code"] == "404":
                return False
            else:
                raise

    def read_binary(self, key: str) -> Optional[bytes]:
        if self.exists(key):
            mprint(f"reading s3://{self.bucket}/{self._get_key(key)} ...")
            response = self.s3client.get_object(
                Bucket=self.bucket, Key=self._get_key(key)
            )
            return response["Body"].read()

        else:
            return None

    def write_binary(self, key: str, binary: bytes) -> None:
        mprint(f"writing s3://{self.bucket}/{self._get_key(key)} ...")
        self.s3client.put_object(
            Bucket=self.bucket, Key=self._get_key(key), Body=binary
        )

    def _get_key(self, key: str) -> Path:
        return f"{self.prefix}{key}"
