from storage_system import StorageSystem
from dataclasses import dataclass, field

class StorageSystemBasicImpl(StorageSystem):
    def __init__(self):
        self.files: dict[str, int] = {}

    def add_file(self, name: str, size: int) -> bool:
        if name in self.files:
            return False
        self.files[name] = size
        return True

    def get_file_size(self, name: str) -> int | None:
        return self.files.get(name)

    def delete_file(self, name: str) -> int | None:
        if name in self.files:
            size = self.files[name]
            del self.files[name]
            return size
        return None

    def get_n_largest(self, prefix: str, n: int) -> list[str]:
        matching_files = [
            (name, size) for name, size in self.files.items() if name.startswith(prefix)
        ]
        matching_files.sort(key=lambda x: (-x[1], x[0]))
        return [name for name, _ in matching_files[:n]]

@dataclass
class File:
    name: str
    size: int
    owner_id: str = "admin"

@dataclass
class User:
    user_id: str
    capacity: int
    used_capacity: int = 0
    file_names: list[str] = field(default_factory=list)

    @property
    def remaining_capacity(self) -> int:
        return self.capacity - self.used_capacity

class StorageSystemAdvancedImpl(StorageSystem):
    def __init__(self):
        self.files: dict[str, File] = {}
        self.users: dict[str, User] = {}
        self.backups: dict[str, dict[str, int]] = {}

    def add_file(self, name: str, size: int) -> bool:
        if name in self.files:
            return False
        self.files[name] = File(name=name, size=size)
        return True

    def get_file_size(self, name: str) -> int | None:
        file = self.files.get(name)
        return file.size if file else None

    def delete_file(self, name: str) -> int | None:
        if name not in self.files:
            return None
        file = self.files[name]
        size = file.size
        if file.owner_id and file.owner_id in self.users:
            user = self.users[file.owner_id]
            user.file_names.remove(name)
            user.used_capacity -= size
        del self.files[name]
        return size

    def get_n_largest(self, prefix: str, n: int) -> list[str]:
        matching_files = [
            file for file in self.files.values() if file.name.startswith(prefix)
        ]
        matching_files.sort(key=lambda x: (-x.size, x.name))
        return [file.name for file in matching_files[:n]]

    def add_user(self, user_id: str, capacity: int) -> bool:
        if user_id in self.users:
            return False
        self.users[user_id] = User(user_id=user_id, capacity=capacity)
        return True

    def add_file_by(self, user_id: str, name: str, size: int) -> int | None:
        if user_id not in self.users:
            return None
        if name in self.files:
            return None
        user = self.users[user_id]
        if size > user.remaining_capacity:
            return None
        self.files[name] = File(name=name, size=size, owner_id=user_id)
        user.file_names.append(name)
        user.used_capacity += size
        return user.remaining_capacity

    def backup_user(self, user_id: str) -> int | None:
        if user_id not in self.users:
            return None
        user = self.users[user_id]
        backup_files = {}
        for file_name in user.file_names:
            if file_name in self.files:
                backup_files[file_name] = self.files[file_name].size
        self.backups[user_id] = backup_files
        return len(backup_files)

    def restore_user(self, user_id: str) -> int | None:
        if user_id not in self.users:
            return None
        user = self.users[user_id]
        for file_name in user.file_names:
            if file_name in self.files:
                del self.files[file_name]
        user.file_names.clear()
        user.used_capacity = 0
        if user_id in self.backups:
            restored_count = 0
            for file_name, size in self.backups[user_id].items():
                conflict = False
                for other_user in self.users.values():
                    if other_user.user_id != user_id and file_name in other_user.file_names:
                        conflict = True
                        break
                if not conflict:
                    self.files[file_name] = File(
                        name=file_name, size=size, owner_id=user_id
                    )
                    user.file_names.append(file_name)
                    user.used_capacity += size
                    restored_count += 1
            return restored_count
        return 0
