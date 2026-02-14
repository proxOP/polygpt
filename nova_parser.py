"""Nova JSON parsing module with hotfix for improved error handling."""

import json
from typing import Any, Dict, Optional


class NovaJSONParser:
    """Parser for Nova JSON responses with robust error handling."""
    
    @staticmethod
    def parse(json_string: str) -> Dict[str, Any]:
        """
        Parse Nova JSON response with validation.
        
        Args:
            json_string: JSON string to parse
            
        Returns:
            Parsed dictionary
            
        Raises:
            ValueError: If JSON is invalid
        """
        try:
            return json.loads(json_string)
        except json.JSONDecodeError as e:
            # Hotfix: Attempt to clean and retry
            cleaned = NovaJSONParser._clean_json(json_string)
            try:
                return json.loads(cleaned)
            except json.JSONDecodeError:
                raise ValueError(f"Failed to parse Nova JSON: {e}")
    
    @staticmethod
    def _clean_json(json_string: str) -> str:
        """Clean common JSON formatting issues."""
        # Remove trailing commas
        cleaned = json_string.replace(",\n}", "\n}")
        cleaned = cleaned.replace(",\n]", "\n]")
        return cleaned
    
    @staticmethod
    def extract_content(response: Dict[str, Any]) -> str:
        """Extract content from Nova API response."""
        if "content" in response:
            content = response["content"]
            if isinstance(content, list) and len(content) > 0:
                return content[0].get("text", "")
        return ""


if __name__ == "__main__":
    # Example usage
    example_json = '{"content": [{"text": "Hello from Nova"}]}'
    parsed = NovaJSONParser.parse(example_json)
    content = NovaJSONParser.extract_content(parsed)
    print(f"Parsed content: {content}")
