# Instructions

Your task is to implement a simplified version of a banking system. All operations that should be supported are listed below.

Solving this task consists of several levels. Subsequent levels are opened when the current level is correctly solved. You always have access to the data for the current and all previous levels.

You can execute a single test case by running the following command in the terminal:

```bash
bash run_single_test.sh "<test_case_name>"
```

# Requirements

Your task is to implement a simplified version of a banking system. Plan your design according to the level specifications below:

* **Level 1**: The banking system should support creating new accounts, depositing money into accounts, and transferring money between two accounts.
* **Level 2**: The banking system should support ranking accounts based on the total value of outgoing transactions.
* **Level 3**: The banking system should allow scheduling payments and checking the status of scheduled payments.
* **Level 4**: The banking system should support merging two accounts while retaining both accounts' balance and transaction histories.

To move to the next level, you should pass all the tests at the current level.

**Note:**

You will receive a list of queries to the system, and the final output should be an array of strings representing the returned values of all queries. each query will only call one operation.

All operations will have a `timestamp` parameter — a stringified timestamp in milliseconds. It is guaranteed that all timestamps are unique and are in a range from 1 to $10^9$. Operations will be given in order of strictly increasing timestamps.

---

# Level 1

The banking system should support creating new accounts and depositing money into and withdrawing/paying money from accounts.

* `create_account(self, timestamp: int, account_id: str) -> bool` — should create a new account with the given `account_id` if it doesn't already exist. Returns `True` if the account was successfully created or `False` if an account with `account_id` already exists.

* `deposit(self, timestamp: int, account_id: str, amount: int) -> int | None` — should deposit the given `amount` of money to the specified account `account_id`. Returns the total amount of money in the account (balance) after processing the query. If the specified account does not exist, should return `None`.

* `pay(self, timestamp: int, account_id: str, amount: int) -> int | None` — should withdraw the given `amount` of money from the specified account. Returns the amount of money in the account (balance) after processing the query. If the specified account does not exist, or if the account has insufficient funds to perform the withdrawal, should return `None`.

## Examples

The example below shows how these operations should work:

| Function Call                     | Explanation                                                     |
| --------------------------------- | --------------------------------------------------------------- |
| `create_account(1, "account1")`   | returns `True`                                                  |
| `create_account(2, "account1")`   | returns `False`; an account with this identifier already exists |
| `create_account(3, "account2")`   | returns `True`                                                  |
| `deposit(4, "non-existing", 200)` | returns `None`; an account with this identifier does not exist  |
| `deposit(5, "account1", 2700)`    | returns `2700`                                                  |
| `pay(6, "non-existing", 200)`     | returns `None`; an account with this identifier does not exist  |
| `pay(7, "account1", 2701)`        | returns `None`; this account has insufficient funds             |
| `pay(8, "account1", 200)`         | returns `2500`                                                  |

the output should be `[True, False, True, None, 2700, None, None, 2500]`.

---

# Level 2

The banking system should support ranking accounts based on the total value of transactions.

* `top_activity(self, timestamp: int, n: int) -> str` — should return the top `n` accounts with the highest total value of transactions sorted in descending order (in case of ties, sorted alphabetically by `account_id` in ascending order). The returned value should be a string representing an array of accounts and transaction values in this format: `<account_id>(<transactionValue>), <account_id2>(<transactionValue2>), ... <account_idn>(<transactionValuen>)`.
    * Total value of transactions is defined as the sum of all transactions for an account (regardless of how the transaction affects account balance), including the amount of money deposited, withdrawn, and/or successfully transferred (transfers will be introduced on level 3, so you can ignore them for now).
    * If less than `n` accounts exist in the system, return all active accounts (in the described format).

## Examples

The example below shows how these operations should work:

| Function Call                   | Explanation                                                |
| ------------------------------- | ---------------------------------------------------------- |
| `create_account(1, "account1")` | returns `True`                                             |
| `create_account(2, "account2")` | returns `True`                                             |
| `create_account(3, "account3")` | returns `True`                                             |
| `deposit(4, "account1", 2000)`  | returns `2000`                                             |
| `deposit(5, "account2", 3000)`  | returns `3000`                                             |
| `deposit(6, "account3", 4000)`  | returns `4000`                                             |
| `top_activity(7, 3)`            | returns `"account3(4000), account2(3000), account1(2000)"` |
| `pay(8, "account1", 1500)`      | returns `500`                                              |
| `pay(9, "account2", 250)`       | returns `2750`                                             |
| `deposit(10, "account3", 250)`  | returns `4250`                                             |
| `top_activity(11, 3)`           | returns `"account3(4250), account1(3500), account2(3250)"` |

