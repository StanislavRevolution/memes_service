from fastapi import UploadFile
from pydantic import BaseModel


class SMemes(BaseModel):
    title: str
    file_to_upload: UploadFile


