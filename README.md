# AutoDoc

AutoDoc is a REST API for managing employee records and generating DOCX documents from templates. It is built with FastAPI, PostgreSQL and Docker.

## Features 

- Company and employee management
- Employee address management
- Employment contracts
- Job roles
- Workplace hazards
- Sanitary examinations
- DOCX document generation
- Request validation with Pydantic
- Database migrations with Alembic
- Docker Compose support
- OpenAPI documentation

## Tech Stack

- Python
- FastAPI
- Pydantic
- PostgreSQL
- SQLAlchemy
- Alembic
- python-docx
- Docker
- Docker Compose

## Overview

AutoDoc generates personalized DOCX documents using a template stored in:
```text
templates/example.docx
```
During document generation, placeholders are replaced with employee data. The generated document is stored temporarily in memory using `BytesIO` and returned with `StreamingResponse`. Generated documents are not saved in the application directory.

## API Methods

The API is divided into the following endpoint groups.

| Group | Description |
|---|---|
| Companies | Manage companies |
| Employees | Manage employees |
| Addresses | Manage employee addresses |
| Contracts | Manage employment contracts |
| Roles | Manage job roles |
| Hazards | Manage workplace hazards |
| Sanitaries | Manage sanitary examinations |
| Documents | Generate and download employee documents |

A company can have multiple employees. An employee can have multiple contracts, and each contract can have a role and sanitary examinations.

## Data Validation

Request data is validated with Pydantic. It includes:

- required and optional fields,
- minimum and maximum text length,
- Polish ZIP codes in the `00-000` format,
- ten-digit VAT numbers,
- separate schemas for creating, updating and returning resources.

Update schemas contain optional fields, allowing clients to send only the values that should be changed.

## Error Handling

| Status | Meaning |
|---|---|
| `200 OK` | Request completed successfully |
| `201 Created` | Resource created successfully |
| `204 No Content` | Resource deleted successfully |
| `404 Not Found` | Requested resource does not exist |
| `409 Conflict` | Database constraint or resource conflict |
| `422 Unprocessable Entity` | Request validation failed |

Database integrity errors are handled with transaction rollback to keep the SQLAlchemy session usable after a failed operation.

## Setup - Docker Compose

Clone the repository:
```bash
git clone https://github.com/mknnnnnnn/autodoc
cd autodoc
```
Create an `.env` file:
```bash
cp .env.example .env
```

Start the application:
```bash
docker compose up -d db
docker compose run --rm api alembic upgrade head
docker compose up -d
```

### Usage

Open Swagger in your browser:
```text
http://localhost:8000/docs
```

Stop the application:
```bash
docker compose down
```

Remove the database volume:
```bash
docker compose down -v
```