from app.dao.base import BaseDAO
from app.memes.models import Memes


class MemesDAO(BaseDAO):
    model = Memes

