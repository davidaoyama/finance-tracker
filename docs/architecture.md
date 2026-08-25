Yep — this should be `docs/architecture.md`. It captures the backend structure and engineering decisions without getting into implementation yet.

# System Architecture

This document defines the initial technical architecture for Financial Tracker.

The application is designed as a local-first full-stack application with a separate frontend, backend, and local SQLite database.

---

## Architecture Overview

```text id="e9d4x7"
┌─────────────────────────────┐
│        Next.js Frontend     │
│      React + TypeScript     │
└──────────────┬──────────────┘
               │
               │ HTTP / REST
               ▼
┌─────────────────────────────┐
│       FastAPI Backend       │
│           Python            │
└──────────────┬──────────────┘
               │
               ▼
┌─────────────────────────────┐
│       Service Layer         │
│      Business Logic         │
└──────────────┬──────────────┘
               │
               ▼
┌─────────────────────────────┐
│      Repository Layer       │
│      Data Access Logic      │
└──────────────┬──────────────┘
               │
               ▼
┌─────────────────────────────┐
│     SQLAlchemy / SQLite     │
└─────────────────────────────┘
```

The frontend never accesses SQLite directly.

All application behavior involving financial data goes through the backend API.

---

# Frontend

## Technology

- Next.js
- React
- TypeScript

The frontend is responsible for:

- Displaying financial information
- Collecting user input
- Form validation for user experience
- Sending requests to the backend API
- Rendering dashboards and visualizations
- Managing client-side UI state

The frontend should not be the source of truth for financial calculations.

Examples of logic that should remain in the backend:

- Account balance updates
- Monthly expense totals
- Goal allocation calculations
- Reward calculations
- Transfer behavior
- Financial validation

---

# Backend

## Technology

- Python
- FastAPI
- Pydantic
- SQLAlchemy
- Alembic
- pytest

The backend is responsible for:

- API endpoints
- Validation
- Business logic
- Financial calculations
- Database access
- Maintaining financial consistency
- Enforcing application rules

---

# Backend Layers

The backend will use a layered architecture.

```text id="4dtw5h"
API Route
   ↓
Service
   ↓
Repository
   ↓
Database
```

Each layer has a specific responsibility.

---

## API / Route Layer

The route layer handles HTTP requests and responses.

Example:

```text id="29b9fr"
POST /transactions
```

The route should:

- Parse the request
- Validate the request structure
- Call the appropriate service
- Return the appropriate response

The route should **not** contain complex financial logic.

Example:

```text id="xk9j9e"
Bad:

POST /transactions
    ├── update balance
    ├── calculate points
    ├── validate category
    ├── create transaction
    └── create goal contribution
```

Instead:

```text id="ft6hlm"
POST /transactions
        ↓
TransactionService
        ↓
business logic
```

---

# Service Layer

The service layer contains application and financial business logic.

Examples:

```text id="3se0gk"
TransactionService
AccountService
GoalService
RewardService
DashboardService
```

Responsibilities may include:

- Validating business rules
- Calculating account balance changes
- Calculating monthly totals
- Calculating rewards
- Creating transfers
- Realizing goal contributions
- Managing goal allocations
- Coordinating multiple repositories

The service layer is where the application decides **what should happen**.

---

# Repository Layer

Repositories handle database access.

Examples:

```text id="7lq7ge"
AccountRepository
TransactionRepository
GoalRepository
CategoryRepository
PaymentMethodRepository
```

Repositories are responsible for:

- Querying records
- Creating records
- Updating records
- Deleting/deactivating records
- Persisting database changes

Repositories should not contain high-level financial business rules.

Example:

```text id="t0f5go"
Repository:
"Find account 123."

Service:
"Determine whether account 123 can be used for this transaction."
```

---

# Database Layer

## Database

SQLite will be used for the initial application.

SQLite is appropriate because:

- The application is local-only
- There is one primary user per local instance
- The application does not require a database server
- Financial data should remain on the user's machine
- The project does not require large-scale concurrent writes

## ORM

SQLAlchemy will be used as the database abstraction layer.

SQLAlchemy will provide:

- Database models
- Relationships
- Queries
- Transactions
- Database connection management

Raw SQL may still be used where it improves clarity or performance.

---

# Database Migrations

Alembic will manage database schema migrations.

Migrations allow the database schema to evolve without manually recreating the database.

Example:

```text id="i0r4m7"
Migration 001
Create accounts

Migration 002
Create transactions

Migration 003
Add reward rules

Migration 004
Add points fields
```

The application should not rely on automatically recreating the database whenever the schema changes.

---

# Financial Operations and Atomicity

Financial operations must be atomic.

An operation that changes multiple records should either complete entirely or not happen at all.

Example: creating an expense.

```text id="fb8m6y"
BEGIN

Validate account
Validate category
Validate payment method
Calculate reward
Create transaction
Update account balance

COMMIT
```

If any operation fails:

```text id="0ylz74"
ROLLBACK
```

This prevents inconsistent states such as:

```text id="85is7b"
Transaction exists
but
Account balance was not updated
```

Operations that should be atomic include:

