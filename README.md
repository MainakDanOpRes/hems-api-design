# Home Energy Management System (HEMS)

A production-oriented Home Energy Management System API built with **Python and FastAPI**.

The goal of this project is to design a system capable of monitoring and managing residential energy assets such as solar PV, batteries, EV chargers, heat pumps, and smart meters.

The system is being developed incrementally, starting from the **domain model** and evolving toward a complete backend with telemetry, scheduling, forecasting, tariffs, and energy optimization.

---

## Project Goals

The system is designed to eventually support:

* Home and device management
* Real-time device state
* Energy measurements and telemetry
* Energy-flow tracking
* Device commands
* Scheduling
* Electricity tariffs and time-varying prices
* Solar PV production forecasting
* Home energy-demand forecasting
* Optimal energy scheduling
* Battery charging/discharging optimization
* EV charging optimization
* Integration with physical gateways and devices
* MQTT-based telemetry and communication
* Authentication and authorization
* Persistent storage with PostgreSQL
* Automated testing
* Containerized deployment
* API documentation with OpenAPI

The project is intentionally being developed step by step so that the domain and architecture remain understandable and maintainable.

---

## Architecture

The target architecture is:

```text
                    ┌─────────────────────┐
                    │      REST API       │
                    │      FastAPI        │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │ Application Services│
                    │                     │
                    │ Scheduling          │
                    │ Forecasting         │
                    │ Tariffs             │
                    │ Optimization         │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │     Domain Model    │
                    │                     │
                    │ Home                │
                    │ Device              │
                    │ Measurement         │
                    │ EnergyFlow          │
                    │ Command             │
                    │ Schedule            │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │   Infrastructure    │
                    │                     │
                    │ PostgreSQL          │
                    │ MQTT                │
                    │ External APIs       │
                    └─────────────────────┘
```

The domain model is kept separate from the API and infrastructure layers so that business rules are not tightly coupled to FastAPI or a particular database.

---

## Domain Model

The current domain model contains the following concepts:

```text
Home
 │
 ├── Devices
 │     │
 │     ├── Device
 │     └── Battery
 │
 ├── Measurements
 │
 └── Energy Flows
```

### Home

Represents a residential energy system.

A home currently contains:

* unique identifier
* name
* timezone
* maximum grid import power
* maximum grid export power

### Device

Represents a physical or logical energy device belonging to a home.

Examples include:

* Smart meter
* Solar PV
* Battery
* EV charger
* Heat pump
* Washing machine

Devices have:

* identity
* type
* manufacturer
* model
* operational status

### Battery

A battery is modeled as a specialized device.

It extends the common `Device` model with battery-specific information such as:

* capacity
* maximum charging power
* maximum discharging power
* state of charge
* current power
* capabilities

The project uses a combination of **inheritance and composition**:

```text
Device
   ↑
Battery
   │
   ├── BatteryState
   └── DeviceCapabilities
```

This allows common device behavior to be shared while keeping device-specific state and capabilities separate.

### Measurement

A measurement represents an observation made by a device at a particular point in time.

Examples:

```text
Battery SOC = 73%
Battery power = 3 kW
PV power = 4.2 kW
Grid import = 2.1 kW
```

Measurements are historical data and will eventually form the foundation for telemetry, monitoring, forecasting, and optimization.

---

## Example Home

The project uses a representative residential energy system for development and testing.

Example devices:

| Device          | Type          | Example             |
| --------------- | ------------- | ------------------- |
| Smart Meter     | Meter         | Grid import/export  |
| Solar PV        | Generator     | 6 kW PV system      |
| Home Battery    | Storage       | 10 kWh battery      |
| EV Charger      | Flexible load | 7.4 kW charger      |
| Heat Pump       | Flexible load | Heating/cooling     |
| Washing Machine | Flexible load | Shiftable appliance |

This example will become progressively more realistic as the system develops.

---

## Technology Stack

Current:

* Python
* Pydantic
* FastAPI

Planned:

