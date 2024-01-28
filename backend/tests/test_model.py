from datetime import datetime
import os
import sys
import unittest
from freezegun import freeze_time
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.join(project_root, '..'))
from app import create_app, db, Quiz, QuizOption, QuizQuestion  # Noqa E402


class TestORM(unittest.TestCase):
    """Test object relational mapper functionality."""

    def setUp(self) -> None:
        """Setup up database."""
        database_url = 'sqlite:///:memory:'
        self._app = create_app(database_url, False)
        self._client = self._app.test_client()

    @freeze_time('2022-01-01 12:00:00')  # Freeze time for the test
    def test_quiz_table(self) -> None:
        """"""
        # Arrange
        quiz_data = {
            'name': 'Quiz Test',
            'code': 'abcde',
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
            code = new_row.code
            quiz_id = new_row.quiz_id
            created_at = new_row.created_at
            updated_at = new_row.updated_at

        # Assert
        self.assertEqual(name, 'Quiz Test')
        self.assertEqual(code, 'abcde')
        self.assertEqual(quiz_id, 1)
        self.assertEqual(created_at, datetime(2022, 1, 1, 12, 0, 0))
        self.assertEqual(updated_at, datetime(2022, 1, 1, 12, 0, 0))

    def test_quiz_table_update_time(self) -> None:
        """"""

    def test_quiz_question_table(self) -> None:
        """"""

    def test_quiz_option_table(self) -> None:
        """"""


if __name__ == '__main__':
    unittest.main(exit=False)
