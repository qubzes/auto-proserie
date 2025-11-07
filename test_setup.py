"""
Quick test script to verify the automation setup
Run this before using the full automation
"""

import os
import sys
from dotenv import load_dotenv

def test_imports():
    """Test if all required packages are installed"""
    print("Testing imports...")
    
    try:
        import pywinauto
        print("✓ pywinauto installed")
    except ImportError:
        print("✗ pywinauto not installed")
        return False
    
    try:
        import google.generativeai as genai
        print("✓ google-generativeai installed")
    except ImportError:
        print("✗ google-generativeai not installed")
        return False
    
    try:
        import pandas
        print("✓ pandas installed")
    except ImportError:
        print("✗ pandas not installed")
        return False
    
    try:
        import psutil
        print("✓ psutil installed")
    except ImportError:
        print("✗ psutil not installed")
        return False
    
    return True


def test_environment():
    """Test if environment is configured correctly"""
    print("\nTesting environment...")
    
    load_dotenv()
    
    api_key = os.getenv('GOOGLE_API_KEY')
    if not api_key or api_key == 'your_google_api_key_here':
        print("✗ GOOGLE_API_KEY not configured in .env")
        return False
    else:
        print("✓ GOOGLE_API_KEY found in .env")
    
    model = os.getenv('GEMINI_MODEL', 'gemini-2.0-flash-exp')
    print(f"✓ Using model: {model}")
    
    return True


def test_gemini_api():
    """Test Gemini API connection"""
    print("\nTesting Gemini API...")
    
    try:
        import google.generativeai as genai
        load_dotenv()
        
        api_key = os.getenv('GOOGLE_API_KEY')
        genai.configure(api_key=api_key)
        
        model = genai.GenerativeModel('gemini-2.0-flash-exp')
        response = model.generate_content("Say 'API test successful' if you can read this.")
        
        if response and response.text:
            print(f"✓ Gemini API is working!")
            print(f"  Response: {response.text[:50]}...")
            return True
        else:
            print("✗ Gemini API returned empty response")
            return False
            
    except Exception as e:
        print(f"✗ Gemini API test failed: {str(e)}")
        return False


def test_proseries_detection():
    """Test ProSeries process detection"""
    print("\nTesting ProSeries detection...")
    
    try:
        import psutil
        
        proseries_names = [
            'ProSeries.exe', 
            'ProSeriesBasic.exe', 
            'ProSeriesProfessional.exe',
            'TaxWise.exe'
        ]
        
        found = False
        for proc in psutil.process_iter(['pid', 'name']):
            try:
                proc_name = proc.info['name']
                if any(name.lower() in proc_name.lower() for name in proseries_names):
                    print(f"✓ Found ProSeries: {proc_name} (PID: {proc.info['pid']})")
                    found = True
                    break
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                pass
        
        if not found:
            print("✗ ProSeries not detected")
            print("  Please start ProSeries before running the automation")
            return False
        
        return True
        
    except Exception as e:
        print(f"✗ Process detection failed: {str(e)}")
        return False


def test_data_files():
    """Test if sample data files exist"""
    print("\nTesting data files...")
    
    if os.path.exists('sample_w2_data.json'):
        print("✓ sample_w2_data.json exists")
        return True
    else:
        print("ℹ sample_w2_data.json not found")
        print("  Run: python run_automation.py --generate-sample sample_w2_data.json")
        return True  # Not critical


def main():
    """Run all tests"""
    print("="*60)
    print("ProSeries W2 Automation - Setup Test")
    print("="*60)
    print()
    
    results = []
    
    # Run tests
    results.append(("Imports", test_imports()))
    results.append(("Environment", test_environment()))
    results.append(("Gemini API", test_gemini_api()))
    results.append(("ProSeries Detection", test_proseries_detection()))
    results.append(("Data Files", test_data_files()))
    
    # Summary
    print("\n" + "="*60)
    print("TEST SUMMARY")
    print("="*60)
    
    for test_name, passed in results:
        status = "✓ PASS" if passed else "✗ FAIL"
        print(f"{status} - {test_name}")
    
    all_passed = all(result[1] for result in results[:4])  # Skip data files check
    
    print("\n" + "="*60)
    if all_passed:
        print("✓ ALL TESTS PASSED!")
        print("\nYou're ready to run the automation:")
        print("  python run_automation.py --json your_w2_data.json")
    else:
        print("✗ SOME TESTS FAILED")
        print("\nPlease fix the issues above before running the automation.")
        print("\nSetup instructions:")
        print("  1. Install requirements: pip install -r requirements.txt")
        print("  2. Create .env file: copy .env.example .env")
        print("  3. Add your Google API key to .env")
        print("  4. Start ProSeries application")
    print("="*60)
    
    return 0 if all_passed else 1


if __name__ == "__main__":
    sys.exit(main())
