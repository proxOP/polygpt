"""Prompt Manager for handling prompt operations."""
from typing import Dict, Optional
from dto.prompt_dto import PromptDTO
from prompts.prompt_constants import STANDARD_PROMPTS, DEFAULT_SYSTEM_PROMPT


class PromptManager:
    """Manages prompt storage and retrieval."""
    
    def __init__(self):
        """Initialize prompt manager with empty storage."""
        self._prompts: Dict[str, PromptDTO] = {}
    
    def register_prompt(self, prompt_dto: PromptDTO) -> None:
        """
        Register a prompt with validation.
        
        Args:
            prompt_dto: PromptDTO instance to register
            
        Raises:
            ValueError: If prompt validation fails
        """
        self._prompts[prompt_dto.prompt_name] = prompt_dto
    
    def get_prompt(self, prompt_name: str) -> Optional[PromptDTO]:
        """
        Retrieve a prompt by name.
        
        Args:
            prompt_name: Standardized prompt name
            
        Returns:
            PromptDTO if found, None otherwise
        """
        return self._prompts.get(prompt_name)
    
    def get_prompt_content(self, prompt_name: str) -> Optional[str]:
        """
        Get prompt content directly.
        
        Args:
            prompt_name: Standardized prompt name
            
        Returns:
            Prompt content string if found, None otherwise
        """
        prompt = self.get_prompt(prompt_name)
        return prompt.content if prompt else None
    
    def list_prompts(self) -> Dict[str, str]:
        """
        List all registered prompts.
        
        Returns:
            Dictionary of prompt names and descriptions
        """
        return {
            name: prompt.description or name 
            for name, prompt in self._prompts.items()
        }
    
    def remove_prompt(self, prompt_name: str) -> bool:
        """
        Remove a prompt.
        
        Args:
            prompt_name: Standardized prompt name
            
        Returns:
            True if removed, False if not found
        """
        if prompt_name in self._prompts:
            del self._prompts[prompt_name]
            return True
        return False
    
    def get_system_prompt(self) -> str:
        """
        Get default system prompt.
        
        Returns:
            Default system prompt string
        """
        return DEFAULT_SYSTEM_PROMPT


# Global prompt manager instance
_prompt_manager: Optional[PromptManager] = None


def get_prompt_manager() -> PromptManager:
    """
    Get or create global prompt manager instance.
    
    Returns:
        PromptManager instance
    """
    global _prompt_manager
    if _prompt_manager is None:
        _prompt_manager = PromptManager()
    return _prompt_manager
