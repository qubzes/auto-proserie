"""
Configuration Examples and Best Practices

This file shows different configuration scenarios for various use cases.
"""

# ==============================================================================
# SCENARIO 1: Single User, Development/Testing
# ==============================================================================

# Standard Gemini configuration for testing
TEST_CONFIG = {
    "GOOGLE_API_KEY": "your-api-key-here",
    "GEMINI_MODEL": "gemini-2.0-flash-exp",  # Fast and cost-effective
    "MAX_RETRIES": 3,
    "FIELD_FILL_DELAY": 0.3,  # Seconds between fields
}

# ==============================================================================
# SCENARIO 2: Production, High Accuracy Needed
# ==============================================================================

# Use latest Gemini model for best accuracy
PRODUCTION_CONFIG = {
    "GOOGLE_API_KEY": "your-api-key-here",
    "GEMINI_MODEL": "gemini-2.0-flash-exp",
    "MAX_RETRIES": 5,
    "FIELD_FILL_DELAY": 0.5,  # More cautious
    "VERIFY_EACH_FIELD": True,  # Read back values
}

# ==============================================================================
# SCENARIO 3: Batch Processing, Cost Optimization
# ==============================================================================

# Balance speed and cost for large batches
BATCH_CONFIG = {
    "GOOGLE_API_KEY": "your-api-key-here",
    "GEMINI_MODEL": "gemini-2.0-flash-exp",  # Very cost-effective
    "BATCH_SIZE": 10,  # Process in groups
    "DELAY_BETWEEN_BATCHES": 30,  # Seconds
    "CACHE_UI_STRUCTURE": True,  # Reuse UI analysis
}

# ==============================================================================
# SCENARIO 4: Different Tax Software
# ==============================================================================

# For Lacerte instead of ProSeries
LACERTE_CONFIG = {
    "APP_NAME": "Lacerte",
    "APP_BUNDLE_ID": "com.intuit.lacerte",
    "GOOGLE_API_KEY": "your-api-key-here",
    "FORM_TYPE": "W2",
}

# For Drake Tax
DRAKE_CONFIG = {
    "APP_NAME": "Drake",
    "APP_BUNDLE_ID": "com.drake.tax",  # hypothetical
    "GOOGLE_API_KEY": "your-api-key-here",
    "FORM_TYPE": "W2",
}

# ==============================================================================
# SCENARIO 5: High Security Environment
# ==============================================================================

# With extra validation and audit logging
SECURE_CONFIG = {
    "GOOGLE_API_KEY": "your-api-key-here",
    "VALIDATE_BEFORE_FILL": True,
    "VERIFY_AFTER_FILL": True,
    "LOG_ALL_ACTIONS": True,
    "LOG_FILE": "/secure/logs/w2_automation.log",
    "SCREENSHOT_BEFORE_AFTER": True,
    "REQUIRE_MANUAL_APPROVAL": True,
}

# ==============================================================================
# ADVANCED CONFIGURATIONS
# ==============================================================================

# Custom AI prompt for specific form layouts
CUSTOM_PROMPT_CONFIG = {
    "GOOGLE_API_KEY": "your-api-key-here",
    "CUSTOM_SYSTEM_PROMPT": """
        You are an expert at ProSeries W2 forms specifically.
        The W2 form has boxes numbered 1-20.
        Box 1 is always in the top-left section labeled "Wages, tips, other compensation".
        Focus on box numbers when mapping fields.
    """,
}

# Removed multi-provider fallback since we're using Gemini only

# ==============================================================================
# USAGE IN CODE
# ==============================================================================

"""
# In your script:

from config_examples import PRODUCTION_CONFIG
import os

# Load configuration
for key, value in PRODUCTION_CONFIG.items():
    os.environ[key] = str(value)

# Then use normally
automation = AIFormAutomation(os.getenv("APP_NAME", "ProSeries"))
"""

# ==============================================================================
# BEST PRACTICES
# ==============================================================================

BEST_PRACTICES = {
    "DO": [
        "Test with sample data first",
        "Review AI mappings before trusting",
        "Keep API keys secure in .env",
        "Grant only necessary permissions",
        "Validate data before filling",
        "Log all automation runs",
        "Have manual review process",
        "Start with one form before batch",
    ],
    "DONT": [
        "Commit API keys to git",
        "Run unattended without testing",
        "Process real SSNs without security",
        "Ignore AI confidence scores",
        "Skip accessibility permissions",
        "Use in production without testing",
        "Fill forms without verification",
        "Trust automation blindly",
    ],
}

# ==============================================================================
# TROUBLESHOOTING CONFIGURATIONS
# ==============================================================================

# Debug mode with verbose logging
DEBUG_CONFIG = {
    "DEBUG_MODE": True,
    "LOG_LEVEL": "DEBUG",
    "SAVE_ALL_UI_SNAPSHOTS": True,
    "SAVE_AI_RESPONSES": True,
    "SCREENSHOT_EACH_FIELD": True,
    "PAUSE_BETWEEN_FIELDS": 1.0,
}

# Minimal config for testing connection only
TEST_CONNECTION_CONFIG = {
    "APP_NAME": "ProSeries",
    "TEST_MODE": True,
    "SKIP_AI": True,  # Just test accessibility
    "DRY_RUN": True,  # Don't actually fill
}
