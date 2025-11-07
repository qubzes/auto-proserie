# 🚀 Quick Start Guide - ProSeries W2 Automation

Get up and running in 5 minutes!

## Prerequisites Checklist

- [ ] Windows 10 or 11
- [ ] Python 3.8+ installed
- [ ] ProSeries tax software installed
- [ ] Google account (for API key)

## Installation (5 Steps)

### 1️⃣ Install Python Packages

Open Command Prompt in the project folder:

```cmd
pip install -r requirements.txt
```

### 2️⃣ Set Up API Key

Copy the example environment file:
```cmd
copy .env.example .env
```

Edit `.env` file and add your Google API key:
```
GOOGLE_API_KEY=your_actual_api_key_here
GEMINI_MODEL=gemini-2.0-flash-exp
```

**Get API Key Here:** https://makersuite.google.com/app/apikey

### 3️⃣ Test Your Setup

```cmd
python test_setup.py
```

This verifies:
- ✓ All packages installed
- ✓ API key configured
- ✓ Gemini API accessible
- ✓ ProSeries detected

### 4️⃣ Create Sample Data

```cmd
python run_automation.py --generate-sample my_w2_data.json
```

Edit `my_w2_data.json` with your actual W2 information.

### 5️⃣ Run the Automation

1. **Start ProSeries** and open a W2 form
2. Run the automation:

```cmd
python run_automation.py --json my_w2_data.json
```

## Basic Commands

```cmd
# Generate sample data
python run_automation.py --generate-sample sample.json

# Fill from JSON
python run_automation.py --json w2_data.json

# Fill from Excel
python run_automation.py --excel w2_data.xlsx

# Fill from CSV
python run_automation.py --csv w2_data.csv

# Validate data only (no filling)
python run_automation.py --json w2_data.json --validate-only

# Test your setup
python test_setup.py
```

## Sample W2 Data Structure

```json
[
  {
    "employee_name": "John Smith",
    "employee_ssn": "123-45-6789",
    "employee_address": "123 Main St",
    "employee_city": "New York",
    "employee_state": "NY",
    "employee_zip": "10001",
    "employer_name": "ABC Corporation",
    "employer_ein": "12-3456789",
    "employer_address": "456 Business Ave",
    "employer_city": "New York",
    "employer_state": "NY",
    "employer_zip": "10002",
    "wages": "75000.00",
    "federal_tax_withheld": "12500.00",
    "social_security_wages": "75000.00",
    "social_security_tax": "4650.00",
    "medicare_wages": "75000.00",
    "medicare_tax": "1087.50",
    "state": "NY",
    "state_wages": "75000.00",
    "state_tax": "4500.00"
  }
]
```

## Required Fields (Minimum)

- `employee_name`
- `employee_ssn`
- `employer_name`
- `employer_ein`
- `wages`
- `federal_tax_withheld`

## Common Issues & Fixes

### "Python not recognized"
→ Reinstall Python with "Add to PATH" checked

### "ProSeries not detected"
→ Make sure ProSeries is running
→ Try running Command Prompt as Administrator

### "API key not found"
→ Check your `.env` file exists
→ Verify `GOOGLE_API_KEY=` has your actual key (no spaces)

### "Fields not filled correctly"
→ Ensure W2 form is the active window
→ Don't touch mouse/keyboard during automation
→ Check `proseries_automation.log` for errors

## Tips for Success

1. ✅ **Test first** - Use sample data before real W2s
2. ✅ **One at a time** - Start with single forms, then batch
3. ✅ **Verify manually** - Always review filled forms
4. ✅ **Keep logs** - Check `proseries_automation.log` for issues
5. ✅ **Backup data** - Save your original W2 data files

## File Organization

```
auto-proseries/
├── proseries_w2_automation.py   ← Main automation engine
├── run_automation.py             ← Command-line interface
├── w2_data_handler.py            ← Data loading & validation
├── test_setup.py                 ← Setup verification tool
├── requirements.txt              ← Python dependencies
├── .env                          ← Your API key (create this)
├── .env.example                  ← Template for .env
├── sample_w2_data.json          ← Example W2 data
├── README.md                     ← Full documentation
├── WINDOWS_SETUP.md             ← Windows-specific guide
├── FAQ.md                        ← Frequently asked questions
└── proseries_automation.log      ← Generated when running
```

## What Happens When You Run?

1. 🔍 **Detects ProSeries** - Finds the running application
2. 📊 **Extracts UI Structure** - Maps all form fields
3. 🤖 **AI Analysis** - Gemini figures out how to fill the form
4. ⌨️ **Executes Actions** - Fills fields one by one
5. 📝 **Logs Everything** - Records all actions taken

## Need More Help?

- 📖 **Full docs:** `README.md`
- 💻 **Windows setup:** `WINDOWS_SETUP.md`
- ❓ **Common questions:** `FAQ.md`
- 📋 **Logs:** `proseries_automation.log`

## Support Resources

- Test your setup: `python test_setup.py`
- Generate sample: `python run_automation.py --generate-sample test.json`
- Validate data: `python run_automation.py --json data.json --validate-only`

---

**Ready? Start with:** `python test_setup.py`

Then: `python run_automation.py --generate-sample my_data.json`

Finally: `python run_automation.py --json my_data.json`

🎉 **That's it! You're automating W2 forms!**
