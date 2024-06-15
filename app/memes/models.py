from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class Memes(Base):
    __tablename__ = 'memes'

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(nullable=False)
    s3_image_url: Mapped[str] = mapped_column(nullable=False, unique=True)

    def __str__(self):
        return f"Мем #{self.id}"

