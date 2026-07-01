# API Routes Reference

Base URL when running locally:

```text
http://localhost:5000
```

Protected routes require a JWT access token:

```http
Authorization: Bearer <access_token>
Content-Type: application/json
```

## Auth

### POST `/api/auth/register`

Create a user account.

Request:

```json
{
  "username": "alice",
  "email": "alice@example.com",
  "password": "secret123"
}
```

Response:

```json
{
  "access_token": "jwt-token",
  "user": {
    "id": 1,
    "username": "alice",
    "email": "alice@example.com",
    "role": "user",
    "is_active": true,
    "created_at": "2026-07-01T10:30:00"
  }
}
```

### POST `/api/auth/login`

Log in and get an access token.

Request:

```json
{
  "email": "alice@example.com",
  "password": "secret123"
}
```

Response:

```json
{
  "access_token": "jwt-token",
  "user": {
    "id": 1,
    "username": "alice",
    "email": "alice@example.com",
    "role": "user",
    "is_active": true,
    "created_at": "2026-07-01T10:30:00"
  }
}
```

### POST `/api/auth/logout`

Requires auth.

Request:

```json
{}
```

Response:

```json
{
  "message": "Logged out successfully"
}
```

### GET `/api/auth/profile`

Requires auth.

Response:

```json
{
  "id": 1,
  "username": "alice",
  "email": "alice@example.com",
  "role": "user",
  "is_active": true,
  "created_at": "2026-07-01T10:30:00"
}
```

## Categories

### GET `/api/categories`

List all categories.

Response:

```json
[
  {
    "id": 1,
    "name": "Science",
    "description": "Science quiz category"
  }
]
```

### POST `/api/categories`

Requires admin.

Request:

```json
{
  "name": "Science",
  "description": "Science quiz category"
}
```

Response:

```json
{
  "id": 1,
  "name": "Science",
  "description": "Science quiz category"
}
```

### PUT `/api/categories/{category_id}`

Requires admin.

Request:

```json
{
  "name": "General Science",
  "description": "Updated science category"
}
```

Response:

```json
{
  "id": 1,
  "name": "General Science",
  "description": "Updated science category"
}
```

### DELETE `/api/categories/{category_id}`

Requires admin.

Response:

```json
{
  "message": "Category deleted"
}
```

## Quizzes

### GET `/api/quizzes`

List public quizzes.

Optional query parameters:

```text
category_id=1
search=science
```

Response:

```json
[
  {
    "id": 1,
    "creator_id": 1,
    "creator_username": "alice",
    "category_id": 1,
    "category_name": "Science",
    "title": "Basic Science Quiz",
    "description": "Simple questions",
    "is_public": true,
    "time_limit": 600,
    "question_count": 2,
    "total_marks": 2,
    "created_at": "2026-07-01T10:30:00"
  }
]
```

### GET `/api/quizzes/{quiz_id}`

Get one quiz with questions. Public users do not receive `correct_answer`; admin or creator can receive answers.

Response:

```json
{
  "id": 1,
  "creator_id": 1,
  "creator_username": "alice",
  "category_id": 1,
  "category_name": "Science",
  "title": "Basic Science Quiz",
  "description": "Simple questions",
  "is_public": true,
  "time_limit": 600,
  "question_count": 1,
  "total_marks": 1,
  "created_at": "2026-07-01T10:30:00",
  "questions": [
    {
      "id": 1,
      "quiz_id": 1,
      "question_text": "What planet is known as the Red Planet?",
      "option_a": "Earth",
      "option_b": "Mars",
      "option_c": "Jupiter",
      "option_d": "Venus",
      "marks": 1,
      "options": [
        { "key": "A", "text": "Earth" },
        { "key": "B", "text": "Mars" },
        { "key": "C", "text": "Jupiter" },
        { "key": "D", "text": "Venus" }
      ]
    }
  ]
}
```

### GET `/api/quizzes/category/{category_id}`

List public quizzes in one category.

Response:

```json
[
  {
    "id": 1,
    "creator_id": 1,
    "creator_username": "alice",
    "category_id": 1,
    "category_name": "Science",
    "title": "Basic Science Quiz",
    "description": "Simple questions",
    "is_public": true,
    "time_limit": 600,
    "question_count": 1,
    "total_marks": 1,
    "created_at": "2026-07-01T10:30:00"
  }
]
```

### POST `/api/quizzes`

Requires auth.

Request:

```json
{
  "title": "Basic Science Quiz",
  "description": "Simple questions",
  "category_id": 1,
  "time_limit": 600,
  "is_public": true
}
```

