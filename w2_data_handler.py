"""
W2 Data Handler - Load and validate W2 data from various sources
"""

import json
import pandas as pd
from typing import Dict, List
import logging

logger = logging.getLogger(__name__)


class W2DataHandler:
    """Handle loading and validating W2 data from different sources"""
    
    REQUIRED_FIELDS = [
        'employee_name',
        'employee_ssn',
        'employer_name',
        'employer_ein',
        'wages',
        'federal_tax_withheld'
    ]
    
    OPTIONAL_FIELDS = [
        'employee_address',
        'employee_city',
        'employee_state',
        'employee_zip',
        'employer_address',
        'employer_city',
        'employer_state',
        'employer_zip',
        'social_security_wages',
        'social_security_tax',
        'medicare_wages',
        'medicare_tax',
        'social_security_tips',
        'allocated_tips',
        'dependent_care_benefits',
        'nonqualified_plans',
        'box_12_codes',
        'statutory_employee',
        'retirement_plan',
        'third_party_sick_pay',
        'state',
        'state_wages',
        'state_tax',
        'local_wages',
        'local_tax',
        'locality_name'
    ]
    
    @staticmethod
    def load_from_json(file_path: str) -> List[Dict]:
        """
        Load W2 data from JSON file
        
        Args:
            file_path: Path to JSON file
            
        Returns:
            List of W2 data dictionaries
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            # Handle both single object and array
            if isinstance(data, dict):
                data = [data]
            
            logger.info(f"Loaded {len(data)} W2 records from {file_path}")
            return data
            
        except Exception as e:
            logger.error(f"Failed to load JSON file: {str(e)}")
            return []
    
    @staticmethod
    def load_from_excel(file_path: str, sheet_name: str = 'W2 Data') -> List[Dict]:
        """
        Load W2 data from Excel file
        
        Args:
            file_path: Path to Excel file
            sheet_name: Name of sheet containing W2 data
            
        Returns:
            List of W2 data dictionaries
        """
        try:
            df = pd.read_excel(file_path, sheet_name=sheet_name)
            
            # Convert to list of dictionaries
            data = df.to_dict('records')
            
            # Clean up NaN values
            for record in data:
                for key, value in record.items():
                    if pd.isna(value):
                        record[key] = ''
            
            logger.info(f"Loaded {len(data)} W2 records from {file_path}")
            return data
            
        except Exception as e:
            logger.error(f"Failed to load Excel file: {str(e)}")
            return []
    
    @staticmethod
    def load_from_csv(file_path: str) -> List[Dict]:
        """
        Load W2 data from CSV file
        
        Args:
            file_path: Path to CSV file
            
        Returns:
            List of W2 data dictionaries
        """
        try:
            df = pd.read_csv(file_path)
            
            # Convert to list of dictionaries
            data = df.to_dict('records')
            
            # Clean up NaN values
            for record in data:
                for key, value in record.items():
                    if pd.isna(value):
                        record[key] = ''
            
            logger.info(f"Loaded {len(data)} W2 records from {file_path}")
            return data
            
        except Exception as e:
            logger.error(f"Failed to load CSV file: {str(e)}")
            return []
    
    @classmethod
    def validate_w2_data(cls, w2_data: Dict) -> tuple[bool, List[str]]:
        """
        Validate W2 data has required fields
        
        Args:
            w2_data: W2 data dictionary
            
        Returns:
            Tuple of (is_valid, list_of_missing_fields)
        """
        missing_fields = []
        
        for field in cls.REQUIRED_FIELDS:
            if field not in w2_data or not w2_data[field]:
                missing_fields.append(field)
        
        is_valid = len(missing_fields) == 0
        
        if not is_valid:
            logger.warning(f"W2 data missing required fields: {missing_fields}")
        
        return is_valid, missing_fields
    
    @classmethod
    def validate_batch(cls, w2_data_list: List[Dict]) -> Dict:
        """
        Validate a batch of W2 data
        
        Args:
            w2_data_list: List of W2 data dictionaries
            
        Returns:
            Dictionary with validation results
        """
        results = {
            'total': len(w2_data_list),
            'valid': 0,
            'invalid': 0,
            'errors': []
        }
        
        for i, w2_data in enumerate(w2_data_list):
            is_valid, missing_fields = cls.validate_w2_data(w2_data)
            
            if is_valid:
                results['valid'] += 1
            else:
                results['invalid'] += 1
                results['errors'].append({
                    'index': i,
                    'employee': w2_data.get('employee_name', 'Unknown'),
                    'missing_fields': missing_fields
                })
        
        return results
    
    @staticmethod
    def format_ssn(ssn: str) -> str:
        """Format SSN to XXX-XX-XXXX format"""
        # Remove any non-digit characters
        digits = ''.join(filter(str.isdigit, ssn))
        
        if len(digits) == 9:
            return f"{digits[0:3]}-{digits[3:5]}-{digits[5:9]}"
        return ssn
    
    @staticmethod
    def format_ein(ein: str) -> str:
        """Format EIN to XX-XXXXXXX format"""
        # Remove any non-digit characters
        digits = ''.join(filter(str.isdigit, ein))
        
        if len(digits) == 9:
            return f"{digits[0:2]}-{digits[2:9]}"
        return ein
    
    @staticmethod
    def format_currency(amount: str | float) -> str:
        """Format currency amount"""
        try:
            # Convert to float if string
            if isinstance(amount, str):
                amount = amount.replace('$', '').replace(',', '')
                amount = float(amount)
            
            return f"{amount:.2f}"
        except (ValueError, TypeError):
            return str(amount)
    
    @classmethod
    def clean_w2_data(cls, w2_data: Dict) -> Dict:
        """
        Clean and format W2 data
        
        Args:
            w2_data: Raw W2 data
            
        Returns:
            Cleaned W2 data
        """
        cleaned = w2_data.copy()
        
        # Format SSN
        if 'employee_ssn' in cleaned:
            cleaned['employee_ssn'] = cls.format_ssn(cleaned['employee_ssn'])
        
        # Format EIN
        if 'employer_ein' in cleaned:
            cleaned['employer_ein'] = cls.format_ein(cleaned['employer_ein'])
        
        # Format currency fields
        currency_fields = [
            'wages', 'federal_tax_withheld', 'social_security_wages',
            'social_security_tax', 'medicare_wages', 'medicare_tax',
            'social_security_tips', 'allocated_tips', 'dependent_care_benefits',
            'nonqualified_plans', 'state_wages', 'state_tax',
            'local_wages', 'local_tax'
        ]
        
        for field in currency_fields:
            if field in cleaned and cleaned[field]:
                cleaned[field] = cls.format_currency(cleaned[field])
        
        return cleaned


def create_sample_w2_data() -> List[Dict]:
    """Create sample W2 data for testing"""
    return [
        {
            'employee_name': 'John Smith',
            'employee_ssn': '123-45-6789',
            'employee_address': '123 Main St',
            'employee_city': 'New York',
            'employee_state': 'NY',
            'employee_zip': '10001',
            'employer_name': 'ABC Corporation',
            'employer_ein': '12-3456789',
            'employer_address': '456 Business Ave',
            'employer_city': 'New York',
            'employer_state': 'NY',
            'employer_zip': '10002',
            'wages': '75000.00',
            'federal_tax_withheld': '12500.00',
            'social_security_wages': '75000.00',
            'social_security_tax': '4650.00',
            'medicare_wages': '75000.00',
            'medicare_tax': '1087.50',
            'state': 'NY',
            'state_wages': '75000.00',
            'state_tax': '4500.00'
        },
        {
            'employee_name': 'Jane Doe',
            'employee_ssn': '987-65-4321',
            'employee_address': '789 Oak Lane',
            'employee_city': 'Los Angeles',
            'employee_state': 'CA',
            'employee_zip': '90001',
            'employer_name': 'XYZ Industries',
            'employer_ein': '98-7654321',
            'employer_address': '321 Commerce Blvd',
            'employer_city': 'Los Angeles',
            'employer_state': 'CA',
            'employer_zip': '90002',
            'wages': '85000.00',
            'federal_tax_withheld': '15300.00',
            'social_security_wages': '85000.00',
            'social_security_tax': '5270.00',
            'medicare_wages': '85000.00',
            'medicare_tax': '1232.50',
            'state': 'CA',
            'state_wages': '85000.00',
            'state_tax': '6800.00'
        }
    ]