---

# Level 3

The banking system should allow scheduling payments and checking the status of scheduled payments.

* `transfer(self, timestamp: int, source_account_id: str, target_account_id: str, amount: int) -> str` — should initiate a transfer between accounts. The given `amount` of money should be withdrawn from the source account `source_account_id` and held until the transfer is accepted by the target account `target_account_id`, or until the transfer expires. The withheld money is added back to the source account's balance if the transfer expires. After the query is processed:
    * Returns an empty string if `source_account_id` is equal to `target_account_id`.
    * Returns an empty string if `source_account_id` or `target_account_id` doesn't exist.
    * Returns an empty string if the source account `source_account_id` has insufficient funds to perform the transfer.
    * The expiration period is 24 hours, which is equal to `24 * 60 * 60 * 1000 = 86400000` milliseconds. A transfer expires at the beginning of the next millisecond after the expiration period ends.
    * A valid `TRANSFER` should return a string containing a unique transfer ID in the following format: `"transfer{ordinal number of the transfer}"`, e.g., `"transfer1"`, `"transfer2"`, etc.
    * For transfers, transaction history for source and target accounts is only updated when the transfer is accepted.
    * Transfers count toward the total value of transactions of both source and target accounts.

* `accept_transfer(self, timestamp: int, account_id: str, transfer_id: str) -> bool` — should accept the transfer with the given `transfer_id`.
    * Returns `True` if the transfer was successfully accepted or `False` otherwise.
    * Returns `False` if a transfer with `transfer_id` does not exist, was already accepted, or has expired.
    * Returns `False` if the given `account_id` was not the target account for the transfer.

## Examples

The examples below show how these operations should work (the section is scrollable to the right):

| Function Call                                        | Explanation                                                             |
| ---------------------------------------------------- | ----------------------------------------------------------------------- |
| `create_account(1, "account1")`                      | returns `True`                                                          |
| `create_account(2, "account2")`                      | returns `True`                                                          |
| `deposit(3, "account1", 2000)`                       | returns `2000`                                                          |
| `deposit(4, "account2", 3000)`                       | returns `3000`                                                          |
| `transfer(5, "account1", "account2", 5000)`          | returns `""`; "account1" has insufficient funds                         |
| `transfer(16, "account1", "account2", 1000)`         | returns `"transfer1"`                                                   |
| `accept_transfer(20, "account1", "transfer1")`       | returns `False`; "account1" is not the target account for this transfer |
| `accept_transfer(21, "non-existing", "transfer1")`   | returns `False`; this account does not exist                            |
| `accept_transfer(22, "account1", "transfer2")`       | returns `False`; this transfer does not exist                           |
| `accept_transfer(25, "account2", "transfer1")`       | returns `True`                                                          |
| `accept_transfer(30, "account2", "transfer1")`       | returns `False`; the transfer was already accepted                      |
| `transfer(40, "account1", "account2", 1000)`         | returns `"transfer2"`                                                   |
| `accept_transfer(86445000, "account2", "transfer2")` | returns `False`; the transfer has expired                               |
| `transfer(86550000, "account1", "account1", 1000)`   | returns `""`; the source account is equal to the target account         |

the output should be: `[True, True, 2000, 3000, "", "transfer1", False, False, False, True, False, "transfer2", False, ""]`.

---

# Level 4

The banking system should support merging two accounts while retaining both accounts' balance and transaction histories.

* `merge_accounts(self, timestamp: int, account_id_1: str, account_id_2: str) -> bool` — should merge two accounts while retaining both accounts' balance, transactions, and transfers. Returns `True` if the merge was successful or `False` otherwise.

* `get_balance(self, timestamp: int, account_id: str, timestamp_at: int) -> int | None` - should get the balance of the account at the given timestamp. Returns the balance of the account at the given timestamp. If the account does not exist, or is deactivate at the given timestamp, returns None.