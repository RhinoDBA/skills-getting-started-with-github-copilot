# Mergington High School Activities API

A super simple FastAPI application that allows students to view and sign up for extracurricular activities.

## Features

- View all available extracurricular activities
- See signed-up participants in each activity card, updated after signup or removal
- Sign up for activities
- Unregister a participant using the trash icon next to their email

## Getting Started

1. Install the dependencies from the repository root:

   ```
   python -m pip install -r requirements.txt
   ```

2. Run the application:

   ```
   python app.py
   ```

3. Open your browser and go to:
   - API documentation: http://localhost:8000/docs
   - Alternative documentation: http://localhost:8000/redoc

## API Endpoints

| Method | Endpoint                                                          | Description                                                         |
| ------ | ----------------------------------------------------------------- | ------------------------------------------------------------------- |
| GET    | `/activities`                                                     | Get all activities with their details and current participant count |
| POST   | `/activities/{activity_name}/signup?email=student@mergington.edu` | Sign up for an activity                                             |
| DELETE | `/activities/{activity_name}/participants?email=student@mergington.edu` | Unregister a participant (404 if the activity or participant is not found) |

## Data Model

The application uses a simple data model with meaningful identifiers:

1. **Activities** - Uses activity name as identifier:

   - Description
   - Schedule
   - Maximum number of participants allowed
   - List of student emails who are signed up

2. **Students** - Uses email as identifier:
   - Name
   - Grade level

All data is stored in memory, which means data will be reset when the server restarts.

## Tests

Run the backend API tests from the repository root:

```
python -m pytest -q
```

The [tests directory](../tests/) contains tests for activity listing, the homepage
redirect, signup, and participant removal. Tests use FastAPI's TestClient, so no
running server or browser is needed. Each test gets fresh activity data, and the
original application state is restored afterward.

To run a single test file:

```
python -m pytest -q tests/test_signup.py
```
