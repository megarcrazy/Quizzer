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

        # Insert existing data
        quiz_data = self._get_default_quiz_data()
        self._insert_sample_data(Quiz, quiz_data)

        question_data = self._get_default_question_data()
        self._insert_sample_data(QuizQuestion, question_data)

        option_data = self._get_default_option_data()
        self._insert_sample_data(QuizOption, option_data)

        route = f'{self._route}/1'

        # Act
        response = self._client.get(route)
        json_data = response.get_json()

        # Assert
        self.assertEqual(response.status_code, 200)
        self.assertIn('full_quiz', json_data)
        self.assertEqual(len(json_data['full_quiz']), 1)
        self.assertDictEqual(
            json_data['full_quiz'][0],
            {
                'created_at': 'Thu, 01 Jan 1970 00:00:00 GMT',
                'correct_answer': True,
                'name': 'Test Quiz',
                'option_id': 1,
                'option_number': 1,
                'option_text': 'Test Option',
                'question_id': 1,
                'question_number': 1,
                'question_text': 'Test Question',
                'quiz_id': 1,
                'updated_at': 'Thu, 01 Jan 1970 00:00:00 GMT'
            }
        )

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

    def test_add_new_quiz(self) -> None:
        """Test server response if there is no error."""
        # Arrange
        data = self._get_default_full_quiz_data()
        data['quiz_data']['quiz_id'] = 0

        # Act
        response = self._client.post(self._route, json=data)
        json_data = response.get_json()

        # Assert
        self.assertEqual(json_data, {'message': 'Quiz saved successfully'})
        self.assertEqual(response.status_code, 200)

    def test_update_quiz(self) -> None:
        """Test updating a quiz without change the size."""
        # Arrange

        # Insert existing data
        quiz_data = self._get_default_quiz_data()
        self._insert_sample_data(Quiz, quiz_data)

        question_data = self._get_default_question_data()
        self._insert_sample_data(QuizQuestion, question_data)

        option_data = self._get_default_option_data()
        self._insert_sample_data(QuizOption, option_data)

        # Set up updated data
        data_updated = self._get_default_full_quiz_data()
        data_updated['quiz_data']['name'] = 'Test Quiz 2'
        data_updated['quiz_data']['quiz_question_data'][0][
            'text'] = 'Test Question 2'
        data_updated['quiz_data']['quiz_question_data'][0][
            'quiz_option_data'][0]['text'] = 'Test Option 2'

        # Act
        response = self._client.post(self._route, json=data_updated)
        json_data = response.get_json()

        # Assert
        self.assertEqual(json_data, {'message': 'Quiz saved successfully'})
        self.assertEqual(response.status_code, 200)

    def test_modify_quiz_increased_size(self) -> None:
        """Test saving a quiz after adding questions and options."""
        # Arrange

        # Insert existing data
        quiz_data = self._get_default_quiz_data()
        self._insert_sample_data(Quiz, quiz_data)

        question_data = self._get_default_question_data()
        self._insert_sample_data(QuizQuestion, question_data)

        option_data = self._get_default_option_data()
        self._insert_sample_data(QuizOption, option_data)

        # Set up updated data
        data_updated = self._get_default_full_quiz_data()
        data_updated['quiz_data']['name'] = 'Test Quiz 2'
        data_updated['quiz_data']['quiz_question_data'].append(
            self._get_default_question_data({'question_number': 2})
        )
        data_updated['quiz_data']['quiz_question_data'][1][
            'quiz_option_data'] = [self._get_default_option_data()]

        # Act
        response = self._client.post(self._route, json=data_updated)
        json_data = response.get_json()

        # Assert
        self.assertEqual(json_data, {'message': 'Quiz saved successfully'})
        self.assertEqual(response.status_code, 200)

    def test_modify_quiz_decreased_size_to_empty(self) -> None:
        """Test saving a quiz after removing all questions and options."""
        # Arrange

        # Insert existing data
        quiz_data = self._get_default_quiz_data()
        self._insert_sample_data(Quiz, quiz_data)

        question_data = self._get_default_question_data()
        self._insert_sample_data(QuizQuestion, question_data)

        option_data = self._get_default_option_data()
        self._insert_sample_data(QuizOption, option_data)

        # Set up updated data
        data_updated = self._get_default_full_quiz_data()
        data_updated['quiz_data']['quiz_question_data'] = []

        # Act
        response = self._client.post(self._route, json=data_updated)
        json_data = response.get_json()

        # Assert
        self.assertEqual(json_data, {'message': 'Quiz saved successfully'})
        self.assertEqual(response.status_code, 200)

    def test_modify_quiz_decreased_size(self) -> None:
        """Test saving a quiz after removing questions and options."""
        # Arrange

        # Insert existing data
        # Quiz 1
        quiz_data = self._get_default_quiz_data()
        self._insert_sample_data(Quiz, quiz_data)

        # Question 1 belonging to Quiz 1
        question_data = self._get_default_question_data()
        self._insert_sample_data(QuizQuestion, question_data)

        # Question 2 belonging to Quiz 1
        question_data_2 = self._get_default_question_data(
            {'question_id': 2, 'question_number': 2})
        self._insert_sample_data(QuizQuestion, question_data_2)

        # Option 1 belonging to Question 1
        option_data = self._get_default_option_data()
        self._insert_sample_data(QuizOption, option_data)

        # Option 2 belonging to Question 1
        option_data_2 = self._get_default_option_data(
            {'option_id': 2, 'option_number': 2})
        self._insert_sample_data(QuizOption, option_data_2)

        # Option 1 belonging to Question 2
        option_data_3 = self._get_default_option_data(
            {'question_id': 2, 'option_id': 3, 'option_number': 1})
        self._insert_sample_data(QuizOption, option_data_3)

        # Set up updated data
        # Updated data contains new data for Question 1
        # With new data having 1 Question and 1 Option
        data_updated = self._get_default_full_quiz_data()

        # Act
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
        data = self._get_default_full_quiz_data()
        data['quiz_data']['quiz_id'] = 2  # Quiz with ID 2 does not exist

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
        quiz_data = self._get_default_quiz_data()
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


