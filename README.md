# Financial Tracker

A local-first personal finance tracker for manually tracking income, expenses, transfers, financial accounts, and savings goals.

The project is designed to run entirely on a user's computer. There is no hosted service, authentication, or cloud storage. Financial data remains in a local SQLite database.

## Why I'm Building This

I want a simple way to answer:

> **What is this month looking like financially?**

The application should make it easy to understand:

* How much I've earned this month
* How much I've spent this month
* How much money I have left over
* Where my money is being spent
* How money is distributed across my accounts
* Whether I'm allocating enough money toward my financial goals

This project is also an opportunity to practice product planning, system design, full-stack development, testing, and writing maintainable software.

## Core Concepts

### Transactions

There are three primary transaction types:

**Expense**

Money spent on something.

Examples:

* Rent
* Restaurants
* Groceries
* Travel
* Entertainment
* Shopping
* Miscellaneous

Expenses can include information such as:

* Amount
* Date/time
* Merchant or description
* Location
* Category
* Payment method
* Recurring status
* Notes

**Income**

Money received.

Examples:

* Paycheck
* Refund
* Reimbursement

Income records include where the money came from and which account received it.

**Transfer**

Money moved between accounts owned by the user.

Examples:

* Checking → HYSA
* Checking → Brokerage
* Checking → Roth IRA
* Checking → Trip Fund

Transfers should not be counted as income or expenses.

### Accounts

Accounts represent where money currently exists.

Examples:

* Checking
* HYSA
* Brokerage
* Roth IRA

The application maintains its own representation of account balances based on the information entered by the user. It is not intended to automatically mirror a bank's records.

### Goals

Goals represent where the user intends to allocate money rather than where money currently exists.

Examples:

* Contribute $1,000/month to a brokerage account
* Save $10,000 in a HYSA
* Save $4,000 for a trip
* Contribute a target amount to a Roth IRA

Goals may be monthly or longer-term.

### Recurring Expenses

Expenses such as subscriptions can be marked as recurring.

Examples:

* Spotify
* Netflix
* Gym membership

Recurring expenses can automatically generate transactions on their scheduled date and can later be stopped or modified.

### Credit Card Rewards

Expenses can record the credit card used for a purchase.

A future feature will allow cards to have category-specific point multipliers so the application can estimate rewards earned.

Example:

```text
Purchase:       $150
Category:       Restaurants
Card:           Chase Sapphire Preferred
Multiplier:     3x
Estimated:      450 points
```

Credit card balance tracking is not currently a goal of the application.

## Dashboard

The dashboard should primarily answer:

> **What is this month looking like?**

The initial dashboard will display information such as:

* Monthly income
* Monthly expenses
* Money remaining
* Spending by category
* Account balances
* Goal progress

Additional analytics and visualizations can be added over time.

## Initial Navigation

```text
Dashboard
Transactions
Accounts
Goals
Recurring Expenses
Settings
```

Transactions can be manually created, edited, and deleted.

The primary transaction actions are:

```text
+ Expense
+ Income
+ Transfer
```

## MVP

The first usable version of Financial Tracker should allow a user to:

1. Create financial accounts
2. Record income
3. Record expenses
4. Record transfers between accounts
5. Categorize expenses
6. Edit and delete transactions
7. Track account balances
8. View monthly income and expenses
9. View remaining monthly money
10. View spending broken down by category

Goals, recurring transactions, credit-card rewards, and more advanced analytics can be developed after the core transaction system works.

## Tech Stack

### Frontend

* React
* TypeScript
* Next.js

### Backend

* Python
* FastAPI

### Database

* SQLite

The frontend and backend are intentionally separate applications communicating through an HTTP API.

```text
Next.js / React
      |
      | HTTP / REST
      v
Python / FastAPI
      |
      v
SQLite
```

## Project Structure

Initial structure:

```text
financial-tracker/
├── frontend/
├── backend/
├── docs/
├── tests/
├── README.md
└── .gitignore
```

The structure may change as the architecture develops.

## Project Principles

### Local First

The application should work entirely on a user's computer without requiring an external service.

### Manual First

Transactions will initially be entered manually. Bank integrations and automatic transaction imports are outside the initial scope.

### Simple Before Complex

Features should be added only after the core transaction and account model works correctly.

### Test Important Financial Logic

Financial calculations and transaction behavior should have automated tests, particularly around:

* Account balances
* Transfers
* Monthly totals
* Expense categorization
* Goal contributions
* Recurring transactions

## Future Ideas

Potential features beyond the MVP include:

* Recurring expense automation
* Monthly and yearly financial goals
* Credit card reward estimation
* Spending trends
* Net worth history
* CSV transaction imports
* More detailed financial analytics
* Custom categories
* Data export and backup

These are ideas rather than committed requirements.

## Status

🚧 Early development / planning
