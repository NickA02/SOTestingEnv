"""File to contain all Question related tests"""

from ..models import Question, QuestionsPublic, Document
import os
import pytest
from .fixtures import question_svc
from ..test.fake_data.question import setup_questions, setup_bad_questions

__authors__ = ["Matthew Futch"]


def test_isQuestionDir(question_svc):
    assert question_svc.isQuestionDir("q1000")
    assert not question_svc.isQuestionDir("1z")


def test_get_questions(question_svc, setup_questions):
    number_of_questions = 2
    tmp_path = setup_questions(number_of_questions)
    os.chdir(tmp_path)

    questions_public = question_svc.load_questions()

    assert questions_public == question_svc.get_questions()


def test_read_file(question_svc, setup_bad_questions):
    number_of_questions = 2
    tmp_path = setup_bad_questions(number_of_questions)
    os.chdir(tmp_path)

    with pytest.raises(Exception):  # exception on 53-54
        (question_svc.load_local_docs(1))[0].content

    with pytest.raises(Exception):  # read_document exception
        question_svc.read_document(
            f"{tmp_path}/es_files/questions/q1/doesntexist.extension", "foo"
        )


def test_load_global_docs(question_svc, setup_bad_questions):
    number_of_questions = 3
    tmp_path = setup_bad_questions(number_of_questions)
    os.chdir(tmp_path)

    assert len(question_svc.load_global_docs()) == 0


def test_refresh_questions(question_svc, setup_questions):
    number_of_questions = 2
    tmp_path = setup_questions(number_of_questions)
    os.chdir(tmp_path)

    startingQuestions = question_svc.load_questions()
    question_svc.refresh_questions()
    refreshedQuestions = question_svc.load_questions()

    assert startingQuestions.questions == refreshedQuestions.questions


def test_load_questions_file_not_found_error(question_svc, setup_questions):
    tmp_path = setup_questions(2)
    os.remove(tmp_path / "es_files" / "questions" / "q1" / "prompt.md")
    os.chdir(tmp_path)

    try:
        question_svc.load_questions()
    except FileNotFoundError:
        pytest.fail("FileNotFoundError was not handled correctly")


def test_load_questions_file_fails_not_questionDir(question_svc, setup_questions):
    tmp_path = setup_questions(2)
    os.mkdir(tmp_path / "es_files" / "questions" / "question1")
    os.chdir(tmp_path)

    assert question_svc.load_questions()


def test_load_question_with_no_starter_code(question_svc, setup_questions):
    tmp_path = setup_questions(2)
    os.remove(tmp_path / "es_files" / "questions" / "q1" / "starter.py")
    os.chdir(tmp_path)
    assert (question_svc.load_question(1).starter_code) == ""


def test_load_questions_generic_exception(question_svc, setup_bad_questions):
    # Create a test environment that triggers a generic exception
    tmp_path = setup_bad_questions(2)
    os.chmod(
        tmp_path / "es_files" / "questions" / "q1" / "prompt.md", 0o000
    )  # Restrict permissions to cause an exception
    os.chdir(tmp_path)

    # Ensure the generic exception is raised correctly
    with pytest.raises(Exception):
        question_svc.load_questions()
