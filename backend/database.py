from sqlmodel import SQLModel, Session, create_engine

DATABASE_URL = "postgresql+psycopg://postgres:root@localhost:5432/postgres"

engine = create_engine(DATABASE_URL)


def get_session():
    with Session(engine) as session:
        yield session
