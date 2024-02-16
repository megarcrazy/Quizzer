from datetime import datetime
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

        # Insert existing data
        quiz_data = self._get_default_quiz_data()
        self._insert_sample_data(Quiz, quiz_data)

        question_data = self._get_default_question_data()
        self._insert_sample_data(QuizQuestion, question_data)

        option_data = self._get_default_option_data()
        self._insert_sample_data(QuizOption, option_data)

        quiz_id = 1

        # Act
        with self._app.app_context():
            result = sql_functions.select_full_quiz(quiz_id)

        # Assert
        self.assertEqual(len(result), 1)
        self.assertDictEqual(
            result[0],
            {
                'created_at': datetime.utcfromtimestamp(0),
                'correct_answer': True,
                'name': 'Test Quiz',
                'option_id': 1,
                'option_number': 1,
                'option_text': 'Test Option',
                'question_id': 1,
                'question_number': 1,
                'question_text': 'Test Question',
                'quiz_id': 1,
                'updated_at': datetime.utcfromtimestamp(0)
            }
        )


class TestSaveQuiz(RouteTestSetup):

    def __init__(self, methodName: str = "runTest") -> None:
        super().__init__(methodName)

    def test_add_new_quiz(self) -> None:
        """Test adding a new quiz with new data."""
        # Arrange
        data = self._get_default_full_quiz_data()
        data['quiz_data']['quiz_id'] = 0

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
        with self._app.app_context():
            # Insert quiz to save to override
            result = sql_functions.save_quiz(data_updated)

        # Assert
        self.assertEqual(result, True)

        # Extract rows from SQL database
        quiz_list, quiz_question_list, quiz_option_list = \
            self._extract_full_quiz_by_id(1)

        self.assertEqual(len(quiz_list), 1)
        self.assertEqual(len(quiz_question_list), 1)
        self.assertEqual(len(quiz_option_list), 1)
        self.assertEqual(quiz_list[0].name, 'Test Quiz 2')
        self.assertEqual(quiz_question_list[0].text, 'Test Question 2')
        self.assertEqual(quiz_option_list[0].text, 'Test Option 2')

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
        with self._app.app_context():
            # Insert quiz to save to override
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
        with self._app.app_context():
            # Insert quiz to save to override
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
        with self._app.app_context():
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
        data = self._get_default_full_quiz_data()
        data['quiz_data']['quiz_id'] = 2  # Quiz with ID 2 does not exist

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
        quiz_data = self._get_default_quiz_data()
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


class TestGetQuizList(RouteTestSetup):

    def __init__(self, methodName: str = "runTest") -> None:
        super().__init__(methodName)

    def test_get_quizzes_empty(self) -> None:
        """Test get quiz list if no quiz exists."""
        # Arrange
        limit = 1

        # Act
        with self._app.app_context():
            quiz_list = sql_functions.get_quiz_list(limit)

        # Assert
        self.assertEqual(quiz_list, [])

    def test_get_quizzes_non_empty(self) -> None:
        """Test get quiz list if quizzes exist."""
        # Arrange
        quiz_data = {'name': 'Test Quiz'}
        self._insert_sample_data(Quiz, quiz_data)  # Create a quiz
        limit = 1

        # Act
        with self._app.app_context():
            quiz_list = sql_functions.get_quiz_list(limit)

        # Assert
        self.assertEqual(quiz_list, [{'name': 'Test Quiz', 'quiz_id': 1}])