* PostgreSQL
* SQLAlchemy
* MQTT
* Docker
* Pytest
* OpenAPI
* Authentication / authorization
* Forecasting libraries
* Optimization solver

---

## Project Structure

Current project structure:

```text
hems/
├── app/
│   ├── __init__.py
│   └── domain/
│       ├── __init__.py
│       ├── home.py
│       ├── device.py
│       ├── battery.py
│       ├── capabilities.py
│       └── measurement.py
│
├── main.py
├── test_domain.py
└── README.md
```

The structure will evolve as application, infrastructure, API, database, and testing layers are introduced.

---

## Development Roadmap

### Phase 1 — Domain Modeling

* [x] Model `Home`
* [x] Model `Device`
* [x] Define device types
* [x] Define device status
* [x] Model device capabilities
* [x] Model `Battery`
* [x] Model battery state
* [x] Model `Measurement`
* [ ] Model energy flows
* [ ] Model device constraints
* [ ] Model commands
* [ ] Model schedules
* [ ] Model tariffs
* [ ] Model forecasts
* [ ] Model optimization plans

### Phase 2 — Application Layer

* [ ] Define application services
* [ ] Define use cases
* [ ] Separate business logic from API layer
* [ ] Add domain validation rules
* [ ] Introduce repositories

### Phase 3 — REST API

* [ ] Home endpoints
* [ ] Device endpoints
* [ ] Measurement endpoints
* [ ] Energy-flow endpoints
* [ ] Command endpoints
* [ ] Schedule endpoints
* [ ] Tariff endpoints
* [ ] Forecast endpoints
* [ ] Optimization endpoints

### Phase 4 — Persistence

* [ ] PostgreSQL
* [ ] SQLAlchemy
* [ ] Database migrations
* [ ] Repository implementations
* [ ] Time-series data strategy

### Phase 5 — Telemetry & Device Integration

* [ ] MQTT integration
* [ ] Gateway model
* [ ] Telemetry ingestion
* [ ] Device state updates
* [ ] Device commands
* [ ] Event processing

### Phase 6 — Energy Intelligence

* [ ] Electricity tariff integration
* [ ] PV production forecasting
* [ ] Home demand forecasting
* [ ] Battery optimization
* [ ] EV charging optimization
* [ ] Flexible-load scheduling
* [ ] Global home energy optimization

### Phase 7 — Production Readiness

* [ ] Authentication
* [ ] Authorization / RBAC
* [ ] Structured logging
* [ ] Error handling
* [ ] Automated tests
* [ ] Integration tests
* [ ] Docker
* [ ] CI/CD
* [ ] API documentation
* [ ] Monitoring
* [ ] Deployment

---

## Design Principles

The project follows several principles:

### Domain first

Business concepts and rules are modeled before implementing API endpoints.

### Separation of concerns

The domain should not depend directly on FastAPI, PostgreSQL, MQTT, or external services.

### Explicit business rules

Energy constraints should be represented explicitly rather than hidden inside API endpoints.

### Time-series awareness

Energy measurements are inherently time-dependent, so historical observations are treated differently from current device state.

### Optimization-ready design

Device capabilities, constraints, forecasts, tariffs, and schedules are being modeled with the future optimization engine in mind.

### Incremental complexity

The system starts with a clear domain model and progressively introduces infrastructure and production concerns.

---

## Current Status

**Early development — Domain Modeling**

The current implementation focuses on establishing a clean domain model before building the complete REST API and persistence layer.

The project is not yet production-ready.

---

## Future Vision

The final system should be able to answer questions such as:

> When should the battery charge?

> Should the battery charge from the grid or wait for solar production?

> When is the cheapest time to charge the EV?

> Can the home avoid exceeding its grid-import limit?

> How much solar energy will be produced tomorrow?

> How should flexible appliances be scheduled around electricity prices?

> What is the optimal energy schedule for the next 24 hours?

The long-term objective is to build these capabilities on top of a well-structured domain model rather than implementing them as isolated API features.
