from uuid import UUID
from datetime import datetime
from typing import Optional
from bson.binary import Binary

from pydantic import BaseModel, Field

from src.models.mixin import JsonMixin


class BaseLike(BaseModel):
    index: Optional[str]  # Index _id field
    user_id: Binary
    added_at: datetime
    value: int = Field(None, ge=0, le=10)


class FilmLike(BaseLike):
    # ключи шардирования film_id, user_id
    film_id: Binary


class BaseLikeAPI(BaseModel):
    index: Optional[str]  # Index _id field
    user_id: UUID
    added_at: datetime
    value: int = Field(None, ge=0, le=10)


class FilmLikeAPI(BaseLikeAPI):
    # ключи шардирования film_id, user_id
    film_id: UUID


class ReviewLike(BaseLike):
    # ключи шардирования review_id, user_id
    review_id: str


class ReviewLikeAPI(BaseLikeAPI):
    # ключи шардирования review_id, user_id
    review_id: str


class Review(BaseModel):
    # ключи шардирования film_id, user_id
    index: Optional[str]  # Index _id field
    film_id: Binary
    user_id: Binary
    text: str
    published_at: datetime
    edited_at: Optional[datetime]


class ReviewAPI(BaseModel):
    # ключи шардирования film_id, user_id
    id: Optional[str]  # Index _id field
    film_id: UUID
    user_id: UUID
    text: str
    published_at: datetime
    edited_at: Optional[datetime]


class Bookmark(BaseModel):
    # ключи шардирования user_id, film_id
    index: Optional[str]  # Index _id field
    film_id: Binary
    user_id: Binary
    added_at: datetime


class BookmarkAPI(BaseModel):
    # ключи шардирования user_id, film_id
    id: Optional[str]  # Index _id field
    film_id: UUID
    user_id: UUID
    added_at: datetime
