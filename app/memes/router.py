from fastapi import APIRouter, UploadFile, Depends, Query

from app.exceptions import EmpyMemesStorageException, ErrorLoadingImageToS3Exception
from app.memes.dao import MemesDAO
from app.s3.s3client import S3Client
from app.users.dependencies import get_current_user
from app.users.models import Users

router = APIRouter(
    prefix='/memes',
    tags=['Работа с мемами']
)


@router.get('')
async def get_memes(page: int = Query(1, ge=1), limit: int = Query(10, ge=1, le=100)):
    all_memes = await MemesDAO.find_all()

    start = (page - 1) * limit
    end = start + limit
    memes_slice = all_memes[start:end]

    if not memes_slice:
        raise EmpyMemesStorageException

    return memes_slice


@router.get('/{meme_id}')
async def get_meme_by_id(meme_id: int):
    image = await MemesDAO.find_by_id(meme_id)
    if not image:
        raise EmpyMemesStorageException

    return image


@router.post('')
async def add_meme(
        title: str,
        upload_file: UploadFile,
        user: Users = Depends(get_current_user) # noqa
):
    s3_client = S3Client()

    image_url_in_s3 = await s3_client.upload_file(upload_file.file, upload_file.filename)
    if not image_url_in_s3:
        raise ErrorLoadingImageToS3Exception

    new_image = await MemesDAO.add(title=title, s3_image_url=image_url_in_s3)

    return new_image


@router.put('/{meme_id}')
async def update_meme(
        meme_id: int,
        title: str
):
    image = await MemesDAO.find_by_id(meme_id)
    if not image:
        raise EmpyMemesStorageException

    updated_image = await MemesDAO.update(model_id=meme_id, title=title)
    return updated_image


@router.delete('/{meme_id}')
async def del_meme(
        meme_id: int,
        user: Users = Depends(get_current_user) # noqa
):
    current_meme = await MemesDAO.find_by_id(meme_id)
    if not current_meme:
        raise EmpyMemesStorageException

    await MemesDAO.delete(id=meme_id)

