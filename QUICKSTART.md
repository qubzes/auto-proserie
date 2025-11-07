# Quick Start Guide

## Setup (5 minutes)

### 1. Install Dependencies
```bash
cd trustlelab
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 2. Configure API Key
```bash
cp .env.example .env
# Edit .env and add your Google API key
# Get it from: https://makersuite.google.com/app/apikey
```

### 3. Grant Accessibility Permissions
1. **System Preferences** → **Security & Privacy** → **Privacy** → **Accessibility**
2. Click 🔒 to unlock
3. Add **Terminal** (or your IDE)
4. Restart Terminal

## Basic Usage

### Test Connection
```bash
# Open ProSeries first, then:
python ui_inspector.py
# Enter "ProSeries" when prompted
# Choose option 2 to see all text fields
```

### Fill a Single W2
```bash
# 1. Generate sample data
python w2_data_handler.py

# 2. Edit sample_w2.json with your data

# 3. Open ProSeries to a blank W2 form

# 4. Run automation
python ai_form_filler.py
```

### Fill Multiple W2s (Batch)
```bash
# 1. Edit sample_w2.csv with your data

# 2. Open ProSeries to first blank W2 form

# 3. Run batch processor
python batch_filler.py sample_w2.csv
```

## Troubleshooting

**Can't connect?**
- Make sure ProSeries is running
- Check accessibility permissions
- Try restarting Terminal

**Fields not filling?**
- Make sure the W2 form is open and visible
- Check ui_debug.json to see what was captured
- Some fields may require clicking/focusing first

**API errors?**
- Verify your GOOGLE_API_KEY in .env
- Get a key from https://makersuite.google.com/app/apikey
- Check you have API access enabled

## Tips

- Start with sample data to test
- Keep ProSeries in focus during automation
- Review ai_mapping.json to see AI's decisions
- Adjust delay in batch_filler.py if needed
