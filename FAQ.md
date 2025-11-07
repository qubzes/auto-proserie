# ProSeries W2 Automation - Frequently Asked Questions

## General Questions

### Q: What is this tool?
A: This is an AI-powered automation tool that fills W2 forms in the ProSeries desktop application. It uses Google's Gemini AI to understand the form structure and Windows UI Automation to interact with the application.

### Q: Is this safe to use?
A: The tool only interacts with the ProSeries application through standard Windows UI Automation APIs. However, you should:
- Test with sample data first
- Manually verify filled forms before submission
- Keep backups of your data
- Ensure compliance with ProSeries license terms

### Q: Does it work on Mac or Linux?
A: No, this tool is designed specifically for Windows as it uses Windows UI Automation APIs. ProSeries is also a Windows-only application.

## Setup Questions

### Q: Where do I get a Google API key?
A: 
1. Go to [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Sign in with your Google account
3. Click "Create API Key"
4. Copy and paste it into your `.env` file

### Q: Is the Google API free?
A: Gemini API has a free tier with generous limits. Check [Google AI pricing](https://ai.google.dev/pricing) for current details.

### Q: What Python version do I need?
A: Python 3.8 or later. We recommend Python 3.10 or 3.11 for best compatibility.

### Q: Installation fails with "permission denied"?
A: Try running Command Prompt as Administrator, or use:
```cmd
pip install --user -r requirements.txt
```

## Usage Questions

### Q: How do I know if ProSeries is detected?
A: Run `python test_setup.py` - it will tell you if ProSeries is detected. You can also check the log file after running the automation.

### Q: Can I fill multiple W2 forms at once?
A: Yes! Put multiple W2 records in your JSON/Excel/CSV file, and the automation will process them one by one.

### Q: How long does it take to fill one form?
A: Typically 10-30 seconds per form, depending on the number of fields and your computer speed.

### Q: What if the form has custom fields?
A: The AI attempts to map your data fields to whatever it finds in the ProSeries UI. For custom fields, you may need to add them to your data file with names similar to what appears in ProSeries.

## Troubleshooting Questions

### Q: "ProSeries not detected" - what do I do?
A: 
1. Make sure ProSeries is actually running
2. Check Task Manager to confirm ProSeries.exe is running
3. Try running as Administrator
4. The script looks for: ProSeries.exe, ProSeriesBasic.exe, ProSeriesProfessional.exe

### Q: Forms aren't being filled correctly?
A:
1. Ensure the W2 form is the active window (click on it)
2. Don't use your mouse/keyboard during automation
3. Check the log file for specific errors
4. Make sure field names in your data roughly match ProSeries labels
5. Try increasing wait times in the code if fields are skipped

### Q: API errors - what do they mean?
A:
- "Invalid API key" - Check your `.env` file
- "Rate limit exceeded" - Wait a few minutes, you've hit API limits
- "Model not found" - Check the model name in your `.env` file
- "Network error" - Check your internet connection

### Q: Can I run this on a remote desktop?
A: Yes, but UI Automation can be slower on RDP. Make sure you have a stable connection.

### Q: The script stops with an error mid-way?
A: Check `proseries_automation.log` for details. Common causes:
- ProSeries dialog boxes popped up
- ProSeries window lost focus
- Network interruption (for API calls)
- Invalid data format

## Data Questions

### Q: What fields are required?
A: Minimum required fields:
- employee_name
- employee_ssn
- employer_name
- employer_ein
- wages
- federal_tax_withheld

### Q: How do I format SSN and EIN?
A: The tool automatically formats them:
- SSN: XXX-XX-XXXX
- EIN: XX-XXXXXXX

You can enter them with or without dashes.

### Q: Can I use Excel instead of JSON?
A: Yes! Create an Excel file with column headers matching the field names:
```cmd
python run_automation.py --excel my_data.xlsx
```

### Q: How do I handle Box 12 codes?
A: Add a field like:
```json
"box_12_codes": [
  {"code": "D", "amount": "5000.00"},
  {"code": "DD", "amount": "2500.00"}
]
```

### Q: What about state and local taxes?
A: Include these fields in your data:
```json
"state": "NY",
"state_wages": "75000.00",
"state_tax": "4500.00",
"locality_name": "New York City",
"local_wages": "75000.00",
"local_tax": "2100.00"
```

## Performance Questions

### Q: Can I speed up the automation?
A: You can reduce wait times in the code, but be careful - too fast may cause fields to be skipped. The current timing is optimized for reliability.

### Q: How many W2s can I process in one run?
A: There's no hard limit, but we recommend batches of 50-100 at a time for manageability.

### Q: Does it work with ProSeries Basic?
A: It should work with all ProSeries versions (Basic, Professional, etc.) as long as they use standard Windows UI controls.

## Security Questions

### Q: Is my API key secure?
A: Your API key stays in your local `.env` file and is never shared. Make sure to:
- Never commit `.env` to version control
- Don't share screenshots of your `.env` file
- Keep file permissions restrictive

### Q: What happens to my W2 data?
A: Your W2 data:
- Is sent to Google's Gemini API for generating fill actions
- Is logged locally in `proseries_automation.log`
- Is never stored by this tool beyond the session

### Q: Can I use this for client data?
A: Check with your compliance/legal team. Consider:
- Google's data handling policies
- Your client agreements
- Professional liability insurance coverage
- Applicable privacy laws (HIPAA, GDPR, etc.)

## Advanced Questions

### Q: Can I customize the AI prompt?
A: Yes! Edit the `ask_gemini_for_actions()` method in `proseries_w2_automation.py` to modify how the AI interprets the form.

### Q: Can I add custom field mappings?
A: Yes, you can modify the prompt to include specific field mapping rules for your ProSeries setup.

### Q: Can I use a different AI model?
A: Yes, change the `GEMINI_MODEL` in your `.env` file to any supported Gemini model:
- gemini-2.0-flash-exp (default, fastest)
- gemini-pro
- gemini-pro-vision

### Q: Can I integrate this with my accounting software?
A: Yes! The `W2DataHandler` class can be extended to read from databases or APIs. You would need to write a custom data loader.

### Q: Can I add screenshots to help the AI?
A: The current version uses UI tree structure. You could extend it to capture and send screenshots to vision-capable models, though this would increase API costs.

## Error Messages

### "Module not found: pywinauto"
```cmd
pip install pywinauto
```

### "Google API key not found"
Create/edit your `.env` file and add:
```
GOOGLE_API_KEY=your_actual_key_here
```

### "Failed to connect to ProSeries"
1. Start ProSeries
2. Make sure it's not minimized
3. Try running as Administrator

### "Element not found"
The UI structure doesn't match what the AI expected. Check the log to see what elements were found.

### "JSON decode error"
Your data file has invalid JSON syntax. Use a JSON validator or check for:
- Missing commas
- Unmatched brackets
- Unescaped quotes

## Still Need Help?

1. Run `python test_setup.py` to diagnose issues
2. Check `proseries_automation.log` for detailed error messages
3. Review the README.md and WINDOWS_SETUP.md
4. Ensure your data format matches the examples
5. Try with the included `sample_w2_data.json` first

---

**Updated:** November 2025 | **Version:** 1.0