class TestEvaluateQuiz(RouteTestSetup):

    def __init__(self, methodName: str = "runTest") -> None:
        super().__init__(methodName)
        self._route = '/evaluate_quiz'

    def test_incorrect_json_input(self) -> None:
        """Test response if the dictionary input is in the wrong format."""
        # Arrange
        data = {}

        # Act
        response = self._client.post(self._route, json=data)
        json_data = response.get_json()

        # Assert
        self.assertEqual(
            json_data,
            {'message': 'Data requires keys "quiz_id" and "selections"'}
        )
        self.assertEqual(response.status_code, 200)

    @patch('app.sql_functions.evaluate_quiz')
    def test_evaluate_quiz_success(self, mock_request: MagicMock) -> None:
        """Test case where the server successfully evaluates quiz."""
        # Arrange
        mock_request.return_value = [True, False]
        data = {'quiz_id': 1, 'selections': []}

        # Act
        response = self._client.post(self._route, json=data)
        json_data = response.get_json()

        # Assert
        self.assertDictEqual(json_data, {'result': [True, False]})
        self.assertEqual(response.status_code, 200)

    @patch('app.sql_functions.evaluate_quiz')
    def test_evaluate_quiz_error_response(
        self, mock_request: MagicMock
    ) -> None:
        """Test the server response if the response is an error."""
        # Arrange
        mock_request.side_effect = Exception(
            'test_evaluate_quiz_error_response')
        data = {'quiz_id': 1, 'selections': []}

        # Act
        response = self._client.post(self._route, json=data)
        json_data = response.get_json()

        # Assert
        self.assertEqual(json_data, {'error': 'An error occurred'})
        self.assertEqual(response.status_code, 500)
        mock_request.assert_called_once_with(1, [])
