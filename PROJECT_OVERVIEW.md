# Project Overview

## What This Does

Automates filling W2 tax forms in ProSeries (or similar desktop tax software) using AI to intelligently understand the application's UI structure and map your data to the correct fields.

## Why It's Better Than Tab/Selector Methods

**Traditional Problems:**
- Desktop apps don't have HTML/CSS selectors
- Tab order changes between versions
- Screen coordinates break when UI changes
- Hardcoded positions are fragile

**Our Solution:**
- Uses **Accessibility APIs** to read UI structure (like DevTools for desktop)
- **AI understands** the form and maps fields intelligently
- **Adapts** to UI changes automatically
- **Works** even if ProSeries updates their interface

## Core Components

### 1. `ui_inspector.py`
- Inspects desktop app UI structure
- Like browser DevTools but for desktop apps
- Shows all form fields, buttons, and elements
- Helps debug automation issues

### 2. `ai_form_filler.py`
- Main automation engine
- Captures UI structure
- Asks AI to map fields
- Fills form automatically
- Generates debug files

### 3. `w2_data_handler.py`
- Validates W2 data (SSN, EIN format, etc.)
- Loads from JSON or CSV
- Generates sample data files
- Ensures data integrity

### 4. `batch_filler.py`
- Processes multiple W2s from CSV
- Handles navigation delays
- Batch processing automation

## Technology Stack

- **Python 3.9+** - Main language
- **atomacos** - macOS Accessibility API wrapper
- **OpenAI GPT-4** or **Anthropic Claude** - AI for field mapping
- **pydantic** - Data validation
- **python-dotenv** - Configuration management

## Workflow

```
┌─────────────────────┐
│   Open ProSeries    │
│   W2 Form           │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│  Capture UI Tree    │
│  (Accessibility)    │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│  Send to AI         │
│  "Map these fields" │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│  AI Returns         │
│  Field Mappings     │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│  Fill Form Fields   │
│  Automatically      │
└─────────────────────┘
```

## Files Generated

- `ui_debug.json` - Full UI structure captured
- `ai_mapping.json` - AI's field mapping decisions
- `sample_w2.json` - Single W2 template
- `sample_w2.csv` - Batch W2 template

## Cost Estimate

- OpenAI GPT-4: ~$0.03-0.10 per W2 form
- Anthropic Claude: ~$0.02-0.08 per W2 form
- Batch of 100 W2s: ~$3-10

## Limitations

- **macOS only** (Windows support would require different APIs)
- **Requires accessibility permissions**
- **AI costs** (but saves massive time)
- **Works best** with consistent form layouts
- May need **manual review** for complex forms

## Possible Extensions

1. **Windows Support** - Use UI Automation API
2. **Other Forms** - 1099, W4, 1040, etc.
3. **OCR Verification** - Screenshot comparison
4. **Web Interface** - GUI for easier use
5. **Form Navigation** - Auto-navigate between forms
6. **Error Recovery** - Retry failed fields
7. **Multi-Monitor** - Handle different screen setups

## Security Considerations

- Store W2 data securely (contains SSN)
- Never commit .env file with API keys
- Consider using key vaults for production
- Review AI mappings before trusting blindly
- Keep logs secure (may contain PII)

## Performance

- Single W2: ~10-20 seconds (mostly AI processing)
- Batch of 10: ~2-4 minutes (with navigation delays)
- UI capture: ~1-2 seconds
- AI mapping: ~5-10 seconds
- Field filling: ~3-5 seconds

## Success Factors

1. ✅ ProSeries must be running and focused
2. ✅ W2 form must be open and visible
3. ✅ Accessibility permissions granted
4. ✅ Valid API key with credits
5. ✅ Form fields must be accessible via Accessibility API
6. ✅ Stable internet connection (for AI calls)
