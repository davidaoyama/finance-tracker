Financial Integrity Constraints

Amounts

- Transaction amounts must be >= 0.
- Goal contribution amounts must be >= 0.
- Reward multipliers must be > 0.

Transactions

- Expense account must reference an active account.
- Income destination account must reference an active account.
- Transfer source and destination accounts must both be active.
- Transfer source and destination accounts cannot be the same.
- Expense category defaults to Miscellaneous when none is provided.
- Expense payment method must reference an active payment method.
- Transfer transactions cannot have category or payment method.
- Income transactions cannot have category or payment method.

Accounts

- Account names must be unique.
- Accounts may have negative balances.
- Inactive accounts cannot be used by new transactions.

Categories

- Category names must be unique.
- Inactive categories cannot be assigned to new transactions.

Payment Methods

- Payment method names must be unique.
- Inactive payment methods cannot be assigned to new transactions.
- Payment methods must have an active funding account.

Goals

- current_allocated_amount may exceed target_amount.
- A goal may have zero or one linked account.
- Goal contributions cannot have negative amounts.
- Goal contribution account references must be active when creating a contribution.

Historical Records

- Existing transactions remain valid if an account/category/payment method is later deactivated.
- Financial records should not be hard-deleted when doing so would destroy historical relationships.
- A transaction referenced by a goal contribution should be marked inactive/deleted rather than physically removed.
