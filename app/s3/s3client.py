import asyncio
from contextlib import asynccontextmanager
from typing import BinaryIO

from aiobotocore.session import get_session
import botocore.exceptions

from app.config import settings


class S3Client:

    def __init__(self):
        self.config = {
            "aws_access_key_id": settings.ACCESS_KEY,
            "aws_secret_access_key": settings.SECRET_KEY,
            "endpoint_url": settings.ENDPOINT_URL,
        }

        self.bucket_name = settings.BUCKET_NAME
        self.session = get_session()

    @asynccontextmanager
    async def get_client(self):
        async with self.session.create_client('s3', **self.config) as client:
            yield client

    async def upload_file(
            self,
            file: BinaryIO,
            object_name: str
    ):
        try:
            async with self.get_client() as client:
                await client.put_object(
                    Bucket=self.bucket_name,
                    Key=object_name,
                    Body=file
                )

            return f'{settings.S3_IMAGE_PRE_LINK}/{object_name}'

        except botocore.exceptions.ClientError as err:
            if err.response['Error']['Code'] == 'InternalError':
                print('Error Message: {}'.format(err.response['Error']['Message']))
                print('Request ID: {}'.format(err.response['ResponseMetadata']['RequestId']))
                print('Http code: {}'.format(err.response['ResponseMetadata']['HTTPStatusCode']))
            return None
