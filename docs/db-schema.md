# Database Schema

This document defines the initial relational database schema for Financial Tracker.

The schema is designed for a local-first SQLite application and is based on the conceptual data model defined in `docs/data-model.md`.

---

## 1. accounts

Represents a real financial account or place where money is held or managed.

```text
accounts
--------
id
name
type
current_balance
created_at
updated_at
is_active
```

### Fields

| Field             | Description                                                                      |
| ----------------- | -------------------------------------------------------------------------------- |
| `id`              | Unique account identifier                                                        |
| `name`            | User-facing account name                                                         |
| `type`            | Account type such as CHECKING, SAVINGS, HYSA, BROKERAGE, RETIREMENT, CREDIT_CARD |
| `current_balance` | Current tracked balance                                                          |
| `created_at`      | When the account was created                                                     |
| `updated_at`      | When the account was last edited                                                 |
| `is_active`       | Whether the account is currently active                                          |

Historical balances are stored separately in `account_balance_history`.

Accounts are deactivated rather than hard-deleted.

---

## 2. transactions

Stores all financial transactions in one table.

Transaction types:

```text
EXPENSE
INCOME
TRANSFER
```

```text
transactions
------------
id
type
amount
transaction_date
name
memo
account_id
source_account_id
destination_account_id
category_id
payment_method_id
points_multiplier
points_earned
created_at
updated_at
```

### Fields

| Field                    | Description                                                        |
| ------------------------ | ------------------------------------------------------------------ |
| `id`                     | Unique transaction identifier                                      |
| `type`                   | EXPENSE, INCOME, or TRANSFER                                       |
| `amount`                 | Positive transaction amount                                        |
| `transaction_date`       | Date the real-world transaction occurred                           |
| `name`                   | Merchant for an expense, source for income, optional for transfers |
| `memo`                   | Optional user note                                                 |
| `account_id`             | Account affected by an expense or income                           |
| `source_account_id`      | Account money leaves for a transfer                                |
| `destination_account_id` | Account money enters for a transfer                                |
| `category_id`            | Expense category                                                   |
| `payment_method_id`      | Payment method used for an expense                                 |
| `points_multiplier`      | Reward multiplier applied when the transaction occurred            |
| `points_earned`          | Points earned from the transaction                                 |
| `created_at`             | When the transaction was entered into the application              |
| `updated_at`             | When the transaction was last edited                               |

### Expense Rules

```text
type = EXPENSE

account_id required
name required
category_id required
payment_method_id required

source_account_id NULL
destination_account_id NULL
```

Example:

```text
Target
$50
Shopping
Chase Sapphire Preferred
Checking
```

The associated account balance decreases.

### Income Rules

```text
type = INCOME

account_id required
name required

category_id NULL
payment_method_id NULL
source_account_id NULL
destination_account_id NULL
```

Example:

```text
Employer
$2,000
Checking
```

The destination account balance increases.

### Transfer Rules

```text
type = TRANSFER

source_account_id required
destination_account_id required

account_id NULL
category_id NULL
payment_method_id NULL
```

Example:

```text
Checking → HYSA
$500
```

Transfers do not count as income or expenses.

### Cash Withdrawal

Cash withdrawals are represented as transfers.

Because Cash is intentionally not tracked as an Account:

```text
type = TRANSFER
source_account_id = Checking
destination_account_id = NULL
```

The transfer represents money leaving the tracked Checking account and entering an untracked cash wallet.

A future cash expense can use:

```text
payment_method_id = Cash
account_id = NULL
```

because the cash wallet is not tracked as an account.

### Transaction Dates

`transaction_date` and `created_at` have different meanings.

Example:

```text
Target purchase
transaction_date = 2026-08-14
created_at       = 2026-08-24 20:51
```

Financial reports use `transaction_date`.

Transaction chronology in the UI can use `created_at`.

### Points Tracking

Points are tracked only for transactions where a reward rule applies.

Example:

