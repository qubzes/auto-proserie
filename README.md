# AI-Powered Desktop Form Automation for ProSeries W2

> Automate W2 form filling in ProSeries (or any desktop tax software) using AI to intelligently understand and interact with the desktop application UI.

## 🎯 Overview

This project solves the problem of automating desktop applications that can't be automated with traditional web scraping. Instead of using fragile tab/selector methods, it uses:

1. **macOS Accessibility APIs** - To read the desktop app's UI structure (like "inspecting HTML" but for desktop apps)
2. **Google Gemini 2.0 Flash** - AI to intelligently map your data to the correct form fields
3. **Smart Automation** - To fill forms accurately and handle complex UI patterns

## ✨ Key Features

- 🤖 **AI-Powered Field Mapping** - Google Gemini 2.0 Flash understands your forms
- 💰 **Cost-Effective** - ~$0.01 per W2 (10x cheaper than GPT-4)
- ⚡ **Fast** - Process forms in seconds with low latency
- 🔍 **UI Structure Inspector** - Examine desktop app UI like browser DevTools
- 📊 **Batch Processing** - Fill multiple W2s from CSV files
- ✅ **Data Validation** - Ensures SSN, EIN, and other fields are properly formatted
- 🎨 **Flexible** - Works with ProSeries, Lacerte, and other desktop apps
- 📝 **Detailed Logging** - See exactly what the AI is doing
- 🆓 **Generous Free Tier** - 1,500 requests/day free

## 🚀 Quick Start

### 2. Prerequisites

- macOS (required for Accessibility APIs)
- Python 3.9+
- Google API key (for Gemini)
- ProSeries (or target application) installed

### 2. Installation

```bash
# Clone or navigate to the project directory
cd trustlelab

# Create a virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 3. Configuration

```bash
# Copy the example environment file
cp .env.example .env

# Edit .env and add your API key
# Get your key from: https://makersuite.google.com/app/apikey
GOOGLE_API_KEY=your-google-api-key-here
```

### 4. Grant Accessibility Permissions

**Critical Step!** Your Python interpreter needs accessibility permissions:

1. Open **System Preferences** → **Security & Privacy** → **Privacy** → **Accessibility**
2. Click the lock 🔒 to make changes
3. Add **Terminal** (or your IDE like VS Code/PyCharm)
4. Restart Terminal/IDE after granting permissions

## 📖 Usage

### Inspect the UI (First Time)

Before automating, inspect the ProSeries UI to understand its structure:

```bash
python ui_inspector.py
```

When prompted:
1. Enter "ProSeries" as the application name
2. Choose option 2 to list all text fields
3. This helps you verify the app is accessible

### Generate Sample Data

Create sample W2 data files:

```bash
python w2_data_handler.py
```

This creates:
- `sample_w2.json` - Single W2 data
- `sample_w2.csv` - Multiple W2s for batch processing

### Fill W2 Forms

1. **Open ProSeries** and navigate to a blank W2 form
2. **Run the automation:**

```bash
python ai_form_filler.py
```

3. The script will:
   - Connect to ProSeries
   - Analyze the UI structure
   - Ask AI to map fields
   - Fill the form automatically

### Custom Data

Edit `sample_w2.json` with your data:

```json
{
  "employer_name": "Your Company",
  "employer_ein": "12-3456789",
  "employee_name": "Employee Name",
  "employee_ssn": "123-45-6789",
  "wages": "75000.00",
  "federal_tax_withheld": "9500.00",
  ...
}
```

## 🏗️ Project Structure

```
trustlelab/
├── ai_form_filler.py      # Main automation script with AI
├── ui_inspector.py        # Tool to inspect desktop app UI
├── w2_data_handler.py     # Data validation and loading
├── requirements.txt       # Python dependencies
├── .env.example          # Environment variables template
├── .env                  # Your API keys (git-ignored)
├── sample_w2.json        # Sample single W2 data
├── sample_w2.csv         # Sample batch W2 data
└── README.md             # This file
```

## 🔧 How It Works

### 1. UI Structure Capture

The script uses macOS Accessibility APIs (via `atomacos`) to read the UI structure:

```python
# Similar to browser DevTools, but for desktop apps
ui_structure = {
  "role": "AXTextField",
  "title": "Employee Name",
  "identifier": "employee_name_field",
  "position": {"x": 100, "y": 200}
}
```

### 2. AI Field Mapping

The UI structure is sent to Gemini 2.0 Flash:

```
"Here's the app UI structure and the W2 data. 
Map each data field to the correct UI element."
```

AI responds with intelligent mappings:

```json
{
  "mappings": [
    {
      "data_field": "employee_name",
      "ui_title": "Employee Name",
      "confidence": "high"
    }
  ]
}
```

### 3. Form Filling

The script uses the AI mapping to fill fields:

```python
element = find_element_by_criteria({"title": "Employee Name"})
element.AXValue = "John Doe"
```

## 🎓 Advanced Usage

### Using with Different Apps

The system works with any desktop application that supports Accessibility APIs:

```python
automation = AIFormAutomation("Lacerte")  # or "Drake", etc.
```

### Batch Processing

Process multiple W2s from CSV:

```python
from w2_data_handler import W2DataLoader

