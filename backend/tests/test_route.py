from typing import Any, Dict
import unittest
from unittest.mock import patch
from flask_sqlalchemy.model import DefaultMeta
from app import create_app, db, Quiz, QuizOption, QuizQuestion


class RouteSetup(unittest.TestCase):
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


class TestGetFullQuiz(RouteSetup):
    """Test get_full_quiz."""

    def __init__(self, methodName: str = "runTest") -> None:
        super().__init__(methodName)
        self._route = '/get-full-quiz'

    def test_full_quiz_empty_table(self) -> None:
        """Empty table with no data or quiz does not exist."""
        # Arrange
        route = f'{self._route}/1'

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
        quiz_data = {'name': 'Test Quiz'}
        self._insert_sample_data(Quiz, quiz_data)

        question_data = {'text': 'Favourite colour?', 'question_number': 1,
                         'quiz_id': 1}
        self._insert_sample_data(QuizQuestion, question_data)

        option_data = {'text': 'Blue', 'option_number': 1, 'question_id': 1}
        self._insert_sample_data(QuizOption, option_data)

        route = f'{self._route}/1'

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
                'created_at', 'name', 'option_id', 'option_number',
                'option_text', 'question_id', 'question_number',
                'question_text', 'quiz_id', 'updated_at'
            ]
        )
        self.assertEqual(dict_data['name'], 'Test Quiz')
        self.assertEqual(dict_data['option_id'], 1)
        self.assertEqual(dict_data['option_number'], 1)
        self.assertEqual(dict_data['option_text'], 'Blue')
        self.assertEqual(dict_data['question_id'], 1)
        self.assertEqual(dict_data['question_number'], 1)
        self.assertEqual(dict_data['question_text'], 'Favourite colour?')
        self.assertEqual(dict_data['quiz_id'], 1)

    @patch('app.sql_functions.select_full_quiz')
    def test_full_quiz_error(self, mock_request) -> None:
        """Test the server response if the response is an error."""
        # Arrange
        mock_request.side_effect = Exception('test_full_quiz_error')
        route = f'{self._route}/test'
        # Act
        response = self._client.get(route)
        json_data = response.get_json()

        # # # Assert
        self.assertEqual(json_data, {'error': 'An error occurred'})
        self.assertEqual(response.status_code, 500)
        mock_request.assert_called_once_with('test')


class TestSaveQuiz(RouteSetup):

    def __init__(self, methodName: str = "runTest") -> None:
        super().__init__(methodName)
        self._route = '/save-quiz'

    def test_empty_response(self) -> None:
        """Test server response if there is no error."""
        # Arrange
        data = {
            'quiz_data': {
                'quiz_id': 0,
                'name': 'test',
                'quiz_question_data': []
            }
        }

        # Act
        response = self._client.post(self._route, json=data)
        json_data = response.get_json()

        # Assert
        self.assertEqual(json_data, {'message': 'Quiz saved successfully'})
        self.assertEqual(response.status_code, 200)

    def test_add_new_quiz(self) -> None:
        """Test adding a new quiz with new data."""
        # Arrange
        data = {
            'quiz_data': {
                'quiz_id': 0,
                'name': 'Test quiz',
                'quiz_question_data': [
                    {
                        'question_number': 1,
                        'text': 'Test question',
                        'quiz_option_data': [
                            {
                                'option_number': 1,
                                'question_number': 1,
                                'text': 'Test option'
                            }
                        ]
                    }
                ]
            }
        }

        # Act
        self._client.post(self._route, json=data)

        # Assert
        # Extract rows from SQL database
        with self._app.app_context():
            quiz_list = Quiz.query.all()
            quiz_question_list = QuizQuestion.query.all()
            quiz_option_list = QuizOption.query.all()

        self.assertEqual(len(quiz_list), 1)
        self.assertEqual(len(quiz_question_list), 1)
        self.assertEqual(len(quiz_option_list), 1)

    def test_update_quiz(self) -> None:
        """Test updating a quiz without change the size."""

    def test_modify_quiz_same_size(self) -> None:
        """Test saving a quiz after adding more questions."""

    def test_modify_quiz_decreased_size(self) -> None:
        """Test saving a quiz after decreasing the amound of questions."""

    @patch('app.sql_functions.save_quiz')
    def test_save_quiz_error_response(self, mock_requests) -> None:
        """Test the server response if the response is an error."""
        # Arrange
        mock_requests.side_effect = Exception('test_save_quiz_error_response')

        # Act
        response = self._client.post(self._route, json={})
        json_data = response.get_json()

        # # Assert
        self.assertEqual(json_data, {'error': 'An error occurred'})
        self.assertEqual(response.status_code, 500)
        mock_requests.assert_called_once_with({})

    def test_incorrect_post_data(self) -> None:
        """Test server response if the data is in the incorrect format."""
        # Arrange
        data = {'test': []}

        # Act
        response = self._client.post(self._route, json=data)
        json_data = response.get_json()

        # # Assert
        self.assertEqual(json_data, {'error': 'An error occurred'})
        self.assertEqual(response.status_code, 500)
