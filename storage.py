"""Storage abstraction for testbed agents with MongoDB support."""

from abc import ABC, abstractmethod
from typing import Any, Dict, Optional
from datetime import datetime


class StorageBackend(ABC):
    """Abstract base class for storage backends."""
    
    @abstractmethod
    def save(self, key: str, data: Dict[str, Any], org_id: str) -> bool:
        """Save data with organization context."""
        pass
    
    @abstractmethod
    def load(self, key: str, org_id: str) -> Optional[Dict[str, Any]]:
        """Load data for specific organization."""
        pass
    
    @abstractmethod
    def delete(self, key: str, org_id: str) -> bool:
        """Delete data for specific organization."""
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
    
    def save(self, key: str, data: Dict[str, Any], org_id: str) -> bool:
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
    
    def load(self, key: str, org_id: str) -> Optional[Dict[str, Any]]:
        """Load agent state from MongoDB."""
        try:
            print(f"[MongoDB] Loading document for org_id={org_id}, key={key}")
            # result = self.db.agents.find_one({"_id": key, "org_id": org_id})
            # return result.get("data") if result else None
            return None
        except Exception as e:
            print(f"[MongoDB] Load failed: {e}")
            return None
    
    def delete(self, key: str, org_id: str) -> bool:
        """Delete agent state from MongoDB."""
        try:
            print(f"[MongoDB] Deleting document for org_id={org_id}, key={key}")
            # self.db.agents.delete_one({"_id": key, "org_id": org_id})
            return True
        except Exception as e:
            print(f"[MongoDB] Delete failed: {e}")
            return False


class MemoryStorage(StorageBackend):
    """In-memory storage for testing."""
    
    def __init__(self):
        self._store: Dict[str, Dict[str, Any]] = {}
    
    def save(self, key: str, data: Dict[str, Any], org_id: str) -> bool:
        """Save to memory."""
        self._store[f"{org_id}:{key}"] = data
        return True
    
    def load(self, key: str, org_id: str) -> Optional[Dict[str, Any]]:
        """Load from memory."""
        return self._store.get(f"{org_id}:{key}")
    
    def delete(self, key: str, org_id: str) -> bool:
        """Delete from memory."""
        self._store.pop(f"{org_id}:{key}", None)
        return True


if __name__ == "__main__":
    # Example usage
    storage = MemoryStorage()
    storage.save("agent_1", {"status": "running"}, "org_123")
    data = storage.load("agent_1", "org_123")
    print(f"Loaded data: {data}")
