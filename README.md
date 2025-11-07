# ProSeries W2 Form Automation with AI

**Automate W2 form filling in ProSeries desktop application using Gemini AI and Windows UI Automation**

This project provides an intelligent automation solution for filling W2 forms in the ProSeries tax preparation software. It uses Google's Gemini AI to understand the form structure and Windows UI Automation to interact with the desktop application.

## 🌟 Features

- **AI-Powered Form Recognition**: Uses Gemini 2.0 Flash to intelligently identify and fill form fields
- **Windows UI Automation**: Leverages `pywinauto` for reliable desktop app interaction
- **Multiple Input Formats**: Supports JSON, Excel, and CSV data files
- **Batch Processing**: Fill multiple W2 forms automatically
- **Data Validation**: Validates W2 data before processing
- **Comprehensive Logging**: Detailed logs for troubleshooting
- **Flexible Configuration**: Easy to configure via environment variables

## 📋 Prerequisites

- **Windows OS** (Windows 10 or later recommended)
- **Python 3.8+** installed
- **ProSeries** tax software installed and running
- **Google API Key** with Gemini API access

## 🚀 Installation

### Step 1: Clone or Download This Project

```bash
cd /path/to/auto-proseries
```

### Step 2: Install Python Dependencies

```bash
pip install -r requirements.txt
```

### Step 3: Set Up Environment Variables

1. Copy the `.env.example` file to `.env`:
   ```bash
   copy .env.example .env
   ```

2. Edit `.env` and add your Google API key:
   ```
   GOOGLE_API_KEY=your_actual_api_key_here
   GEMINI_MODEL=gemini-2.0-flash-exp
   ```

### Step 4: Get Your Google API Key

1. Go to [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Create a new API key
3. Copy the key to your `.env` file

## 📖 Usage

### Basic Usage

1. **Start ProSeries** application on your Windows machine
2. **Navigate to the W2 form** section
3. **Prepare your W2 data** in JSON, Excel, or CSV format
4. **Run the automation**:

```bash
python run_automation.py --json sample_w2_data.json
```

### Generate Sample Data

Create a sample W2 data file to get started:

```bash
python run_automation.py --generate-sample my_w2_data.json
```

This creates a JSON file with example W2 data that you can edit with your actual information.

### Command-Line Options

```bash
# Fill from JSON file
python run_automation.py --json w2_data.json

# Fill from Excel file
python run_automation.py --excel w2_data.xlsx --sheet "W2 Data"

# Fill from CSV file
python run_automation.py --csv w2_data.csv

# Use a specific Gemini model
python run_automation.py --json w2_data.json --model gemini-2.0-flash-exp

# Validate data without filling forms
python run_automation.py --json w2_data.json --validate-only

# Provide API key via command line
python run_automation.py --json w2_data.json --api-key YOUR_API_KEY
```

## 📝 W2 Data Format

### JSON Format

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

### Excel Format

Create an Excel file with a sheet named "W2 Data" and columns matching the JSON field names:

| employee_name | employee_ssn | employer_name | employer_ein | wages | federal_tax_withheld | ... |
|---------------|--------------|---------------|--------------|-------|----------------------|-----|
| John Smith    | 123-45-6789  | ABC Corp      | 12-3456789   | 75000 | 12500                | ... |

### CSV Format

Similar to Excel, create a CSV file with headers matching the field names.

## 🔧 How It Works

1. **Process Detection**: The script detects the running ProSeries application
2. **UI Extraction**: Extracts the UI structure using Windows UI Automation API
3. **AI Analysis**: Sends the UI structure to Gemini AI along with W2 data
4. **Action Generation**: Gemini generates a sequence of actions to fill the form
5. **Execution**: The script executes the actions to fill the form fields
6. **Verification**: Logs all actions and results for verification

## 📊 Required W2 Fields

The following fields are required for each W2 record:

- `employee_name` - Employee's full name
- `employee_ssn` - Employee's Social Security Number
- `employer_name` - Employer's legal name
- `employer_ein` - Employer Identification Number
- `wages` - Total wages, tips, other compensation
- `federal_tax_withheld` - Federal income tax withheld

## 🎯 Optional W2 Fields

Additional fields you can include:

- Employee address information (address, city, state, zip)
- Employer address information
- `social_security_wages` and `social_security_tax`
- `medicare_wages` and `medicare_tax`
- `social_security_tips`
- `allocated_tips`
- `dependent_care_benefits`
- `nonqualified_plans`
- State and local tax information

## 🐛 Troubleshooting

### ProSeries Not Detected

- Ensure ProSeries is running before starting the automation
- Check if the process name matches (the script looks for ProSeries.exe, ProSeriesBasic.exe, etc.)
- Try starting ProSeries as Administrator

### Form Fields Not Filled

- Check the logs in `proseries_automation.log`
- The W2 form must be the active/focused window
- Ensure field names in your data match what ProSeries expects
- Try adjusting the wait times in the script

### API Errors

- Verify your Google API key is valid
- Check you have Gemini API access enabled
- Ensure you haven't exceeded API rate limits

### UI Automation Issues

- Make sure Windows UI Automation is enabled
- Run the script as Administrator if needed
- Close any dialogs or pop-ups in ProSeries

## 📁 Project Structure

```
auto-proseries/
├── proseries_w2_automation.py   # Main automation script
├── w2_data_handler.py            # W2 data loading and validation
├── run_automation.py             # CLI interface
├── requirements.txt              # Python dependencies
├── .env.example                  # Environment variables template
├── sample_w2_data.json          # Sample W2 data
├── README.md                     # This file
└── proseries_automation.log      # Log file (created when running)
```

## 🔐 Security Notes

- **Never commit your `.env` file** with real API keys
- Store sensitive W2 data securely
- Review logs before sharing (they may contain sensitive information)
- Use strong access controls on files containing W2 data

## ⚠️ Important Disclaimers

1. **Test First**: Always test with sample data before using with real W2 information
2. **Verify Data**: Manually verify filled forms before submission
3. **Backup**: Keep backups of your original data
4. **Compliance**: Ensure your use complies with ProSeries license terms
5. **No Warranty**: This tool is provided as-is without warranty

## 🤝 Support

For issues or questions:

1. Check the log file: `proseries_automation.log`
2. Review the troubleshooting section above
3. Ensure all prerequisites are met
4. Verify your W2 data format matches the examples

## 📄 License

This project is provided for educational and automation purposes. Ensure compliance with all applicable software licenses and regulations.

## 🔄 Updates and Improvements

To improve the automation:

1. **Adjust UI traversal depth** in `get_ui_tree_structure()` if needed
2. **Customize field mappings** in the AI prompt
3. **Add retry logic** for failed actions
4. **Extend data validation** for specific business rules

## 💡 Tips for Best Results

1. **Clean Data**: Ensure W2 data is properly formatted
2. **Full Screen**: Run ProSeries in full screen for better UI detection
3. **Minimize Distractions**: Close unnecessary windows
4. **One Form at a Time**: Start with single forms before batch processing
5. **Monitor First Run**: Watch the first automation run to ensure it works correctly

---

**Built for Windows** | **Powered by Gemini AI** | **Uses Windows UI Automation**
