from sqlmodel import SQLModel, Field, Relationship


class AnimeBase(SQLModel):
    name: str = Field(max_length=25)
    release_year: int = Field(ge=1888, lt=2030)


class Anime(AnimeBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    reviews: list["Review"] = Relationship(back_populates="anime")


class AnimeCreate(AnimeBase):
    pass


class AnimeUpdate(SQLModel):
    name: str | None = None
    release_year: int | None = None


class UserBase(SQLModel):
    username: str = Field(unique=True, index=True)
    email: str

class User(UserBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    reviews: list["Review"] = Relationship(back_populates="user")

class UserCreate(UserBase):
    pass

class ReviewBase(SQLModel):
   rating: int= Field(ge=0, le=10) 
   comment: str
   user_id: int

class Review(ReviewBase, table=True):
   id: int | None = Field(default=None, primary_key=True)
   anime_id: int = Field(foreign_key="anime.id")
   anime: Anime = Relationship(back_populates="reviews")
   user_id: int = Field(foreign_key="user.id")
   user: User = Relationship(back_populates="reviews")

class ReviewCreate(ReviewBase):
    pass


class AnimeReadWithStats(AnimeBase):
    id: int
    review_count: int = 0
    average_rating: float | None = None