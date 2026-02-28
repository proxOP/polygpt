"""Storage abstraction for testbed agents with MongoDB support."""

from abc import ABC, abstractmethod
from typing import Any, Dict, Optional
from datetime import datetime


class StorageBackend(ABC):
    """Abstract base class for storage backends."""
    
    @abstractmethod
    def save(self, key: str, data: Dict[str, Any], org_id: Optional[str] = None) -> bool:
        """Save data with organization context."""
        pass
    
    @abstractmethod
    def load(self, key: str, org_id: Optional[str] = None) -> Optional[Dict[str, Any]]:
        """Load data for specific organization or legacy/global key if org_id is None."""
        pass
    
    @abstractmethod
    def delete(self, key: str, org_id: Optional[str] = None) -> bool:
        """Delete data for specific organization or legacy/global key if org_id is None."""
        pass


class MongoDBStorage(StorageBackend):
    """MongoDB storage implementation for testbed agents."""
    
    def __init__(self, connection_string: str):
        """
        Initialize MongoDB storage.
        
        Args:
            connection_string: MongoDB connection URI
        """
        self.connection_string = connection_string
        self.db = None
        self._connect()
    
    def _connect(self):
        """Establish MongoDB connection."""
        # Placeholder for actual MongoDB connection
        print(f"[MongoDB] Connecting to: {self.connection_string}")
        # self.db = MongoClient(self.connection_string)
    
    def save(self, key: str, data: Dict[str, Any], org_id: Optional[str] = None) -> bool:
        """
        Save agent state to MongoDB.
        
        Updated storage save method includes org_id tracking and timestamps.
        """
        try:
            document = {
                "_id": key,
                "org_id": org_id,
                "data": data,
                "created_at": datetime.utcnow(),
                "updated_at": datetime.utcnow()
            }
            print(f"[MongoDB] Saving document for org_id={org_id}, key={key}")
            # self.db.agents.update_one({"_id": key}, {"$set": document}, upsert=True)
            return True
        except Exception as e:
            print(f"[MongoDB] Save failed: {e}")
            return False
    
    def load(self, key: str, org_id: Optional[str] = None) -> Optional[Dict[str, Any]]:
        """Load agent state from MongoDB.

        If `org_id` is provided, attempt an org-scoped lookup first. If not found,
        a legacy/global lookup (without org restriction) could be attempted.
        """
        try:
            print(f"[MongoDB] Loading document for org_id={org_id}, key={key}")
            # If org_id is provided, search by both _id and org_id first
            # result = self.db.agents.find_one({"_id": key, "org_id": org_id})
            # if not result and org_id is not None:
            #     # Fallback to legacy/global record
            #     result = self.db.agents.find_one({"_id": key})
            # return result.get("data") if result else None
            return None
        except Exception as e:
            print(f"[MongoDB] Load failed: {e}")
            return None
    
    def delete(self, key: str, org_id: Optional[str] = None) -> bool:
        """Delete agent state from MongoDB."""
        try:
            print(f"[MongoDB] Deleting document for org_id={org_id}, key={key}")
            # Prefer org-scoped delete if org_id provided, otherwise delete global/legacy
            # if org_id is not None:
            #     self.db.agents.delete_one({"_id": key, "org_id": org_id})
            # else:
            #     self.db.agents.delete_one({"_id": key})
            return True
        except Exception as e:
            print(f"[MongoDB] Delete failed: {e}")
            return False


class MemoryStorage(StorageBackend):
    """In-memory storage for testing."""
    
    def __init__(self):
        self._store: Dict[str, Dict[str, Any]] = {}
    
    def save(self, key: str, data: Dict[str, Any], org_id: Optional[str] = None) -> bool:
        """Save to memory. Uses `org_id:key` when org_id provided, otherwise uses legacy key."""
        store_key = f"{org_id}:{key}" if org_id is not None else key
        self._store[store_key] = data
        return True
    
    def load(self, key: str, org_id: Optional[str] = None) -> Optional[Dict[str, Any]]:
        """Load from memory.

        If `org_id` provided, try org-scoped key first then fallback to legacy key.
        """
        if org_id is not None:
            found = self._store.get(f"{org_id}:{key}")
            if found is not None:
                return found
            # Fallback to legacy/global record
            return self._store.get(key)
        return self._store.get(key)
    
    def delete(self, key: str, org_id: Optional[str] = None) -> bool:
        """Delete from memory. Attempts org-scoped delete then legacy delete."""
        if org_id is not None:
            self._store.pop(f"{org_id}:{key}", None)
        self._store.pop(key, None)
        return True


if __name__ == "__main__":
    # Example usage
    storage = MemoryStorage()
    storage.save("agent_1", {"status": "running"}, "org_123")
    data = storage.load("agent_1", "org_123")
    print(f"Loaded data: {data}")
