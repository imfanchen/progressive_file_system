#!/usr/bin/env python3

from storage_system_impl import StorageSystemBasicImpl, StorageSystemAdvancedImpl

def test_level_1_basic():
    """Test Level 1: Basic File Operations using README examples"""
    print("Testing Level 1: Basic File Operations")
    storage = StorageSystemBasicImpl()
    
    # Test add_file
    assert storage.add_file("/dir/file1.txt", 5) == True
    assert storage.add_file("/dir/file2.txt", 20) == True
    assert storage.add_file("/dir/deeper/file3.mov", 9) == True
    assert storage.add_file("/big_file.mp4", 20) == True
    
    # Test duplicate file
    assert storage.add_file("/dir/file1.txt", 10) == False
    
    # Test get_file_size
    assert storage.get_file_size("/dir/file1.txt") == 5
    assert storage.get_file_size("/dir/file2.txt") == 20
    assert storage.get_file_size("/dir/deeper/file3.mov") == 9
    assert storage.get_file_size("/big_file.mp4") == 20
    assert storage.get_file_size("/nonexistent.txt") == None
    
    # Test delete_file
    assert storage.delete_file("/dir/file1.txt") == 5
    assert storage.get_file_size("/dir/file1.txt") == None
    assert storage.delete_file("/nonexistent.txt") == None
    
    print("✓ Level 1 tests passed!")

def test_level_2_statistics():
    """Test Level 2: File Statistics using README examples"""
    print("\nTesting Level 2: File Statistics")
    storage = StorageSystemBasicImpl()
    
    # Add test files from README examples
    storage.add_file("/dir/file1.txt", 5)
    storage.add_file("/dir/file2.txt", 20)
    storage.add_file("/dir/deeper/file3.mov", 9)
    storage.add_file("/big_file.mp4", 20)
    
    # Test get_n_largest examples from README
    assert storage.get_n_largest("/dir", 2) == ["/dir/file2.txt", "/dir/file1.txt"]
    assert storage.get_n_largest("/dir/file", 3) == ["/dir/file1.txt"]
    assert storage.get_n_largest("/another_dir", 2) == []
    assert storage.get_n_largest("/", 2) == ["/big_file.mp4", "/dir/file2.txt"]
    
    # Additional edge cases
    assert storage.get_n_largest("/dir", 10) == ["/dir/file2.txt", "/dir/file1.txt", "/dir/deeper/file3.mov"]
    assert storage.get_n_largest("/dir/deeper", 1) == ["/dir/deeper/file3.mov"]
    assert storage.get_n_largest("/", 1) == ["/big_file.mp4"]
    
    print("✓ Level 2 tests passed!")

def test_level_3_user_management():
    """Test Level 3: User Management with creative scenarios"""
    print("\nTesting Level 3: User Management")
    storage = StorageSystemAdvancedImpl()
    
    # Test user creation
    assert storage.add_user("alice", 100) == True
    assert storage.add_user("bob", 200) == True
    assert storage.add_user("alice", 150) == False  # Duplicate user
    
    # Test file operations by users
    assert storage.add_file_by("alice", "/alice/doc1.txt", 30) == 70  # 100 - 30
    assert storage.add_file_by("alice", "/alice/doc2.txt", 40) == 30  # 70 - 40
    assert storage.add_file_by("alice", "/alice/doc3.txt", 50) == None  # Exceeds capacity (30 < 50)
    
    assert storage.add_file_by("bob", "/bob/video.mp4", 150) == 50  # 200 - 150
    assert storage.add_file_by("bob", "/bob/photo.jpg", 30) == 20   # 50 - 30
    
    # Test admin operations (Level 1 methods)
    assert storage.add_file("/admin/system.log", 1000) == True
    assert storage.add_file("/admin/config.json", 500) == True
    
    # Test file size retrieval
    assert storage.get_file_size("/alice/doc1.txt") == 30
    assert storage.get_file_size("/bob/video.mp4") == 150
    assert storage.get_file_size("/admin/system.log") == 1000
    
    # Test file deletion and capacity update
    assert storage.delete_file("/alice/doc1.txt") == 30
    assert storage.add_file_by("alice", "/alice/new_doc.txt", 30) == 70  # Capacity restored
    
    # Test non-existent user
    assert storage.add_file_by("charlie", "/charlie/file.txt", 10) == None
    
    # Test duplicate file names across users
    assert storage.add_file_by("alice", "/shared/file.txt", 20) == 50
    assert storage.add_file_by("bob", "/shared/file.txt", 20) == None  # Name conflict
    
    print("✓ Level 3 tests passed!")

