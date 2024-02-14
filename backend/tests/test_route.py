from unittest.mock import patch, MagicMock
import os
import sys
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
from app import Quiz, QuizOption, QuizQuestion  # Noqa: E402
from tests.route_setup import RouteTestSetup  # Noqa: E402


class TestGetFullQuiz(RouteTestSetup):
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
        self.assertEqual(response.status_code, 200)
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
        self.assertEqual(response.status_code, 200)
        self.assertIn('full_quiz', json_data)
        self.assertEqual(len(json_data['full_quiz']), 1)
        self.assertCountEqual(
            json_data['full_quiz'][0].keys(),
            [
                'created_at', 'name', 'option_id', 'option_number',
                'option_text', 'question_id', 'question_number',
                'question_text', 'quiz_id', 'updated_at'
            ]
        )
        self.assertEqual(json_data['full_quiz'][0]['name'], 'Test Quiz')
        self.assertEqual(json_data['full_quiz'][0]['option_id'], 1)
        self.assertEqual(json_data['full_quiz'][0]['option_number'], 1)
        self.assertEqual(json_data['full_quiz'][0]['option_text'], 'Blue')
        self.assertEqual(json_data['full_quiz'][0]['question_id'], 1)
        self.assertEqual(json_data['full_quiz'][0]['question_number'], 1)
        self.assertEqual(
            json_data['full_quiz'][0]['question_text'], 'Favourite colour?')
        self.assertEqual(json_data['full_quiz'][0]['quiz_id'], 1)

    @patch('app.sql_functions.select_full_quiz')
    def test_full_quiz_error(self, mock_request: MagicMock) -> None:
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


class TestSaveQuiz(RouteTestSetup):

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
        response = self._client.post(self._route, json=data)
        json_data = response.get_json()

        # Assert
        self.assertEqual(json_data, {'message': 'Quiz saved successfully'})
        self.assertEqual(response.status_code, 200)

    def test_update_quiz(self) -> None:
        """Test updating a quiz without change the size."""
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

        data_updated = {
            'quiz_data': {
                'quiz_id': 1,
                'name': 'Test quiz 2',
                'quiz_question_data': [
                    {
                        'question_number': 1,
                        'text': 'Test question 2',
                        'quiz_option_data': [
                            {
                                'option_number': 1,
                                'question_number': 1,
                                'text': 'Test option 2'
                            }
                        ]
                    }
                ]
            }
        }

        # Act
        # Insert quiz to save to override
        self._client.post(self._route, json=data)
        response = self._client.post(self._route, json=data_updated)
        json_data = response.get_json()

        # Assert
        self.assertEqual(json_data, {'message': 'Quiz saved successfully'})
        self.assertEqual(response.status_code, 200)

    def test_modify_quiz_increased_size(self) -> None:
        """Test saving a quiz after adding questions and options."""
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

        data_updated = {
            'quiz_data': {
                'quiz_id': 1,
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
                    },
                    {
                        'question_number': 2,
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
        response = self._client.post(self._route, json=data_updated)
        json_data = response.get_json()

        # Assert
        self.assertEqual(json_data, {'message': 'Quiz saved successfully'})
        self.assertEqual(response.status_code, 200)

    def test_modify_quiz_decreased_size_to_empty(self) -> None:
        """Test saving a quiz after removing all questions and options."""
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

        data_updated = {
            'quiz_data': {
                'quiz_id': 1,
                'name': 'Test quiz',
                'quiz_question_data': []
            }
        }

        # Act
        self._client.post(self._route, json=data)
        response = self._client.post(self._route, json=data_updated)
        json_data = response.get_json()

        # Assert
        self.assertEqual(json_data, {'message': 'Quiz saved successfully'})
        self.assertEqual(response.status_code, 200)

    def test_modify_quiz_decreased_size(self) -> None:
        """Test saving a quiz after removing questions and options."""
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
                                'text': 'Test option A1'
                            },
                            {
                                'option_number': 2,
                                'question_number': 1,
                                'text': 'Test option A2'
                            }
                        ]
                    },
                    {
                        'question_number': 2,
                        'text': 'Test question',
                        'quiz_option_data': [
                            {
                                'option_number': 1,
                                'question_number': 1,
                                'text': 'Test option B1'
                            }
                        ]
                    }
                ]
            }
        }

        data_updated = {
            'quiz_data': {
                'quiz_id': 1,
                'name': 'Test quiz',
                'quiz_question_data': [
                    {
                        'question_number': 1,
                        'text': 'Test question',
                        'quiz_option_data': [
                            {
                                'option_number': 1,
                                'question_number': 1,
                                'text': 'Test option A1'
                            }
                        ]
                    }
                ]
            }
        }

        # Act
        self._client.post(self._route, json=data)
        response = self._client.post(self._route, json=data_updated)
        json_data = response.get_json()

        # Assert
        self.assertEqual(json_data, {'message': 'Quiz saved successfully'})
        self.assertEqual(response.status_code, 200)

    @patch('app.sql_functions.save_quiz')
    def test_save_quiz_error_response(self, mock_request: MagicMock) -> None:
        """Test the server response if the response is an error."""
        # Arrange
        mock_request.side_effect = Exception('test_save_quiz_error_response')

        # Act
        response = self._client.post(self._route, json={})
        json_data = response.get_json()

        # # Assert
        self.assertEqual(json_data, {'error': 'An error occurred'})
        self.assertEqual(response.status_code, 500)
        mock_request.assert_called_once_with({})

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

    def test_quiz_not_found(self) -> None:
        """Test saving a quiz where the quiz id does not exist."""
        # Arrange
        data = {
            'quiz_data': {
                'quiz_id': 2,
                'name': 'Test quiz',
                'quiz_question_data': []
            }
        }

        # Act
        response = self._client.post(self._route, json=data)
        json_data = response.get_json()

        # # Assert
        self.assertEqual(json_data, {'message': 'Failed to save quiz'})
        self.assertEqual(response.status_code, 200)


