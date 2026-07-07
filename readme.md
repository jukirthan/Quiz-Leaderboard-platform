# Quiz & Leaderboard Platform - Backend

A Flask REST API where users can create quizzes by category, other users can attempt them, and scores are ranked on a leaderboard.

## Features

- User registration and login (JWT based)
- Role-based access: only admins can create quizzes/questions
- Creators can build quizzes with multiple choice questions and correct answers
- Browse quizzes by category
- Take a quiz and get the score calculated on the server
- Leaderboard per quiz and per category
- User dashboard showing quizzes created and attempts taken
- Timed quizzes (time_limit field)
- Question shuffling (shuffle_questions field)
- Badge on leaderboard (Gold / Silver / Bronze) based on percentage

## Tech Stack

- Python, Flask
- Flask-SQLAlchemy (SQLite by default)
- Flask-JWT-Extended for authentication
- Flask-Bcrypt for password hashing

## Setup

1. Create a virtual environment

```
python -m venv venv
venv\Scripts\activate
```

2. Install dependencies

```
pip install -r requirements.txt
```

3. Copy `.env.example` to `.env` and update values if needed

4. Run the app

```
python run.py
```

5. (Optional) Seed default categories

```
python run_seeders.py
```

6. Create an admin user (required to create quizzes/questions)

Either register with an `admin_code` matching `ADMIN_SIGNUP_CODE` in your `.env`, or promote an existing user:

```
python make_admin.py user@example.com
```

The API will be running at `http://127.0.0.1:5000`

## Roles

- Every user has a `role` of either `user` (default) or `admin`.
- Only `admin` users can create quizzes/questions (`POST /api/quizzes/`).
- Set `ADMIN_SIGNUP_CODE` in `.env` and pass it as `admin_code` in the register request body to sign up directly as an admin, or use `make_admin.py` to promote an existing account.

## API Endpoints

### Auth
- `POST /api/auth/register` - register a new user (optional `admin_code` field to sign up as admin)
- `POST /api/auth/login` - login and receive a JWT token

### Categories
- `GET /api/categories/` - list all categories
- `POST /api/categories/` - create a category (auth required)

### Quizzes
- `GET /api/quizzes/` - list all quizzes
- `GET /api/quizzes/?category_id=1` - list quizzes by category
- `POST /api/quizzes/` - create a quiz with questions (admin only)
- `GET /api/quizzes/<id>` - get quiz questions to attempt (no correct answers shown)
- `GET /api/quizzes/<id>/detail` - get quiz with correct answers (auth required, creator use)
- `DELETE /api/quizzes/<id>` - delete a quiz (auth required, only creator)

### Attempts
- `POST /api/attempts/` - submit answers for a quiz, score is calculated server side (auth required)
- `GET /api/attempts/leaderboard/quiz/<quiz_id>` - leaderboard for a quiz
- `GET /api/attempts/leaderboard/category/<category_id>` - leaderboard for a category
- `GET /api/attempts/my-attempts` - list attempts of logged in user (auth required)

### Dashboard
- `GET /api/dashboard/` - quizzes created and attempts taken by logged in user (auth required)

## Sample: Create Quiz Request Body

```json
{
  "title": "Basic Python Quiz",
  "description": "Test your python basics",
  "category_id": 1,
  "time_limit": 10,
  "shuffle_questions": true,
  "questions": [
    {
      "question_text": "What is the output of 2 + 2?",
      "option_a": "3",
      "option_b": "4",
      "option_c": "5",
      "option_d": "6",
      "correct_option": "b"
    }
  ]
}
```

## Sample: Submit Attempt Request Body

```json
{
  "quiz_id": 1,
  "time_taken": 120,
  "answers": {
    "1": "b"
  }
}
```
