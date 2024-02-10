# Quizzer Backend
The Quizzer project uses a Python Flask backend.

# How to run
The current Python version used in this program is 3.10.9 (64-bit).

It is important to create a virtual environment when running a Python project. Create a virtual environment in a folder like ".venv" with:
```
python -m venv .venv
```
Activate the environment with:
<br />
Windows
```
.\venv\Scripts\activate
```
Unix or MacOS
```
source venv/bin/activate
```
Install the required packages with:
```
pip install -r requirements.txt
```
Run the application with:
```
python run.py
```
Run unit tests with:
```
python -m unittest discover -v -s ./tests -p "test_*.py"
```
# Linter
Linter: Flake8 https://flake8.pycqa.org/en/latest/
