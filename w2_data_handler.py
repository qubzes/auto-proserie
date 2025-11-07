"""
W2 Form Data Handler

This module handles loading W2 data from various formats (JSON, CSV, dict)
and validates the data before form filling.
"""

import json
import csv
from typing import Dict, List, Any
from pathlib import Path
from pydantic import BaseModel, Field, validator


class W2FormData(BaseModel):
    """W2 Form data structure with validation."""
    
    # Employer Information
    employer_name: str = Field(..., description="Employer's name")
    employer_ein: str = Field(..., description="Employer Identification Number (EIN)")
    employer_address: str = Field(..., description="Employer's street address")
    employer_city: str = Field(..., description="Employer's city")
    employer_state: str = Field(..., description="Employer's state (2-letter code)")
    employer_zip: str = Field(..., description="Employer's ZIP code")
    
    # Employee Information
    employee_ssn: str = Field(..., description="Employee's Social Security Number")
    employee_name: str = Field(..., description="Employee's full name")
    employee_address: str = Field(..., description="Employee's street address")
    employee_city: str = Field(..., description="Employee's city")
    employee_state: str = Field(..., description="Employee's state (2-letter code)")
    employee_zip: str = Field(..., description="Employee's ZIP code")
    
    # Wage Information
    wages: str = Field(..., description="Wages, tips, other compensation (Box 1)")
    federal_tax_withheld: str = Field(..., description="Federal income tax withheld (Box 2)")
    social_security_wages: str = Field(..., description="Social security wages (Box 3)")
    social_security_tax: str = Field(..., description="Social security tax withheld (Box 4)")
    medicare_wages: str = Field(..., description="Medicare wages and tips (Box 5)")
    medicare_tax: str = Field(..., description="Medicare tax withheld (Box 6)")
    
    # Optional fields
    social_security_tips: str = Field(default="", description="Social security tips (Box 7)")
    allocated_tips: str = Field(default="", description="Allocated tips (Box 8)")
    dependent_care_benefits: str = Field(default="", description="Dependent care benefits (Box 10)")
    nonqualified_plans: str = Field(default="", description="Nonqualified plans (Box 11)")
    
    @validator('employer_ein')
    def validate_ein(cls, v):
        """Validate EIN format (XX-XXXXXXX)."""
        v = v.strip()
        if not v:
            return v
        # Remove any formatting
        ein = v.replace('-', '')
        if len(ein) != 9 or not ein.isdigit():
            raise ValueError('EIN must be 9 digits (format: XX-XXXXXXX)')
        return f"{ein[:2]}-{ein[2:]}"
    
    @validator('employee_ssn')
    def validate_ssn(cls, v):
        """Validate SSN format (XXX-XX-XXXX)."""
        v = v.strip()
        if not v:
            return v
        # Remove any formatting
        ssn = v.replace('-', '').replace(' ', '')
        if len(ssn) != 9 or not ssn.isdigit():
            raise ValueError('SSN must be 9 digits (format: XXX-XX-XXXX)')
        return f"{ssn[:3]}-{ssn[3:5]}-{ssn[5:]}"
    
    @validator('employer_state', 'employee_state')
    def validate_state(cls, v):
        """Validate state codes are 2 letters."""
        v = v.strip().upper()
        if len(v) != 2 or not v.isalpha():
            raise ValueError('State must be a 2-letter code (e.g., NY, CA)')
        return v
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return self.dict()