```text
amount = 150
category = Restaurants
payment_method = Chase Sapphire Preferred
points_multiplier = 3.0
points_earned = 450
```

Historical transactions store the multiplier that was used when the transaction was created.

Changing a reward rule later does not change historical transactions.

Total points collected for a payment method can be calculated from:

```text
SUM(points_earned)
```

The application tracks **points earned through the tracker**, not the card's actual available points balance.

---

## 3. categories

Represents the category used to classify expenses.

```text
categories
----------
id
name
created_at
updated_at
is_active
```

### Initial Examples

```text
Rent
Restaurants
Groceries
Shopping
Entertainment
Travel
Miscellaneous
```

Categories are flat in the initial version.

Users can create additional categories.

Categories are deactivated rather than hard-deleted.

---

## 4. payment_methods

Represents how an expense was paid.

```text
payment_methods
---------------
id
name
type
funding_account_id
created_at
updated_at
is_active
```

### Fields

| Field                | Description                                    |
| -------------------- | ---------------------------------------------- |
| `id`                 | Unique payment method identifier               |
| `name`               | User-facing name                               |
| `type`               | CREDIT_CARD, DEBIT_CARD, CASH, ZELLE, or VENMO |
| `funding_account_id` | Account associated with the payment method     |
| `created_at`         | Creation timestamp                             |
| `updated_at`         | Last edit timestamp                            |
| `is_active`          | Whether the payment method is currently active |

Every payment method has a linked/funding account.

Example:

```text
Chase Sapphire Preferred
type = CREDIT_CARD
funding_account_id = Checking
```

Cash is supported as a payment method but does not have a tracked cash Account.

Reward rules are stored separately in `reward_rules`.

---

## 5. goals

Represents an intended allocation of money toward a purpose.

```text
goals
-----
id
name
target_amount
current_allocated_amount
linked_account_id
frequency
status
start_date
target_date
created_at
updated_at
```

### Fields

| Field                      | Description                               |
| -------------------------- | ----------------------------------------- |
| `id`                       | Unique goal identifier                    |
| `name`                     | Goal name                                 |
| `target_amount`            | Intended target amount                    |
| `current_allocated_amount` | Current amount allocated toward the goal  |
| `linked_account_id`        | Optional account associated with the goal |
| `frequency`                | ONE_TIME, MONTHLY, or YEARLY              |
| `status`                   | ACTIVE, COMPLETED, CANCELLED, or EXPIRED  |
| `start_date`               | Date the goal starts                      |
| `target_date`              | Optional target completion date           |
| `created_at`               | Creation timestamp                        |
| `updated_at`               | Last edit timestamp                       |

### Examples

Virtual goal:

```text
Xbox
target_amount = 500
linked_account_id = NULL
frequency = ONE_TIME
```

Account-linked goal:

```text
HYSA Savings
target_amount = 5000
linked_account_id = SoFi HYSA
frequency = YEARLY
```

`current_allocated_amount` represents the current planning/allocation state.

It does not directly change the linked Account balance.

---

## 6. goal_contributions

Represents an allocation of money toward a goal.

```text
goal_contributions
------------------
id
goal_id
amount
date
account_id
transaction_id
created_at
```

### Fields

| Field            | Description                           |
| ---------------- | ------------------------------------- |
| `id`             | Unique contribution identifier        |
| `goal_id`        | Goal receiving the contribution       |
| `amount`         | Amount allocated                      |
| `date`           | Date of the contribution              |
| `account_id`     | Account the allocated money came from |
| `transaction_id` | Optional linked financial transaction |
| `created_at`     | When the contribution was entered     |

### Virtual Contribution

```text
Xbox Goal
+$500
account_id = Checking
transaction_id = NULL
```

The Checking balance does not change.

### Realized Contribution

```text
HYSA Goal
+$500
account_id = Checking
transaction_id = <transfer transaction ID>
```

The linked transaction represents the actual transfer:

```text
Checking -$500
SoFi HYSA +$500
```

This relationship allows the user to navigate from:

```text
Goal
→ Contribution
→ Transfer
→ Account
```

