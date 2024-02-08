from fastapi import Depends, HTTPException, Query, APIRouter
from config import app, get_session
from typing import Annotated
from sqlmodel import Session, select
from model import Hero, HeroCrete, HeroResponse, HeroUpdate

router = APIRouter()


@router.get("/heroes", response_model=list[Hero])
def get_heroes(session: Annotated[Session, Depends(get_session)]):
    heroes = session.exec(select(Hero)).all()
    return heroes

# get limited heroes


@router.get("/heroes/limited", response_model=list[Hero])
def get_heroes_limited(session: Annotated[Session, Depends(get_session)], limit: int = Query(default=2, le=4), offset: int = Query(default=0, le=1)):
    heroes = session.exec(select(Hero).limit(limit).offset(offset)).all()
    return heroes
# create heroes


@router.post("/heroes", response_model=HeroResponse)
def create_hero(hero: HeroCrete, db: Annotated[Session, Depends(get_session)]):
    hero_to_insert = Hero.model_validate(hero)
    db.add(hero_to_insert)
    db.commit()
    db.refresh(hero_to_insert)
    return hero_to_insert

# get single hero


@router.get("/heroes/{hero_id}", response_model=HeroResponse)
def get_hero_by_id(hero_id: int, session: Annotated[Session, Depends(get_session)]):
    hero = session.get(Hero, hero_id)
    if not hero:
        raise HTTPException(
            status_code=404, detail="Hero not found of  id {hero_id}")
    return hero


@router.patch("/heroes{hero_id}", response_model=HeroResponse)
def update_hero(hero_id: int, hero_data: HeroUpdate, session: Annotated[Session, Depends(get_session)]):
    hero = session.get(Hero, hero_id)
    if not hero:
        raise HTTPException(status_code=404, detail="Hero not found")
    hero_dict_data = hero_data.model_dump(exclude_unset=True)
    print("hero_dict_data", hero_dict_data)

    for key, value in hero_dict_data.items():
        setattr(hero, key, value)
    print("hero", hero)
    session.add(hero)
    session.commit()
    session.refresh(hero)
    return hero

# delete hero


@router.delete("/heroes/{hero_id}")
def delete_hero(hero_id: int, session: Annotated[Session, Depends(get_session)]):
    hero = session.get(Hero, hero_id)
    if not hero:
        raise HTTPException(status_code=404, detail="Hero not found")
    session.delete(hero)
    session.commit()
    return {"message": "Hero deleted successfully"}
