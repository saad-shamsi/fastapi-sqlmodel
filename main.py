from fastapi import FastAPI, Depends, HTTPException, Query
from sqlmodel import Field, Session, SQLModel, create_engine, select
from config import engine, app
from hero import router as hero_router
from teams import router as team_router


# Include the routers from hero and team
app.include_router(hero_router, prefix="/hero", tags=["heroes"])
app.include_router(team_router, prefix="/team", tags=["teams"])


def create_tables():
    SQLModel.metadata.create_all(engine)


@app.on_event("startup")
def on_startup():
    create_tables()


@app.get("/")
async def read_root():
    return {"Hello": "World"}
