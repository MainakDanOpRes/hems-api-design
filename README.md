# Home Energy Management System API

A Python REST API for managing home energy devices, representing energy-system constraints, and building toward intelligent home energy management.

This project is being developed as a portfolio project to demonstrate API design, domain modelling, software testing, persistence, and energy-management concepts.

## Project goals

The long-term goal is to build a Home Energy Management System (HEMS) that can represent a home's energy devices and constraints, collect measurements, and eventually support scheduling and energy optimisation.

The implementation is being developed incrementally, with an emphasis on clear separation of responsibilities, validated data, and maintainable code.

## Current features

- **Home management:** Register homes with a time zone and maximum grid import/export power limits.
- **Device management:** Register devices associated with a home and retrieve individual devices.
- **Device status:** Update a device's operational status.
- **Domain modelling:** Represent device types, statuses, capabilities, measurements, energy flows, and operating constraints.
- **Input validation:** Validate request data, names, time zones, and power limits.
- **HTTP error handling:** Return appropriate HTTP status codes for missing resources and invalid requests.
- **Automated tests:** Test domain behaviour, service logic, validation, and API endpoints.

### Supported device categories

The domain model currently includes:

- Solar photovoltaic (PV) systems
- Batteries
- Electric vehicle (EV) chargers
- Heat pumps
- Smart meters
- Washing machines

## Technology stack

- **Python 3.12+**
- **FastAPI** — REST API framework
- **Pydantic** — data modelling and validation
- **Uvicorn** — ASGI application server
- **pytest** — automated testing
- **uv** — dependency and project management

PostgreSQL, SQLAlchemy, and Alembic are planned for the persistence layer.

## Architecture

The project separates the API, application services, domain models, and repositories.

```text
app/
├── api/           # HTTP routes, request validation and dependencies
├── domain/        # Core energy and device domain models
├── services/      # Application use cases and business logic
└── repositories/  # Data access abstractions and implementations
```

The main responsibilities are:

- **API layer:** Handles HTTP requests, validates inputs, and translates application errors into HTTP responses.
- **Service layer:** Coordinates use cases, such as registering homes and devices or updating device status.
- **Domain layer:** Defines the core concepts, data structures, and validation rules of the HEMS.
- **Repository layer:** Abstracts data access so persistence can evolve without coupling business logic to a particular storage implementation.

The current repository implementation uses in-memory storage. A PostgreSQL-backed implementation is planned.

## Getting started

### Prerequisites

- Python 3.12 or later
- [uv](https://docs.astral.sh/uv/)

### 1. Clone the repository

```bash
git clone <your-repository-url>
cd hems_api_design
```

Replace `<your-repository-url>` with your GitHub repository URL.

### 2. Install dependencies

```bash
uv sync
```

### 3. Run the API

```bash
uv run uvicorn app.main:app --reload
```

The API will normally be available at:

- API base URL: http://127.0.0.1:8000
- Interactive Swagger documentation: http://127.0.0.1:8000/docs
- Alternative API documentation: http://127.0.0.1:8000/redoc

### 4. Run the tests

```bash
uv run python -m pytest -v
```

## API overview

The API currently provides endpoints for:

| Method | Endpoint | Purpose |
|---|---|---|
| `GET` | `/health` | Check API health |
| `POST` | `/homes` | Register a home |
| `GET` | `/homes/{home_id}` | Retrieve a home |
| `GET` | `/homes/{home_id}/devices` | List devices belonging to a home |
| `POST` | `/devices/homes/{home_id}` | Register a device for a home |
| `GET` | `/devices/{device_id}` | Retrieve a device |
| `PATCH` | `/devices/{device_id}/status` | Update a device's status |

Consult the interactive Swagger documentation at `/docs` for request schemas, response formats, and endpoint details.

## Testing

The project uses pytest to verify domain rules, application-service behaviour, request validation, and API responses.

Run the complete test suite with:

```bash
uv run python -m pytest -v
```

Tests are developed alongside features to help prevent regressions as the architecture evolves.

## Roadmap

- [x] Define core home and device domain models
- [x] Implement home and device registration
- [x] Add API endpoints for retrieving homes and devices
- [x] Implement device status updates
- [x] Add automated tests for domain, services, and API behaviour
- [ ] Add PostgreSQL persistence
- [ ] Introduce SQLAlchemy and Alembic migrations
- [ ] Add persistent measurements and energy-flow records
- [ ] Model device availability and scheduling
- [ ] Implement energy-management constraints and scheduling logic
- [ ] Develop an energy optimisation strategy
- [ ] Add deployment configuration and operational documentation

## Design principles

The project aims to demonstrate:

- Separation of concerns and modular architecture
- Explicit domain models and validation rules
- Repository abstractions for replaceable persistence
- Clear error handling and HTTP semantics
- Test-driven, incremental development
- A gradual path from API fundamentals toward energy-management functionality

## Status

**In active development.**

The current version focuses on the core API, domain model, and application-service structure. Persistent storage, scheduling, and optimisation remain future development milestones.

## License

No license has been selected yet. A license can be added once the intended reuse and distribution terms have been decided.
