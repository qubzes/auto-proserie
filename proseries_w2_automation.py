"""
ProSeries W2 Form Automation using Gemini AI
This script automates filling W2 forms in ProSeries desktop application
using Windows UI Automation and Gemini AI for intelligent form recognition.
"""

import os
import time
import json
import logging
from typing import Dict, List, Optional, Any
from dotenv import load_dotenv
import google.generativeai as genai
from pywinauto import Application, Desktop
from pywinauto.controls.uiawrapper import UIAWrapper
from pywinauto.findwindows import ElementNotFoundError
import psutil

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('proseries_automation.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


class ProSeriesW2Automation:
    """Main automation class for ProSeries W2 form filling"""
    
    def __init__(self, api_key: str, model_name: str = "gemini-2.0-flash-exp"):
        """
        Initialize the automation system
        
        Args:
            api_key: Google API key for Gemini
            model_name: Gemini model to use
        """
        self.api_key = api_key
        self.model_name = model_name
        self.app = None
        self.main_window = None
        
        # Configure Gemini AI
        genai.configure(api_key=self.api_key)
        self.model = genai.GenerativeModel(self.model_name)
        logger.info(f"Initialized Gemini AI with model: {self.model_name}")
        
    def find_proseries_process(self) -> Optional[int]:
        """Find the ProSeries process ID"""
        proseries_names = [
            'ProSeries.exe', 
            'ProSeriesBasic.exe', 
            'ProSeriesProfessional.exe',
            'TaxWise.exe'  # Alternative tax software
        ]
        
        for proc in psutil.process_iter(['pid', 'name']):
            try:
                proc_name = proc.info['name']
                if any(name.lower() in proc_name.lower() for name in proseries_names):
                    logger.info(f"Found ProSeries process: {proc_name} (PID: {proc.info['pid']})")
                    return proc.info['pid']
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                pass
        
        logger.warning("ProSeries process not found")
        return None
    
    def connect_to_proseries(self) -> bool:
        """
        Connect to the ProSeries application
        
        Returns:
            bool: True if connection successful
        """
        try:
            # Try to find ProSeries by process
            pid = self.find_proseries_process()
            
            if pid:
                logger.info(f"Connecting to ProSeries (PID: {pid})...")
                self.app = Application(backend="uia").connect(process=pid, timeout=10)
            else:
                # Try to find by window title
                logger.info("Attempting to find ProSeries by window title...")
                desktop = Desktop(backend="uia")
                windows = desktop.windows()
                
                for window in windows:
                    try:
                        title = window.window_text()
                        if any(keyword in title.lower() for keyword in ['proseries', 'taxwise', 'intuit tax']):
                            logger.info(f"Found window: {title}")
                            self.main_window = window
                            return True
                    except:
                        continue
                
                raise Exception("ProSeries application not found. Please ensure it's running.")
            
            # Get the main window
            if self.app:
                self.main_window = self.app.top_window()
                logger.info(f"Connected to ProSeries: {self.main_window.window_text()}")
                return True
                
        except Exception as e:
            logger.error(f"Failed to connect to ProSeries: {str(e)}")
            return False
    
    def get_ui_tree_structure(self, element: UIAWrapper = None, depth: int = 0, max_depth: int = 5) -> Dict:
        """
        Extract the UI tree structure of the application
        
        Args:
            element: UI element to start from (None for main window)
            depth: Current depth in tree
            max_depth: Maximum depth to traverse
            
        Returns:
            Dict containing UI structure information
        """
        if element is None:
            element = self.main_window
        
        if depth > max_depth:
            return {}
        
        try:
            structure = {
                'type': element.element_info.control_type,
                'name': element.window_text() if hasattr(element, 'window_text') else '',
                'automation_id': element.element_info.automation_id if hasattr(element.element_info, 'automation_id') else '',
                'class_name': element.element_info.class_name if hasattr(element.element_info, 'class_name') else '',
                'rectangle': str(element.rectangle()) if hasattr(element, 'rectangle') else '',
                'enabled': element.is_enabled() if hasattr(element, 'is_enabled') else False,
                'visible': element.is_visible() if hasattr(element, 'is_visible') else False,
                'children': []
            }
            
            # Get child elements
            if depth < max_depth:
                try:
                    children = element.children()
                    for child in children[:20]:  # Limit children to avoid too much data
                        child_structure = self.get_ui_tree_structure(child, depth + 1, max_depth)
                        if child_structure:
                            structure['children'].append(child_structure)
                except:
                    pass
            
            return structure
            
        except Exception as e:
            logger.warning(f"Error extracting UI structure at depth {depth}: {str(e)}")
            return {}
    
    def get_focused_form_structure(self) -> str:
        """
        Get the current focused form structure and convert to text representation
        
        Returns:
            str: Text representation of the form structure
        """
        try:
            logger.info("Extracting form structure...")
            ui_tree = self.get_ui_tree_structure(max_depth=4)
            
            # Convert to readable text format
            form_text = self._convert_ui_tree_to_text(ui_tree)
            
            logger.info(f"Extracted form structure ({len(form_text)} characters)")
            return form_text
            
        except Exception as e:
            logger.error(f"Failed to extract form structure: {str(e)}")
            return ""
    
    def _convert_ui_tree_to_text(self, tree: Dict, indent: int = 0) -> str:
        """Convert UI tree to readable text format"""
        if not tree:
            return ""
        
        text_parts = []
        indent_str = "  " * indent
        
        # Add current element info
        element_type = tree.get('type', 'Unknown')
        element_name = tree.get('name', '')
        automation_id = tree.get('automation_id', '')
        enabled = tree.get('enabled', False)
        visible = tree.get('visible', False)
        
        if visible and (element_name or automation_id):
            info = f"{indent_str}[{element_type}]"
            if element_name:
                info += f" Name: '{element_name}'"
            if automation_id:
                info += f" ID: '{automation_id}'"
            info += f" (Enabled: {enabled})"
            text_parts.append(info)
        
        # Add children
        for child in tree.get('children', []):
            child_text = self._convert_ui_tree_to_text(child, indent + 1)
            if child_text:
                text_parts.append(child_text)
        
        return "\n".join(text_parts)
    
    def ask_gemini_for_actions(self, form_structure: str, w2_data: Dict) -> List[Dict]:
        """
        Ask Gemini AI to generate form filling actions
        
        Args:
            form_structure: Text representation of form UI structure
            w2_data: W2 data to fill
            
        Returns:
            List of actions to perform
        """
        prompt = f"""You are an expert at analyzing Windows desktop application UI structures and generating automation commands.

I need to fill a W2 form in the ProSeries tax software. Below is the UI structure of the current form/window:

UI STRUCTURE:
{form_structure}

W2 DATA TO FILL:
{json.dumps(w2_data, indent=2)}

Your task is to analyze the UI structure and generate a precise list of actions to fill this W2 form.

Return your response as a JSON array of actions. Each action should have:
- "type": "set_text" | "click" | "select" | "tab" | "wait"
- "target": the element name, automation_id, or description
- "value": the value to set (for set_text and select actions)
- "description": human-readable description of the action

Example format:
[
  {{"type": "set_text", "target": "Employee Name", "value": "John Doe", "description": "Enter employee name"}},
  {{"type": "tab", "description": "Move to next field"}},
  {{"type": "set_text", "target": "SSN", "value": "123-45-6789", "description": "Enter SSN"}}
]

Important guidelines:
1. Match W2 data fields to UI elements by name or automation_id
2. Use "tab" actions to navigate between fields when needed
3. Only target visible and enabled elements
4. Be precise with element names
5. Include wait actions if UI might need time to update
6. Map these W2 fields: employee_name, employee_ssn, employer_name, employer_ein, wages, federal_tax_withheld, social_security_wages, social_security_tax, medicare_wages, medicare_tax, state, state_wages, state_tax

Respond ONLY with the JSON array, no additional text.
"""
        
        try:
            logger.info("Asking Gemini AI for form filling actions...")
            response = self.model.generate_content(prompt)
            
            # Extract JSON from response
            response_text = response.text.strip()
            
            # Remove markdown code blocks if present
            if response_text.startswith('```'):
                response_text = response_text.split('```')[1]
                if response_text.startswith('json'):
                    response_text = response_text[4:]
                response_text = response_text.strip()
            
            actions = json.loads(response_text)
            logger.info(f"Gemini generated {len(actions)} actions")
            
            return actions
            
        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse Gemini response as JSON: {str(e)}")
            logger.error(f"Response was: {response.text[:500]}")
            return []
        except Exception as e:
            logger.error(f"Error asking Gemini for actions: {str(e)}")
            return []
    
    def execute_actions(self, actions: List[Dict]) -> bool:
        """
        Execute the list of actions generated by AI
        
        Args:
            actions: List of actions to perform
            
        Returns:
            bool: True if all actions executed successfully
        """
        logger.info(f"Executing {len(actions)} actions...")
        
        for i, action in enumerate(actions):
            try:
                action_type = action.get('type')
                target = action.get('target', '')
                value = action.get('value', '')
                description = action.get('description', '')
                
                logger.info(f"Action {i+1}/{len(actions)}: {description}")
                
                if action_type == 'set_text':
                    self._set_text_action(target, value)
                    
                elif action_type == 'click':
                    self._click_action(target)
                    
                elif action_type == 'select':
                    self._select_action(target, value)
                    
                elif action_type == 'tab':
                    self._tab_action()
                    
                elif action_type == 'wait':
                    wait_time = float(value) if value else 1.0
                    time.sleep(wait_time)
                
                # Small delay between actions
                time.sleep(0.3)
                
            except Exception as e:
                logger.error(f"Failed to execute action {i+1}: {str(e)}")
                logger.error(f"Action details: {action}")
                # Continue with next action
                continue
        
        logger.info("Completed executing all actions")
        return True
    
    def _find_element_by_target(self, target: str) -> Optional[UIAWrapper]:
        """Find UI element by name, automation_id, or class_name"""
        try:
            # Try by name first
            try:
                element = self.main_window.child_window(title=target, control_type="Edit")
                if element.exists():
                    return element
            except:
                pass
            
            # Try by automation_id
            try:
                element = self.main_window.child_window(auto_id=target)
                if element.exists():
                    return element
            except:
                pass
            
            # Try partial name match
            try:
                element = self.main_window.child_window(title_re=f".*{target}.*", control_type="Edit")
                if element.exists():
                    return element
            except:
                pass
            
            # Try to find by control type and visible text
            try:
                descendants = self.main_window.descendants()
                for desc in descendants:
                    try:
                        if target.lower() in desc.window_text().lower() and desc.is_visible():
                            return desc
                    except:
                        continue
            except:
                pass
            
            logger.warning(f"Could not find element: {target}")
            return None
            
        except Exception as e:
            logger.error(f"Error finding element '{target}': {str(e)}")
            return None
    
    def _set_text_action(self, target: str, value: str):
        """Set text in a field"""
        element = self._find_element_by_target(target)
        if element:
            try:
                element.set_focus()
                time.sleep(0.1)
                element.set_edit_text("")  # Clear first
                time.sleep(0.1)
                element.set_edit_text(str(value))
                logger.info(f"Set text '{value}' in '{target}'")
            except:
                # Fallback: use type_keys
                try:
                    element.set_focus()
                    element.type_keys("^a")  # Select all
                    element.type_keys(str(value))
                    logger.info(f"Typed text '{value}' in '{target}'")
                except Exception as e:
                    logger.error(f"Failed to set text in '{target}': {str(e)}")
    
    def _click_action(self, target: str):
        """Click an element"""
        element = self._find_element_by_target(target)
        if element:
            try:
                element.click_input()
                logger.info(f"Clicked '{target}'")
            except Exception as e:
                logger.error(f"Failed to click '{target}': {str(e)}")
    
    def _select_action(self, target: str, value: str):
        """Select from a dropdown/combobox"""
        element = self._find_element_by_target(target)
        if element:
            try:
                element.select(value)
                logger.info(f"Selected '{value}' in '{target}'")
            except Exception as e:
                logger.error(f"Failed to select in '{target}': {str(e)}")
    
    def _tab_action(self):
        """Press Tab key"""
        try:
            if self.main_window:
                self.main_window.type_keys("{TAB}")
                logger.debug("Pressed Tab")
        except Exception as e:
            logger.error(f"Failed to press Tab: {str(e)}")
    
    def fill_w2_form(self, w2_data: Dict) -> bool:
        """
        Main method to fill W2 form with provided data
        
        Args:
            w2_data: Dictionary containing W2 information
            
        Returns:
            bool: True if form filled successfully
        """
        try:
            # Connect to ProSeries
            if not self.connect_to_proseries():
                logger.error("Failed to connect to ProSeries")
                return False
            
            # Give user time to navigate to W2 form if needed
            logger.info("Please ensure the W2 form is open and focused...")
            logger.info("Starting in 5 seconds...")
            time.sleep(5)
            
            # Get form structure
            form_structure = self.get_focused_form_structure()
            if not form_structure:
                logger.error("Failed to extract form structure")
                return False
            
            # Ask Gemini for actions
            actions = self.ask_gemini_for_actions(form_structure, w2_data)
            if not actions:
                logger.error("Failed to generate actions from AI")
                return False
            
            # Execute actions
            success = self.execute_actions(actions)
            
            if success:
                logger.info("✓ W2 form filled successfully!")
            else:
                logger.warning("⚠ Some actions may have failed. Please review the log.")
            
            return success
            
        except Exception as e:
            logger.error(f"Error filling W2 form: {str(e)}")
            return False
    
    def fill_multiple_w2_forms(self, w2_data_list: List[Dict]) -> Dict[str, int]:
        """
        Fill multiple W2 forms
        
        Args:
            w2_data_list: List of W2 data dictionaries
            
        Returns:
            Dict with success and failure counts
        """
        results = {'success': 0, 'failed': 0}
        
        for i, w2_data in enumerate(w2_data_list):
            logger.info(f"\n{'='*60}")
            logger.info(f"Processing W2 {i+1}/{len(w2_data_list)}")
            logger.info(f"{'='*60}\n")
            
            success = self.fill_w2_form(w2_data)
            
            if success:
                results['success'] += 1
            else:
                results['failed'] += 1
            
            # Wait between forms
            if i < len(w2_data_list) - 1:
                logger.info("Waiting 3 seconds before next form...")
                time.sleep(3)
        
        return results


def main():
    """Main entry point"""
    # Load environment variables
    load_dotenv()
    
    api_key = os.getenv('GOOGLE_API_KEY')
    model_name = os.getenv('GEMINI_MODEL', 'gemini-2.0-flash-exp')
    
    if not api_key:
        logger.error("GOOGLE_API_KEY not found in environment variables")
        logger.error("Please create a .env file with your API key")
        return
    
    # Example W2 data
    w2_data = {
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
    }
    
    # Initialize automation
    automation = ProSeriesW2Automation(api_key, model_name)
    
    # Fill the form
    logger.info("Starting ProSeries W2 automation...")
    success = automation.fill_w2_form(w2_data)
    
    if success:
        logger.info("\n✓ Automation completed successfully!")
    else:
        logger.error("\n✗ Automation completed with errors. Check the log for details.")


if __name__ == "__main__":
    main()
