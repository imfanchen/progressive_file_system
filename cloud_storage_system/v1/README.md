# Instructions

Your task is to implement a simple cloud storage system that maps objects (files) to their meta-information. The system should maintain files and their associated data, such as names and sizes. This system is in-memory, meaning there is no need to interact with the real filesystem.

# Requirements

Plan your design according to the level specifications below:

- **Level 1:** Basic File Operations - The cloud storage system should support basic file operations: add, retrieve, and delete files.
- **Level 2:** File Statistics - Support for retrieving statistics about files with a specific prefix.
- **Level 3:** User Management - Support for multiple users, each with a storage capacity limit. All users share the same cloud storage system.
- **Level 4:** Backup and Restore - Support for backing up and restoring files for individual users.

---

# Level 1

The cloud storage system should support basic file operations: adding, retrieving, and deleting files.

- `add_file(self, name: str, size: int) -> bool`  
  Adds a new file with the specified name and size to the storage.  
  Fails if a file with the same name already exists.  
  Returns: True if the file is added successfully, False otherwise.

- `get_file_size(self, name: str) -> int | None`  
  Retrieves the size of the file with the given name.  
  Returns: The file size if it exists, or None otherwise.

- `delete_file(self, name: str) -> int | None`  
  Deletes the file with the specified name.  
  Returns: The size of the deleted file if the operation is successful, or None if the file does not exist.

---

# Level 2

Support for retrieving statistics about files with a specific prefix.

- `get_n_largest(self, prefix: str, n: int) -> List[str]`  
  Returns a list of the names of the top n largest files with names starting with the specified prefix.  
  Files should be sorted by size in descending order. In case of a tie, names should be sorted lexicographically.  
  If no such files exist, return an empty list.  
  If the number of matching files is less than n, return all of them in the specified format.

---

# Level 3

Support for multiple users, each with a storage capacity limit. All users share the same cloud storage system.

- `add_user(self, user_id: str, capacity: int) -> bool`  
  Adds a new user with the specified storage capacity (in bytes).  
  Fails if a user with the same user_id already exists.  
  Returns: True if the user is added successfully, False otherwise.

- `add_file_by(self, user_id: str, name: str, size: int) -> int | None`  
  Adds a file owned by the specified user, following the same logic as add_file from Level 1.  
  A file cannot be added if it exceeds the user's remaining capacity.  
  Returns: The user's remaining capacity if the file is added successfully, or None otherwise.

**Note:** 

All Level 1 add_file operations are performed by the "admin" user, who has unlimited storage capacity.

---

# Level 4

Support for backing up and restoring files for individual users.

- `backup_user(self, user_id: str) -> int | None`  
  Backs up the current state of all files owned by the user.  
  The backup is stored separately and is not affected by subsequent file manipulations.  
  Overwrites any previous backups for the same user.  
  Returns: The number of files backed up, or None if the user does not exist.

- `restore_user(self, user_id: str) -> int | None`  
  Restores the user's files to their latest backup.  
  If no backup exists, all files owned by the user are deleted.  
  Files that cannot be restored (e.g., due to naming conflicts with other users) are ignored.  
  Returns: The number of files successfully restored, or None if the user does not exist.

**Notes:**

- The restore_user operation does not affect the user's capacity.
- Merging users does not affect the backup of user_id1, but user_id2 is deleted along with its backup.