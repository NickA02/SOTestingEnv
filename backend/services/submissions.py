"""Service to handle the Submissions and interaction with Judge0 API"""

import os
import sys
import requests  # type: ignore
from ..models import Submission, ConsoleLog, Team
from io import BytesIO  # Creates an in-memory "file"
from zipfile import ZipFile
from exceptions import ResourceNotFoundException


__authors__ = ["Nicholas Almy", "Andrew Lockard"]

submissions_dir = "es_files/submissions"


class SubmissionService:
    """Service that deals with Submission CRUD operations"""

    def __init__(self):
        pass

    def submit(self, team_name: str, submission: Submission) -> None:
        """Submit a file to the submission folder... Only supports Python files"""
        # sys.stdout.write(f"Debug: Team name is {team_name}")
        question_dir = f"q{submission.question_num}"
        file = f"{team_name}.py"

        # Create the submission directory if it doesn't exist
        if not os.path.exists(submissions_dir):
            os.makedirs(submissions_dir)

        # Create the question directory if it doesn't exist
        if not os.path.exists(os.path.join(submissions_dir, question_dir)):
            os.makedirs(os.path.join(submissions_dir, question_dir))

        # Write the file to the submission directory
        with open(os.path.join(submissions_dir, question_dir, file), "w") as f:
            f.write(submission.file_contents)

    def submit_and_run(self, team: Team, submission: Submission) -> ConsoleLog:
        """Submit a file to the submission folder, runs it and returns the console logs"""
        self.submit(team.name, submission)
        return self.run_submission(submission.question_num, team.name, forScore=False)

    def run_submission(
        self, question_num: int, team_name: str, forScore: bool = False
    ) -> ConsoleLog:
        """Run a submission on an Autograder and return the console logs
        Args:
            question_num (int): The question number
            team_name (str): The team name
            forScore (bool): Whether the submission is for final grading or not
        Returns:
            ConsoleLog: The console log of the submission
        """
        submission_path = f"es_files/submissions/q{question_num}/{team_name}.py"
        with open(submission_path, "r") as f:
            submission_code = f.read()
        res = requests.post(
            "http://host.docker.internal:2358/submissions?wait=true",
            headers={"Content-Type": "application/json"},
            json={
                "source_code": submission_code,
                "language_id": 71,
            },
        )

        if res.status_code == 201:
            token = res.json()["token"]
        else:
            sys.stdout.write(f"Error: {res.json()}")
            return ConsoleLog(console_log=f"Error: Submission Failed")

        res = requests.get(f"http://host.docker.internal:2358/submissions/{token}")
        if res.status_code == 200:
            actual_response = res.json()["stdout"]
            sys.stdout.write(f"\n\n{res.json()}\n\n")
            if actual_response is None:
                actual_response = ""
            return ConsoleLog(console_log=actual_response)
        else:
            return ConsoleLog(console_log=f"Error: {res.json()["error"]} Submission")

    def package_submission(
        self, team_name: str, question_number: int, demo=False
    ) -> str:
        """Packages submission files into a string of a .zip contents.

        This packages together all files in autograder_utils
        as well as the `test_cases.py` (if demo = False) file for that question.
        With demo=True, `demo_cases.py` is packaged instead.
        """

        utils_dir = "backend/autograder_utils"
        question_dir = os.path.join("es_files", "questions", f"q{question_number}")

        # with BytesIO() as f: # Creates an in memory buffer we can use just like a file
        with ZipFile(
            "new_zip.zip", "w"
        ) as new_zip:  # Creates a new zip in memory we can add to
            # Add all files in autograder_utils
            if not os.path.exists(utils_dir):
                raise ResourceNotFoundException("No Utils Created.")

            for file in os.listdir(utils_dir):
                new_zip.write(os.path.join(utils_dir, file), arcname=file)

            # Add test/demo case file
            if demo:
                path = os.path.join(question_dir, "demo_cases.py")
                if not os.path.exists(path):
                    raise ResourceNotFoundException(
                        f"Question {question_number} not found"
                    )
                new_zip.write(path, arcname="demo_cases.py")
            else:
                path = os.path.join(question_dir, "test_cases.py")
                if not os.path.exists(path):
                    raise ResourceNotFoundException(
                        f"Question {question_number} not found"
                    )
                new_zip.write(path, arcname="test_cases.py")

            # Add submission file
            path = os.path.join(
                submissions_dir, f"q{question_number}", f"{team_name}.py"
            )
            if not os.path.exists(path):
                raise ResourceNotFoundException(
                    f"Team {team_name} did not submit question {question_number}"
                )
            new_zip.write(path, arcname="submission.py")
