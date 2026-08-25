# API Design

The Financial Tracker backend exposes a REST API for the Next.js frontend.

The API is local-only and communicates with the frontend over HTTP.

Base URL:

```text
http://localhost:8000/api
```

## API Principles

- The frontend does not access SQLite directly.
- Business logic belongs in the backend.
- Financial operations should be atomic.
- The API should represent product behavior rather than simply exposing database tables.
- Destructive operations should preserve historical financial data where necessary.

---

# Accounts

Accounts represent tracked financial accounts.

```text
GET    /accounts
GET    /accounts/{id}
POST   /accounts
PATCH  /accounts/{id}
DELETE /accounts/{id}
POST   /accounts/{id}/adjust-balance
GET    /accounts/{id}/transactions
GET    /accounts/{id}/balance-history
```

`DELETE` deactivates the account rather than physically deleting it.

## Create Account

```http
POST /accounts
```

Example request:

```json
{
  "name": "Chase Checking",
  "type": "CHECKING",
  "current_balance": 5000.0
}
```

## Adjust Account Balance

```http
POST /accounts/{id}/adjust-balance
```

Example:

```json
{
  "balance": 4920.0,
  "reason": "Bank statement reconciliation"
}
```

The backend should update the current balance and create an `ADJUSTMENT` record in account balance history.

---

# Transactions

Expenses, income, and transfers are represented by one transaction resource.

```text
GET    /transactions
GET    /transactions/{id}
POST   /transactions
PATCH  /transactions/{id}
DELETE /transactions/{id}
```

## Expense

```http
POST /transactions
```

Example:

```json
{
  "type": "EXPENSE",
  "amount": 150.0,
  "transaction_date": "2026-08-24",
  "name": "Target",
  "memo": "Kitchen supplies",
  "account_id": 1,
  "category_id": 4,
  "payment_method_id": 2
}
```

The backend must:

1. Validate the account is active.
2. Validate the category is active.
3. Validate the payment method is active.
4. Validate the payment method's funding account.
5. Determine the applicable reward rule.
6. Store the reward multiplier.
7. Calculate and store points earned.
8. Create the transaction.
9. Decrease the account's current balance.
10. Commit the operation atomically.

If any step fails, the entire operation should roll back.

## Income

```http
POST /transactions
```

Example:

```json
{
  "type": "INCOME",
  "amount": 2000.0,
  "transaction_date": "2026-08-23",
  "name": "Employer",
  "memo": "August paycheck",
  "account_id": 1
}
```

The backend must:

1. Validate the account is active.
2. Create the transaction.
3. Increase the account's current balance.
4. Commit the operation atomically.

## Transfer

```http
POST /transactions
```

Example:

```json
{
  "type": "TRANSFER",
  "amount": 500.0,
  "transaction_date": "2026-08-24",
  "source_account_id": 1,
  "destination_account_id": 2,
  "memo": "Monthly savings"
}
```

The backend must:

1. Validate both accounts are active.
2. Verify source and destination accounts are different.
3. Decrease the source account balance.
4. Increase the destination account balance.
5. Create the transaction.
6. Commit the operation atomically.

Transfers do not count as income or expenses.

## Cash Withdrawal

Cash withdrawals are represented as transfers.

Example:

```json
{
  "type": "TRANSFER",
  "amount": 500.0,
  "transaction_date": "2026-08-24",
  "source_account_id": 1,
  "destination_account_id": null,
  "name": "Cash withdrawal"
}
```

The Checking account decreases, but Cash is not represented as a tracked account.

## Editing Transactions

```http
PATCH /transactions/{id}
```

Editing a transaction must correctly reverse the transaction's previous financial effects and apply the new effects.

Example:

```text
Old expense:
$100

Edited expense:
$150

Account balance should change by an additional $50.
```

Changing a transaction should also update any affected reward calculations.

Historical relationships must be preserved.

## Deleting Transactions

```http
DELETE /transactions/{id}
```

Transactions should not be physically deleted when doing so would destroy historical relationships, such as a goal contribution linked to the transaction.

The backend should instead mark the transaction as inactive/deleted and reverse its financial effects appropriately.

---

# Categories

```text
GET    /categories
POST   /categories
PATCH  /categories/{id}
DELETE /categories/{id}
```

Deleting a category deactivates it.

Expenses without a specified category should default to `Miscellaneous`.

Inactive categories cannot be assigned to new transactions.

---

# Payment Methods

```text
GET    /payment-methods
GET    /payment-methods/{id}
POST   /payment-methods
PATCH  /payment-methods/{id}
DELETE /payment-methods/{id}
```

