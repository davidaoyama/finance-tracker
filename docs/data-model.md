# Data Model

This document describes the conceptual data model for Financial Tracker.

The purpose of this model is to define the major financial entities and their relationships before designing the database schema.

---

## Account

An Account represents a real location where the user's money is held or managed.

Examples:

- Checking account
- Savings account
- HYSA
- Brokerage account
- Roth IRA

An account may contain:

- Name
- Account type
- Current tracked balance
- Starting balance

### Balance Concepts

The application distinguishes between money that physically exists in an account and money that has been virtually allocated toward goals.

#### Actual Balance

The amount of money currently represented as existing in the account.

Example:

```text
Checking Actual Balance: $2,000
```

#### Allocated Balance

Money that still physically exists in the account but has been allocated toward one or more goals.

Example:

```text
Xbox Goal: $500
```

The $500 still exists in Checking but is considered committed toward the Xbox goal.

#### Available Balance

Money that has not been allocated toward a goal.

```text
Available Balance = Actual Balance - Goal Allocations
```

Example:

```text
Checking

Actual Balance:       $2,000
Goal Allocations:       $500
Available Balance:    $1,500
```

Goal allocations do not change the actual account balance.

---

## Transaction

A Transaction is a recorded financial event that changes the financial state of one or more accounts.

There are three transaction types:

```text
EXPENSE
INCOME
TRANSFER
```

Transaction amounts are stored as positive values.

The transaction type determines how the amount affects the financial model.

Common transaction information may include:

- Amount
- Date/time
- Name/description
- Memo
- Location

---

## Expense

An Expense represents money spent by the user.

Example:

```text
Merchant: McDonald's
Amount: $15
Category: Restaurants
Payment Method: Chase Sapphire Preferred
Date: August 24
```

Expenses contribute toward:

- Monthly expenses
- All-time expenses
- Category spending
- Payment-method spending

An expense decreases the actual balance of the account ultimately funding the expense.

For the purposes of this application, the user is assumed to maintain sufficient funds in their funding account. Overdraft and credit-limit behavior is outside the intended scope.

---

## Income

Income represents money received by the user from an external source.

Examples:

- Paycheck
- Refund
- Reimbursement

Income includes a destination account.

Example:

```text
Source: Employer
Amount: $2,000
Destination: Checking
```

The destination account's actual balance increases by the income amount.

---

## Transfer

A Transfer represents money moving between two accounts owned by the user.

Example:

```text
$500

Checking
   ↓
SoFi HYSA
```

A transfer:

- Decreases the source account
- Increases the destination account
- Does not create income
- Does not create an expense
- Does not change the user's total amount of money

Example:

```text
Before

Checking:     $2,000
HYSA:         $3,000
Total:        $5,000

Transfer $500 Checking → HYSA

After

Checking:     $1,500
HYSA:         $3,500
Total:        $5,000
```

---

## Category

A Category classifies expenses according to what the money was spent on.

Initial examples include:

- Rent
- Restaurants
- Groceries
- Shopping
- Entertainment
- Travel
- Miscellaneous

Categories allow expenses to be grouped for reporting and dashboard visualizations.

Example:

```text
August Spending

Rent             $1,500
Restaurants        $400
Groceries          $300
Entertainment      $150
Travel             $500
```

Categories may become user-configurable in a future version.

---

## Payment Method

A Payment Method describes how an expense was paid.

Examples:

- Chase Sapphire Preferred
- Another credit card
- Debit card
- Cash

For credit cards, the primary purpose of Payment Method is to track:

- Spending by card
- Spending category
- Future credit-card reward calculations

The application does not initially attempt to maintain accurate credit-card balances.

### Funding Account

A payment method may ultimately be associated with an account used to fund it.

For example:

```text
Chase Sapphire Preferred
        ↓
Paid from
        ↓
Checking
```

For the initial product, the user's checking account can be treated as the underlying source of funds for credit-card spending.

More detailed credit-card accounting is outside the initial scope.

---

## Goal

A Goal represents an intended allocation of money toward a purpose.

A goal has:

- Name
- Target amount
- Current allocated amount
- Optional associated account
- Optional target period

Examples:

```text
Xbox
Target: $500
Account: None
```

or:

```text
HYSA Savings
Target: $5,000
Account: SoFi HYSA
```

A goal does not necessarily represent money physically moving between accounts.

---

## Goal Contribution

A Goal Contribution represents money being allocated toward a goal.

This is different from a financial transaction.

Example:

```text
Paycheck received:

+$2,000 → Checking

Then:

$500 allocated → Xbox Goal
```

The goal contribution does not decrease the actual Checking balance.

Instead:

```text
Checking Actual Balance:       $2,000
Xbox Allocation:                 $500
Checking Available Balance:    $1,500
```

A goal can have many Goal Contributions.

Goal progress can therefore be calculated from its contributions.

---

## Account-Linked Goals

A goal may optionally reference an Account.

For example:

```text
Goal:
Save $5,000 in SoFi HYSA
```

Money can physically move through a Transfer:

```text
Checking → SoFi HYSA
```

while that movement also contributes toward the associated goal.

This allows the application to distinguish between:

- Moving money
- Allocating money
- Measuring progress toward a goal

---

## Entity Relationships

Conceptually:

```text
Account
  │
  ├──── Transactions
  │       │
  │       ├── Expense
  │       ├── Income
  │       └── Transfer
  │
  └──── Goal Allocations
            │
            ▼
           Goal
            │
            └── Goal Contributions


Expense
  ├── Category
  └── Payment Method


Transfer
  ├── Source Account
  └── Destination Account


Goal
  └── Optional Associated Account
```

### Relationship Summary

- An Account can participate in many Transactions.
- An Expense has a Category.
- An Expense has a Payment Method.
- Income has a destination Account.
- A Transfer has a source Account and destination Account.
- A Goal can have many Goal Contributions.
- A Goal may optionally be associated with an Account.
- A Goal Contribution may allocate money currently held within an Account.

---

## Financial Invariants

The application should preserve several important rules.

### Transfers Preserve Total Money

```text
Total before transfer = Total after transfer
```

### Goal Allocations Do Not Move Money

Allocating $500 toward a goal does not reduce the Actual Balance of the account.

### Available Money Accounts for Allocations

```text
Available Balance =
Actual Balance - Active Goal Allocations
```

### Expenses Reduce Actual Money

Expenses reduce the Actual Balance of their funding account.

### Income Increases Actual Money

Income increases the Actual Balance of its destination account.

### Transactions and Allocations Are Different

Transactions describe actual financial activity.

Goal Contributions describe how existing money is mentally/planning-wise allocated.

Keeping these concepts separate is a core part of the application's financial model.

---

## Assumptions and Non-Goals

For the initial version:

- Users manually enter financial data.
- The application does not synchronize with banks.
- Account balances represent the user's own tracked balances.
- Credit-card balances do not need to be tracked.
- Credit limits do not need to be modeled.
- Overdraft behavior does not need to be modeled.
- Investment holdings and individual securities do not need to be tracked.
- Goals represent allocations rather than separate stores of money.
