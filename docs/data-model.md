Yes. I’d **update `data-model.md` rather than create another document**, because these are refinements to the same conceptual model.

I’d add a section covering the final decisions around dates, transaction/account behavior, goals, and balance tracking. Here’s the updated document you can use to replace your current `docs/data-model.md`:

# Data Model

This document describes the conceptual data model for Financial Tracker.

The purpose of this model is to define the major financial entities, relationships, and financial rules before designing the database schema.

---

## Account

An Account represents a real location where the user's money is held or managed.

Examples:

- Checking
- Savings / HYSA
- Brokerage
- Roth IRA
- Credit Card

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

#### Goal Allocations

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

A transaction amount is stored as a positive value. The transaction type determines how the amount affects the financial model.

### Common Transaction Fields

Every transaction has:

- `id`
- `type`
- `amount`
- `transaction_date`
- `created_at`
- `name`
- `memo`
- `source_or_merchant`

### Transaction Date vs. Created At

The application distinguishes between when the financial event occurred and when it was entered into the tracker.

#### `transaction_date`

The date the financial activity actually occurred.

Example:

```text
Target purchase
$50
Transaction date: August 14
```

This date is used for financial reporting and monthly totals.

#### `created_at`

The date and time the user entered the transaction into the tracker.

Example:

```text
Created at: August 24, 8:51 PM
```

This is used to preserve input chronology and display recently entered transactions in the order they were added.

Exact time of the real-world financial transaction is not required.

---

## Expense

An Expense represents money spent by the user.

Example:

```text
Merchant: Target
Amount: $150
Category: Shopping
Payment Method: Chase Sapphire Preferred
Account: Checking
Transaction Date: August 14
```

An expense may contain:

- Amount
- Transaction date
- Merchant
- Memo
- Payment method
- Funding account
- Category

An expense decreases the actual balance of its associated account.

Expenses contribute toward:

- Monthly expense totals
- All-time expense totals
- Category spending
- Payment-method spending

The user is assumed to spend only money available to them. Overdraft behavior and credit-limit management are outside the initial scope.

---

## Income

Income represents money received by the user from an external source.

Example:

```text
Source: Employer
Amount: $2,000
Destination Account: Checking
Transaction Date: August 23
```

Income may contain:

- Amount
- Transaction date
- Source
- Memo
- Destination account

Income increases the actual balance of the destination account.

A payment method is not required for income.

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

A transfer contains:

- Amount
- Transaction date
- Source account
- Destination account
- Name
- Memo

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

## Account and Payment Method

For expenses, the application distinguishes between the payment method and the account that ultimately funds the expense.

Example:

```text
Expense: $150 McDonald's
Payment Method: Chase Sapphire Preferred
Account: Checking
```

The payment method describes how the purchase was made.

The account describes the user's tracked source of funds.

This allows the application to separately track:

- Total spending from a payment method
- Spending by category on a payment method
- The account whose tracked balance should decrease

For the initial product, credit card balances do not need to be modeled.

Example:

```text
Chase Sapphire Preferred
Payment method for transaction
        ↓
Checking
Tracked funding account
```

The application assumes the user ultimately pays the credit card from Checking and wants the expense reflected against available Checking funds immediately.

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

Payment methods are primarily used for spending analysis and future credit-card reward calculations.

A payment method may have reward rules added later.

Example:

```text
Payment Method:
Chase Sapphire Preferred

Restaurant multiplier:
3x
```

---

## Goal

A Goal represents an intended allocation of money toward a purpose.

A goal has:

- Name
- Target amount
- Current allocated amount
- Optional linked account
- Optional target period

Examples:

```text
Xbox
Target: $500
Linked Account: None
```

or:

```text
HYSA Savings
Target: $5,000
Linked Account: SoFi HYSA
```

A goal is a planning abstraction. It does not necessarily represent money physically moving between accounts.

A goal can have multiple contributions.

A goal may have **zero or one linked account**.

---

## Goal Contribution

A Goal Contribution represents money being allocated toward a goal.

A goal contribution is distinct from a financial transaction.

Example:

