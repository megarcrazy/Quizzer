# Quizzer

The Quizzer project is a web application that combines a Python Flask backend with a Typescript React frontend.
The main features of this website includes:
  - Storing and editing saved quizzes
  - Playing quizzes

## How to Run

### Backend (Python Flask)

To run the backend, follow these instructions:

1. Navigate to the `backend` directory.
    ```
    cd backend
    ```
2. Set up a virtual environment (recommended).
    ```
    python -m venv .venv
    ```
3. Activate the virtual environment.
    - On Windows:
        ```
        .venv\Scripts\activate
        ```
    - On Unix or MacOS:
        ```
        source .venv/bin/activate
        ```
4. Install the required Python packages.
    ```
    pip install -r requirements.txt
    ```
5. Run the Flask application.
    ```
    python run.py
    ```

The Flask backend runs at [http://localhost:5000].

### Frontend (Typescript React)

To run the frontend, follow these instructions:

1. Navigate to the `frontend` directory.
    ```
    cd frontend
    ```
2. Install the required Node.js packages.
    ```
    npm install
    ```
3. Start the React development server.
    ```
    npm start
    ```

The React frontend runs at [http://localhost:3000].

## Project Structure
- `backend`: Contains the Python Flask backend code.
- `frontend`: Contains the Typescript React frontend code.