Example:

```json
{
  "name": "Chase Sapphire Preferred VISA",
  "type": "CREDIT_CARD",
  "funding_account_id": 1
}
```

Payment methods are deactivated rather than physically deleted.

Inactive payment methods cannot be used for new transactions.

---

# Reward Rules

```text
GET    /payment-methods/{id}/reward-rules
POST   /payment-methods/{id}/reward-rules
PATCH  /reward-rules/{id}
DELETE /reward-rules/{id}
```

Example:

```json
{
  "category_id": 4,
  "multiplier": 3.0
}
```

A default rule can use a null category:

```json
{
  "category_id": null,
  "multiplier": 1.0
}
```

When calculating rewards:

1. Look for an active category-specific rule.
2. If none exists, use the active default rule.
3. If neither exists, award zero points.

Historical transactions store the multiplier and points earned at the time the transaction was created.

Changing a reward rule does not recalculate historical transactions.

---

# Goals

```text
GET    /goals
GET    /goals/{id}
POST   /goals
PATCH  /goals/{id}
DELETE /goals/{id}

GET    /goals/{id}/contributions
POST   /goals/{id}/contributions
```

Example:

```json
{
  "name": "Xbox",
  "target_amount": 500.0,
  "current_allocated_amount": 0,
  "linked_account_id": null,
  "frequency": "ONE_TIME",
  "status": "ACTIVE",
  "start_date": "2026-08-24",
  "target_date": null
}
```

Goals may be:

```text
ONE_TIME
MONTHLY
YEARLY
```

Goal statuses:

```text
ACTIVE
COMPLETED
CANCELLED
EXPIRED
```

A goal can have zero or one linked account.

---

# Goal Contributions

```http
GET  /goals/{id}/contributions
POST /goals/{id}/contributions
```

Example:

```json
{
  "amount": 500.0,
  "date": "2026-08-24",
  "account_id": 1
}
```

Creating a contribution initially creates a virtual allocation.

The contribution may optionally be linked to a transaction later.

---

# Realizing a Goal Contribution

A goal contribution can be turned into a real financial transfer.

```http
POST /goals/{goal_id}/contributions/{contribution_id}/realize
```

Example:

```json
{
  "target_account_id": 2
}
```

The backend must:

1. Validate the goal and contribution.
2. Validate the source account.
3. Determine the destination account.
4. Create the transfer transaction.
5. Update the source account balance.
6. Update the destination account balance.
7. Link the transfer transaction to the contribution.
8. Commit the entire operation atomically.

For a goal with a linked account, the linked account can be used as the default destination.

---

# Dashboard

The dashboard is a product-level aggregation rather than a direct representation of a database table.

```http
GET /dashboard
```

Optional month query:

```http
GET /dashboard?month=2026-08
```

Example response:

```json
{
  "period": {
    "year": 2026,
    "month": 8
  },
  "monthly_income": 5000.0,
  "monthly_expenses": 2400.0,
  "money_remaining": 2600.0,
  "spending_by_category": [
    {
      "category": "Restaurants",
      "amount": 450.0
    },
    {
      "category": "Shopping",
      "amount": 300.0
    }
  ],
  "accounts": [
    {
      "id": 1,
      "name": "Chase Checking",
      "balance": 5200.0,
      "allocated": 800.0,
      "available": 4400.0
    }
  ],
  "goals": [
    {
      "id": 1,
      "name": "Xbox",
      "target": 500.0,
      "allocated": 250.0,
      "progress": 0.5
    }
  ]
}
```

The backend is responsible for dashboard calculations so the frontend does not need to independently implement financial business logic.

---

# Database Transactions and Atomicity

Financial operations must be atomic.

For example, creating an expense should not be implemented as independent operations:

```text
1. Insert transaction
2. Update account balance
3. Calculate rewards
```

Instead:

```text
BEGIN TRANSACTION

Validate input
Validate related records
Calculate rewards
Insert transaction
Update account balance

COMMIT
```

If any step fails:

```text
ROLLBACK
```

This prevents inconsistent states such as:

```text
Transaction exists
but
Account balance was not updated
```

The same principle applies to:

- Expenses
- Income
- Transfers
- Balance adjustments
- Realized goal contributions

---

# Initial API Resources

```text
/accounts
/transactions
/categories
/payment-methods
/reward-rules
/goals
/goal-contributions
/dashboard
```

`account_balance_history` is not exposed as a general writeable resource. Balance history should be generated and managed by backend business logic.
