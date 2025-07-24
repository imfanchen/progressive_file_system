# Instructions

Your task is to implement a simplified version of an in-memory database. All operations that should be supported by this database are described below.

Solving this task consists of several levels. Subsequent levels are opened when the current level is correctly solved. You always have access to the data for the current and all previous levels.

You can execute a single test case by running the following command in the terminal:

```bash
bash run_single_test.sh "<test_case_name>"
```

# Requirements

Your task is to implement a simplified version of an in-memory database. Plan your design according to the level specifications below:

- **Level 1:** In-memory database should support basic operations to manipulate records, fields, and values within fields.
- **Level 2:** In-memory database should support displaying a specific record's fields based on a filter.
- **Level 3:** In-memory database should support TTL (Time-To-Live) configurations on database records.
- **Level 4:** In-memory database should support backup and restore functionality.

> To move to the next level, you need to pass all the tests at this level.

**Note:** 

You will receive a list of queries to the system, and the final output should be an array of strings representing the returned values of all queries. Each query will only call one operation.

---

# Level 1

The in-memory database should support basic operations to manipulate records, fields, and values within fields.

- `set(self, key: str, field: str, value: str) -> None`  
  Inserts a field-value pair to the record associated with `key`. If the field in the record already exists, replace the existing value with the specified value. If the record does not exist, create a new one.

- `get(self, key: str, field: str) -> str | None`  
  Returns the value contained within the field of the record associated with `key`. If the record or the field doesn't exist, return `None`.

- `delete(self, key: str, field: str) -> bool`  
  Removes the field from the record associated with `key`. Returns `True` if the field was successfully deleted, and `False` if the key or the field does not exist in the database.

## Examples

| Queries            | Explanations                                             |
| ------------------ | -------------------------------------------------------- |
| set("A", "B", "E") | Database state: `{ "A": { "B": "E" } }`                  |
| set("A", "C", "F") | Database state: `{ "A": { "C": "F", "B": "E" } }`        |
| get("A", "B")      | Returns `"E"`                                            |
| get("A", "D")      | Returns `None`                                           |
| delete("A", "B")   | Returns `True`; Database state: `{ "A": { "C": "F" } }`  |
| delete("A", "D")   | Returns `False`; Database state: `{ "A": { "C": "F" } }` |

---

# Level 2

The database should support displaying data based on filters. Introduce an operation to support printing some fields of a record.

- `scan(self, key: str) -> list[str]`  
  Returns a list of strings representing the fields of a record associated with `key`. The returned list should be in the format `["<field_1>(<value_1>)", "<field_2>(<value_2>)", ...]`, where fields are sorted lexicographically. If the specified record does not exist, returns an empty list.

- `scan_by_prefix(self, key: str, prefix: str) -> list[str]`  
  Returns a list of strings representing some fields of a record associated with `key`. Only fields that start with `prefix` should be included. The returned list should follow the same format as `scan` with fields sorted lexicographically.

## Examples

| Queries                  | Explanations                                                  |
| ------------------------ | ------------------------------------------------------------- |
| set("A", "BC", "E")      | Database state: `{ "A": { "BC": "E" } }`                      |
| set("A", "BD", "F")      | Database state: `{ "A": { "BC": "E", "BD": "F" } }`           |
| set("A", "C", "G")       | Database state: `{ "A": { "BC": "E", "BD": "F", "C": "G" } }` |
| scan_by_prefix("A", "B") | Returns `["BC(E)", "BD(F)"]`                                  |
| scan("A")                | Returns `["BC(E)", "BD(F)", "C(G)"]`                          |
| scan_by_prefix("B", "B") | Returns `[]`                                                  |

---

# Level 3

Support the timeline of operations and TTL (Time-To-Live) settings for records and fields. Each operation from previous levels now has an alternative version with a timestamp parameter to represent when the operation was executed.

- `set_at(self, key: str, field: str, value: str, timestamp: int) -> None`  
  Inserts a field-value pair or updates the value of the field in the record associated with `key`.

- `set_at_with_ttl(self, key: str, field: str, value: str, timestamp: int, ttl: int) -> None`  
  Inserts a field-value pair or updates the value of the field in the record associated with `key`. Also sets its TTL starting at `timestamp`.

- `delete_at(self, key: str, field: str, timestamp: int) -> bool`  
  Same as `delete`, but with timestamp.