def test_level_4_backup_restore():
    """Test Level 4: Backup and Restore with creative scenarios"""
    print("\nTesting Level 4: Backup and Restore")
    storage = StorageSystemAdvancedImpl()
    
    # Setup users and files
    storage.add_user("alice", 100)
    storage.add_user("bob", 200)
    
    storage.add_file_by("alice", "/alice/doc1.txt", 30)
    storage.add_file_by("alice", "/alice/doc2.txt", 40)
    storage.add_file_by("bob", "/bob/video.mp4", 150)
    storage.add_file_by("bob", "/bob/photo.jpg", 30)
    
    # Test backup
    assert storage.backup_user("alice") == 2
    assert storage.backup_user("bob") == 2
    assert storage.backup_user("charlie") == None  # Non-existent user
    
    # Test restore scenario 1: Delete files and restore
    storage.delete_file("/alice/doc1.txt")
    storage.add_file_by("alice", "/alice/temp.txt", 20)
    assert storage.restore_user("alice") == 2
    assert storage.get_file_size("/alice/doc1.txt") == 30  # Restored
    assert storage.get_file_size("/alice/doc2.txt") == 40  # Restored
    assert storage.get_file_size("/alice/temp.txt") == None  # Gone
    
    # Test restore scenario 2: File conflicts
    storage.add_file_by("bob", "/shared/file.txt", 50)
    storage.backup_user("bob")
    storage.add_file_by("alice", "/shared/file.txt", 30)  # Create conflict
    assert storage.restore_user("bob") == 1  # Only 1 file restored (conflict ignored)
    assert storage.get_file_size("/shared/file.txt") == 30  # Alice's file remains
    
    # Test restore scenario 3: No backup exists
    storage.add_user("eve", 100)
    storage.add_file_by("eve", "/eve/file1.txt", 50)
    storage.add_file_by("eve", "/eve/file2.txt", 30)
    assert storage.restore_user("eve") == 0  # No backup, all files deleted
    assert storage.get_file_size("/eve/file1.txt") == None
    assert storage.get_file_size("/eve/file2.txt") == None
    
    # Test restore scenario 4: Multiple backups
    storage.add_file_by("alice", "/alice/new_doc.txt", 25)
    storage.backup_user("alice")  # New backup overwrites old one
    storage.delete_file("/alice/doc2.txt")
    storage.add_file_by("alice", "/alice/another.txt", 35)
    assert storage.restore_user("alice") == 2  # Only files from latest backup
    assert storage.get_file_size("/alice/doc1.txt") == 30
    assert storage.get_file_size("/alice/new_doc.txt") == 25
    assert storage.get_file_size("/alice/doc2.txt") == None  # Not in latest backup
    assert storage.get_file_size("/alice/another.txt") == None  # Not in backup
    
    print("✓ Level 4 tests passed!")

def test_edge_cases():
    """Test edge cases and error conditions"""
    print("\nTesting Edge Cases")
    
    # Test with empty storage
    storage = StorageSystemBasicImpl()
    assert storage.get_n_largest("/", 5) == []
    assert storage.get_file_size("/any") == None
    assert storage.delete_file("/any") == None
    
    # Test with zero and negative sizes
    storage_adv = StorageSystemAdvancedImpl()
    storage_adv.add_user("test", 100)
    assert storage_adv.add_file_by("test", "/test/zero.txt", 0) == 100
    assert storage_adv.add_file_by("test", "/test/negative.txt", -10) == 110  # Negative size allowed
    
    # Test with very large numbers
    storage_adv.add_user("large", 1000000)
    assert storage_adv.add_file_by("large", "/large/big.txt", 999999) == 1
    
    # Test with special characters in names
    assert storage_adv.add_file("/special/!@#$%^&*().txt", 100) == True
    assert storage_adv.get_file_size("/special/!@#$%^&*().txt") == 100
    
    print("✓ Edge cases tests passed!")

def main():
    """Run all tests"""
    print("Running StorageSystem Tests\n")
    
    try:
        test_level_1_basic()
        test_level_2_statistics()
        test_level_3_user_management()
        test_level_4_backup_restore()
        test_edge_cases()
        print("\n🎉 All tests passed! StorageSystem implementation is working correctly.")
    except AssertionError as e:
        print(f"\n❌ Test failed: {e}")
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")

if __name__ == "__main__":
    main() 