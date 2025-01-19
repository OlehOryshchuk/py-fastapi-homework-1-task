from datetime import datetime
from decimal import Decimal

from pydantic import (
    BaseModel,
    PositiveInt,
    Field,
    NonNegativeInt,
    AnyHttpUrl
)


class MovieDetailResponseSchem(BaseModel):
    id: PositiveInt
    name: str
    date: datetime.date
    score: float
    genre: str = Field(..., max_length=255)
    overview: str
    crew: str
    orig_title: str = Field(..., max_length=255)
    status: str = Field(..., max_length=50)
    orig_lan: str = Field(..., max_length=50)
    budget: Decimal = Field(
        ..., ge=0, le=10**8 - 1, multiple_of=0.01
    )
    revenue: float
    country: Field(..., max_length=3)


class MovieListResponseSchema(BaseModel):
    movies: list[MovieDetailResponseSchem]
    prev_page: AnyHttpUrl
    next_page: AnyHttpUrl
    total_pages: NonNegativeInt
    total_items: NonNegativeInt
