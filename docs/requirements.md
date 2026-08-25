# Product Requirements

## 1. Accounts

### Create Account

The user must be able to create an account.

An account should contain:

- Name
- Account type
- Starting balance

Initial account types may include:

- Checking
- Savings / HYSA
- Brokerage
- Retirement
- Other

### View Accounts

The user must be able to view:

- Account name
- Account type
- Current tracked balance

### Edit Account

The user must be able to modify account information.

### Delete Account

The user must be able to delete an account.

The application must prevent or appropriately handle deletion of an account referenced by existing transactions.

---

## 2. Expenses

The user must be able to manually create an expense.

An expense should support:

- Amount
- Date/time
- Merchant/description
- Category
- Payment method
- Location
- Notes

Initial categories may include:

- Rent
- Restaurants
- Groceries
- Shopping
- Entertainment
- Travel
- Miscellaneous

Creating an expense associated with a tracked cash account should decrease that account's balance.

An expense must contribute toward:

- Monthly expense totals
- All-time expense totals
- Category spending totals

The user must be able to edit and delete an expense.

---

## 3. Income

The user must be able to manually record income.

Income should support:

- Amount
- Date/time
- Source
- Destination account
- Description/notes

Examples include:

- Paycheck
- Refund
- Reimbursement
- Other income

Creating income should increase the balance of the selected destination account.

Income must contribute toward monthly and all-time income calculations.

The user must be able to edit and delete income.

---

## 4. Transfers

The user must be able to transfer money between two tracked accounts.

A transfer should contain:

- Amount
- Date/time
- Source account
- Destination account
- Description/notes

When a transfer is recorded:

- The source account balance decreases
- The destination account balance increases
- Total net worth is unchanged
- Monthly expenses are unchanged
- Monthly income is unchanged

The user must be able to edit and delete transfers.

---

## 5. Transactions

The application must provide a transaction history containing expenses, income, and transfers.

Each transaction must have a transaction type:

```text
EXPENSE
INCOME
TRANSFER
```

The user should be able to:

- View transactions
- Add transactions
- Edit transactions
- Delete transactions

The transaction list should display enough information to identify the transaction without opening it.

---

## 6. Dashboard

The dashboard must provide an overview of the user's current financial position.

The primary reporting period for the MVP is the current calendar month.

The dashboard must display:

### Monthly Income

Total income recorded during the current month.

### Monthly Expenses

Total expenses recorded during the current month.

### Money Remaining

For the MVP:

```text
Money Remaining = Monthly Income - Monthly Expenses
```

Transfers must not affect this calculation.

### Spending by Category

Expenses should be grouped by category so the user can understand where money is being spent.

### Account Balances

The dashboard should display the current tracked balance of each account.

---

## 7. Transaction Management

The application should provide prominent actions for:

```text
+ Expense
+ Income
+ Transfer
```

Selecting an action should open an input form/modal.

After creation, transactions must be editable and deletable.

Changes to a transaction must be reflected in:

- Account balances
- Dashboard totals
- Category totals

Deleting a transaction must reverse its financial effects.

---

## 8. Data Persistence

Financial data must persist after the application is closed and restarted.

The MVP will use a local SQLite database.

The application must not require an internet connection for normal operation.

---

## 9. Recurring Expenses — Post-MVP

The user should eventually be able to designate an expense as recurring.

A recurring expense should support:

- Amount
- Category
- Payment method
- Frequency
- Next occurrence
- Active/inactive status

The system should be able to create future transactions according to the recurrence schedule.

The user should be able to stop a recurring expense.

---

## 10. Goals — Post-MVP

The user should eventually be able to define financial allocation goals.

Goals may include:

- Target amount
- Target account/bucket
- Monthly contribution target
- Yearly contribution target

The application should show progress toward these goals.

---

## 11. Credit Card Rewards — Post-MVP

The application should eventually support payment methods with category-specific rewards.

Example:

```text
Card: Chase Sapphire Preferred
Category: Restaurants
Multiplier: 3x
Expense: $150

Estimated points earned: 450
```

Credit cards do not need balance tracking for the initial product.

---

## 12. Technical Requirements

### Frontend

- React
- TypeScript
- Next.js

### Backend

- Python
- FastAPI

### Database

- SQLite

### Architecture

The frontend and backend must remain separate applications.

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

The frontend should interact with financial data through the backend API rather than accessing SQLite directly.

## 13. Testing

Important financial behavior should have automated tests.

Priority areas include:

- Expense balance calculations
- Income balance calculations
- Transfer calculations
- Editing transactions
- Deleting transactions
- Monthly totals
- Category totals
- Ensuring transfers are excluded from income/expense calculations

Financial calculations should not rely solely on frontend logic.
