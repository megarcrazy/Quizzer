from typing import Any, Dict
import unittest
from flask_sqlalchemy.model import DefaultMeta
from app import create_app, db, Quiz, QuizOption, QuizQuestion


class TestRoute(unittest.TestCase):
    """Flask application route testing class."""

    def setUp(self) -> None:
        """Setup mock database."""
        database_url = 'sqlite:///:memory:'
        self._app = create_app(database_url, False)
        self._client = self._app.test_client()

    def insert_sample_data(
        self, Table: DefaultMeta, data: Dict[str, Any]
    ) -> None:
        """Insert sample row data to sqlite database."""
        with self._app.app_context():
            new_row = Table(**data)
            # Add new row and commit changes
            db.session.add(new_row)
            db.session.commit()
        return new_row

    def test_full_quiz_empty_table(self) -> None:
        """Empty table with no data."""
        # Arrange
        route = '/debug-full-quiz'

        # Act
        response = self._client.get(route)
        json_data = response.get_json()

        # Assert
        # Check status code
        self.assertEqual(response.status_code, 200)
        # Check dictionary key
        self.assertIn('full_quiz', json_data)
        self.assertEqual(json_data['full_quiz'], [])

    def test_full_quiz_one_line(self) -> None:
        """Empty table with no data."""
        # Arrange
        quiz_data = {'name': 'Test Quiz', 'code': '12345'}
        self.insert_sample_data(Quiz, quiz_data)

        question_data = {'text': 'Favourite colour?', 'quiz_id': 1}
        self.insert_sample_data(QuizQuestion, question_data)

        option_data = {'text': 'Blue', 'question_id': 1}
        self.insert_sample_data(QuizOption, option_data)

        route = '/debug-full-quiz'

        # Act
        response = self._client.get(route)
        json_data = response.get_json()

        # Assert
        self.assertIn('full_quiz', json_data)
        self.assertEqual(len(json_data['full_quiz']), 1)
        dict_data = json_data['full_quiz'][0]
        self.assertCountEqual(
            dict_data.keys(),
            [
                'code',
                'created_at',
                'name',
                'option_id',
                'option_text',
                'question_id',
                'question_text',
                'quiz_id',
                'updated_at'
            ]
        )
        self.assertEqual(dict_data['code'], '12345')
        self.assertEqual(dict_data['name'], 'Test Quiz')
        self.assertEqual(dict_data['option_id'], 1)
        self.assertEqual(dict_data['option_text'], 'Blue')
        self.assertEqual(dict_data['question_id'], 1)
        self.assertEqual(dict_data['question_text'], 'Favourite colour?')
        self.assertEqual(dict_data['quiz_id'], 1)


if __name__ == '__main__':
    unittest.main(exit=False)
