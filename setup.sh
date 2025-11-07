#!/bin/bash

# Setup script for AI-Powered Desktop Form Automation

echo "======================================================"
echo "AI-Powered W2 Form Automation Setup (Gemini)"
echo "======================================================"
echo ""

# Check Python version
echo "Checking Python version..."
python3 --version

if [ $? -ne 0 ]; then
    echo "❌ Python 3 is not installed. Please install Python 3.9 or higher."
    exit 1
fi

# Create virtual environment
echo ""
echo "Creating virtual environment..."
python3 -m venv venv

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Upgrade pip
echo ""
echo "Upgrading pip..."
pip install --upgrade pip

# Install dependencies
echo ""
echo "Installing dependencies..."
pip install -r requirements.txt

if [ $? -ne 0 ]; then
    echo ""
    echo "⚠️  Some dependencies failed to install."
    echo "This is common with atomacos. Try manually:"
    echo "  pip install atomacos"
    echo ""
fi

# Create .env file if it doesn't exist
if [ ! -f .env ]; then
    echo ""
    echo "Creating .env file..."
    cp .env.example .env
    echo "✓ Created .env file"
    echo ""
    echo "⚠️  IMPORTANT: Edit .env and add your Google API key!"
    echo "  Get it from: https://makersuite.google.com/app/apikey"
    echo "  nano .env"
    echo "  (or use any text editor)"
fi

# Generate sample data
echo ""
echo "Generating sample data files..."
python w2_data_handler.py

echo ""
echo "======================================================"
echo "✓ Setup Complete!"
echo "======================================================"
echo ""
echo "Next steps:"
echo "1. Edit .env and add your Google API key"
echo "   Get it from: https://makersuite.google.com/app/apikey"
echo "2. Grant Accessibility permissions:"
echo "   System Preferences → Security & Privacy → Privacy → Accessibility"
echo "   Add Terminal to the list"
echo "3. Test with: python ui_inspector.py"
echo ""
echo "See QUICKSTART.md for detailed usage instructions."
echo ""
