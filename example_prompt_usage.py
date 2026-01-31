"""Example usage and tests for Prompt DTO and Manager."""
from dto.prompt_dto import PromptDTO
from prompts.prompt_manager import get_prompt_manager
from prompts.prompt_constants import (
    PROMPT_ASSESSMENT,
    PROMPT_CODIFY,
    PROMPT_USER_QUERY,
)


def main():
    """Demonstrate prompt handling functionality."""
    
    # Get prompt manager instance
    manager = get_prompt_manager()
    
    # Create and register prompts with validation
    try:
        # Valid prompt
        assessment_prompt = PromptDTO(
            prompt_name=PROMPT_ASSESSMENT,
            content="Analyze the policy for assessment purposes.",
            version="1.0",
            description="Assessment Agent Prompt"
        )
        manager.register_prompt(assessment_prompt)
        print(f"✓ Registered: {PROMPT_ASSESSMENT}")
        
        # Another valid prompt
        codify_prompt = PromptDTO(
            prompt_name=PROMPT_CODIFY,
            content="Generate code based on specifications.",
            version="1.0",
            description="Codify Code Generation Prompt"
        )
        manager.register_prompt(codify_prompt)
        print(f"✓ Registered: {PROMPT_CODIFY}")
        
        user_query_prompt = PromptDTO(
            prompt_name=PROMPT_USER_QUERY,
            content="Process user query and extract intent.",
            version="1.0",
            description="User Query Processor Prompt"
        )
        manager.register_prompt(user_query_prompt)
        print(f"✓ Registered: {PROMPT_USER_QUERY}")
        
    except ValueError as e:
        print(f"✗ Validation error: {e}")
    
    # Retrieve prompts
    print("\n--- Registered Prompts ---")
    for prompt_name, description in manager.list_prompts().items():
        print(f"• {prompt_name}: {description}")
    
    # Get specific prompt content
    print("\n--- Prompt Content Retrieval ---")
    content = manager.get_prompt_content(PROMPT_ASSESSMENT)
    if content:
        print(f"Assessment Prompt Content: {content}")
    
    # Test invalid prompt (wildcard in name)
    print("\n--- Validation Test ---")
    try:
        invalid_prompt = PromptDTO(
            prompt_name="assessment*prompt",  # Invalid: contains wildcard
            content="Invalid prompt"
        )
        manager.register_prompt(invalid_prompt)
    except ValueError as e:
        print(f"✓ Validation caught invalid prompt: {e}")
    
    # Test invalid prompt (not lowercase)
    try:
        invalid_prompt = PromptDTO(
            prompt_name="Assessment Prompt",  # Invalid: not lowercase
            content="Invalid prompt"
        )
        manager.register_prompt(invalid_prompt)
    except ValueError as e:
        print(f"✓ Validation caught invalid prompt: {e}")
    
    print("\n✓ Prompt handling system ready!")


if __name__ == "__main__":
    main()
