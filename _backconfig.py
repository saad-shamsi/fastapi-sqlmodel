
from sqlmodel import create_engine, Session
from fastapi import FastAPI

connection_string = "postgresql://saadshamsi13:hrpGdD8As6IZ@ep-bitter-sunset-a1x6gnrg.ap-southeast-1.aws.neon.tech/anew?sslmode=require"

engine = create_engine(connection_string)

app = FastAPI()


def get_session():
    with Session(engine) as session:
        yield session
