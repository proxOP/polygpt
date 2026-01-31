"""Prompt DTO with validation for prompt_name."""
from typing import Optional
from dataclasses import dataclass


@dataclass
class PromptDTO:
    """Data Transfer Object for prompts with validation."""
    
    prompt_name: str
    content: str
    version: str = "1.0"
    description: Optional[str] = None
    
    def __post_init__(self):
        """Validate prompt_name after initialization."""
        self._validate_prompt_name()
    
    def _validate_prompt_name(self) -> None:
        """
        Validate prompt_name directly.
        - Must not be empty
        - Must not contain wildcard characters
        - Must be standardized format (lowercase with underscores)
        """
        if not self.prompt_name or not isinstance(self.prompt_name, str):
            raise ValueError("prompt_name must be a non-empty string")
        
        # Check for wildcard characters
        if any(char in self.prompt_name for char in ['*', '?', '**', '%']):
            raise ValueError(f"prompt_name cannot contain wildcard characters: {self.prompt_name}")
        
        # Check for standardized format
        if not self.prompt_name.islower() or ' ' in self.prompt_name:
            raise ValueError(f"prompt_name must be lowercase with underscores, got: {self.prompt_name}")
    
    def to_dict(self) -> dict:
        """Convert DTO to dictionary."""
        return {
            'prompt_name': self.prompt_name,
            'content': self.content,
            'version': self.version,
            'description': self.description
        }
