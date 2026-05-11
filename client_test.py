"""
    Testing file for functions.py
"""

from user_store import Store

def test_create_and_get():
    store = Store()
    store.post_user_info("alice", {"name": "alice", "age": 20})
    assert store.get_user_info("alice") == {"name": "alice", "age": 20}
    assert store.get_key("alice") == 1

def test_exists_and_count():
    store = Store()
    store.post_user_info("alice", {"name": "alice", "age": 20})
    store.post_user_info("john", {"name": "john"})
    store.post_user_info("roy", {"name": "roy", "age": 49, "email": "roy.gmail.com"})
    assert store.exists("john")
    assert store.count() == 3

def test_patch_user():
    store = Store()
    store.post_user_info("alice", {"name": "alice", "age": 20})
    store.patch_user_info("alice", {"age": 23})
    assert store.get_user_info("alice") == {"name": "alice", "age": 23}

def test_delete_user():
    store = Store()
    store.post_user_info("alice", {"name": "alice", "age": 20})
    store.post_user_info("john", {"name": "john"})
    store.post_user_info("roy", {"name": "roy", "age": 49, "email": "roy.gmail.com"})
    deleted = store.delete_user_info("john")
    assert deleted == {"name": "john"}
    assert not store.exists("john")
    assert store.count() == 2
    assert store.exists("alice")
    assert store.exists("roy")


if __name__ == "__main__":
    test_create_and_get()
    test_exists_and_count()
    test_patch_user()
    test_delete_user()
    print("All tests passed!")
