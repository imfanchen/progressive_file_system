from abc import ABC

class MemoryDatabase(ABC):
    """
    MemoryDatabase interface for an in-memory database supporting multiple levels of operations.
    """

    def set(self, key: str, field: str, value: str) -> None:
        """Inserts or updates a field-value pair in the record associated with key."""
        pass

    def get(self, key: str, field: str) -> str | None:
        """Returns the value of the field in the record associated with key, or None if not found."""
        pass

    def delete(self, key: str, field: str) -> bool:
        """Removes the field from the record associated with key. Returns True if deleted, False otherwise."""
        pass

    def scan(self, key: str) -> list[str]:
        """Returns a list of strings representing the fields of a record, formatted as '<field>(<value>)', sorted lexicographically."""
        pass

    def scan_by_prefix(self, key: str, prefix: str) -> list[str]:
        """Returns a list of strings for fields starting with prefix, formatted as '<field>(<value>)', sorted lexicographically."""
        pass

    def set_at(self, key: str, field: str, value: str, timestamp: int) -> None:
        """Inserts or updates a field-value pair in the record at a specific timestamp."""
        pass

    def set_at_with_ttl(self, key: str, field: str, value: str, timestamp: int, ttl: int) -> None:
        """Inserts or updates a field-value pair in the record at a specific timestamp with TTL."""
        pass

    def delete_at(self, key: str, field: str, timestamp: int) -> bool:
        """Removes the field from the record at a specific timestamp. Returns True if deleted, False otherwise."""
        pass

    def get_at(self, key: str, field: str, timestamp: int) -> str | None:
        """Returns the value of the field in the record at a specific timestamp, or None if not found or expired."""
        pass

    def scan_at(self, key: str, timestamp: int) -> list[str]:
        """Returns a list of strings representing the fields of a record at a specific timestamp, formatted as '<field>(<value>)', sorted lexicographically."""
        pass

    def scan_by_prefix_at(self, key: str, prefix: str, timestamp: int) -> list[str]:
        """Returns a list of strings for fields starting with prefix at a specific timestamp, formatted as '<field>(<value>)', sorted lexicographically."""
        pass

    def backup(self, timestamp: int) -> int:
        """Saves the database state at the specified timestamp. Returns the number of non-empty non-expired records."""
        pass

    def restore(self, timestamp: int, timestamp_to_restore: int) -> None:
        """Restores the database from the latest backup before or at timestamp_to_restore, recalculating TTLs."""
        pass

