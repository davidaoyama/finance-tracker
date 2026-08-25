# Product Definition

## Product

Financial Tracker is a local-first personal finance application for tracking spending, income, account balances, transfers, and financial goals.

The application is designed primarily for personal use and runs entirely on the user's computer.

## Problem

It can be difficult to quickly understand:

- How much money has been spent this month
- How much money has been earned this month
- How much money is left over
- Where money is being spent
- How money is distributed across financial accounts
- Whether enough money is being allocated toward financial goals

Financial information may exist across checking accounts, savings accounts, investment accounts, and credit cards, making it difficult to visualize everything together.

## Primary Product Question

The dashboard should answer:

> **What is this month looking like financially?**

Specifically:

- How much income have I received?
- How much have I spent?
- How much is left over?
- What am I spending money on?
- Where is my money currently allocated?

## Target User

The initial target user is an individual who wants to manually track and visualize their personal finances without connecting bank accounts or sending financial data to an external service.

The application is single-user and local-first.

## Product Principles

### Local First

All financial data should remain on the user's computer.

The application should not require:

- An account
- Authentication
- Cloud storage
- A hosted backend
- Bank account integrations

### Manual First

Users manually enter their financial activity.

Automation and importing can be considered later.

### Simple Financial Model

The application should make a clear distinction between:

- **Expense:** money spent
- **Income:** money received
- **Transfer:** money moved between owned accounts

Transfers must not count as expenses or income.

### Accounts vs. Goals

An **account** represents where money currently exists.

Examples:

- Checking
- HYSA
- Brokerage
- Roth IRA

A **goal** represents where the user intends to allocate money.

Examples:

- Save $10,000 in a HYSA
- Invest $1,000 per month
- Save $4,000 for a trip

### User-Controlled Data

The tracker represents the user's personal model of their finances.

Account balances do not need to perfectly match the balances reported by financial institutions.

## MVP

The MVP should allow the user to:

- Create and manage financial accounts
- Record expenses
- Record income
- Record transfers
- Categorize expenses
- Edit and delete transactions
- Track account balances
- View transaction history
- View monthly income
- View monthly expenses
- View money remaining for the month
- View spending by category
- View account balances from the dashboard

## Post-MVP

Potential future functionality includes:

- Financial goals
- Recurring expenses
- Credit card point multipliers
- Estimated credit card rewards
- More detailed analytics
- Historical trends
- Custom categories
- CSV imports
- Backup/export functionality

These features are not requirements for the initial MVP.

## Success Criteria

The MVP is successful when the user can manually record their financial activity and use the dashboard to understand their current monthly financial position without referencing another tracking tool.
