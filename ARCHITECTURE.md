# System Architecture

```
┌─────────────────────────────────────────────────────────────────────────┐
│                         USER INTERACTION                                 │
└────────────────────────────────┬────────────────────────────────────────┘
                                 │
                                 ▼
                    ┌────────────────────────┐
                    │   W2 Data Input        │
                    │   - JSON File          │
                    │   - CSV File           │
                    │   - Manual Entry       │
                    └────────┬───────────────┘
                             │
                             ▼
                    ┌────────────────────────┐
                    │  w2_data_handler.py    │
                    │  - Validate SSN/EIN    │
                    │  - Format data         │
                    │  - Create objects      │
                    └────────┬───────────────┘
                             │
                             ▼
┌────────────────────────────────────────────────────────────────────────────┐
│                         MAIN AUTOMATION FLOW                                │
│                                                                             │
│  ┌─────────────────────────────────────────────────────────────────────┐  │
│  │                      ai_form_filler.py                              │  │
│  │                                                                     │  │
│  │  Step 1: Connect to Application                                    │  │
│  │  ┌──────────────────┐                                              │  │
│  │  │ atomacos         │  ←─── macOS Accessibility API                │  │
│  │  │ Connect to app   │                                              │  │
│  │  └────────┬─────────┘                                              │  │
│  │           │                                                         │  │
│  │           ▼                                                         │  │
│  │  Step 2: Capture UI Structure                                      │  │
│  │  ┌──────────────────┐                                              │  │
│  │  │ Traverse UI Tree │  ───→  Save to ui_debug.json                 │  │
│  │  │ Get all elements │                                              │  │
│  │  └────────┬─────────┘                                              │  │
│  │           │                                                         │  │
│  │           ▼                                                         │  │
│  │  Step 3: AI Field Mapping                                          │  │
│  │  ┌──────────────────┐                                              │  │
│  │  │ Send to AI:      │                                              │  │
│  │  │ - UI structure   │  ───→  OpenAI GPT-4                          │  │
│  │  │ - W2 data        │  ───→  or Anthropic Claude                   │  │
│  │  └────────┬─────────┘                                              │  │
│  │           │                                                         │  │
│  │           ▼                                                         │  │
│  │  ┌──────────────────┐                                              │  │
│  │  │ AI Response:     │  ───→  Save to ai_mapping.json               │  │
│  │  │ Field mappings   │                                              │  │
│  │  └────────┬─────────┘                                              │  │
│  │           │                                                         │  │
│  │           ▼                                                         │  │
│  │  Step 4: Fill Form                                                 │  │
│  │  ┌──────────────────┐                                              │  │
│  │  │ For each mapping:│                                              │  │
│  │  │ - Find element   │                                              │  │
│  │  │ - Focus field    │                                              │  │
│  │  │ - Set value      │  ───→  ProSeries W2 Form                     │  │
│  │  │ - Verify         │                                              │  │
│  │  └──────────────────┘                                              │  │
│  │                                                                     │  │
│  └─────────────────────────────────────────────────────────────────────┘  │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
                             │
                             ▼
                    ┌────────────────────────┐
                    │   Filled W2 Form       │
                    │   in ProSeries         │
                    └────────────────────────┘


═══════════════════════════════════════════════════════════════════════════════
                              SUPPORTING TOOLS
═══════════════════════════════════════════════════════════════════════════════

┌─────────────────────────┐      ┌─────────────────────────┐
│   ui_inspector.py       │      │   batch_filler.py       │
│                         │      │                         │
│  - Test connection      │      │  - Process CSV          │
│  - View UI elements     │      │  - Multiple W2s         │
│  - Debug accessibility  │      │  - Auto-navigation      │
│  - Export structure     │      │  - Progress tracking    │
└─────────────────────────┘      └─────────────────────────┘


═══════════════════════════════════════════════════════════════════════════════
                            DATA FLOW EXAMPLE
═══════════════════════════════════════════════════════════════════════════════

INPUT (sample_w2.json):
{
  "employee_name": "John Doe",
  "employee_ssn": "123-45-6789",
  "wages": "75000.00",
  ...
}
          │
          ▼
CAPTURED UI STRUCTURE:
{
  "role": "AXTextField",
  "title": "Employee Name",
  "identifier": "emp_name_field",
  ...
}
          │
          ▼
AI MAPPING:
{
  "data_field": "employee_name",
  "ui_title": "Employee Name",
  "confidence": "high"
}
          │
          ▼
AUTOMATION ACTION:
element.AXValue = "John Doe"
          │
          ▼
RESULT:
✓ Field filled successfully


═══════════════════════════════════════════════════════════════════════════════
                         TECHNOLOGY STACK
═══════════════════════════════════════════════════════════════════════════════

┌──────────────────┐
│   Python 3.9+    │  Core Language
└────────┬─────────┘
         │
    ┌────┴────┬────────────┬──────────────┬──────────────┐
    │         │            │              │              │
    ▼         ▼            ▼              ▼              ▼
┌────────┐ ┌──────┐  ┌─────────┐  ┌──────────┐  ┌─────────┐
│atomacos│ │OpenAI│  │Anthropic│  │ pydantic │  │ dotenv  │
│        │ │  or  │  │         │  │          │  │         │
│macOS   │ │GPT-4 │  │ Claude  │  │Validation│  │ Config  │
│Access  │ │      │  │         │  │          │  │         │
└────────┘ └──────┘  └─────────┘  └──────────┘  └─────────┘


═══════════════════════════════════════════════════════════════════════════════
                         FILE DEPENDENCIES
═══════════════════════════════════════════════════════════════════════════════

requirements.txt
     │
     ├──→ atomacos (UI automation)
     ├──→ openai (AI provider 1)
     ├──→ anthropic (AI provider 2)
     ├──→ pydantic (data validation)
     └──→ python-dotenv (config)

.env
     │
     └──→ API_KEYS, CONFIG

w2_data_handler.py
     │
     ├──→ Validates W2 data
     └──→ Used by ai_form_filler.py

ai_form_filler.py
     │
     ├──→ Uses w2_data_handler
     ├──→ Uses atomacos
     ├──→ Calls AI APIs
     └──→ Used by batch_filler.py

batch_filler.py
     │
     ├──→ Uses ai_form_filler
     └──→ Uses w2_data_handler

ui_inspector.py
     │
     └──→ Standalone debugging tool
