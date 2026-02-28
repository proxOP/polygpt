"""Standardized prompt names and constants."""

# Standardized prompt names (replacing inconsistent/wild prompt names)
PROMPT_ASSESSMENT = "assessment_prompt"
PROMPT_BRE_RULES = "bre_rules_prompt"
PROMPT_CODIFY = "codify_prompt"
PROMPT_GENERATE_OPTIONS = "generate_options_prompt"
PROMPT_KEYS_MAPPER = "keys_mapper_prompt"
PROMPT_SUMMARIZE = "summarize_prompt"
PROMPT_USER_QUERY = "user_query_processor_prompt"
PROMPT_COMPARE = "compare_processor_prompt"
PROMPT_TEST_BED = "test_bed_prompt"
PROMPT_RULIFY = "rulify_prompt"
PROMPT_FRAUD_DETECTION = "fraud_detection_prompt"

# Dictionary mapping for prompt standardization
STANDARD_PROMPTS = {
    PROMPT_ASSESSMENT: "Assessment Agent Prompt",
    PROMPT_BRE_RULES: "BRE Rules Agent Prompt",
    PROMPT_CODIFY: "Codify Code Generation Prompt",
    PROMPT_GENERATE_OPTIONS: "Generate Options Agent Prompt",
    PROMPT_KEYS_MAPPER: "Keys Mapper Agent Prompt",
    PROMPT_SUMMARIZE: "Summarize Agent Prompt",
    PROMPT_USER_QUERY: "User Query Processor Prompt",
    PROMPT_COMPARE: "Compare Processor Prompt",
    PROMPT_TEST_BED: "Test Bed Agent Prompt",
    PROMPT_RULIFY: "Rulify Agent Prompt",
    PROMPT_FRAUD_DETECTION: "Fraud Detection Prompt",
}

# Default system prompts
DEFAULT_SYSTEM_PROMPT = "You are a helpful assistant."
