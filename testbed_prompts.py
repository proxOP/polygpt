"""Prompt management for testbed with MongoDB storage integration."""

from typing import List, Dict, Any, Optional
from storage import StorageBackend, MongoDBStorage
from testbed_agent import TestbedAgent


@dataclass
class TestbedPrompt:
    """Template for testbed prompts with organization context."""
    prompt_id: str
    org_id: str
    org_name: str
    title: str
    content: str
    version: int = 1
    tags: List[str] = None
    
    def __post_init__(self):
        if self.tags is None:
            self.tags = []


class TestbedPromptManager:
    """
    Manage prompts for testbed agents.
    
    Migrated testbed prompts to MongoDB storage for persistence and scalability.
    """
    
    def __init__(self, storage: StorageBackend):
        """
        Initialize prompt manager.
        
        Args:
            storage: Storage backend (MongoDB or in-memory)
        """
        self.storage = storage
        self.prompts: Dict[str, TestbedPrompt] = {}
    
    def create_prompt(self, prompt_id: str, org_id: str, org_name: str, 
                      title: str, content: str, tags: List[str] = None) -> TestbedPrompt:
        """Create a new testbed prompt."""
        prompt = TestbedPrompt(
            prompt_id=prompt_id,
            org_id=org_id,
            org_name=org_name,
            title=title,
            content=content,
            tags=tags or []
        )
        self.prompts[prompt_id] = prompt
        self._save_prompt(prompt)
        return prompt
    
    def get_prompt(self, prompt_id: str, org_id: str) -> Optional[TestbedPrompt]:
        """Retrieve prompt by ID."""
        if prompt_id in self.prompts:
            return self.prompts[prompt_id]
        
        # Try loading from storage
        data = self.storage.load(prompt_id, org_id)
        if data:
            return TestbedPrompt(**data)
        return None
    
    def list_org_prompts(self, org_id: str) -> List[TestbedPrompt]:
        """List all prompts for an organization."""
        return [p for p in self.prompts.values() if p.org_id == org_id]
    
    def update_prompt(self, prompt_id: str, org_id: str, **kwargs) -> Optional[TestbedPrompt]:
        """Update existing prompt."""
        prompt = self.get_prompt(prompt_id, org_id)
        if not prompt:
            return None
        
        for key, value in kwargs.items():
            if hasattr(prompt, key):
                setattr(prompt, key, value)
        
        prompt.version += 1
        self._save_prompt(prompt)
        return prompt
    
    def delete_prompt(self, prompt_id: str, org_id: str) -> bool:
        """Delete prompt."""
        success = self.storage.delete(prompt_id, org_id)
        self.prompts.pop(prompt_id, None)
        return success
    
    def _save_prompt(self, prompt: TestbedPrompt) -> bool:
        """Save prompt to storage."""
        from dataclasses import asdict
        return self.storage.save(
            key=prompt.prompt_id,
            data=asdict(prompt),
            org_id=prompt.org_id
        )
    
    def test_prompt(self, prompt_id: str, org_id: str, agent: TestbedAgent) -> str:
        """Test a prompt with an agent."""
        prompt = self.get_prompt(prompt_id, org_id)
        if not prompt:
            raise ValueError(f"Prompt {prompt_id} not found")
        
        return agent.run(prompt.content)


if __name__ == "__main__":
    from dataclasses import dataclass
    
    # Example usage
    storage = MongoDBStorage("mongodb://localhost:27017/polygpt")
    manager = TestbedPromptManager(storage)
    
    # Create prompt
    prompt = manager.create_prompt(
        prompt_id="prompt_001",
        org_id="org_123",
        org_name="Acme Corp",
        title="Classification Task",
        content="Classify the sentiment: 'I love this product!'",
        tags=["classification", "sentiment"]
    )
    
    print(f"Created prompt: {prompt.title}")
    
    # Test with agent
    agent = TestbedAgent("agent_1", "org_123", "Acme Corp")
    result = manager.test_prompt("prompt_001", "org_123", agent)
    print(f"Test result: {result}")
