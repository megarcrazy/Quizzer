import os
import sys
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
from app import sql_functions, Quiz, QuizOption, QuizQuestion  # Noqa: E402
from tests.route_setup import RouteTestSetup  # Noqa: E402


class TestGetFullQuiz(RouteTestSetup):
    """Test get_full_quiz."""

    def __init__(self, methodName: str = "runTest") -> None:
        super().__init__(methodName)

    def test_full_quiz_empty_table(self) -> None:
        """Empty table with no data or quiz does not exist."""
        # Arrange
        quiz_id = 1

        # Act
        with self._app.app_context():
            result = sql_functions.select_full_quiz(quiz_id)

        # Assert
        self.assertEqual(result, [])

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

        quiz_id = 1

        # Act
        with self._app.app_context():
            result = sql_functions.select_full_quiz(quiz_id)

        # Assert
        self.assertEqual(len(result), 1)
        self.assertCountEqual(
            result[0].keys(),
            [
                'created_at', 'name', 'option_id', 'option_number',
                'option_text', 'question_id', 'question_number',
                'question_text', 'quiz_id', 'updated_at'
            ]
        )
        self.assertEqual(result[0]['name'], 'Test Quiz')
        self.assertEqual(result[0]['option_id'], 1)
        self.assertEqual(result[0]['option_number'], 1)
        self.assertEqual(result[0]['option_text'], 'Blue')
        self.assertEqual(result[0]['question_id'], 1)
        self.assertEqual(result[0]['question_number'], 1)
        self.assertEqual(result[0]['question_text'], 'Favourite colour?')
        self.assertEqual(result[0]['quiz_id'], 1)


class TestSaveQuiz(RouteTestSetup):

    def __init__(self, methodName: str = "runTest") -> None:
        super().__init__(methodName)

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
        with self._app.app_context():
            result = sql_functions.save_quiz(data)

        # Assert
        self.assertEqual(result, True)

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
        with self._app.app_context():
            result = sql_functions.save_quiz(data)

        # Assert
        self.assertEqual(result, True)

        # Extract rows from SQL database
        quiz_list, quiz_question_list, quiz_option_list = \
            self._extract_full_quiz_by_id(1)

        self.assertEqual(len(quiz_list), 1)
        self.assertEqual(len(quiz_question_list), 1)
        self.assertEqual(len(quiz_option_list), 1)

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
        with self._app.app_context():
            # Insert quiz to save to override
            sql_functions.save_quiz(data)
            result = sql_functions.save_quiz(data_updated)

        # Assert
        self.assertEqual(result, True)

        # Extract rows from SQL database
        quiz_list, quiz_question_list, quiz_option_list = \
            self._extract_full_quiz_by_id(1)

        self.assertEqual(len(quiz_list), 1)
        self.assertEqual(len(quiz_question_list), 1)
        self.assertEqual(len(quiz_option_list), 1)
        self.assertEqual(quiz_list[0].name, 'Test quiz 2')
        self.assertEqual(quiz_question_list[0].text, 'Test question 2')
        self.assertEqual(quiz_option_list[0].text, 'Test option 2')

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
        with self._app.app_context():
            # Insert quiz to save to override
            sql_functions.save_quiz(data)
            result = sql_functions.save_quiz(data_updated)

        # Assert
        self.assertEqual(result, True)

        # Extract rows from SQL database
        quiz_list, quiz_question_list, quiz_option_list = \
            self._extract_full_quiz_by_id(1)

        self.assertEqual(len(quiz_list), 1)
        self.assertEqual(len(quiz_question_list), 2)
        self.assertEqual(len(quiz_option_list), 2)

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
        # Act
        with self._app.app_context():
            # Insert quiz to save to override
            sql_functions.save_quiz(data)
            result = sql_functions.save_quiz(data_updated)

        # Assert
        self.assertEqual(result, True)

        # Extract rows from SQL database
        quiz_list, quiz_question_list, quiz_option_list = \
            self._extract_full_quiz_by_id(1)

        self.assertEqual(len(quiz_list), 1)
        self.assertEqual(len(quiz_question_list), 0)
        self.assertEqual(len(quiz_option_list), 0)

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
        with self._app.app_context():
            # Insert quiz to save to override
            sql_functions.save_quiz(data)
            result = sql_functions.save_quiz(data_updated)

        # Assert
        self.assertEqual(result, True)

        # Extract rows from SQL database
        quiz_list, quiz_question_list, quiz_option_list = \
            self._extract_full_quiz_by_id(1)

        self.assertEqual(len(quiz_list), 1)
        self.assertEqual(len(quiz_question_list), 1)
        self.assertEqual(len(quiz_option_list), 1)

    def test_incorrect_data_format(self) -> None:
        """Test server response if the data is in the incorrect format."""
        # Arrange
        data = {'test': []}

        # Act
        with self._app.app_context():
            # Expect an exception
            with self.assertRaises(Exception) as context:
                # Insert quiz to save to override
                sql_functions.save_quiz(data)

        # Assert
        self.assertEqual(context.exception.__class__, KeyError)

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
        with self._app.app_context():
            result = sql_functions.save_quiz(data)

        # # Assert
        self.assertEqual(result, False)


class TestDeleteQuiz(RouteTestSetup):

    def __init__(self, methodName: str = "runTest") -> None:
        super().__init__(methodName)
        self._route = '/delete-quiz'

    def test_delete_quiz_sucessful(self) -> None:
        """Test successfully deleting a quiz in the database."""
        # Arrange
        delete_quiz_data = {'quiz_id': 1}
        quiz_data = {'name': 'Test Quiz'}
        self._insert_sample_data(Quiz, quiz_data)  # Create a quiz

        # Act
        with self._app.app_context():
            result = sql_functions.delete_quiz(delete_quiz_data)

        # Assert
        self.assertEqual(result, True)
        quiz_list = self._extract_quiz_by_id(1)
        self.assertEqual(quiz_list, [])

    def test_delete_quiz_not_exist(self) -> None:
        """Test attempting to delete a quiz that does not exist."""
        # Arrange
        delete_quiz_data = {'quiz_id': 1}

        # Act
        with self._app.app_context():
            result = sql_functions.delete_quiz(delete_quiz_data)

        # Assert
        self.assertEqual(result, False)

    def test_incorrect_data_format(self) -> None:
        """Test server response if the data is in the incorrect format."""
        # Arrange
        delete_quiz_data = {'quiz': 1}

        # Act
        with self._app.app_context():
            # Expect an exception
            with self.assertRaises(Exception) as context:
                # Insert quiz to save to override
                sql_functions.delete_quiz(delete_quiz_data)

        # Assert
        self.assertEqual(context.exception.__class__, KeyError)
