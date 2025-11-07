#!/bin/bash

# Quick test script to verify Gemini integration

echo "======================================================"
echo "Testing Gemini API Connection"
echo "======================================================"
echo ""

# Check if .env exists
if [ ! -f .env ]; then
    echo "❌ .env file not found"
    echo "Run: cp .env.example .env"
    echo "Then add your Google API key"
    exit 1
fi

# Check if API key is set
if ! grep -q "GOOGLE_API_KEY=AIza" .env 2>/dev/null; then
    echo "❌ Google API key not configured in .env"
    echo ""
    echo "To fix:"
    echo "1. Get your key from: https://makersuite.google.com/app/apikey"
    echo "2. Edit .env and add: GOOGLE_API_KEY=your-key-here"
    exit 1
fi

echo "✓ .env file found"
echo "✓ API key configured"
echo ""

# Test Python and dependencies
echo "Testing Python dependencies..."

python3 << 'EOF'
import sys
import os

try:
    # Load environment
    from dotenv import load_dotenv
    load_dotenv()
    print("✓ python-dotenv installed")
    
    # Test Gemini import
    import google.generativeai as genai
    print("✓ google-generativeai installed")
    
    # Test API key
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key or not api_key.startswith("AIza"):
        print("❌ Invalid API key format")
        sys.exit(1)
    
    print("✓ API key format valid")
    
    # Test API connection
    print("\nTesting Gemini API connection...")
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel("gemini-2.0-flash-exp")
    
    # Simple test prompt
    response = model.generate_content(
        "Reply with just: OK",
        generation_config=genai.GenerationConfig(
            temperature=0.1,
            max_output_tokens=10,
        )
    )
    
    print(f"✓ API connection successful!")
    print(f"  Response: {response.text.strip()}")
    print("\n✅ All tests passed! Your Gemini integration is working.")
    
except ImportError as e:
    print(f"❌ Missing dependency: {e}")
    print("\nRun: pip install -r requirements.txt")
    sys.exit(1)
except Exception as e:
    print(f"❌ Error: {e}")
    print("\nCheck:")
    print("1. Your API key is correct")
    print("2. You have internet connection")
    print("3. Gemini API is enabled in Google Cloud")
    sys.exit(1)
EOF

if [ $? -eq 0 ]; then
    echo ""
    echo "======================================================"
    echo "🎉 Ready to automate W2 forms!"
    echo "======================================================"
    echo ""
    echo "Try:"
    echo "  python ui_inspector.py     # Inspect ProSeries UI"
    echo "  python ai_form_filler.py   # Fill a W2 form"
fi
