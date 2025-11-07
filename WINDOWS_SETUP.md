# Windows Installation and Usage Guide

## Quick Start for Windows Users

### Step 1: Install Python

1. Download Python 3.8 or later from [python.org](https://www.python.org/downloads/)
2. During installation, **CHECK** "Add Python to PATH"
3. Verify installation by opening Command Prompt and typing:
   ```cmd
   python --version
   ```

### Step 2: Set Up the Project

1. Extract the project files to a folder (e.g., `C:\ProSeriesAutomation`)
2. Open Command Prompt and navigate to the folder:
   ```cmd
   cd C:\ProSeriesAutomation
   ```

3. Install required packages:
   ```cmd
   pip install -r requirements.txt
   ```

### Step 3: Configure API Key

1. Copy `.env.example` to `.env`:
   ```cmd
   copy .env.example .env
   ```

2. Open `.env` in Notepad:
   ```cmd
   notepad .env
   ```

3. Replace `your_google_api_key_here` with your actual Google API key
4. Save and close Notepad

### Step 4: Get Google API Key

1. Go to [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Sign in with your Google account
3. Click "Create API Key"
4. Copy the key and paste it in your `.env` file

### Step 5: Test the Setup

Run the test script to verify everything is working:

```cmd
python test_setup.py
```

This will check:
- ✓ All required packages are installed
- ✓ API key is configured
- ✓ Gemini API is accessible
- ✓ ProSeries is running

### Step 6: Prepare Your W2 Data

Generate a sample data file:

```cmd
python run_automation.py --generate-sample my_w2_data.json
```

Edit `my_w2_data.json` with your actual W2 information using Notepad or any text editor.

### Step 7: Run the Automation

1. **Start ProSeries** application
2. **Open the W2 form** you want to fill
3. Run the automation:
   ```cmd
   python run_automation.py --json my_w2_data.json
   ```

## Alternative: Use the Batch File

Double-click `setup_and_run.bat` to automatically:
- Check if Python is installed
- Install required packages
- Verify .env file exists
- Show usage instructions

## Troubleshooting on Windows

### Error: "Python is not recognized"

- Reinstall Python and check "Add Python to PATH"
- Or manually add Python to PATH:
  1. Search "Environment Variables" in Windows
  2. Edit PATH variable
  3. Add Python installation directory (e.g., `C:\Python39\`)

### Error: "pip is not recognized"

Try using `python -m pip` instead:
```cmd
python -m pip install -r requirements.txt
```

### Error: "ProSeries not detected"

- Make sure ProSeries is running
- Try running Command Prompt as Administrator
- Check Task Manager to confirm ProSeries.exe is running

### Error: "Access Denied"

- Run Command Prompt as Administrator
- Check Windows security settings
- Ensure UI Automation is enabled in Windows

### Error: "Failed to fill form fields"

- Ensure the W2 form is the active window in ProSeries
- Don't click or type while automation is running
- Check `proseries_automation.log` for detailed error messages

## File Formats Supported

### JSON Format
```json
[
  {
    "employee_name": "John Smith",
    "employee_ssn": "123-45-6789",
    "wages": "75000.00",
    ...
  }
]
```

### Excel Format
Create an Excel file with columns:
- employee_name
- employee_ssn
- employer_name
- wages
- federal_tax_withheld
- etc.

Use command:
```cmd
python run_automation.py --excel my_w2_data.xlsx
```

### CSV Format
Create a CSV file with the same columns as Excel.

Use command:
```cmd
python run_automation.py --csv my_w2_data.csv
```

## Advanced Usage

### Validate Data Without Filling
```cmd
python run_automation.py --json my_w2_data.json --validate-only
```

### Use Different Gemini Model
```cmd
python run_automation.py --json my_w2_data.json --model gemini-pro
```

### Process Multiple W2 Forms
Put multiple records in your JSON file:
```json
[
  {"employee_name": "John Smith", ...},
  {"employee_name": "Jane Doe", ...},
  {"employee_name": "Bob Johnson", ...}
]
```

## Logs and Debugging

Check `proseries_automation.log` for detailed information about:
- What actions were taken
- Any errors encountered
- UI elements found
- API responses

## Security Best Practices

1. Never share your `.env` file
2. Store W2 data files securely
3. Delete data files after use if they contain sensitive information
4. Review filled forms manually before submission

## Getting Help

If you encounter issues:

1. Run `python test_setup.py` to diagnose problems
2. Check `proseries_automation.log` for error messages
3. Ensure all prerequisites are met
4. Verify your W2 data format matches the examples

---

**Windows 10/11 Compatible** | **Python 3.8+** | **ProSeries Professional**