```text
Income:
+$2,000 → Checking

Goal allocation:
$500 → Xbox Goal
```

The contribution does not reduce the actual Checking balance.

After the allocation:

```text
Checking Actual Balance:       $2,000
Xbox Goal Allocation:            $500
Checking Available Balance:    $1,500
```

A goal can have many contributions.

---

## Virtual vs. Real Goal Contributions

A goal contribution may remain a virtual allocation or become a real transfer.

### Virtual Goal Contribution

Example:

```text
Goal: Xbox
Contribution: $500
Linked Account: None
```

The application records that $500 has been allocated toward the goal.

No account balance changes.

This allows the user to decide later whether they actually want to spend the money.

### Real Goal Contribution

A goal can optionally be linked to an account.

Example:

```text
Goal:
Save $5,000 in SoFi HYSA

Linked Account:
SoFi HYSA
```

If the user chooses to make a $500 contribution real, the application creates a transfer:

```text
Checking -$500
SoFi HYSA +$500
```

The contribution therefore represents both:

- Progress toward the goal
- A real movement of money

The user explicitly chooses whether to make a contribution a real transfer.

---

## Goal Completion Does Not Necessarily Mean Spending

A goal can be completed without the money being spent.

Example:

```text
Goal: Xbox
Target: $500
Allocated: $500
```

The goal is complete even if the user ultimately decides not to purchase an Xbox.

If the user later purchases the Xbox, that purchase is recorded as a separate Expense.

This preserves the distinction between:

- Planning to spend money
- Actually spending money

---

## Account Balance History

Accounts maintain a current tracked balance.

The application also maintains balance history so the dashboard can visualize changes over time without recalculating historical balances every time.

Conceptually:

```text
Checking

Current Balance:
$5,240

Balance History:
Aug 1     $4,800
Aug 8     $5,100
Aug 15    $4,900
Aug 24    $5,240
```

An account may also have a starting balance when initially created.

The user may manually adjust a tracked balance when the application's balance differs from the user's actual financial records.

Balance correction behavior will be defined during database and API design.

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
  ├──── Balance History
  │
  └──── Goal Allocations


Expense
  ├── Category
  └── Payment Method


Transfer
  ├── Source Account
  └── Destination Account


Goal
  ├── Goal Contributions
  │
  └── Optional Linked Account


Goal Contribution
  └── Optional resulting Transfer
```

### Relationship Summary

- An Account can participate in many Transactions.
- An Account can have many balance-history records.
- An Expense has a Category.
- An Expense has a Payment Method.
- An Expense has a Funding Account.
- Income has a Destination Account.
- A Transfer has a Source Account and Destination Account.
- A Transfer has a Destination Account.
- A Goal can have many Goal Contributions.
- A Goal has zero or one linked Account.
- A Goal Contribution belongs to one Goal.
- A Goal Contribution may optionally result in a real Transfer.

---

## Financial Invariants

The application should preserve several important rules.

### Transfers Preserve Total Money

```text
Total before transfer = Total after transfer
```

### Goal Allocations Do Not Move Money

A virtual goal allocation does not reduce an account's Actual Balance.

### Available Balance Accounts for Allocations

```text
Available Balance =
Actual Balance - Active Goal Allocations
```

### Expenses Reduce Actual Money

An expense reduces the Actual Balance of its funding account.

### Income Increases Actual Money

Income increases the Actual Balance of its destination account.

### Transactions and Allocations Are Different

Transactions describe actual financial activity.

Goal Contributions describe planning/allocation activity.

Keeping these concepts separate is a core part of the application's financial model.

---

## Assumptions and Non-Goals

For the initial version:

- Users manually enter financial data.
- The application does not synchronize with banks.
- Account balances represent the user's tracked view of their finances.
- Users are assumed not to spend beyond available real-world funds.
- Credit-card balances do not need to be tracked.
- Credit limits do not need to be modeled.
- Overdraft behavior does not need to be modeled.
- Investment holdings and individual securities do not need to be tracked.
- Goals represent allocations rather than separate stores of money.
- Exact real-world transaction times do not need to be stored.
- Transaction input time must be stored.
