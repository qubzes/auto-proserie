"""
Command-line interface for ProSeries W2 automation
"""

import argparse
import sys
import os
from dotenv import load_dotenv
from proseries_w2_automation import ProSeriesW2Automation, logger
from w2_data_handler import W2DataHandler


def main():
    """Main CLI entry point"""
    parser = argparse.ArgumentParser(
        description='Automate W2 form filling in ProSeries using AI',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Fill W2 from JSON file
  python run_automation.py --json w2_data.json
  
  # Fill W2 from Excel file
  python run_automation.py --excel w2_data.xlsx
  
  # Fill W2 from CSV file
  python run_automation.py --csv w2_data.csv
  
  # Use specific Gemini model
  python run_automation.py --json w2_data.json --model gemini-2.0-flash-exp
  
  # Generate sample data file
  python run_automation.py --generate-sample sample_w2_data.json
        """
    )
    
    # Input source arguments
    input_group = parser.add_mutually_exclusive_group(required=True)
    input_group.add_argument(
        '--json',
        type=str,
        help='Path to JSON file containing W2 data'
    )
    input_group.add_argument(
        '--excel',
        type=str,
        help='Path to Excel file containing W2 data'
    )
    input_group.add_argument(
        '--csv',
        type=str,
        help='Path to CSV file containing W2 data'
    )
    input_group.add_argument(
        '--generate-sample',
        type=str,
        help='Generate sample W2 data file and exit'
    )
    
    # Optional arguments
    parser.add_argument(
        '--sheet',
        type=str,
        default='W2 Data',
        help='Sheet name for Excel file (default: W2 Data)'
    )
    parser.add_argument(
        '--model',
        type=str,
        help='Gemini model to use (overrides .env)'
    )
    parser.add_argument(
        '--api-key',
        type=str,
        help='Google API key (overrides .env)'
    )
    parser.add_argument(
        '--validate-only',
        action='store_true',
        help='Only validate W2 data without filling forms'
    )
    
    args = parser.parse_args()
    
    # Handle sample generation
    if args.generate_sample:
        generate_sample_file(args.generate_sample)
        return
    
    # Load environment variables
    load_dotenv()
    
    # Get API key
    api_key = args.api_key or os.getenv('GOOGLE_API_KEY')
    if not api_key:
        logger.error("Google API key not found!")
        logger.error("Set GOOGLE_API_KEY in .env file or use --api-key argument")
        sys.exit(1)
    
    # Get model name
    model_name = args.model or os.getenv('GEMINI_MODEL', 'gemini-2.0-flash-exp')
    
    # Load W2 data
    w2_data_list = load_w2_data(args)
    
    if not w2_data_list:
        logger.error("No W2 data loaded. Exiting.")
        sys.exit(1)
    
    logger.info(f"Loaded {len(w2_data_list)} W2 record(s)")
    
    # Validate data
    validation_results = W2DataHandler.validate_batch(w2_data_list)
    logger.info(f"Validation: {validation_results['valid']} valid, {validation_results['invalid']} invalid")
    
    if validation_results['invalid'] > 0:
        logger.warning("Invalid records found:")
        for error in validation_results['errors']:
            logger.warning(f"  Record {error['index']} ({error['employee']}): Missing {error['missing_fields']}")
        
        if validation_results['valid'] == 0:
            logger.error("No valid records to process. Exiting.")
            sys.exit(1)
    
    # If validate-only mode, exit here
    if args.validate_only:
        logger.info("Validation complete. Exiting (--validate-only mode)")
        sys.exit(0)
    
    # Clean the data
    w2_data_list = [W2DataHandler.clean_w2_data(w2) for w2 in w2_data_list]
    
    # Initialize automation
    logger.info(f"Initializing automation with model: {model_name}")
    automation = ProSeriesW2Automation(api_key, model_name)
    
    # Process W2 forms
    if len(w2_data_list) == 1:
        logger.info("Processing single W2 form...")
        success = automation.fill_w2_form(w2_data_list[0])
        
        if success:
            logger.info("✓ W2 form filled successfully!")
            sys.exit(0)
        else:
            logger.error("✗ Failed to fill W2 form")
            sys.exit(1)
    else:
        logger.info(f"Processing {len(w2_data_list)} W2 forms...")
        results = automation.fill_multiple_w2_forms(w2_data_list)
        
        logger.info(f"\n{'='*60}")
        logger.info(f"SUMMARY: {results['success']} successful, {results['failed']} failed")
        logger.info(f"{'='*60}\n")
        
        if results['failed'] > 0:
            sys.exit(1)
        else:
            sys.exit(0)


def load_w2_data(args) -> list:
    """Load W2 data from specified source"""
    if args.json:
        logger.info(f"Loading W2 data from JSON: {args.json}")
        return W2DataHandler.load_from_json(args.json)
    
    elif args.excel:
        logger.info(f"Loading W2 data from Excel: {args.excel}")
        return W2DataHandler.load_from_excel(args.excel, args.sheet)
    
    elif args.csv:
        logger.info(f"Loading W2 data from CSV: {args.csv}")
        return W2DataHandler.load_from_csv(args.csv)
    
    return []


def generate_sample_file(output_path: str):
    """Generate sample W2 data file"""
    import json
    from w2_data_handler import create_sample_w2_data
    
    sample_data = create_sample_w2_data()
    
    try:
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(sample_data, f, indent=2)
        
        logger.info(f"✓ Sample W2 data generated: {output_path}")
        logger.info(f"  Contains {len(sample_data)} sample records")
        logger.info(f"  Edit this file with your actual W2 data")
        
    except Exception as e:
        logger.error(f"Failed to generate sample file: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()
