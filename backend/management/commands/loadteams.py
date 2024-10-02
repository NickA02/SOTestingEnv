from django.core.management.base import BaseCommand
from django.utils.crypto import get_random_string
from utils.passwords import save_teams_from_csv
import polars as pl
import datetime as dt


class Command(BaseCommand):
    # python help function
    help = "Load teams into database"

    def add_arguments(self, parser):
        parser.add_argument(
            "file",
            type=str,
            help="Location of CSV File structured as [Team Number, Start Time, End Time]",
        )

    def handle(self, *args, **kwargs):
        file: str = kwargs["file"]
        if not file.endswith(".csv"):
            self.stdout.write("Error -- File not in supported format (.csv)")
            return

        user_table = pl.read_csv(file)
        if not user_table:
            self.stdout.write("Error -- File not found.")

        if save_teams_from_csv(user_table):
            self.stdout.write(f"Saved to file {file}")
        else:
            self.stdout.write(f"Error -- See logs for more detail")

        self.stdout.write(user_table)
