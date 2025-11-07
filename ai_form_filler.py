#!/usr/bin/env python3
"""
AI-Powered Desktop Form Automation

This script uses AI (GPT-4 or Claude) to intelligently fill forms in desktop applications
by understanding the UI structure and mapping data to the correct fields.
"""

import json
import os
import time
from typing import Dict, Optional, Any
from dataclasses import dataclass

import atomacos
import google.generativeai as genai
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


@dataclass
class FormField:
    """Represents a form field to be filled."""
    label: str
    value: Any
    field_type: str = "text"  # text, number, date, checkbox, etc.


class AIFormAutomation:
    """AI-powered form automation for desktop applications."""
    
    def __init__(self, app_name: str):
        """
        Initialize the automation system.
        
        Args:
            app_name: Name of the desktop application
        """
        self.app_name = app_name
        self.app = None
        
        # Set up Gemini AI
        self._setup_ai_client()
        
    def _setup_ai_client(self):
        """Initialize the Gemini AI client."""
        api_key = os.getenv("GOOGLE_API_KEY")
        if not api_key:
            raise ValueError("GOOGLE_API_KEY not found in environment variables")
        
        genai.configure(api_key=api_key)
        self.model_name = os.getenv("GEMINI_MODEL", "gemini-2.0-flash-exp")
        self.model = genai.GenerativeModel(self.model_name)
    
    def connect_to_app(self) -> bool:
        """Connect to the desktop application."""
        try:
            self.app = atomacos.NativeUIElement.getAppRefByLocalizedName(self.app_name)
            print(f"✓ Connected to {self.app_name}")
            return True
        except Exception as e:
            print(f"✗ Failed to connect to {self.app_name}: {e}")
            return False
    
    def get_ui_structure(self, element=None, max_depth: int = 6) -> Dict:
        """Get the UI structure of the application."""
        if element is None:
            try:
                element = self.app.AXFocusedWindow
            except Exception:
                element = self.app
        
        return self._traverse_ui_tree(element, max_depth)
    
    def _traverse_ui_tree(self, element, max_depth: int, current_depth: int = 0) -> Dict:
        """Recursively traverse the UI tree."""
        if current_depth >= max_depth:
            return {"truncated": True}
        
        try:
            ui_info = {
                "role": self._safe_get(element, "AXRole"),
                "title": self._safe_get(element, "AXTitle"),
                "description": self._safe_get(element, "AXDescription"),
                "value": self._safe_get(element, "AXValue"),
                "identifier": self._safe_get(element, "AXIdentifier"),
                "enabled": self._safe_get(element, "AXEnabled"),
            }
            
            # Only include relevant fields
            ui_info = {k: v for k, v in ui_info.items() if v}
            
            # Get children
            try:
                children = element.AXChildren or []
                if children:
                    ui_info["children"] = [
                        self._traverse_ui_tree(child, max_depth, current_depth + 1)
                        for child in children
                    ]
            except Exception:
                pass
            
            return ui_info
        except Exception as e:
            return {"error": str(e)}
    
    def _safe_get(self, element, attr_name: str):
        """Safely get an attribute from an element."""
        try:
            value = getattr(element, attr_name, None)
            if value is not None:
                return str(value) if not isinstance(value, (str, int, float, bool)) else value
            return None
        except Exception:
            return None
    
    def ask_ai_to_map_fields(self, ui_structure: Dict, form_data: Dict[str, Any]) -> Dict[str, str]:
        """
        Ask AI to map form data to UI elements.
        
        Args:
            ui_structure: The UI tree structure
            form_data: Data to fill in the form
            
        Returns:
            Mapping of data fields to UI element identifiers
        """
        prompt = self._create_mapping_prompt(ui_structure, form_data)
        
        try:
            # Generate response using Gemini
            response = self.model.generate_content(
                prompt,
                generation_config=genai.GenerationConfig(
                    temperature=0.1,
                    top_p=0.95,
                    top_k=40,
                    max_output_tokens=2048,
                )
            )
            
            mapping_json = response.text
            
            # Extract JSON from the response
            mapping_json = self._extract_json(mapping_json)
            mapping = json.loads(mapping_json)
            
            print("✓ AI generated field mapping")
            return mapping
            
        except Exception as e:
            print(f"✗ AI mapping failed: {e}")
            return {}
    
    def _create_mapping_prompt(self, ui_structure: Dict, form_data: Dict) -> str:
        """Create a prompt for the AI to map fields."""
        prompt = f"""You are an expert at analyzing desktop application UI structures and mapping form data to the correct UI elements. You understand accessibility APIs and can identify which UI element corresponds to which data field.

I need to fill a form in a desktop application with the following data:

FORM DATA TO FILL:
{json.dumps(form_data, indent=2)}

UI STRUCTURE OF THE APPLICATION:
{json.dumps(ui_structure, indent=2)}

Please analyze the UI structure and map each piece of form data to the appropriate UI element. 
Look for text fields (AXTextField), combo boxes (AXComboBox), checkboxes (AXCheckBox), etc.
Match based on titles, descriptions, identifiers, or contextual positioning.

Return ONLY a JSON object with this structure:
{{
  "mappings": [
    {{
      "data_field": "name_of_data_field",
      "ui_path": "description of how to find the element",
      "ui_identifier": "identifier if available",
      "ui_title": "title of the field",
      "confidence": "high/medium/low"
    }}
  ],
  "instructions": "Any special instructions for filling the form in sequence"
}}
"""
        return prompt
    
    def _extract_json(self, text: str) -> str:
        """Extract JSON from AI response that may contain markdown or explanations."""
        # Try to find JSON between ```json and ```
        import re
        json_match = re.search(r'```(?:json)?\s*(\{.*?\})\s*```', text, re.DOTALL)
        if json_match:
            return json_match.group(1)
        
        # Try to find JSON directly
        json_match = re.search(r'\{.*\}', text, re.DOTALL)
        if json_match:
            return json_match.group(0)
        
        return text
    
    def find_element_by_criteria(self, criteria: Dict, root=None) -> Optional[Any]:
        """
        Find a UI element based on various criteria.
        
        Args:
            criteria: Dict with 'title', 'identifier', 'role', etc.
            root: Starting element (None = focused window)
            
        Returns:
            The matching element or None
        """
        if root is None:
            try:
                root = self.app.AXFocusedWindow
            except Exception:
                root = self.app
        
        return self._search_element(root, criteria)
    
    def _search_element(self, element, criteria: Dict, max_depth: int = 10, current_depth: int = 0) -> Optional[Any]:
        """Recursively search for an element matching criteria."""
        if current_depth >= max_depth:
            return None
        
        try:
            # Check if current element matches
            matches = True
            for key, value in criteria.items():
                attr_name = f"AX{key.title().replace('_', '')}"
                elem_value = self._safe_get(element, attr_name)
                if value and elem_value:
                    if value.lower() not in str(elem_value).lower():
                        matches = False
                        break
            
            if matches:
                return element
            
            # Search children
            try:
                for child in (element.AXChildren or []):
                    result = self._search_element(child, criteria, max_depth, current_depth + 1)
                    if result:
                        return result
            except Exception:
                pass
                
        except Exception:
            pass
        
        return None
    
    def fill_field(self, element, value: Any) -> bool:
        """
        Fill a form field with a value.
        
        Args:
            element: The UI element to fill
            value: The value to enter
            
        Returns:
            True if successful, False otherwise
        """
        try:
            # Focus the element first
            element.AXFocused = True
            time.sleep(0.2)
            
            # Set the value
            element.AXValue = str(value)
            time.sleep(0.1)
            
            # Confirm by pressing tab (to trigger any validation)
            element.Press()
            
            print(f"  ✓ Filled field with: {value}")
            return True
            
        except Exception as e:
            print(f"  ✗ Failed to fill field: {e}")
            return False
    
    def fill_form(self, form_data: Dict[str, Any]) -> bool:
        """
        Automatically fill a form using AI to understand the structure.
        
        Args:
            form_data: Dictionary of field names and values to fill
            
        Returns:
            True if successful, False otherwise
        """
        print(f"\n{'='*60}")
        print(f"Starting AI-Powered Form Automation")
        print(f"{'='*60}\n")
        
        # Step 1: Get UI structure
        print("📋 Step 1: Analyzing UI structure...")
        ui_structure = self.get_ui_structure()
        
        # Save for debugging
        with open("ui_debug.json", 'w') as f:
            json.dump(ui_structure, f, indent=2)
        print("  ✓ UI structure captured (saved to ui_debug.json)")
        
        # Step 2: Ask AI to map fields
        print("\n🤖 Step 2: AI analyzing form and creating field mapping...")
        mapping = self.ask_ai_to_map_fields(ui_structure, form_data)
        
        if not mapping:
            print("  ✗ AI could not create a mapping")
            return False
        
        # Save mapping for review
        with open("ai_mapping.json", 'w') as f:
            json.dump(mapping, f, indent=2)
        print("  ✓ Field mapping created (saved to ai_mapping.json)")
        
        # Step 3: Fill the form based on AI mapping
        print("\n✍️  Step 3: Filling form fields...")
        
        if "instructions" in mapping:
            print(f"\nAI Instructions: {mapping['instructions']}\n")
        
        success_count = 0
        for item in mapping.get("mappings", []):
            data_field = item.get("data_field")
            value = form_data.get(data_field)
            
            if value is None:
                continue
            
            print(f"\n  Filling '{data_field}' = '{value}'")
            print(f"    Confidence: {item.get('confidence', 'unknown')}")
            
            # Build search criteria
            criteria = {}
            if item.get("ui_title"):
                criteria["title"] = item["ui_title"]
            if item.get("ui_identifier"):
                criteria["identifier"] = item["ui_identifier"]
            
            # Find and fill the element
            element = self.find_element_by_criteria(criteria)
            
            if element:
                if self.fill_field(element, value):
                    success_count += 1
                time.sleep(0.3)  # Small delay between fields
            else:
                print(f"  ⚠️  Could not locate element for '{data_field}'")
        
        # Summary
        print(f"\n{'='*60}")
        print(f"✓ Form filling complete!")
        print(f"  Successfully filled: {success_count}/{len(mapping.get('mappings', []))} fields")
        print(f"{'='*60}\n")
        
        return success_count > 0


def main():
    """Main entry point for the automation script."""
    # Example W2 data
    w2_data = {
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
    }
    
    print("=" * 60)
    print("AI-Powered Desktop Form Automation")
    print("=" * 60)
    print()
    
    app_name = input("Enter application name (default: ProSeries): ").strip() or "ProSeries"
    
    automation = AIFormAutomation(app_name)
    
    if not automation.connect_to_app():
        print("\n⚠️  Could not connect to the application.")
        print("\nMake sure:")
        print("1. The application is running")
        print("2. The W2 form is open and visible")
        print("3. Accessibility permissions are granted")
        return
    
    print("\n✓ Ready to fill the form")
    print("\nData to be filled:")
    for key, value in w2_data.items():
        print(f"  {key}: {value}")
    
    input("\nPress ENTER to start automation...")
    
    automation.fill_form(w2_data)


if __name__ == "__main__":
    main()
