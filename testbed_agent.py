"""Testbed agent module with organization support."""

from typing import Any, Dict, Optional
from dataclasses import dataclass, asdict
from enum import Enum
from storage import StorageBackend, MemoryStorage


class AgentStatus(Enum):
    """Agent execution status."""
    IDLE = "idle"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"


@dataclass
class AgentState:
    """
    Agent state with organization context.
    
    Added org_id and org_name support for multi-tenant architecture.
    """
    agent_id: str
    org_id: Optional[str] = None
    org_name: Optional[str] = None
    status: AgentStatus
    config: Dict[str, Any]
    results: Optional[Dict[str, Any]] = None
    error: Optional[str] = None
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for storage."""
        data = asdict(self)
        data["status"] = self.status.value
        return data
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "AgentState":
        """Create from dictionary."""
        # Convert status field
        data["status"] = AgentStatus(data["status"]) if isinstance(data.get("status"), str) else data.get("status")
        # Provide backward-compatible defaults for org fields
        if "org_id" not in data:
            data["org_id"] = None
        if "org_name" not in data:
            data["org_name"] = None
        return cls(**data)


class TestbedAgent:
    """Testbed agent for running prompt experiments."""
    
    def __init__(self, agent_id: str, org_id: Optional[str] = None, org_name: Optional[str] = None, 
                 storage: Optional[StorageBackend] = None):
        """
        Initialize testbed agent.
        
        Args:
            agent_id: Unique agent identifier
            org_id: Organization ID for multi-tenant support
            org_name: Organization name
            storage: Storage backend (defaults to memory)
        """
        self.agent_id = agent_id
        self.org_id = org_id
        self.org_name = org_name
        self.storage = storage or MemoryStorage()
        self.state = AgentState(
            agent_id=agent_id,
            org_id=org_id,
            org_name=org_name,
            status=AgentStatus.IDLE,
            config={}
        )
    
    def configure(self, config: Dict[str, Any]) -> None:
        """Configure agent with custom settings."""
        self.state.config = config
        self._save_state()
    
    def run(self, prompt: str) -> str:
        """
        Execute agent with given prompt.
        
        Returns:
            Agent response
        """
        self.state.status = AgentStatus.RUNNING
        self._save_state()
        
        try:
            # Simulate processing
            result = f"[{self.org_name}] Processed: {prompt}"
            self.state.results = {"response": result}
            self.state.status = AgentStatus.COMPLETED
            return result
        except Exception as e:
            self.state.error = str(e)
            self.state.status = AgentStatus.FAILED
            raise
        finally:
            self._save_state()
    
    def get_state(self) -> AgentState:
        """Get current agent state."""
        return self.state
    
    def _save_state(self) -> bool:
        """Save state to storage."""
        return self.storage.save(
            key=self.agent_id,
            data=self.state.to_dict(),
            org_id=self.org_id
        )
    
    def _load_state(self) -> bool:
        """Load state from storage."""
        # Try org-scoped load first (if org_id present), otherwise attempt legacy/global load
        data = self.storage.load(self.agent_id, self.org_id)
        if not data and self.org_id is not None:
            # Attempt legacy/global load without org_id for backward compatibility
            data = self.storage.load(self.agent_id, None)

        if data:
            # Merge loaded values into state while preserving current org context when missing
            loaded = AgentState.from_dict(data)
            # If loaded doesn't have org_id/org_name, prefer current agent values
            if not loaded.org_id:
                loaded.org_id = self.org_id
            if not loaded.org_name:
                loaded.org_name = self.org_name
            self.state = loaded
            return True
        return False


if __name__ == "__main__":
    # Example usage
    agent = TestbedAgent(
        agent_id="test_agent_1",
        org_id="org_123",
        org_name="Acme Corp"
    )
    
    agent.configure({"model": "gpt-4", "temperature": 0.7})
    result = agent.run("What is AI?")
    print(f"Result: {result}")
    print(f"State: {agent.get_state()}")