class TestDeleteQuiz(RouteTestSetup):

    def __init__(self, methodName: str = "runTest") -> None:
        super().__init__(methodName)
        self._route = '/delete-quiz'

    def test_delete_quiz_sucessful(self) -> None:
        """Test successfully deleting a quiz in the database."""
        # Arrange
        post_data = {'quiz_id': 1}
        quiz_data = {'name': 'Test Quiz'}
        self._insert_sample_data(Quiz, quiz_data)  # Create a quiz

        # Act
        response = self._client.post(self._route, json=post_data)
        json_data = response.get_json()

        # Assert
        self.assertEqual(json_data, {'message': 'Quiz deleted successfully'})
        self.assertEqual(response.status_code, 200)

    def test_delete_quiz_not_exist(self) -> None:
        """Test attempting to delete a quiz that does not exist."""
        # Arrange
        post_data = {'quiz_id': 1}

        # Act
        response = self._client.post(self._route, json=post_data)
        json_data = response.get_json()

        # Assert
        self.assertEqual(json_data, {'message': 'Failed to delete quiz'})
        self.assertEqual(response.status_code, 200)

    @patch('app.sql_functions.delete_quiz')
    def test_delete_quiz_error_response(
        self, mock_request: MagicMock
    ) -> None:
        """Test the server response if the response is an error."""
        # Arrange
        data = {}
        mock_request.side_effect = Exception(
            'test_delete_quiz_error_response')

        # Act
        response = self._client.post(self._route, json=data)
        json_data = response.get_json()

        # Assert
        self.assertEqual(json_data, {'error': 'An error occurred'})
        self.assertEqual(response.status_code, 500)
        mock_request.assert_called_once_with({})


class TestGetQuizzes(RouteTestSetup):

    def __init__(self, methodName: str = "runTest") -> None:
        super().__init__(methodName)
        self._route = '/get-quiz'

    def test_get_quizzes_empty(self) -> None:
        """Test get quiz list if no quiz exists."""
        # Arrange
        route = f'{self._route}/1'

        # Act
        response = self._client.get(route)
        json_data = response.get_json()

        # Assert
        self.assertEqual(json_data, {'quiz_list': []})
        self.assertEqual(response.status_code, 200)

    def test_get_quizzes_non_empty(self) -> None:
        """Test get quiz list if quizzes exist."""
        # Arrange
        quiz_data = {'name': 'Test Quiz'}
        self._insert_sample_data(Quiz, quiz_data)
        route = f'{self._route}/1'

        # Act
        response = self._client.get(route)
        json_data = response.get_json()

        # Assert
        self.assertIn('quiz_list', json_data)
        self.assertCountEqual(
            json_data['quiz_list'], [{'name': 'Test Quiz', 'quiz_id': 1}])
        self.assertEqual(response.status_code, 200)

    def test_get_quizzes_wrong_limit_data_type(self) -> None:
        """Test get quiz list if input limit cannot be converted to an
        integer.
        """
        # Arrange
        route = f'{self._route}/test'

        # Act
        response = self._client.get(route)
        json_data = response.get_json()

        # Assert
        self.assertEqual(
            json_data, {'message': 'limit needs to be an integer'})
        self.assertEqual(response.status_code, 200)

    @patch('app.sql_functions.get_quiz_list')
    def test_get_quizzes_error_response(
        self, mock_request: MagicMock
    ) -> None:
        """Test the server response if the response is an error."""
        # Arrange
        mock_request.side_effect = Exception(
            'test_get_quizzes_error_response')
        route = f'{self._route}/1'

        # Act
        response = self._client.get(route)
        json_data = response.get_json()

        # Assert
        self.assertEqual(json_data, {'error': 'An error occurred'})
        self.assertEqual(response.status_code, 500)
        mock_request.assert_called_once_with('1')
