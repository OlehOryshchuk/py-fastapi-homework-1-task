from typing import (
    Annotated
)

from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    Query,
)
from sqlalchemy.orm import Session
from sqlalchemy import (
    select
)

from src.database import get_db, MovieModel
from src.schemas.movies import (
    MovieListResponseSchema,
    MovieDetailResponseSchema,
)
from src.schemas.paginations import (
    PaginationQuerySchema
)
from src.routes.paginations import (
    get_paginated_response,
    get_paginate_query
)


router = APIRouter()


@router.get("/movies/", response_model=MovieListResponseSchema)
async def list_movies(
        q: Annotated[PaginationQuerySchema, Query()],
        db: Session = Depends(get_db),
):
    query = select(MovieModel)
    paginated = get_paginate_query(
        query=query, page=q.page, per_page=q.per_page
    )
    paginated_res = get_paginated_response(
        db=db, per_page=q.per_page, page=q.page,
        query=query, url_path="/theater/movies/"
    )
    movies = db.scalars(paginated).all()

    if not movies:
        raise HTTPException(status_code=404, detail="No movies found.")

    return MovieListResponseSchema(
        movies=movies,
        **paginated_res
    )


@router.get("/movies/{movie_id}/", response_model=MovieDetailResponseSchema)
async def detail_movie(movie_id: int, db: Session = Depends(get_db)):
    movie = db.get(MovieModel, movie_id)

    if not movie:
        raise HTTPException(
            status_code=404,
            detail="Movie with the given ID was not found."
        )
    return movie
