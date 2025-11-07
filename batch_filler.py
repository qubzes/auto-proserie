#!/usr/bin/env python3
"""
Batch W2 Form Filler

Process multiple W2 forms from a CSV file automatically.
"""

import sys
import time
from pathlib import Path

from ai_form_filler import AIFormAutomation
from w2_data_handler import W2DataLoader


def batch_fill_forms(csv_file: str, app_name: str = "ProSeries", delay: int = 5):
    """
    Fill multiple W2 forms from a CSV file.
    
    Args:
        csv_file: Path to CSV file with W2 data
        app_name: Name of the desktop application
        delay: Seconds to wait between forms (for manual navigation)
    """
    print("=" * 60)
    print("Batch W2 Form Filler")
    print("=" * 60)
    print()
    
    # Load W2 data from CSV
    print(f"📂 Loading W2 data from {csv_file}...")
    try:
        w2_records = W2DataLoader.from_csv(csv_file)
        print(f"✓ Loaded {len(w2_records)} W2 records\n")
    except Exception as e:
        print(f"✗ Failed to load CSV: {e}")
        return
    
    # Initialize automation
    automation = AIFormAutomation(app_name)
    
    if not automation.connect_to_app():
        print(f"\n⚠️  Could not connect to {app_name}")
        print("\nMake sure:")
        print(f"1. {app_name} is running")
        print("2. A blank W2 form is open")
        print("3. Accessibility permissions are granted")
        return
    
    # Process each W2
    for i, w2_data in enumerate(w2_records, 1):
        print(f"\n{'='*60}")
        print(f"Processing W2 {i}/{len(w2_records)}")
        print(f"Employee: {w2_data.employee_name}")
        print(f"Employer: {w2_data.employer_name}")
        print(f"{'='*60}\n")
        
        # Fill the form
        success = automation.fill_form(w2_data.to_dict())
        
        if success:
            print(f"\n✓ W2 {i} completed successfully!")
        else:
            print(f"\n⚠️  W2 {i} had issues. Review the form.")
        
        # Wait for next form (unless it's the last one)
        if i < len(w2_records):
            print(f"\n⏳ Waiting {delay} seconds...")
            print("   Please navigate to the next blank W2 form.")
            print("   (Press Ctrl+C to stop)")
            
            try:
                time.sleep(delay)
            except KeyboardInterrupt:
                print("\n\n⚠️  Batch processing interrupted by user.")
                print(f"   Processed {i}/{len(w2_records)} forms.")
                break
    
    print(f"\n{'='*60}")
    print("✓ Batch processing complete!")
    print(f"{'='*60}\n")


def interactive_mode():
    """Run in interactive mode with user prompts."""
    print("=" * 60)
    print("Batch W2 Form Filler - Interactive Mode")
    print("=" * 60)
    print()
    
    # Get CSV file
    csv_file = input("Enter path to CSV file (default: sample_w2.csv): ").strip()
    if not csv_file:
        csv_file = "sample_w2.csv"
    
    if not Path(csv_file).exists():
        print(f"\n✗ File not found: {csv_file}")
        print("\nTo create a sample CSV, run:")
        print("  python w2_data_handler.py")
        return
    
    # Get app name
    app_name = input("Enter application name (default: ProSeries): ").strip()
    if not app_name:
        app_name = "ProSeries"
    
    # Get delay
    delay_input = input("Seconds between forms (default: 5): ").strip()
    try:
        delay = int(delay_input) if delay_input else 5
    except ValueError:
        delay = 5
    
    print("\n✓ Configuration:")
    print(f"  CSV File: {csv_file}")
    print(f"  Application: {app_name}")
    print(f"  Delay: {delay} seconds")
    
    input("\nPress ENTER to start batch processing...")
    
    batch_fill_forms(csv_file, app_name, delay)


def main():
    """Main entry point."""
    if len(sys.argv) > 1:
        # Command line mode
        csv_file = sys.argv[1]
        app_name = sys.argv[2] if len(sys.argv) > 2 else "ProSeries"
        delay = int(sys.argv[3]) if len(sys.argv) > 3 else 5
        
        batch_fill_forms(csv_file, app_name, delay)
    else:
        # Interactive mode
        interactive_mode()


if __name__ == "__main__":
    main()
