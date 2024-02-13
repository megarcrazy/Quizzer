from typing import Any, Dict, List, Tuple
import unittest
import os
import sys
from flask_sqlalchemy.model import DefaultMeta
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
from app import create_app, db, Quiz, QuizOption, QuizQuestion  # Noqa: E402


class RouteTestSetup(unittest.TestCase):
    """Flask application route testing class."""

    def setUp(self) -> None:
        """Setup mock database."""
        database_url = 'sqlite:///:memory:'
        self._app = create_app(database_url, False)
        self._client = self._app.test_client()

    def _insert_sample_data(
        self, Table: DefaultMeta, data: Dict[str, Any]
    ) -> None:
        """Insert sample row data to sqlite database."""
        with self._app.app_context():
            new_row = Table(**data)
            # Add new row and commit changes
            db.session.add(new_row)
            db.session.commit()
        return new_row

    def _extract_full_quiz_by_id(
        self, quiz_id: int
    ) -> Tuple[List[Quiz], List[QuizQuestion], List[QuizOption]]:
        """Extraction quiz, quiz question and quiz option lists a given
        quiz id.
        """
        quiz_list = self._extract_quiz_by_id(quiz_id)
        quiz_question_list = self._extract_question_by_quiz_id(quiz_id)
        quiz_option_list = self._extract_option_by_quiz_id(quiz_id)
        return quiz_list, quiz_question_list, quiz_option_list

    def _extract_quiz_by_id(self, quiz_id: int) -> List[Quiz]:
        """Extract all quiz rows by id."""
        with self._app.app_context():
            quiz_list = Quiz.query.filter(Quiz.quiz_id == quiz_id).all()
        return quiz_list

    def _extract_question_by_quiz_id(self, quiz_id: int) -> List[QuizQuestion]:
        """Extract inner join of quiz and questions filtered by quiz id."""
        with self._app.app_context():
            quiz_question_list = (
                db.session.query(QuizQuestion)
                .join(Quiz, QuizQuestion.quiz_id == Quiz.quiz_id)
                .filter(Quiz.quiz_id == quiz_id)
                .all()
            )
        return quiz_question_list

    def _extract_option_by_quiz_id(self, quiz_id: int) -> List[QuizQuestion]:
        """Extract inner join of quiz, questions and options filtered by quiz
        id.
        """
        with self._app.app_context():
            quiz_option_list = (
                db.session.query(QuizOption)
                .join(Quiz, QuizQuestion.quiz_id == Quiz.quiz_id)
                .join(QuizQuestion,
                      QuizOption.question_id == QuizQuestion.question_id)
                .filter(Quiz.quiz_id == quiz_id)
                .all()
            )
        return quiz_option_list
