from datetime import datetime
from typing import Any, Dict, List, Optional, Tuple
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

    def _get_default_full_quiz_data(self) -> Dict[str, Any]:
        """Generate a default dictionary with full quiz data."""
        quiz_data = self._get_default_quiz_data()
        question_data = self._get_default_question_data()
        option_data = self._get_default_option_data()

        # Link rows
        quiz_data['quiz_question_data'] = [question_data]
        question_data['quiz_option_data'] = [option_data]

        # Generate sample full quiz data
        data = {'quiz_data': quiz_data}
        return data

    def _get_default_quiz_data(
        self, modifications: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Generate a default dictionary with quiz data."""
        data = {
            'quiz_id': 1,
            'name': 'Test Quiz',
            'created_at': datetime.utcfromtimestamp(0),
            'updated_at': datetime.utcfromtimestamp(0)
        }
        if modifications is not None:
            for key, item in modifications.items():
                data[key] = item
        return data

    def _get_default_question_data(
        self,  modifications: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Generate a default dictionary with question data."""
        data = {
            'question_id': 1,
            'quiz_id': 1,
            'question_number': 1,
            'text': 'Test Question'
        }
        if modifications is not None:
            for key, item in modifications.items():
                data[key] = item
        return data

    def _get_default_option_data(
        self,  modifications: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Generate a default dictionary with option data."""
        data = {
            'option_id': 1,
            'question_id': 1,
            'option_number': 1,
            'text': 'Test Option',
            'correct_answer': True
        }
        if modifications is not None:
            for key, item in modifications.items():
                data[key] = item
        return data
