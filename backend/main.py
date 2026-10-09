from fastapi import FastAPI, HTTPException, Depends
from backend.models import AnimeCreate, Anime, AnimeUpdate, AnimeReadWithStats
from backend.models import ReviewCreate, Review
from backend.models import UserCreate, User
from contextlib import asynccontextmanager
from sqlmodel import SQLModel, Session, select
from backend.database import engine, get_session
from fastapi.middleware.cors import CORSMiddleware


@asynccontextmanager
async def lifespan(app: FastAPI):
    SQLModel.metadata.create_all(engine) 
    yield
    SQLModel.metadata.clear()

app = FastAPI(lifespan=lifespan)

origins = [
    "http://localhost:5173"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/animes")
async def get_all_animes(session: Session = Depends(get_session)):
    statement = select(Anime)
    results = session.exec(statement)
    return results.all()


@app.get("/animes/{anime_id}")
async def get_anime_by_id(anime_id: int, session: Session = Depends(get_session)):
    statement = select(Anime).where(Anime.id == anime_id)
    anime = session.exec(statement).one_or_none()
    if anime is None:
        raise HTTPException(status_code=404)

    avg_rating = 0
    count = 0

    if anime.reviews:
        count = len(anime.reviews)
        avg_rating = sum(r.rating for r in anime.reviews) / count

    result = AnimeReadWithStats(id=anime_id, name=anime.name, release_year=anime.release_year, average_rating=avg_rating, review_count=count)
    return result


@app.post("/animes", status_code=201)
async def create_anime(anime: AnimeCreate, session: Session = Depends(get_session)) -> Anime:
    try:
        response = Anime.model_validate(anime)
        session.add(response)
        session.commit()
        session.refresh(response)
        return response
    except Exception as e:
        raise HTTPException(status_code=400)


@app.delete("/animes/{anime_id}")
async def delete_anime_by_id(anime_id: int, session: Session = Depends(get_session)):
    get_statement = select(Anime).where(Anime.id == anime_id)
    anime = session.exec(get_statement).one_or_none()

    if anime is None:
        raise HTTPException(status_code=404)

    session.delete(anime)
    session.commit()

    return {"message": "Removal Complete"}


@app.patch("/animes/{anime_id}")
async def update_anime_by_id(anime_id: int, anime_update: AnimeUpdate, session: Session = Depends(get_session)):
    get_anime = select(Anime).where(Anime.id == anime_id)
    anime = session.exec(get_anime).one_or_none()

    if anime is None:
        raise HTTPException(status_code=404)

    extra_data = anime_update.model_dump(exclude_unset=True)
    anime.sqlmodel_update(extra_data)

    session.add(anime)
    session.commit()
    session.refresh(anime)

    return anime


@app.post("/animes/{anime_id}/reviews")
async def create_review(anime_id: int, review: ReviewCreate, session: Session = Depends(get_session)):
    get_anime_statement = select(Anime).where(Anime.id == anime_id)
    anime = session.exec(get_anime_statement).one_or_none()

    get_user_statement = select(User).where(User.id == review.user_id)
    user = session.exec(get_user_statement).one_or_none()

    if anime is None or user is None:
        raise HTTPException(status_code=404)

    review = Review(rating=review.rating,
                    comment=review.comment, anime_id=anime_id, user_id=review.user_id)
    session.add(review)
    session.commit()
    session.refresh(review)
    return review


@app.get("/animes/{anime_id}/reviews")
async def get_reviews_by_anime(anime_id: int, session: Session = Depends(get_session)):
    anime_statement = select(Anime).where(Anime.id == anime_id)
    anime_exists = session.exec(anime_statement).one_or_none()

    if anime_exists is None:
        raise HTTPException(status_code=404)

    return anime_exists.reviews


@app.post("/users", status_code=201)
async def create_user(user_create: UserCreate, session: Session = Depends(get_session)):
    try:
        user = User.model_validate(user_create)
        session.add(user)
        session.commit()
        session.refresh(user)
        return user
    except Exception as e:
        raise HTTPException(status_code=400)


@app.get("/users")
async def get_all_users(session: Session = Depends(get_session)):
    statement = select(User)
    result = session.exec(statement)

    return result.all()


@app.get("/users/{user_id}/reviews")
async def get_all_user_reviews(user_id: int, session: Session = Depends(get_session)):
    get_user_statemente = select(User).where(User.id == user_id)
    user = session.exec(get_user_statemente).one_or_none()

    if user is None:
        raise HTTPException(status_code=404)

    return user.reviews