- Creating expenses
- Creating income
- Creating transfers
- Editing transactions
- Deleting/deactivating transactions
- Adjusting account balances
- Realizing goal contributions
- Updating related goal allocation state

---

# Project Structure

Initial backend structure:

```text id="fp5q2m"
backend/
├── app/
│   ├── main.py
│   │
│   ├── api/
│   │   └── routes/
│   │       ├── accounts.py
│   │       ├── transactions.py
│   │       ├── categories.py
│   │       ├── payment_methods.py
│   │       ├── goals.py
│   │       ├── reward_rules.py
│   │       └── dashboard.py
│   │
│   ├── models/
│   │   ├── account.py
│   │   ├── transaction.py
│   │   ├── category.py
│   │   ├── payment_method.py
│   │   ├── goal.py
│   │   ├── goal_contribution.py
│   │   ├── account_balance_history.py
│   │   └── reward_rule.py
│   │
│   ├── schemas/
│   │   ├── account.py
│   │   ├── transaction.py
│   │   ├── category.py
│   │   ├── payment_method.py
│   │   ├── goal.py
│   │   └── reward_rule.py
│   │
│   ├── services/
│   │   ├── account_service.py
│   │   ├── transaction_service.py
│   │   ├── goal_service.py
│   │   ├── reward_service.py
│   │   └── dashboard_service.py
│   │
│   ├── repositories/
│   │   ├── account_repository.py
│   │   ├── transaction_repository.py
│   │   ├── category_repository.py
│   │   ├── payment_method_repository.py
│   │   ├── goal_repository.py
│   │   └── reward_rule_repository.py
│   │
│   ├── db/
│   │   ├── database.py
│   │   └── base.py
│   │
│   └── core/
│       └── config.py
│
├── tests/
│   ├── unit/
│   └── integration/
│
├── alembic/
├── alembic.ini
├── requirements.txt
└── README.md
```

This structure is intentionally modular but should grow only as the application needs additional code.

---

# Testing Strategy

Testing is part of the development process rather than a final step.

## Unit Tests

Unit tests should focus on isolated business logic.

Examples:

- Reward calculation
- Monthly expense calculation
- Goal progress calculation
- Available balance calculation
- Transfer validation

## Integration Tests

Integration tests should verify interactions between:

- API
- Services
- Database

Examples:

- Creating an expense updates the account balance
- Creating a transfer updates both accounts
- Realizing a goal contribution creates a transfer
- Editing a transaction correctly reverses and reapplies financial effects

## Financial Invariants

Tests should verify important financial rules.

Examples:

```text id="wwr1t4"
Transfer:
Total money before = Total money after

Expense:
Account balance decreases by amount

Income:
Account balance increases by amount

Goal allocation:
Actual account balance does not change unless the allocation is realized

Reward:
Historical points do not change when reward rules are edited
```

---

# Frontend / Backend Separation

The frontend and backend are independent applications.

```text id="7fh2px"
frontend/
    Next.js + React + TypeScript

backend/
    Python + FastAPI
```

The frontend communicates with the backend exclusively through the API.

This allows:

- Independent frontend/backend development
- Clear API contracts
- Backend-focused testing
- Future replacement of either layer
- Practice building a traditional full-stack architecture

---

# Local Development

The intended development environment is:

```text id="4zqfgt"
Browser
   ↓
Next.js development server
   ↓
FastAPI development server
   ↓
SQLite database file
```

No external services are required for normal application functionality.

---

# Initial Development Milestone

The first implementation milestone is intentionally small.

## Milestone 1 — Backend Foundation

1. Create the Python backend project.
2. Install and configure FastAPI.
3. Create the FastAPI application.
4. Add a health-check endpoint.
5. Set up SQLite.
6. Set up SQLAlchemy.
7. Set up Alembic.
8. Create the initial database migration.
9. Create the `accounts` model.
10. Create account CRUD endpoints.
11. Write tests for account behavior.

The first endpoint should be:

```http
GET /api/health
```

Expected response:

```json
{
  "status": "ok"
}
```

---

# Initial Implementation Order

After the backend foundation:

```text id="yssxkl"
1. Backend project setup
2. SQLite connection
3. SQLAlchemy setup
4. Alembic migrations
5. Accounts
6. Account tests
7. Categories
8. Payment methods
9. Transactions
10. Transaction financial logic
11. Transaction tests
12. Goals
13. Goal contributions
14. Rewards
15. Dashboard
16. Frontend
```

The order may change as development reveals new requirements.

---

# Engineering Principles

### Keep Business Logic Out of Routes

Routes coordinate requests. Services contain application behavior.

### Keep Database Access Out of Services When Practical

Services should use repositories rather than constructing database queries throughout business logic.

### Keep Financial Operations Atomic

Multiple changes that represent one financial operation should commit together.

### Prefer Explicitness Over Cleverness

Financial logic should be easy to read and reason about.

### Test Financial Rules

Incorrect financial calculations are more important than superficial UI bugs.

### Build Incrementally

Avoid creating the entire architecture before the application needs it.

The project should evolve as requirements and implementation details become clearer.