- `get_at(self, key: str, field: str, timestamp: int) -> str | None`  
  Same as `get`, but with timestamp.

- `scan_at(self, key: str, timestamp: int) -> list[str]`  
  Same as `scan`, but with timestamp.

- `scan_by_prefix_at(self, key: str, prefix: str, timestamp: int) -> list[str]`  
  Same as `scan_by_prefix`, but with timestamp.

## Examples

### Example 1

| Queries                                | Explanations                                                                                                                                       |
| -------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------- |
| set_at_with_ttl("A", "BC", "E", 1, 9)  | Database state: `{"A": {"BC": "E"}}` where {"BC": "E"} expires at timestamp 10.                                                                    |
| set_at_with_ttl("A", "BC", "E", 5, 10) | Database state: `{"A": {"BC": "E"}}` as field "BC" in record "A" already  exists, it was overwritten, and {"BC": "E"} now expires at timestamp 15. |
| set_at("A", "BD", "F", "5")            | Database state: `{"A": {"BC": E", "BD": "F"}}` where {"BD": "F"} does not expire.                                                                  |
| scan_by_prefix_at("A", "B", 14)        | Returns `["BC(E)", "BD(F)"]`                                                                                                                       |
| scan_by_prefix_at("A", "B", 15)        | Returns `["BD(F)"]`                                                                                                                                |


### Example 2

| Queries                               | Explanations                                                                                                                                    |
| ------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------- |
| set_at("A", "B", "C", "1")            | Database state: `{"A": {"B": "C"}}`                                                                                                             |
| set_at_with_ttl("X", "Y", "Z", 2, 15) | Database state: `{"X": {"Y": "Z"}, "A": {"B": "C"}}` where {"Y": "Z"} expires at timestamp 17                                                   |
| get_at("X", "Y", "3")                 | Returns `"Z"`                                                                                                                                   |
| set_at_with_ttl("A", "D", "E", 4, 10) | Database state: `{"X": {"Y": "Z"}, "A": {"D": "E", "B": "C"}}` where {"D": "E"} expires at timestamp 14 and {"Y": "Z"} expires at timestamp 17. |
| scan_at("A", "13")                    | Returns `["B(C), D(E)"]`                                                                                                                        |
| scan_at("X", "16")                    | Returns `["Y(Z)"]`                                                                                                                              |
| scan_at("X", "17")                    | Returns `[]`; Note that all fields in record "X" have expired.                                                                                  |
| delete_at("X", "Y", "20")             | Returns `False`; the record "X" was expired at timestamp 17 and can't be deleted.                                                               |

---

# Level 4

Introduce operations to support backing up and restoring the database state based on timestamps. When restoring, TTL expiration times should be recalculated accordingly.

- `backup(self, timestamp: int) -> int`  
  Saves the database state at the specified timestamp, including the remaining TTL for all records and fields. Returns the number of non-empty non-expired records.

- `restore(self, timestamp: int, timestamp_to_restore: int) -> None`  
  Restores the database from the latest backup before or at `timestamp_to_restore`. Expiration times should be recalculated accordingly.

These operations ensure database persistence and allow restoration to previous states, maintaining TTL integrity over time.

## Examples

| Queries                               | Explanations                                                                                                                            |
| ------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------- |
| set_at_with_ttl("A", "B", "C", 1, 10) | Database state: `{"A": {"B": "C"}}` with lifespan `[1, 11)`, meaning that the record should be deleted at timestamp = 11.               |
| backup(3)                             | Returns `1`; saves the database state.                                                                                                  |
| set_at("A", "D", "E", 4)              | Database state: `{"A": {"D": "E", "B": "C"}}`                                                                                           |
| backup(5)                             | Returns `1`; saves the database state.                                                                                                  |
| delete_at("A", "B", 8)                | Return `True`, database state: `{"A": {"D": "E"}}`                                                                                      |
| backup(9)                             | Returns `1`; saves the database state.                                                                                                  |
| restore(10, 7)                        | Restores the database to state of last backup at timestamp = 5: {"A": {"D": "E", "B": "C"}} with {"B": "C"} expiring at timestamp = 16. |
| backup(11)                            | Returns `1`; saves the database state.                                                                                                  |
| scan_at("A", 15)                      | Returns `["B(C)", "D(E)"]`                                                                                                              |
| scan_at("A", 16)                      | Returns `["D(E)"]`                                                                                                                      |