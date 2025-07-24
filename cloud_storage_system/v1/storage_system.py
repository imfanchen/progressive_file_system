from abc import ABC

class StorageSystem(ABC):
    

    def add_file(self, name: str, size: int) -> bool:
        """Adds a new file with the specified name and size to the storage."""
        pass
    
    def get_file_size(self, name: str) -> int | None:
        """Retrieves the size of the file with the given name."""
        pass
    
    def delete_file(self, name: str) -> int | None:
        """Deletes the file with the specified name."""
        pass
    
    def get_n_largest(self, prefix: str, n: int) -> list[str]:
        """Returns a list of the names of the top n largest files with names starting with the specified prefix."""
        pass
    
    def add_user(self, user_id: str, capacity: int) -> bool:
        """Adds a new user with the specified storage capacity."""
        pass
    
    def add_file_by(self, user_id: str, name: str, size: int) -> int | None:
        """Adds a file owned by the specified user."""
        pass
    
    def backup_user(self, user_id: str) -> int | None:
        """Backs up the current state of all files owned by the user."""
        pass

    def restore_user(self, user_id: str) -> int | None:
        """Restores the user's files to their latest backup."""
        pass