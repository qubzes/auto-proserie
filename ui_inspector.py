#!/usr/bin/env python3
"""
UI Inspector for macOS Desktop Applications

This script inspects the accessibility tree of a desktop application
(similar to inspecting HTML elements in a web browser).
It captures the UI structure that AI can understand.
"""

import json
import sys
from typing import Dict, List, Optional
import atomacos

class UIInspector:
    """Inspect and capture UI elements from macOS applications."""
    
    def __init__(self, app_name: str):
        """
        Initialize inspector for a specific application.
        
        Args:
            app_name: Name of the application (e.g., "ProSeries")
        """
        self.app_name = app_name
        self.app = None
        
    def connect_to_app(self) -> bool:
        """
        Connect to the running application.
        
        Returns:
            True if connection successful, False otherwise
        """
        try:
            # Find the application by name
            self.app = atomacos.getAppRefByBundleId(self._get_bundle_id())
            if not self.app:
                # Try by localized name
                self.app = atomacos.NativeUIElement.getAppRefByLocalizedName(self.app_name)
            print(f"✓ Connected to {self.app_name}")
            return True
        except Exception as e:
            print(f"✗ Failed to connect to {self.app_name}: {e}")
            print(f"  Make sure {self.app_name} is running and accessibility permissions are granted.")
            return False
    
    def _get_bundle_id(self) -> Optional[str]:
        """Get bundle ID for common tax software."""
        bundle_ids = {
            "ProSeries": "com.intuit.proseries",
            "Lacerte": "com.intuit.lacerte",
        }
        return bundle_ids.get(self.app_name)
    
    def get_ui_tree(self, element=None, max_depth: int = 10, current_depth: int = 0) -> Dict:
        """
        Recursively get the UI tree structure.
        
        Args:
            element: Starting element (None = root window)
            max_depth: Maximum depth to traverse
            current_depth: Current depth in tree
            
        Returns:
            Dictionary representing the UI tree
        """
        if current_depth >= max_depth:
            return {"truncated": True}
        
        if element is None:
            element = self.app
        
        try:
            ui_info = {
                "role": self._safe_get_attr(element, "AXRole"),
                "title": self._safe_get_attr(element, "AXTitle"),
                "description": self._safe_get_attr(element, "AXDescription"),
                "value": self._safe_get_attr(element, "AXValue"),
                "help": self._safe_get_attr(element, "AXHelp"),
                "identifier": self._safe_get_attr(element, "AXIdentifier"),
                "enabled": self._safe_get_attr(element, "AXEnabled"),
                "position": self._safe_get_attr(element, "AXPosition"),
                "size": self._safe_get_attr(element, "AXSize"),
            }
            
            # Get children recursively
            children = []
            try:
                child_elements = element.AXChildren or []
                for child in child_elements:
                    child_info = self.get_ui_tree(child, max_depth, current_depth + 1)
                    if child_info:
                        children.append(child_info)
            except:
                pass
            
            if children:
                ui_info["children"] = children
            
            return ui_info
            
        except Exception as e:
            return {"error": str(e)}
    
    def _safe_get_attr(self, element, attr_name: str):
        """Safely get an attribute from an element."""
        try:
            value = getattr(element, attr_name, None)
            # Convert to serializable format
            if value is not None:
                return str(value) if not isinstance(value, (str, int, float, bool)) else value
            return None
        except:
            return None
    
    def find_elements_by_role(self, role: str, element=None) -> List:
        """
        Find all elements with a specific role (e.g., 'AXTextField', 'AXButton').
        
        Args:
            role: The AXRole to search for
            element: Starting element (None = root)
            
        Returns:
            List of matching elements with their properties
        """
        if element is None:
            element = self.app
        
        matches = []
        
        try:
            if self._safe_get_attr(element, "AXRole") == role:
                matches.append({
                    "role": role,
                    "title": self._safe_get_attr(element, "AXTitle"),
                    "description": self._safe_get_attr(element, "AXDescription"),
                    "value": self._safe_get_attr(element, "AXValue"),
                    "identifier": self._safe_get_attr(element, "AXIdentifier"),
                    "position": self._safe_get_attr(element, "AXPosition"),
                    "element": element  # Keep reference for interaction
                })
            
            # Search children
            try:
                for child in (element.AXChildren or []):
                    matches.extend(self.find_elements_by_role(role, child))
            except:
                pass
                
        except:
            pass
        
        return matches
    
    def get_all_text_fields(self) -> List:
        """Find all text input fields in the application."""
        return self.find_elements_by_role("AXTextField")
    
    def get_all_buttons(self) -> List:
        """Find all buttons in the application."""
        return self.find_elements_by_role("AXButton")
    
    def get_focused_window_structure(self) -> Dict:
        """Get the structure of the currently focused window."""
        try:
            window = self.app.AXFocusedWindow
            if window:
                return self.get_ui_tree(window, max_depth=5)
            return {"error": "No focused window"}
        except Exception as e:
            return {"error": str(e)}
    
    def save_ui_structure(self, filename: str = "ui_structure.json"):
        """Save the current UI structure to a JSON file."""
        structure = self.get_focused_window_structure()
        with open(filename, 'w') as f:
            json.dump(structure, f, indent=2)
        print(f"✓ UI structure saved to {filename}")
        return structure
    
    def print_text_fields_summary(self):
        """Print a summary of all text fields found."""
        fields = self.get_all_text_fields()
        print(f"\n📝 Found {len(fields)} text fields:\n")
        for i, field in enumerate(fields, 1):
            title = field.get('title') or field.get('description') or 'Untitled'
            value = field.get('value', '')
            identifier = field.get('identifier', 'N/A')
            print(f"{i}. {title}")
            print(f"   Identifier: {identifier}")
            print(f"   Current value: {value}")
            print(f"   Position: {field.get('position')}")
            print()


def main():
    """Main entry point for the UI inspector."""
    print("=" * 60)
    print("Desktop Application UI Inspector")
    print("=" * 60)
    print()
    
    if len(sys.argv) > 1:
        app_name = " ".join(sys.argv[1:])
    else:
        app_name = input("Enter the application name (e.g., ProSeries): ").strip()
    
    if not app_name:
        print("Error: Application name is required")
        return
    
    inspector = UIInspector(app_name)
    
    if not inspector.connect_to_app():
        print("\n⚠️  Could not connect to the application.")
        print("\nTroubleshooting:")
        print("1. Make sure the application is running")
        print("2. Grant accessibility permissions:")
        print("   System Preferences → Security & Privacy → Privacy → Accessibility")
        print("   Add Terminal or your Python IDE to the list")
        return
    
    print("\nChoose an action:")
    print("1. Save full UI structure to JSON")
    print("2. List all text fields")
    print("3. List all buttons")
    print("4. Save focused window structure")
    
    choice = input("\nEnter choice (1-4): ").strip()
    
    if choice == "1":
        structure = inspector.get_ui_tree(max_depth=8)
        filename = "ui_structure_full.json"
        with open(filename, 'w') as f:
            json.dump(structure, f, indent=2)
        print(f"✓ Full UI structure saved to {filename}")
    
    elif choice == "2":
        inspector.print_text_fields_summary()
        
    elif choice == "3":
        buttons = inspector.get_all_buttons()
        print(f"\n🔘 Found {len(buttons)} buttons:\n")
        for i, btn in enumerate(buttons, 1):
            title = btn.get('title', 'Untitled')
            print(f"{i}. {title}")
    
    elif choice == "4":
        inspector.save_ui_structure("focused_window.json")
    
    else:
        print("Invalid choice")


if __name__ == "__main__":
    main()
