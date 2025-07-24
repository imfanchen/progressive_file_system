from memory_database import MemoryDatabase


class MemoryDatabaseBasicImpl(MemoryDatabase):
    def __init__(self):
        # Simple structure: {key: {field: value}}
        self.db = {}

    def set(self, key: str, field: str, value: str) -> None:
        if key not in self.db:
            self.db[key] = {}
        self.db[key][field] = value

    def get(self, key: str, field: str) -> str | None:
        if key in self.db and field in self.db[key]:
            return self.db[key][field]
        return None

    def delete(self, key: str, field: str) -> bool:
        if key in self.db and field in self.db[key]:
            del self.db[key][field]
            if not self.db[key]:
                del self.db[key]
            return True
        return False

    def scan(self, key: str) -> list[str]:
        if key in self.db:
            result = [f"{field}({value})" for field, value in self.db[key].items()]
            return sorted(result)
        return []

    def scan_by_prefix(self, key: str, prefix: str) -> list[str]:
        if key in self.db:
            result = [f"{field}({value})" for field, value in self.db[key].items() if field.startswith(prefix)]
            return sorted(result)
        return []


class MemoryDatabaseAdvancedImpl(MemoryDatabase):
    def __init__(self):
        # {key: {field: [(timestamp, value, expire_at)]}}
        self.db = {}
        # List of backups: (timestamp, db_snapshot)
        self.backups = []

    def set_at(self, key: str, field: str, value: str, timestamp: int) -> None:
        if key not in self.db:
            self.db[key] = {}
        if field not in self.db[key]:
            self.db[key][field] = []
        self.db[key][field].append((timestamp, value, None))

    def set_at_with_ttl(self, key: str, field: str, value: str, timestamp: int, ttl: int) -> None:
        expired_at = timestamp + ttl
        if key not in self.db:
            self.db[key] = {}
        if field not in self.db[key]:
            self.db[key][field] = []
        self.db[key][field].append((timestamp, value, expired_at))

    def delete_at(self, key: str, field: str, timestamp: int) -> bool:
        if key in self.db and field in self.db[key]:
            deleted = False
            later_versions = []
            # Remove all versions up to timestamp that are not expired
            for t, v, e in self.db[key][field]:
                if t <= timestamp and (e is None or e > timestamp):
                    deleted = True
                else:
                    later_versions.append((t, v, e))
            if deleted:
                if later_versions:
                    self.db[key][field] = later_versions
                else:
                    del self.db[key][field]
                    if not self.db[key]:
                        del self.db[key]
                return True
        return False

    def get_at(self, key: str, field: str, timestamp: int) -> str | None:
        if key in self.db and field in self.db[key]:
            # Find the latest version at or before timestamp that is not expired
            for t, v, e in reversed(self.db[key][field]):
                if t <= timestamp and (e is None or e > timestamp):
                    return v
        return None

    def scan_at(self, key: str, timestamp: int) -> list[str]:
        if key not in self.db:
            return []
        result = []
        for field in self.db[key]:
            # Find the latest version at or before timestamp that is not expired
            for t, v, e in reversed(self.db[key][field]):
                if t <= timestamp and (e is None or e > timestamp):
                    result.append(f"{field}({v})")
                    break
        return sorted(result)

    def scan_by_prefix_at(self, key: str, prefix: str, timestamp: int) -> list[str]:
        if key not in self.db:
            return []
        result = []
        for field in self.db[key]:
            if field.startswith(prefix):
                # Find the latest version at or before timestamp that is not expired
                for t, v, e in reversed(self.db[key][field]):
                    if t <= timestamp and (e is None or e > timestamp):
                        result.append(f"{field}({v})")
                        break
        return sorted(result)

    def backup(self, timestamp: int) -> int:
        count = 0
        snapshot = {}
        # Only backup non-empty, non-expired records at timestamp
        for key in self.db:
            fields = {}
            for field in self.db[key]:
                # Find the latest version at or before timestamp that is not expired
                for t, v, e in reversed(self.db[key][field]):
                    if t <= timestamp and (e is None or e > timestamp):
                        fields[field] = (t, v, e)
                        break
            if fields:
                snapshot[key] = fields
                count += 1
        self.backups.append((timestamp, snapshot))
        return count

    def restore(self, timestamp: int, timestamp_to_restore: int) -> None:
        # Find the latest backup at or before timestamp_to_restore
        backup_to_restore = None
        for t, snapshot in reversed(self.backups):
            if t <= timestamp_to_restore:
                backup_to_restore = (t, snapshot)
                break
        if backup_to_restore is None:
            self.db = {}
            return
        backup_at, snapshot = backup_to_restore
        new_db = {}
        for key in snapshot:
            new_db[key] = {}
            for field in snapshot[key]:
                t, v, e = snapshot[key][field]
                if e is not None:
                    remaining_ttl = e - backup_at
                    new_expired_at = timestamp + remaining_ttl
                else:
                    new_expired_at = None
                new_db[key][field] = [(t, v, new_expired_at)]
        self.db = new_db



