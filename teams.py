from fastapi import Depends, HTTPException, APIRouter
from typing import Annotated
from model import Team, TeamBase, TeamCreate, TeamResponse, TeamUpdate
from sqlmodel import select, Session
from config import app, get_session

router = APIRouter()


@router.get("/teams", response_model=list[Team])
def get_teams(session: Annotated[Session, Depends(get_session)]):
    teams = session.exec(select(Team)).all()
    return teams

# single team


@router.get("teams/{team_id}", response_model=TeamResponse)
def get_single_team(team_id: int, session: Annotated[Session, Depends(get_session)]):
    team = session.get(Team, team_id)
    if not team:
        raise HTTPException(status_code=404, detail="Team not found")
    return team

# create team


@router.post("/teams", response_model=TeamResponse)
def create_team(team: TeamCreate, session: Annotated[Session, Depends(get_session)]):
    team_to_insert = Team.model_validate(team)
    session.add(team_to_insert)
    session.commit()
    session.refresh(team_to_insert)
    return team_to_insert

# update team


@router.patch("/teams/{team_id}", response_model=TeamResponse)
def team_update(team_id: int, team_data: TeamUpdate, session: Annotated[Session, Depends(get_session)]):
    team = session.get(Team, team_id)
    if not team:
        raise HTTPException(status_code=404, detail="Team not found")
    team_dict_data = team_data.model_dump(exclude_unset=True)
    for key, value in team_dict_data.items():
        setattr(team, key, value)
    session.add(team)
    session.commit()
    session.refresh(team)
    return team


@router.delete("/teams/{team_id}")
def delete_team(team_id: int, session: Annotated[Session, Depends(get_session)]):
    team = session.get(Team, team_id)
    if not team:
        raise HTTPException(status_code=404, detail="Team not found")
    session.delete(team)
    session.commit()
    return {"done": "team deleted successfully"}