w2_records = W2DataLoader.from_csv("sample_w2.csv")
for w2_data in w2_records:
    automation.fill_form(w2_data.to_dict())
    # Wait for user to navigate to next form or automate that too
```

### Custom Field Mappings

If AI mapping isn't perfect, you can review and adjust:

```bash
# After running, check these files:
cat ui_debug.json       # See the full UI structure
cat ai_mapping.json     # See how AI mapped fields
```

### Debugging

Enable verbose logging:

```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

### Configuration Options

### Environment Variables

```bash
# Google API Key (required)
GOOGLE_API_KEY=your-api-key-here

# Model (default: gemini-2.0-flash-exp)
GEMINI_MODEL=gemini-2.0-flash-exp
```

### Customizing AI Behavior

Edit the prompt in `ai_form_filler.py` → `_create_mapping_prompt()` to adjust how AI understands your specific form.

## 🚨 Troubleshooting

### "Failed to connect to application"

**Solution:** 
1. Ensure the app is running
2. Check accessibility permissions (see step 4 above)
3. Try using the app's exact name as shown in the menu bar

### "AI could not create a mapping"

**Solution:**
1. Check `ui_debug.json` to see if UI structure was captured
2. Try opening the exact form/window you want to fill
3. Ensure your API key is valid and has credits

### Fields Not Filling Correctly

**Solution:**
1. Run `ui_inspector.py` to examine field properties
2. Check `ai_mapping.json` to see AI's confidence levels
3. Some fields may need manual interaction first (clicking tabs, etc.)

### Import Errors

**Solution:**
```bash
# Reinstall dependencies
pip install --upgrade -r requirements.txt

# For atomacos specifically (macOS only):
pip install atomacos pyobjc-framework-Cocoa pyobjc-framework-Quartz
```

## 🔐 Security Notes

- ⚠️ **Never commit `.env`** with real API keys (it's in `.gitignore`)
- 🔒 **SSN/Tax Data**: Keep `sample_w2.json` and CSV files secure
- 🛡️ **API Costs**: Gemini is very cost-effective (~$0.01 per W2)
- 👁️ **Screen Recording**: macOS may ask for screen recording permissions

## 🤝 Contributing

Ideas for improvements:
- [ ] Support for other tax forms (1099, W4, etc.)
- [ ] Windows support using UI Automation
- [ ] Visual verification (screenshot comparison)
- [ ] Web interface for easier configuration
- [ ] Docker containerization

## 📄 License

MIT License - feel free to modify and use for your own projects!

## 🙏 Acknowledgments

- Built with macOS Accessibility APIs
- Powered by Google Gemini 2.0 Flash
- Uses `atomacos` for UI automation

## 📞 Support

Having issues? 
1. Check the Troubleshooting section above
2. Review the debug files (`ui_debug.json`, `ai_mapping.json`)
3. Run `ui_inspector.py` to verify connectivity

---

**Made with ❤️ for tax professionals tired of manual data entry**
