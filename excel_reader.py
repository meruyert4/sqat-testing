"""
Excel Data Reader Module
This module reads test data from an Excel file using openpyxl library.
"""

from openpyxl import load_workbook


def read_test_data(file_path):
    """
    Reads test data from an Excel file.
    
    Args:
        file_path (str): Path to the Excel file
        
    Returns:
        dict: Dictionary containing all test data
    """
    try:
        # Load the workbook
        workbook = load_workbook(file_path)
        
        # Select the active sheet (or you can specify sheet name)
        sheet = workbook.active
        
        # Create a dictionary to store test data
        test_data = {}
        
        # Read data from Excel (assuming data starts from row 2, row 1 is headers)
        # Column A: Field Name, Column B: Value
        for row in range(2, sheet.max_row + 1):
            field_name = sheet.cell(row=row, column=1).value
            field_value = sheet.cell(row=row, column=2).value
            
            if field_name and field_value is not None:
                test_data[field_name] = field_value
        
        workbook.close()
        
        print(f"Successfully loaded test data from: {file_path}")
        print(f"Total fields loaded: {len(test_data)}")
        
        return test_data
        
    except FileNotFoundError:
        print(f"Error: Excel file not found at {file_path}")
        raise
    except Exception as e:
        print(f"Error reading Excel file: {e}")
        raise


def get_browserstack_config(file_path, browser_name):
    """
    Reads BrowserStack configuration from Excel file.
    
    Args:
        file_path (str): Path to the Excel file
        browser_name (str): Name of the browser (Chrome or Firefox)
        
    Returns:
        dict: BrowserStack capabilities
    """
    try:
        workbook = load_workbook(file_path)
        
        # Assuming BrowserStack config is in a sheet named 'BrowserStack'
        if 'BrowserStack' in workbook.sheetnames:
            sheet = workbook['BrowserStack']
        else:
            # If no separate sheet, use the active sheet
            sheet = workbook.active
        
        bs_config = {}
        
        # Read BrowserStack configuration
        for row in range(2, sheet.max_row + 1):
            config_key = sheet.cell(row=row, column=1).value
            config_value = sheet.cell(row=row, column=2).value
            
            if config_key and config_value:
                bs_config[config_key] = config_value
        
        workbook.close()
        
        # Set browser-specific capabilities
        capabilities = {
            'browserName': browser_name,
            'browserVersion': bs_config.get('browser_version', 'latest'),
            'os': bs_config.get('os', 'Windows'),
            'osVersion': bs_config.get('os_version', '11'),
            'projectName': bs_config.get('project_name', 'Aviasales Automation'),
            'buildName': bs_config.get('build_name', 'Flight Booking Test'),
            'name': f'Flight Booking - {browser_name}'
        }
        
        return capabilities, bs_config.get('username'), bs_config.get('access_key')
        
    except Exception as e:
        print(f"Error reading BrowserStack config: {e}")
        raise


if __name__ == "__main__":
    # Test the excel reader
    print("Testing Excel Reader...")
    print("\nMake sure you have created 'test_data.xlsx' file with proper structure.")
    print("\nExpected Excel structure:")
    print("Column A: Field Name | Column B: Value")
    print("Example:")
    print("url | https://www.aviasales.kz")
    print("from_city | Астана")
    print("to_city | Уральск")
