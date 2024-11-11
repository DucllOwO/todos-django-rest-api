# TodoAPI

This project is a Django REST API application for managing a basic todo list. It includes CRUD operations, token-based authentication, including tests to cover the API endpoints and auto-generated API documentation using Swagger.

## Setup Instructions

1. **Clone the Repository**

```bash
git clone <your-repository-url>
cd TodoAPI
```

2. Create and Activate a Virtual Environment

• On macOS/Linux:

```
python3 -m venv venv
source venv/bin/activate
```

3. Install Dependencies

```
pip install -r requirements.txt
```

4. Apply Migrations

```
python manage.py migrate
```

5. Create a Superuser

```
python manage.py createsuperuser
```

Follow the prompts to set up the superuser account to login.

6. Run the Development Server

```
python manage.py runserver
```

The application will be accessible at http://127.0.0.1:8000/api/v1.

## API Endpoints

The following API endpoints are available:

- List All Todos
  - GET /api/v1/todos/
- Create a New Todo
  - POST /api/v1/todos/
  - Request Body:

```
{
  "title": "Sample Todo",
  "description": "This is a sample todo item.",
  "completed": false
}
```

- Retrieve a Single Todo
  - GET /api/v1/todos/{id}/
- Update a Todo
  - PUT /api/v1/todos/{id}/
  - Request Body:

```
{
"title": "Updated Todo",
"description": "This is an updated description.",
"completed": true
}
```

- Delete a Todo
  - DELETE /api/v1/todos/{id}/

## Authentication

This API uses token-based authentication. To interact with the API endpoints, follow these steps:

1. Obtain an Authentication Token

```
curl -X POST -d "username=yourusername&password=yourpassword" http://127.0.0.1:8000/api/v1/token/
```

The response will include a token:

```
{
  "token": "your-generated-token"
}
```

2. Include the Token in Your Requests

For authenticated requests, include the token in the Authorization header:

```
curl -H "Authorization: Token your-generated-token" http://127.0.0.1:8000/api/v1/todos/
```

## API Documentation

Interactive API documentation is available via Swagger:

    •	Swagger UI: http://127.0.0.1:8000/api/v1/swagger/
    •	ReDoc: http://127.0.0.1:8000/api/v1/redoc/

## Running Tests

To run the test suite:

```
python manage.py test
```

This command will execute the tests defined in the todos/tests.py file.
