# SupportDesk API

A RESTful IT support ticket management API built with **Python, FastAPI, SQLAlchemy, and SQLite**.

SupportDesk API provides endpoints to create, retrieve, update, delete, and list IT support tickets. It includes request validation, database persistence, pagination, priority filtering, and automated tests.

## Features

- Create support tickets.
- Retrieve a ticket by its ID.
- List tickets with pagination.
- Filter tickets by priority.
- Update existing tickets.
- Delete tickets.
- Validate request data with Pydantic.
- Persist ticket records using SQLAlchemy and SQLite.
- Configure application settings through environment variables.
- Automated API tests using pytest.

## Tech Stack

- Python 3.13+
- FastAPI
- SQLAlchemy
- SQLite
- Pydantic
- Uvicorn
- Pytest
- HTTPX

## Project Structure

```text
SupportDeskAPI/
├── app/
│   ├── core/
│   │   └── config.py
│   ├── db/
│   │   ├── database.py
│   │   └── models.py
│   ├── routers/
│   │   └── tickets.py
│   ├── schemas/
│   │   └── ticket.py
│   └── main.py
├── tests/
│   ├── conftest.py
│   ├── test_main.py
│   └── test_tickets.py
├── .env.example
├── .gitignore
├── requirements.txt
└── README.md
```

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/YargamCR/supportdesk-api.git
cd supportdesk-api
```

### 2. Create a virtual environment

```bash
python -m venv .venv
```

Activate it on Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

### 3. Install dependencies

```bash
python -m pip install -r requirements.txt
```

### 4. Configure environment variables

Create your local `.env` file from the example:

```powershell
Copy-Item .env.example .env
```

Default configuration:

```env
APP_NAME="SupportDesk API"
APP_VERSION=0.1.0
ENVIRONMENT=development
DATABASE_URL=sqlite:///./supportdesk.db
```

### 5. Start the API

```bash
python -m uvicorn app.main:app --reload
```

The API will be available at:

`http://127.0.0.1:8000`

Interactive API documentation:

- Swagger UI: `http://127.0.0.1:8000/docs`
- ReDoc: `http://127.0.0.1:8000/redoc`

## API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| POST | `/tickets/` | Create a ticket |
| GET | `/tickets/` | List tickets |
| GET | `/tickets/{ticket_id}` | Retrieve a ticket |
| PUT | `/tickets/{ticket_id}` | Update a ticket |
| DELETE | `/tickets/{ticket_id}` | Delete a ticket |

### Ticket Data

A ticket contains:

| Field | Type | Description |
|---|---|---|
| id | Integer | Unique ticket identifier |
| title | String | Ticket title |
| description | String | Detailed issue description |
| priority | String | `low`, `medium`, or `high` |

Priority defaults to `medium` when omitted.

### Create a Ticket

**POST** `/tickets/`

Example request:

```json
{
    "title": "Computer not starting",
    "description": "The workstation does not boot after pressing the power button.",
    "priority": "high"
}
```

Example response:

```json
{
    "message": "Ticket created successfully",
    "data": {
        "id": 1,
        "title": "Computer not starting",
        "description": "The workstation does not boot after pressing the power button.",
        "priority": "high"
    }
}
```

### List Tickets

**GET** `/tickets/`

Supported query parameters:

| Parameter | Default | Description |
|---|---:|---|
| skip | 0 | Number of records to skip |
| limit | 10 | Maximum number of records to return (1–100) |
| priority | None | Optional priority filter |

Example:

```text
GET /tickets/?skip=0&limit=10&priority=high
```

### Error Handling

The API returns HTTP `404 Not Found` when a requested ticket does not exist.

Invalid request data is handled through FastAPI and Pydantic validation.

## Running Tests

Run the automated test suite:

```bash
python -m pytest -v
```

The project currently includes tests covering:

- Root endpoint.
- Ticket creation and validation.
- Ticket retrieval.
- Ticket updates.
- Ticket deletion.
- Missing ticket handling.
- Pagination.
- Priority filtering.
- Default priority behavior.

## Future Improvements

- Ticket status management.
- User authentication and authorization.
- Role-based access control.
- Database migrations with Alembic.
- PostgreSQL support.
- Additional filtering and search capabilities.

---

**SupportDesk API** — A practical REST API project focused on backend development, database integration, and automated testing.