and from:

```text
Account
→ Transaction
→ Goal Contribution
```

---

## 7. account_balance_history

Stores historical end-of-day account balances and manual balance adjustments.

```text
account_balance_history
-----------------------
id
account_id
balance
date
type
reason
created_at
```

### Fields

| Field        | Description                             |
| ------------ | --------------------------------------- |
| `id`         | Unique history record identifier        |
| `account_id` | Account being recorded                  |
| `balance`    | Account balance at the recorded point   |
| `date`       | Date the balance represents             |
| `type`       | EOD or ADJUSTMENT                       |
| `reason`     | Optional reason for a manual adjustment |
| `created_at` | When the record was created             |

### EOD Snapshot

The application records the account's end-of-day balance.

Example:

```text
Checking
August 24
EOD
$5,240
```

These records allow historical visualization such as:

* Weekly balance trends
* Monthly balance trends
* Changes in account balances
* Comparing different days

### Manual Adjustment

Example:

```text
Checking
August 24
ADJUSTMENT
$4,920
reason = "Bank statement reconciliation"
```

Manual adjustments should remain visible in the historical record.

The current balance in `accounts.current_balance` represents the live tracked balance.

---

## 8. reward_rules

Defines how a payment method earns points based on expense categories.

```text
reward_rules
------------
id
payment_method_id
category_id
multiplier
created_at
updated_at
is_active
```

### Fields

| Field               | Description                           |
| ------------------- | ------------------------------------- |
| `id`                | Unique reward rule identifier         |
| `payment_method_id` | Payment method receiving the reward   |
| `category_id`       | Optional category the rule applies to |
| `multiplier`        | Reward multiplier such as 3.0         |
| `created_at`        | Creation timestamp                    |
| `updated_at`        | Last edit timestamp                   |
| `is_active`         | Whether the rule is currently active  |

### Category-Specific Rule

```text
Chase Sapphire Preferred
Restaurants
3.0x
```

### Default Rule

A `NULL` `category_id` represents the default multiplier for categories without a more specific rule.

Example:

```text
Chase Sapphire Preferred
category_id = NULL
multiplier = 1.0
```

### Rule Uniqueness

A payment method should not have multiple active rules for the same category.

Conceptually:

```text
payment_method_id + category_id
```

should be unique among active reward rules.

### Historical Rewards

Changing a reward rule only affects future transactions.

Historical transactions keep the `points_multiplier` and `points_earned` that were recorded when the transaction occurred.

---

# Relationships

```text
accounts
   │
   ├──< transactions
   ├──< account_balance_history
   ├──< goal_contributions
   └──< payment_methods
              │
              └──< reward_rules


categories
   │
   ├──< transactions
   └──< reward_rules


goals
   │
   └──< goal_contributions
              │
              └── transaction (optional)


transactions
   ├── account
   ├── source_account
   ├── destination_account
   ├── category
   └── payment_method
```

`<` indicates a one-to-many relationship.

---

# Core Relationships

### Account → Transactions

One account can participate in many transactions.

An expense/income uses `account_id`.

A transfer uses:

```text
source_account_id
destination_account_id
```

### Category → Transactions

One category can be used by many expense transactions.

### Payment Method → Transactions

One payment method can be used by many expense transactions.

### Payment Method → Reward Rules

One payment method can have multiple reward rules.

### Account → Payment Methods

One account can fund multiple payment methods.

Example:

```text
Checking
├── Chase Sapphire Preferred
├── Capital One Savor
└── Debit Card
```

### Goal → Goal Contributions

One goal can have many contributions.

### Goal → Account

A goal can have zero or one linked account.

### Goal Contribution → Transaction

A contribution can optionally reference a transaction.

This is used when a virtual allocation becomes a real financial transfer.

---

# Initial Table List

```text
accounts
transactions
categories
payment_methods
goals
goal_contributions
account_balance_history
reward_rules
```

This is the initial database model. Additional tables can be introduced as requirements evolve.
