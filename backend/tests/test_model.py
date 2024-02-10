from datetime import datetime
import unittest
from freezegun import freeze_time
import os
import sys
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
from app import create_app, db, Quiz, QuizOption, QuizQuestion  # Noqa: E402


class TestORM(unittest.TestCase):
    """Test object relational mapper functionality."""

    def setUp(self) -> None:
        """Setup up database."""
        database_url = 'sqlite:///:memory:'
        self._app = create_app(database_url, False)
        self._client = self._app.test_client()

    @freeze_time('2022-01-01 12:00:00')  # Freeze time for the test
    def test_quiz_table(self) -> None:
        """Test 'Quiz' table SQL."""
        # Arrange
        quiz_data = {
            'name': 'Quiz Test',
            'created_at': datetime.now(),
            'updated_at': datetime.now()
        }

        # Act
        with self._app.app_context():
            new_row = Quiz(**quiz_data)
            # Add new row and commit changes
            db.session.add(new_row)
            db.session.commit()

            # Get row values
            name = new_row.name
            quiz_id = new_row.quiz_id
            created_at = new_row.created_at
            updated_at = new_row.updated_at

        # Assert
        self.assertEqual(name, 'Quiz Test')
        self.assertEqual(quiz_id, 1)
        self.assertEqual(created_at, datetime(2022, 1, 1, 12, 0, 0))
        self.assertEqual(updated_at, datetime(2022, 1, 1, 12, 0, 0))

    def test_quiz_question_table(self) -> None:
        """Test 'QuizQuestion' table SQL."""
        # Arrange
        quiz_question_data = {
            'quiz_id': 1,
            'question_number': 1,
            'text': 'What is the unit of power?',
        }

        # Act
        with self._app.app_context():
            new_row = QuizQuestion(**quiz_question_data)
            # Add new row and commit changes
            db.session.add(new_row)
            db.session.commit()

            # Get row values
            quiz_id = new_row.quiz_id
            question_number = new_row.question_number
            text = new_row.text

        # Assert
        self.assertEqual(quiz_id, 1)
        self.assertEqual(question_number, 1)
        self.assertEqual(text, 'What is the unit of power?')

    def test_quiz_option_table(self) -> None:
        """Test 'QuizOption' table SQL."""
        # Arrange
        quiz_option_data = {
            'question_id': 1,
            'option_number': 1,
            'text': 'Watt'
        }

        # Act
        with self._app.app_context():
            new_row = QuizOption(**quiz_option_data)
            # Add new row and commit changes
            db.session.add(new_row)
            db.session.commit()

            # Get row values
            question_id = new_row.question_id
            option_number = new_row.option_number
            text = new_row.text

        # Assert
        self.assertEqual(question_id, 1)
        self.assertEqual(option_number, 1)
        self.assertEqual(text, 'Watt')
