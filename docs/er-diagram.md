erDiagram

    ACCOUNTS {
        int id PK
        string name UK
        string type
        decimal current_balance
        datetime created_at
        datetime updated_at
        boolean is_active
    }

    TRANSACTIONS {
        int id PK
        string type
        decimal amount
        date transaction_date
        string name
        string memo
        int account_id FK
        int source_account_id FK
        int destination_account_id FK
        int category_id FK
        int payment_method_id FK
        decimal points_multiplier
        int points_earned
        datetime created_at
        datetime updated_at
    }

    CATEGORIES {
        int id PK
        string name UK
        datetime created_at
        datetime updated_at
        boolean is_active
    }

    PAYMENT_METHODS {
        int id PK
        string name UK
        string type
        int funding_account_id FK
        datetime created_at
        datetime updated_at
        boolean is_active
    }

    GOALS {
        int id PK
        string name
        decimal target_amount
        decimal current_allocated_amount
        int linked_account_id FK
        string frequency
        string status
        date start_date
        date target_date
        datetime created_at
        datetime updated_at
    }

    GOAL_CONTRIBUTIONS {
        int id PK
        int goal_id FK
        decimal amount
        date date
        int account_id FK
        int transaction_id FK
        datetime created_at
    }

    ACCOUNT_BALANCE_HISTORY {
        int id PK
        int account_id FK
        decimal balance
        date date
        string type
        string reason
        datetime created_at
    }

    REWARD_RULES {
        int id PK
        int payment_method_id FK
        int category_id FK
        decimal multiplier
        datetime created_at
        datetime updated_at
        boolean is_active
    }

    ACCOUNTS ||--o{ TRANSACTIONS : "used_by"
    ACCOUNTS ||--o{ TRANSACTIONS : "source_of"
    ACCOUNTS ||--o{ TRANSACTIONS : "destination_of"

    CATEGORIES ||--o{ TRANSACTIONS : "categorizes"
    PAYMENT_METHODS ||--o{ TRANSACTIONS : "used_for"

    ACCOUNTS ||--o{ PAYMENT_METHODS : "funds"

    ACCOUNTS ||--o{ ACCOUNT_BALANCE_HISTORY : "has"

    ACCOUNTS o|--o{ GOALS : "linked_to"
    GOALS ||--o{ GOAL_CONTRIBUTIONS : "has"
    ACCOUNTS ||--o{ GOAL_CONTRIBUTIONS : "funds"
    TRANSACTIONS o|--o{ GOAL_CONTRIBUTIONS : "realizes"

    PAYMENT_METHODS ||--o{ REWARD_RULES : "has"
    CATEGORIES o|--o{ REWARD_RULES : "applies_to"