class W2DataLoader:
    """Load and manage W2 form data from various sources."""
    
    @staticmethod
    def from_json(file_path: str) -> W2FormData:
        """
        Load W2 data from a JSON file.
        
        Args:
            file_path: Path to JSON file
            
        Returns:
            Validated W2FormData object
        """
        with open(file_path, 'r') as f:
            data = json.load(f)
        return W2FormData(**data)
    
    @staticmethod
    def from_csv(file_path: str) -> List[W2FormData]:
        """
        Load multiple W2 records from a CSV file.
        
        Args:
            file_path: Path to CSV file
            
        Returns:
            List of validated W2FormData objects
        """
        records = []
        with open(file_path, 'r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                records.append(W2FormData(**row))
        return records
    
    @staticmethod
    def from_dict(data: Dict[str, Any]) -> W2FormData:
        """
        Create W2FormData from a dictionary.
        
        Args:
            data: Dictionary with W2 data
            
        Returns:
            Validated W2FormData object
        """
        return W2FormData(**data)
    
    @staticmethod
    def create_sample_json(file_path: str = "sample_w2.json"):
        """Create a sample W2 JSON file for reference."""
        sample_data = {
            "employer_name": "ABC Corporation",
            "employer_ein": "12-3456789",
            "employer_address": "123 Main Street",
            "employer_city": "New York",
            "employer_state": "NY",
            "employer_zip": "10001",
            "employee_ssn": "123-45-6789",
            "employee_name": "John Doe",
            "employee_address": "456 Oak Avenue",
            "employee_city": "Brooklyn",
            "employee_state": "NY",
            "employee_zip": "11201",
            "wages": "75000.00",
            "federal_tax_withheld": "9500.00",
            "social_security_wages": "75000.00",
            "social_security_tax": "4650.00",
            "medicare_wages": "75000.00",
            "medicare_tax": "1087.50",
            "social_security_tips": "",
            "allocated_tips": "",
            "dependent_care_benefits": "",
            "nonqualified_plans": ""
        }
        
        with open(file_path, 'w') as f:
            json.dump(sample_data, f, indent=2)
        
        print(f"✓ Sample W2 data saved to {file_path}")
        return sample_data
    
    @staticmethod
    def create_sample_csv(file_path: str = "sample_w2.csv"):
        """Create a sample W2 CSV file for batch processing."""
        sample_data = [
            {
                "employer_name": "ABC Corporation",
                "employer_ein": "12-3456789",
                "employer_address": "123 Main Street",
                "employer_city": "New York",
                "employer_state": "NY",
                "employer_zip": "10001",
                "employee_ssn": "123-45-6789",
                "employee_name": "John Doe",
                "employee_address": "456 Oak Avenue",
                "employee_city": "Brooklyn",
                "employee_state": "NY",
                "employee_zip": "11201",
                "wages": "75000.00",
                "federal_tax_withheld": "9500.00",
                "social_security_wages": "75000.00",
                "social_security_tax": "4650.00",
                "medicare_wages": "75000.00",
                "medicare_tax": "1087.50",
                "social_security_tips": "",
                "allocated_tips": "",
                "dependent_care_benefits": "",
                "nonqualified_plans": ""
            },
            {
                "employer_name": "XYZ Company",
                "employer_ein": "98-7654321",
                "employer_address": "789 Business Blvd",
                "employer_city": "Los Angeles",
                "employer_state": "CA",
                "employer_zip": "90001",
                "employee_ssn": "987-65-4321",
                "employee_name": "Jane Smith",
                "employee_address": "321 Palm Street",
                "employee_city": "Los Angeles",
                "employee_state": "CA",
                "employee_zip": "90002",
                "wages": "85000.00",
                "federal_tax_withheld": "12000.00",
                "social_security_wages": "85000.00",
                "social_security_tax": "5270.00",
                "medicare_wages": "85000.00",
                "medicare_tax": "1232.50",
                "social_security_tips": "",
                "allocated_tips": "",
                "dependent_care_benefits": "",
                "nonqualified_plans": ""
            }
        ]
        
        with open(file_path, 'w', newline='') as f:
            fieldnames = sample_data[0].keys()
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(sample_data)
        
        print(f"✓ Sample W2 CSV saved to {file_path}")


def main():
    """Generate sample data files."""
    print("=" * 60)
    print("W2 Data File Generator")
    print("=" * 60)
    print()
    
    W2DataLoader.create_sample_json()
    W2DataLoader.create_sample_csv()
    
    print("\nYou can now:")
    print("1. Edit sample_w2.json with your data")
    print("2. Edit sample_w2.csv for batch processing multiple W2s")
    print("3. Use these files with the ai_form_filler.py script")


if __name__ == "__main__":
    main()
