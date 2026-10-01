"""
JSON-file-backed "database" so data persists across restarts, without
needing a real database engine set up.
 
All users are kept in a single users.json file. This module loads that
file into memory on startup, and rewrites it after every mutation.
Swap this module out for a real DB (SQLAlchemy + Postgres/SQLite, etc.)
without changing the route logic in main.py.
"""
 
import json
from itertools import count
from pathlib import Path
from typing import Dict, Optional
 
from models import User, UserCreate, UserUpdate
 
DATA_FILE = Path(__file__).parent / "users.json"
 
_users_db: Dict[int, User] = {}
_id_counter = count(1)
 
 
def _load() -> None:
    """Load users.json into memory. Called once at module import time."""
    global _id_counter
 
    if not DATA_FILE.exists():
        DATA_FILE.write_text("[]")
 
    raw = json.loads(DATA_FILE.read_text() or "[]")
    for entry in raw:
        user = User(**entry)
        _users_db[user.id] = user
 
    max_id = max(_users_db.keys(), default=0)
    _id_counter = count(max_id + 1)
 
 
def _save() -> None:
    """Persist the current in-memory state back to users.json."""
    data = [user.model_dump(mode="json") for user in _users_db.values()]
    DATA_FILE.write_text(json.dumps(data, indent=2))
 
 
def create_user(user_in: UserCreate) -> User:
    new_id = next(_id_counter)
    user = User(id=new_id, **user_in.model_dump())
    _users_db[new_id] = user
    _save()
    return user
 
 
def get_user(user_id: int) -> Optional[User]:
    return _users_db.get(user_id)
 
 
def get_all_users() -> list[User]:
    return list(_users_db.values())
 
 
def replace_user(user_id: int, user_in: UserCreate) -> Optional[User]:
    if user_id not in _users_db:
        return None
    user = User(id=user_id, **user_in.model_dump())
    _users_db[user_id] = user
    _save()
    return user
 
 
def update_user(user_id: int, user_in: UserUpdate) -> Optional[User]:
    existing = _users_db.get(user_id)
    if existing is None:
        return None
    update_data = user_in.model_dump(exclude_unset=True)
    updated = existing.model_copy(update=update_data)
    _users_db[user_id] = updated
    _save()
    return updated
 
 
def delete_user(user_id: int) -> bool:
    if user_id in _users_db:
        del _users_db[user_id]
        _save()
        return True
    return False
 
 
_load()