Response:

```json
{
  "id": 1,
  "creator_id": 1,
  "creator_username": "alice",
  "category_id": 1,
  "category_name": "Science",
  "title": "Basic Science Quiz",
  "description": "Simple questions",
  "is_public": true,
  "time_limit": 600,
  "question_count": 0,
  "total_marks": 0,
  "created_at": "2026-07-01T10:30:00"
}
```

### PUT `/api/quizzes/{quiz_id}`

Requires quiz creator or admin.

Request:

```json
{
  "title": "Updated Science Quiz",
  "description": "Updated description",
  "category_id": 1,
  "time_limit": 900,
  "is_public": true
}
```

Response:

```json
{
  "id": 1,
  "creator_id": 1,
  "creator_username": "alice",
  "category_id": 1,
  "category_name": "Science",
  "title": "Updated Science Quiz",
  "description": "Updated description",
  "is_public": true,
  "time_limit": 900,
  "question_count": 1,
  "total_marks": 1,
  "created_at": "2026-07-01T10:30:00",
  "questions": [
    {
      "id": 1,
      "quiz_id": 1,
      "question_text": "What planet is known as the Red Planet?",
      "option_a": "Earth",
      "option_b": "Mars",
      "option_c": "Jupiter",
      "option_d": "Venus",
      "marks": 1,
      "correct_answer": "B"
    }
  ]
}
```

### DELETE `/api/quizzes/{quiz_id}`

Requires quiz creator or admin.

Response:

```json
{
  "message": "Quiz deleted"
}
```

### GET `/api/my/quizzes`

Requires auth. Lists quizzes created by the current user.

Response:

```json
[
  {
    "id": 1,
    "creator_id": 1,
    "creator_username": "alice",
    "category_id": 1,
    "category_name": "Science",
    "title": "Basic Science Quiz",
    "description": "Simple questions",
    "is_public": true,
    "time_limit": 600,
    "question_count": 1,
    "total_marks": 1,
    "created_at": "2026-07-01T10:30:00"
  }
]
```

## Questions

### POST `/api/quizzes/{quiz_id}/questions`

Requires admin.

Request:

```json
{
  "question_text": "What planet is known as the Red Planet?",
  "option_a": "Earth",
  "option_b": "Mars",
  "option_c": "Jupiter",
  "option_d": "Venus",
  "correct_answer": "B",
  "marks": 1
}
```

Response:

```json
{
  "id": 1,
  "quiz_id": 1,
  "question_text": "What planet is known as the Red Planet?",
  "option_a": "Earth",
  "option_b": "Mars",
  "option_c": "Jupiter",
  "option_d": "Venus",
  "marks": 1,
  "correct_answer": "B"
}
```

### PUT `/api/questions/{question_id}`

Requires admin.

Request:

```json
{
  "question_text": "Which planet is called the Red Planet?",
  "option_a": "Earth",
  "option_b": "Mars",
  "option_c": "Jupiter",
  "option_d": "Venus",
  "correct_answer": "B",
  "marks": 2
}
```

Response:

```json
{
  "id": 1,
  "quiz_id": 1,
  "question_text": "Which planet is called the Red Planet?",
  "option_a": "Earth",
  "option_b": "Mars",
  "option_c": "Jupiter",
  "option_d": "Venus",
  "marks": 2,
  "correct_answer": "B"
}
```

### DELETE `/api/questions/{question_id}`

Requires admin.

Response:

```json
{
  "message": "Question deleted"
}
```

## Attempts

### POST `/api/quizzes/{quiz_id}/start`

Requires auth. The quiz must be public and must have questions.

Request:

```json
{}
```

Response:

```json
{
  "attempt_id": 1,
  "quiz_id": 1,
  "total_marks": 2,
  "time_limit": 600,
  "questions": [
    {
      "id": 1,
      "question_text": "What planet is known as the Red Planet?",
      "marks": 1,
      "options": [
        { "key": "A", "text": "Earth" },
        { "key": "B", "text": "Mars" },
        { "key": "C", "text": "Jupiter" },
        { "key": "D", "text": "Venus" }
      ]
    }
  ]
}
```

### POST `/api/quizzes/{quiz_id}/submit`

Requires auth.

Request:

```json
{
  "attempt_id": 1,
  "answers": [
    {
      "question_id": 1,
      "selected_answer": "B"
    },
    {
      "question_id": 2,
      "selected_answer": "A"
    }
  ]
}
```

Response:

