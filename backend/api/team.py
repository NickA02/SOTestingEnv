"""API Routes associated with Teams and TeamMember data objects"""
from typing import List
from fastapi import APIRouter, Depends
from ..models.team import TeamPublic
from ..services.team import TeamService
from fastapi import APIRouter, Depends
from ..models.team_members import TeamMemberCreate, TeamMemberPublic
from ..services.team import TeamService

__authors__ = ["Andrew Lockard", "Mustafa Aljumayli"]

api = APIRouter(prefix="/api/team")

openapi_tags = {
    "name": "Teams",
    "description": "Routes for Teams and TeamMembers."
}

# TODO: Update these to follow better conventions
@api.get("/", response_model=list[TeamPublic], tags=["Teams"])
async def get_teams(team_service: TeamService = Depends()) -> List[TeamPublic]:
    """Gets all teams"""
    return team_service.get_all_teams()

@api.get("/{id}", response_model=TeamPublic, tags=["Teams"])
async def get_team(id: int, team_service: TeamService = Depends()) -> TeamPublic:
    """Gets the team object"""
    return team_service.get_team(id)

@api.get("/name/{name}", response_model=TeamPublic, tags=["Teams"])
async def get_team(name: str, team_service: TeamService = Depends()) -> TeamPublic:
    """Gets the team by name"""
    return team_service.get_team(name)

# TODO: Add validation to these routes, we only want people on that team to get that info
# When we add validation we should be able to remove the field for team_id
@api.get("/members/{team_id}", response_model=list[TeamMemberPublic], tags=["Teams"])
def get_team_members(team_id: int, team_svc: TeamService = Depends()):
    """Gets all the team members for a team, currently specified with team_id"""
    return team_svc.get_team_members(team_id)

@api.post("/members/{team_id}", response_model=TeamMemberPublic, tags=["Teams"])
def add_team_member(new_member: TeamMemberCreate, team_id: int, team_svc: TeamService = Depends()):
    """Adds a team member to the currently logged in team.
    
    Currenlty it adds to the team given by team_id"""
    return team_svc.add_team_member(new_member, team_id)

@api.delete("/members/{member_id}/{team_id}", response_model=None, tags=["Teams"])
def delete_team_member(member_id: int, team_id: int, team_svc: TeamService = Depends()):
    """Deletes a team member from the currenlty logged in team.
    
    Currenlty this is checked as a part of the route."""
    team_svc.delete_team_member(member_id, team_id)
