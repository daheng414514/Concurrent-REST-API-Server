"""
    Thread-safe in-memory store for user data.
    
    Invariants:
    - name_key: name -> id
    - db: id -> info (dict)
    - All public methods acquire self.lock
"""


import threading

class Store:


    def __init__(self):
        self.next_id = 1
        self.db = {}     ##{id : info}
        self.name_key={}     ##{name : id}
        self.lock = threading.Lock()



    def count(self) -> int:
        with self.lock:
            return len(self.name_key)



    def clear(self) -> None:
        with self.lock:
            self.next_id = 1
            self.db.clear()
            self.name_key.clear()



    def exists(self, name) -> bool:
        if not isinstance(name, str) or not name.strip():
            return False
        with self.lock:
            return name in self.name_key



    def _validate_name(self, name) -> None:
        if not isinstance(name, str) or not name.strip():
            raise TypeError("Name must be a non-empty string")



    def get_user_info(self, name) -> dict:
        with self.lock:
            self._validate_name(name)
            if name not in self.name_key:
                raise KeyError("User not found.")
            key = self.name_key[name]
            return self.db[key]



    def get_key(self, name) -> int:
        with self.lock:
            self._validate_name(name)
            if name not in self.name_key:
                raise KeyError("User not found.")
            return self.name_key[name]

    

    def post_user_info(self, name, info) -> int:
        with self.lock:
            self._validate_name(name)
            if not isinstance(info, dict):
                raise TypeError("User data must be a dictionary")
            if name in self.name_key:
                raise KeyError("User already exists.")
            new_id = self.next_id
            self.next_id += 1
            self.name_key[name] = new_id
            self.db[new_id] = info
            return new_id
        


    def put_user_info(self, name, replace) -> dict:
        with self.lock:
            self._validate_name(name)
            if name not in self.name_key:
                raise KeyError("User not found.")
            key = self.name_key[name]
            if not isinstance(replace, dict):
                raise TypeError("User data must be a dictionary")
            self.db[key] = replace
            return self.db[key]


    def patch_user_info(self, name, change) -> dict:
        with self.lock:
            self._validate_name(name)
            if name not in self.name_key:
                raise KeyError("User not found.")
            key = self.name_key[name]
            if not isinstance(change, dict):
                raise TypeError("Patch data must be a dictionary")
            self.db[key].update(change)
            return self.db[key]



    def delete_user_info(self, name) -> dict:
        with self.lock:
            self._validate_name(name)
            if name not in self.name_key:
                raise KeyError("User not found.")
            delete_id = self.name_key[name]
            delete_info = self.db[delete_id]
            del self.db[delete_id]
            del self.name_key[name]
            return delete_info



    def list_users(self) -> list[str]:
        with self.lock:
            return sorted(self.name_key.keys())


    
    def _print_name_key(self):
        with self.lock:
            name_key_copy = self.name_key.copy()
        print("\nName : Key Report:\n")
        print("------------------\n")
        for name in sorted(name_key_copy):
            print(f"{name} : {name_key_copy[name]}\n")



    def _print_db(self):
        with self.lock:
            db_copy = self.db.copy()
        print("\nID : Info Report:\n")
        print("------------------\n")
        for user_id in sorted(db_copy):
            print(f"{user_id} : {db_copy[user_id]}\n")