```json
{
  "attempt_id": 1,
  "score": 1,
  "total_marks": 2,
  "percentage": 50.0,
  "answers": [
    {
      "question_id": 1,
      "selected_answer": "B",
      "correct_answer": "B",
      "is_correct": true,
      "marks": 1
    },
    {
      "question_id": 2,
      "selected_answer": "A",
      "correct_answer": "C",
      "is_correct": false,
      "marks": 0
    }
  ],
  "leaderboard_rank": 3
}
```

### GET `/api/my/attempts`

Requires auth. Lists completed attempts for the current user.

Response:

```json
[
  {
    "id": 1,
    "user_id": 1,
    "quiz_id": 1,
    "quiz_title": "Basic Science Quiz",
    "score": 1,
    "total_marks": 2,
    "percentage": 50.0,
    "completed_at": "2026-07-01T10:45:00"
  }
]
```

### GET `/api/attempts/{attempt_id}`

Requires attempt owner or admin.

Response:

```json
{
  "id": 1,
  "user_id": 1,
  "quiz_id": 1,
  "quiz_title": "Basic Science Quiz",
  "score": 1,
  "total_marks": 2,
  "percentage": 50.0,
  "completed_at": "2026-07-01T10:45:00",
  "answers": [
    {
      "question_id": 1,
      "question_text": "What planet is known as the Red Planet?",
      "selected_answer": "B",
      "correct_answer": "B",
      "is_correct": true
    }
  ]
}
```

## Leaderboard

### GET `/api/leaderboard/quiz/{quiz_id}`

Top 50 users for a quiz.

Response:

```json
[
  {
    "rank": 1,
    "user_id": 1,
    "username": "alice",
    "score": 2,
    "total_marks": 2,
    "percentage": 100.0,
    "completed_at": "2026-07-01T10:45:00"
  }
]
```

### GET `/api/leaderboard/category/{category_id}`

Top 50 users for a category.

Response:

```json
[
  {
    "user_id": 1,
    "username": "alice",
    "total_score": 12,
    "rank": 1
  }
]
```

## Dashboard

### GET `/api/dashboard`

Requires auth.

Response:

```json
{
  "user": {
    "id": 1,
    "username": "alice",
    "email": "alice@example.com",
    "role": "user",
    "is_active": true,
    "created_at": "2026-07-01T10:30:00"
  },
  "stats": {
    "quizzes_created": 1,
    "total_attempts": 3,
    "highest_score": 100.0
  },
  "created_quizzes": [
    {
      "id": 1,
      "creator_id": 1,
      "creator_username": "alice",
      "category_id": 1,
      "category_name": "Science",
      "title": "Basic Science Quiz",
      "description": "Simple questions",
      "is_public": true,
      "time_limit": 600,
      "question_count": 1,
      "total_marks": 1,
      "created_at": "2026-07-01T10:30:00"
    }
  ],
  "recent_attempts": [
    {
      "id": 1,
      "user_id": 1,
      "quiz_id": 1,
      "quiz_title": "Basic Science Quiz",
      "score": 1,
      "total_marks": 1,
      "percentage": 100.0,
      "completed_at": "2026-07-01T10:45:00"
    }
  ]
}
```

## Admin

### GET `/api/admin/users`

Requires admin.

Response:

```json
[
  {
    "id": 1,
    "username": "alice",
    "email": "alice@example.com",
    "role": "user",
    "is_active": true,
    "created_at": "2026-07-01T10:30:00"
  }
]
```

### GET `/api/admin/quizzes`

Requires admin. Lists all quizzes, including non-public quizzes.

Response:

```json
[
  {
    "id": 1,
    "creator_id": 1,
    "creator_username": "alice",
    "category_id": 1,
    "category_name": "Science",
    "title": "Basic Science Quiz",
    "description": "Simple questions",
    "is_public": true,
    "time_limit": 600,
    "question_count": 1,
    "total_marks": 1,
    "created_at": "2026-07-01T10:30:00"
  }
]
```

### DELETE `/api/admin/quizzes/{quiz_id}`

Requires admin.

Response:

```json
{
  "message": "Quiz deleted"
}
```

### DELETE `/api/admin/users/{user_id}`

Requires admin.

Response:

```json
{
  "message": "User deleted"
}
```

## Error Examples

Validation or permission errors use this shape:

```json
{
  "error": "title is required"
}
```

Common status codes:

```text
200 OK
201 Created
400 Bad Request
401 Unauthorized
403 Forbidden
404 Not Found
409 Conflict
```
