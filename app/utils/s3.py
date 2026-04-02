import aioboto3
from app.config import MINIO_ENDPOINT, MINIO_ACCESS_KEY, MINIO_SECRET_KEY, MINIO_SECURE

class S3Client:
    def __init__(self):
        self.session = aioboto3.Session()
        self.config = {
            "endpoint_url": f"http://{MINIO_ENDPOINT}",
            "aws_access_key_id": MINIO_ACCESS_KEY,
            "aws_secret_access_key": MINIO_SECRET_KEY,
            "use_ssl": MINIO_SECURE,
        }

    async def upload_file(self, file_content: bytes, object_name: str, bucket: str):
        async with self.session.client("s3", **self.config) as s3:
            await s3.put_object(Bucket=bucket, Key=object_name, Body=file_content)
            return f"http://localhost:9000/{bucket}/{object_name}"

    async def check_connection(self):
        async with self.session.client("s3", **self.config) as s3:
            await s3.list_buckets()
            return True

s3_client = S3Client()