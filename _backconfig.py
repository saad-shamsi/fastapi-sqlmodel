
from sqlmodel import create_engine, Session
from fastapi import FastAPI

connection_string = "add connnection string here"

engine = create_engine(connection_string)

app = FastAPI()


def get_session():
    with Session(engine) as session:
        yield session
