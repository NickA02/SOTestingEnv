"""Service to handle the Teams feature"""

from typing import List
from ..db import db_session
from fastapi import Depends
from sqlmodel import Session, select, and_
import polars as pl
import datetime as dt

from .exceptions import ResourceNotFoundException, InvalidCredentialsException

from ..models import Team

__authors__ = ["Nicholas Almy", "Mustafa Aljumayli"]

WORD_LIST = "/workspaces/SOTestingEnv/es_files/unique_words.csv"

"""For now, password creation is done off of the database. Will need to rework
to integrate it into the db"""


class TeamService:
    """Service that preforms actions on Team Table."""

    def __init__(
        self, session: Session = Depends(db_session)
    ):  # Add all dependencies via FastAPI injection in the constructor
        self._session = session

    def df_row_to_team(self, team_df: pl.DataFrame) -> Team:
        """Converts a DataFrame row to a Team object.
        Args:
            team_df (pl.DataFrame): DataFrame row to convert
        Returns:
            Team: Team object created from the DataFrame row
        """
        team = Team(
            id=team_df["id"],
            name=team_df["Team Number"],
            password=team_df["Password"],
            start_time=dt.datetime.strptime(team_df["Start Time"], "%H:%M").time(),
            end_time=dt.datetime.strptime(team_df["End Time"], "%H:%M").time(),
        )
        return team

    def df_to_teams(self, teams_df: pl.DataFrame) -> list[Team]:
        """Converts a DataFrame to a list of Team objects.
        Args:
            teams_df (pl.DataFrame): DataFrame to convert
        Returns:
            list[Team]: List of Team objects created from the DataFrame
        """

        teams = []
        for team in teams_df.iter_rows(named="True"):
            teams.append(self.df_row_to_team(team))
        return teams

    def team_to_df(self, team: Team) -> pl.DataFrame:
        """Converts a Team object to a DataFrame row.
        Args:
            team (Team): Team object to convert
        Returns:
            pl.DataFrame: DataFrame row created from the Team object
        """
        team_df = pl.DataFrame(
            {
                "id": [team.id],
                "Team Number": [team.name],
                "Password": [team.password],
                "Start Time": [team.start_time.strftime("%H:%M")],
                "End Time": [team.end_time.strftime("%H:%M")],
            }
        )
        return team_df

    def teams_to_df(self, teams: list[Team]) -> pl.DataFrame:
        """Converts a list of Team objects to a DataFrame.
        Args:
            teams (list[Team]): List of Team objects to convert
        Returns:
            pl.DataFrame: DataFrame created from the list of Team objects
        """
        team_dfs = []
        for team in teams:
            team_dfs.append(self.team_to_df(team))
        return pl.concat(team_dfs)

    def update_team(self, team: Team) -> Team:
        """Update a team in the database.
        Args:
            team (Team): Team object to update
        Returns:
            Team: Updated Team object
        Raises:
            ResourceNotFoundException: If the team does not exist in the database
        """
        existing_team: Team | None = self._session.exec(
            select(Team).where(Team.id == team.id)
        ).one_or_none()
        if existing_team:
            existing_team.name = team.name
            existing_team.password = team.password
            existing_team.start_time = team.start_time
            existing_team.end_time = team.end_time
            self._session.add(existing_team)
            self._session.commit()
            return existing_team
        else:
            raise ResourceNotFoundException("Team", team.id)

    def create_team(self, team: Team) -> Team:
        """Create a new team in the database.
        Args:
            team (Team): Team object to create
        Returns:
            Team: Created Team object
        """
        self._session.add(team)
        self._session.commit()
        return team

    def get_team(self, identifier) -> Team:
        """Gets the team by id (int) or name (str)"""
        if isinstance(identifier, int):
            team = self._session.get(Team, identifier)
            if team is None:
                raise ResourceNotFoundException(
                    f"Team with id={identifier} was not found"
                )
        elif isinstance(identifier, str):
            team = self._session.exec(
                select(Team).where(Team.name == identifier)
            ).first()
            if not team:
                raise ResourceNotFoundException(
                    f"Team with name={identifier} was not found"
                )
        else:
            raise ValueError("Identifier must be an int (id) or a str (name)")
        return team

    def get_all_teams(self) -> List[Team]:
        """Gets a list of all the teams"""
        teams = self._session.exec(select(Team)).all()
        if not teams:
            raise ResourceNotFoundException(f"Teams were not found")
        return teams

    def get_team_with_credentials(self, name: str, password: str) -> Team:
        """Gets team with a team name and password."""
        team = self._session.exec(
            select(Team).where(and_(Team.name == name, Team.password == password))
        ).first()
        if not team:
            raise InvalidCredentialsException("Incorrect credentials. Please try again")
        return team
