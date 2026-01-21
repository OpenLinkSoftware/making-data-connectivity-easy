  #!/usr/bin/env python3
"""
ODBC DSN Manager for macOS
Standard ODBC Administrator for iODBC and unixODBC with cursor-based navigation

USAGE:
    python3 odbc-driver-manager-3.py

FEATURES:
    - Test DSNs with direct connection attempts
    - Show detailed DSN configuration information
    - Add new DSNs with comprehensive settings
    - Register new ODBC drivers
    - List installed drivers with status
    - Reconfigure ODBC configuration files
    - Circular menu navigation for easy selection

OPTIONS:
    The main menu provides these operations:
    
    1. Show DSN details - View comprehensive DSN configuration
    2. Test a DSN - Test connection to an existing DSN
    3. Test a custom DSN - Directly test any DSN by name
    4. Add a new DSN - Create new DSN with essential settings
    5. List installed drivers - View registered ODBC drivers
    6. Show driver details - View driver configuration
    7. Register a new driver - Add new ODBC driver
    8. Reconfigure files - Change ODBC configuration files
    9. Refresh - Reload current configuration
    10. Exit - Quit the application

NAVIGATION:
    - Use ↑/↓ arrow keys to navigate menus
    - Press Enter to select an option
    - Press 'q' or ESC to cancel/quit
    - Follow on-screen prompts for input

REQUIREMENTS:
    - Python 3.x
    - pyodbc library (pip install pyodbc)
    - iODBC or unixODBC installed
    - Proper ODBC configuration files

EXAMPLES:
    Test an existing DSN:
        1. Select "Test a DSN" from main menu
        2. Choose DSN from circular menu
        3. Select ODBC manager (unixODBC/iODBC/Both)
        4. View connection results
    
    Add a new DSN:
        1. Select "Add a new DSN" from main menu
        2. Enter DSN name and connection parameters
        3. DSN is created with essential OpenLink settings
        4. Option to test immediately

TROUBLESHOOTING:
    - If DSNs don't appear, check ODBCINI environment variable
    - Run 'odbcinst -j' to verify configuration file locations
    - Ensure drivers are properly registered in odbcinst.ini
    - Check that database servers are running and accessible
"""

import os
import sys
import subprocess
import configparser
import curses
from pathlib import Path
from collections import defaultdict

class ODBCManager:
    def __init__(self):
        self.has_unixodbc = False
        self.has_iodbc = False
        
        # ODBC configuration files
        self.odbcini = None  # DSN definitions
        self.odbcinst = None  # Driver definitions
        
    def detect_odbc_managers(self):
        """Detect which ODBC managers are available"""
        self.has_unixodbc = subprocess.run(['which', 'odbcinst'], 
                                          capture_output=True).returncode == 0
        self.has_iodbc = (subprocess.run(['which', 'iodbctest'], 
                                        capture_output=True).returncode == 0 
                         or Path('/Library/ODBC').exists())
        
        if not self.has_unixodbc and not self.has_iodbc:
            print("Error: Neither unixODBC nor iODBC found on this system")
            print("\nTo install:")
            print("  iODBC:    brew install libiodbc")
            print("  unixODBC: brew install unixodbc")
            sys.exit(1)
    
    def locate_config_files(self):
        """Locate ODBC configuration files using standard locations"""
        print("\n" + "="*63)
        print("ODBC Configuration")
        print("="*63)
        
        # Check environment variables first
        env_odbcini = os.environ.get('ODBCINI')
        env_odbcinst = os.environ.get('ODBCINST') or os.environ.get('ODBCINSTINI')
        
        print("\nEnvironment variables:")
        print(f"  ODBCINI: {env_odbcini or '<not set>'}")
        print(f"  ODBCINST: {env_odbcinst or '<not set>'}")
        print()
        
        # Standard search paths for odbc.ini
        odbcini_paths = []
        if env_odbcini:
            odbcini_paths.append(env_odbcini)
        odbcini_paths.extend([
            str(Path.home() / '.odbc.ini'),
            str(Path.home() / 'Library/ODBC/odbc.ini'),
            '/etc/odbc.ini',
            '/usr/local/etc/odbc.ini',
        ])
        
        # Remove duplicates while preserving order
        seen = set()
        odbcini_paths = [x for x in odbcini_paths if not (x in seen or seen.add(x))]
        
        # Standard search paths for odbcinst.ini
        odbcinst_paths = []
        if env_odbcinst:
            odbcinst_paths.append(env_odbcinst)
        odbcinst_paths.extend([
            str(Path.home() / '.odbcinst.ini'),
            str(Path.home() / 'Library/ODBC/odbcinst.ini'),
            '/Library/ODBC/odbcinst.ini',
            '/etc/odbcinst.ini',
            '/usr/local/etc/odbcinst.ini',
        ])
        
        # Remove duplicates while preserving order
        seen = set()
        odbcinst_paths = [x for x in odbcinst_paths if not (x in seen or seen.add(x))]
        
        print("Available odbc.ini files:")
        found_odbcini = []
        for i, path in enumerate(odbcini_paths, 1):
            if Path(path).exists():
                print(f"  {i}) {path} ✓")
                found_odbcini.append(path)
            else:
                print(f"  {i}) {path} (not found)")
        
        print("\nAvailable odbcinst.ini files:")
        found_odbcinst = []
        for i, path in enumerate(odbcinst_paths, 1):
            if Path(path).exists():
                print(f"  {i}) {path} ✓")
                found_odbcinst.append(path)
            else:
                print(f"  {i}) {path} (not found)")
        
        print()
        
        # Select odbc.ini
        if found_odbcini:
            if len(found_odbcini) == 1:
                self.odbcini = found_odbcini[0]
                print(f"Using odbc.ini: {self.odbcini}")
            else:
                choice = self.menu_select(
                    "Select odbc.ini file:",
                    found_odbcini + ["Specify custom path"]
                )
                if choice == -1:
                    print("Configuration cancelled")
                    sys.exit(0)
                elif choice < len(found_odbcini):
                    self.odbcini = found_odbcini[choice]
                else:
                    self.odbcini = input("Enter path to odbc.ini: ").strip()
        else:
            create = input("No odbc.ini found. Create one? (y/n): ").strip().lower()
            if create == 'y':
                options = [
                    f"{Path.home()}/.odbc.ini (user-level)",
                    f"{Path.home()}/Library/ODBC/odbc.ini (user-level)",
                    "/etc/odbc.ini (system-level, requires sudo)",
                    "Custom path"
                ]
                choice = self.menu_select("Where should it be created?", options)
                
                if choice == -1:
                    print("Configuration cancelled")
                    sys.exit(0)
                elif choice == 0:
                    self.odbcini = str(Path.home() / '.odbc.ini')
                elif choice == 1:
                    self.odbcini = str(Path.home() / 'Library/ODBC/odbc.ini')
                    Path(self.odbcini).parent.mkdir(parents=True, exist_ok=True)
                elif choice == 2:
                    self.odbcini = '/etc/odbc.ini'
                else:
                    self.odbcini = input("Enter path: ").strip()
                
                Path(self.odbcini).parent.mkdir(parents=True, exist_ok=True)
                Path(self.odbcini).touch()
                print(f"Created: {self.odbcini}")
            else:
                print("Cannot proceed without odbc.ini")
                sys.exit(1)
        
        # Select odbcinst.ini
        if found_odbcinst:
            if len(found_odbcinst) == 1:
                self.odbcinst = found_odbcinst[0]
                print(f"Using odbcinst.ini: {self.odbcinst}")
            else:
                choice = self.menu_select(
                    "Select odbcinst.ini file:",
                    found_odbcinst + ["Specify custom path"]
                )
                if choice == -1:
                    # Use first found as default
                    self.odbcinst = found_odbcinst[0]
                    print(f"Using default: {self.odbcinst}")
                elif choice < len(found_odbcinst):
                    self.odbcinst = found_odbcinst[choice]
                else:
                    self.odbcinst = input("Enter path to odbcinst.ini: ").strip()
        else:
            # Default to same directory as odbc.ini
            odbcinst_default = str(Path(self.odbcini).parent / 'odbcinst.ini')
            create = input(f"No odbcinst.ini found. Create at {odbcinst_default}? (y/n): ").strip().lower()
            if create == 'y':
                self.odbcinst = odbcinst_default
                Path(self.odbcinst).parent.mkdir(parents=True, exist_ok=True)
                Path(self.odbcinst).touch()
                print(f"Created: {self.odbcinst}")
            else:
                custom = input("Enter path to odbcinst.ini (or press Enter to skip): ").strip()
                if custom:
                    self.odbcinst = custom
                else:
                    print("Warning: No driver configuration file selected")
        
        # Set environment variables
        if self.odbcini:
            os.environ['ODBCINI'] = self.odbcini
        if self.odbcinst:
            os.environ['ODBCINST'] = self.odbcinst
            os.environ['ODBCINSTINI'] = self.odbcinst  # For iODBC
        
        print()
        print("="*63)
        print()
    
    def menu_select(self, title, options, stdscr=None):
        """Display a cursor-based menu and return selected index"""
        def _menu(stdscr):
            curses.curs_set(0)  # Hide cursor
            current = 0
            
            while True:
                stdscr.clear()
                h, w = stdscr.getmaxyx()
                
                # Title
                stdscr.addstr(0, 0, title, curses.A_BOLD)
                stdscr.addstr(1, 0, "─" * min(len(title), w-1))
                
                # Menu items
                for idx, option in enumerate(options):
                    y = idx + 3
                    if y >= h - 1:
                        break
                    
                    if idx == current:
                        stdscr.addstr(y, 0, f"► {option}", curses.A_REVERSE)
                    else:
                        stdscr.addstr(y, 0, f"  {option}")
                
                # Instructions
                if len(options) + 5 < h:
                    stdscr.addstr(h-2, 0, "↑/↓: Navigate  Enter: Select  q: Quit", curses.A_DIM)
                
                stdscr.refresh()
                
                # Handle input
                key = stdscr.getch()
                
                if key == curses.KEY_UP:
                    # Circular navigation: up from top goes to bottom
                    if current > 0:
                        current -= 1
                    else:
                        current = len(options) - 1
                elif key == curses.KEY_DOWN:
                    # Circular navigation: down from bottom goes to top
                    if current < len(options) - 1:
                        current += 1
                    else:
                        current = 0
                elif key == ord('\n') or key == curses.KEY_ENTER or key == 10:
                    return current
                elif key == ord('q') or key == ord('Q') or key == 27:  # ESC
                    return -1
        
        if stdscr is None:
            return curses.wrapper(_menu)
        else:
            return _menu(stdscr)
    
    def read_ini_file(self, filepath):
        """Read an INI file, handling duplicates and malformed entries"""
        if not filepath or not Path(filepath).exists():
            return {}
        
        # Read file manually to handle duplicates
        dsn_dict = {}
        current_section = None
        
        try:
            with open(filepath, 'r') as f:
                for line_num, line in enumerate(f, 1):
                    line = line.strip()
                    
                    # Skip empty lines and comments
                    if not line or line.startswith(('#', ';')):
                        continue
                    
                    # Section header
                    if line.startswith('[') and line.endswith(']'):
                        section_name = line[1:-1].strip()
                        
                        # Skip ODBC Data Sources section
                        if section_name in ['ODBC', 'ODBC Data Sources']:
                            current_section = None
                            continue
                        
                        # Handle duplicates by appending number
                        original_name = section_name
                        counter = 1
                        while section_name in dsn_dict:
                            section_name = f"{original_name}__{counter}"
                            counter += 1
                        
                        if section_name != original_name:
                            print(f"Warning: Duplicate section '{original_name}' renamed to '{section_name}'")
                        
                        current_section = section_name
                        dsn_dict[current_section] = {}
                    
                    # Key-value pair
                    elif '=' in line and current_section is not None:
                        key, value = line.split('=', 1)
                        key = key.strip()
                        value = value.strip()
                        dsn_dict[current_section][key] = value
        
        except Exception as e:
            print(f"Warning: Error reading {filepath}: {e}")
        
        return dsn_dict
    
    def write_ini_file(self, filepath, config):
        """Write an INI file"""
        try:
            Path(filepath).parent.mkdir(parents=True, exist_ok=True)
            with open(filepath, 'w') as f:
                config.write(f, space_around_delimiters=True)
            return True
        except PermissionError:
            print(f"Error: Permission denied writing to {filepath}")
            print("Try running with sudo or using a different location")
            return False
        except Exception as e:
            print(f"Error writing to {filepath}: {e}")
            return False
    
    def list_dsns_grouped(self, show_details=True):
        """List DSNs grouped by driver"""
        if show_details:
            print("\n" + "="*63)
            print(f"Data Source Names (DSNs)")
            print(f"File: {self.odbcini}")
            print("="*63)
        
        if not self.odbcini or not Path(self.odbcini).exists():
            if show_details:
                print("  (odbc.ini not found)")
                print("="*63)
                print()
            return []
        
        dsn_dict = self.read_ini_file(self.odbcini)
        
        if not dsn_dict:
            if show_details:
                print("  (No DSNs configured)")
                print("="*63)
                print()
            return []
        
        # Group DSNs by driver (case-insensitive lookup)
        driver_dsns = defaultdict(list)
        
        for dsn_name, dsn_config in dsn_dict.items():
            # Try case-insensitive lookup for Driver key
            driver = 'unknown'
            for key, value in dsn_config.items():
                if key.lower() == 'driver':
                    driver = value.strip()
                    break
            driver_dsns[driver].append(dsn_name)
        
        # Sort DSNs alphabetically within each driver group
        for driver in sorted(driver_dsns.keys()):
            driver_dsns[driver].sort()
        
        # Display grouped by driver with alphabetical sorting and paging
        dsn_number = 0
        numbered_dsns = []
        dsns_per_page = 20  # Show 20 DSNs per page
        current_page = 1
        
        if show_details:
            for driver in sorted(driver_dsns.keys()):
                print(f"\nDriver: {driver}")
                print("─"*63)
                
                # Implement paging for large DSN lists
                for i, dsn in enumerate(driver_dsns[driver]):
                    dsn_number += 1
                    print(f"  {dsn_number}. {dsn}")
                    numbered_dsns.append(dsn)
                    
                    # Add paging every dsns_per_page DSNs
                    if dsn_number % dsns_per_page == 0 and dsn_number < len([d for dsns in driver_dsns.values() for d in dsns]):
                        print(f"\n--- Page {current_page} (Press Enter for more) ---")
                        input()  # Wait for user to continue
                        current_page += 1
            
            print(f"\n{'='*63}")
            print(f"Total: {dsn_number} DSNs")
            print("="*63)
            print()
        else:
            # Simple flat list without details
            for driver in sorted(driver_dsns.keys()):
                numbered_dsns.extend(driver_dsns[driver])
        
        return numbered_dsns
    
    def show_dsn_details(self, dsn_name):
        """Show detailed configuration for a DSN"""
        print(f"\nDSN: {dsn_name}")
        print("─"*63)
        
        if not self.odbcini or not Path(self.odbcini).exists():
            print(f"Error: {self.odbcini} doesn't exist")
            return None
        
        dsn_dict = self.read_ini_file(self.odbcini)
        
        if dsn_name not in dsn_dict:
            print("DSN not found")
            return None
        
        for key, value in dsn_dict[dsn_name].items():
            # Mask passwords
            if key.upper() in ['PWD', 'PASSWORD']:
                print(f"{key} = ********")
            else:
                print(f"{key} = {value}")
        
        print("─"*63)
        print()
        
        return dsn_dict[dsn_name]
    
    def test_dsn_unixodbc(self, dsn_name, username=None, password=None):
        """Test DSN with unixODBC using standard ODBC calls
        
        Uses Python's pyodbc library for standard ODBC testing instead of isql
        """
        print("Testing with unixODBC (standard ODBC)...")
        
        # Build connection string - simple format for pyodbc
        if username and password:
            conn_str = f"DSN={dsn_name};UID={username};PWD={password}"
            display_conn_str = f"DSN={dsn_name};UID={username};PWD={'*' * len(password)}"
        else:
            conn_str = f"DSN={dsn_name}"
            display_conn_str = f"DSN={dsn_name}"
        
        try:
            import pyodbc
            print(f"Debug: unixODBC connection string: {display_conn_str}")
            
            # Set environment variables for unixODBC
            import os
            if self.odbcini:
                os.environ['ODBCINI'] = self.odbcini
            
            # Set ODBCINST - this is critical for driver lookup
            odbcinst_path = self.odbcinst
            if not odbcinst_path:
                # If not explicitly set, try to find it
                odbcinst_path = os.environ.get('ODBCINST')
                if not odbcinst_path:
                    # Try common locations
                    common_locations = [
                        '/Library/ODBC/odbcinst.ini',
                        '/usr/local/etc/odbcinst.ini',
                        str(Path.home() / '.odbcinst.ini')
                    ]
                    for location in common_locations:
                        if Path(location).exists():
                            odbcinst_path = location
                            break
            
            if odbcinst_path:
                os.environ['ODBCINST'] = odbcinst_path
                os.environ['ODBCINSTINI'] = odbcinst_path
                print(f"Debug: Set ODBCINST to {odbcinst_path}")
            else:
                print("Warning: ODBCINST not set - driver lookup may fail")
            
            # Check for common DSN configuration issue: Driver field contains path instead of name
            # This causes IM002 errors
            dsn_config = self.read_ini_file(self.odbcini)
            if dsn_name in dsn_config:
                driver_setting = dsn_config[dsn_name].get('Driver', '')
                # If driver setting looks like a path (contains '/' or '\\'), try to fix it
                if '/' in driver_setting or '\\' in driver_setting:
                    print(f"Warning: DSN '{dsn_name}' uses driver path instead of name: {driver_setting}")
                    
                    # Try to find the correct driver name in odbcinst.ini
                    if odbcinst_path and Path(odbcinst_path).exists():
                        odbcinst_config = self.read_ini_file(odbcinst_path)
                        correct_driver_name = None
                        
                        for driver_name, driver_config in odbcinst_config.items():
                            if driver_config.get('Driver') == driver_setting:
                                correct_driver_name = driver_name
                                break
                        
                        if correct_driver_name:
                            print(f"Info: Found matching driver: {correct_driver_name}")
                            # pyodbc handles spaces in DSN names automatically - no quoting needed
                            if username and password:
                                conn_str = f"DSN={dsn_name};UID={username};PWD={password}"
                                display_conn_str = f"DSN={dsn_name};UID={username};PWD={'*' * len(password)}"
                            else:
                                conn_str = f"DSN={dsn_name}"
                                display_conn_str = f"DSN={dsn_name}"

                            print(f"Debug: Using corrected connection string: {display_conn_str}")
                        else:
                            print("Error: Could not find matching driver in odbcinst.ini")
            
            # Connect using pyodbc - use the exact format from working example
            print(f"Debug: Attempting connection with: pyodbc.connect('{conn_str}')")
            try:
                conn = pyodbc.connect(conn_str)
                cursor = conn.cursor()
                
                # Test query
                cursor.execute("SELECT 'Connection OK' AS Status")
                result = cursor.fetchone()
                
                cursor.close()
                conn.close()
                
                if result and result[0] == 'Connection OK':
                    print("✓ unixODBC connection successful")
                    return True
                else:
                    print("✗ unixODBC connection failed - unexpected result")
                    return False
                    
            except pyodbc.Error as e:
                print(f"✗ unixODBC connection failed: {e}")
                print("\nTroubleshooting tips for OpenLink drivers:")
                print("  1. Check WideAsUTF16=Yes in DSN configuration")
                print("  2. Verify driver is registered in odbcinst.ini")
                print("  3. Check ODBCINI and ODBCINST environment variables")
                print("  4. Ensure database server is running and accessible")
                return False
            except Exception as e:
                print(f"✗ unixODBC connection failed: {e}")
                return False
                print("✓ unixODBC connection successful")
                return True
            else:
                print("✗ unixODBC connection failed - unexpected result")
                print(f"Connection string used: {display_conn_str}")
                return False
                
        except pyodbc.Error as e:
            print("✗ unixODBC connection failed")
            print(f"Connection string used: {display_conn_str}")
            print(f"Error: {e}")
            return False
        except ImportError:
            print("✗ pyodbc library not found - install with: pip install pyodbc")
            return False
        except Exception as e:
            print(f"✗ unixODBC connection failed: {e}")
            print(f"Connection string used: {display_conn_str}")
            return False
    
    def test_dsn_iodbc(self, dsn_name, username=None, password=None):
        """Test DSN with iODBC using standard ODBC calls
        
        Uses Python's pyodbc library for standard ODBC testing instead of iodbctest
        """
        print("Testing with iODBC (standard ODBC)...")
        
        # Build connection string - simple format for pyodbc
        if username and password:
            conn_str = f"DSN={dsn_name};UID={username};PWD={password}"
            display_conn_str = f"DSN={dsn_name};UID={username};PWD={'*' * len(password)}"
        else:
            conn_str = f"DSN={dsn_name}"
            display_conn_str = f"DSN={dsn_name}"
        
        try:
            import pyodbc
            print(f"Debug: iODBC connection string: {display_conn_str}")
            
            # Set environment variables for iODBC
            import os
            if self.odbcini:
                os.environ['ODBCINI'] = self.odbcini
            
            # Set ODBCINST - this is critical for driver lookup
            odbcinst_path = self.odbcinst
            if not odbcinst_path:
                # If not explicitly set, try to find it
                odbcinst_path = os.environ.get('ODBCINST')
                if not odbcinst_path:
                    # Try common locations
                    common_locations = [
                        '/Library/ODBC/odbcinst.ini',
                        '/usr/local/etc/odbcinst.ini',
                        str(Path.home() / '.odbcinst.ini')
                    ]
                    for location in common_locations:
                        if Path(location).exists():
                            odbcinst_path = location
                            break
            
            if odbcinst_path:
                os.environ['ODBCINST'] = odbcinst_path
                os.environ['ODBCINSTINI'] = odbcinst_path
                print(f"Debug: Set ODBCINST to {odbcinst_path}")
            else:
                print("Warning: ODBCINST not set - driver lookup may fail")
            
            # Check for common DSN configuration issue: Driver field contains path instead of name
            # This causes IM002 errors
            dsn_config = self.read_ini_file(self.odbcini)
            if dsn_name in dsn_config:
                driver_setting = dsn_config[dsn_name].get('Driver', '')
                # If driver setting looks like a path (contains '/' or '\\'), try to fix it
                if '/' in driver_setting or '\\' in driver_setting:
                    print(f"Warning: DSN '{dsn_name}' uses driver path instead of name: {driver_setting}")
                    
                    # Try to find the correct driver name in odbcinst.ini
                    if odbcinst_path and Path(odbcinst_path).exists():
                        odbcinst_config = self.read_ini_file(odbcinst_path)
                        correct_driver_name = None
                        
                        for driver_name, driver_config in odbcinst_config.items():
                            if driver_config.get('Driver') == driver_setting:
                                correct_driver_name = driver_name
                                break
                        
                        if correct_driver_name:
                            print(f"Info: Found matching driver: {correct_driver_name}")
                            # pyodbc handles spaces in DSN names automatically - no quoting needed
                            if username and password:
                                conn_str = f"DSN={dsn_name};UID={username};PWD={password}"
                                display_conn_str = f"DSN={dsn_name};UID={username};PWD={'*' * len(password)}"
                            else:
                                conn_str = f"DSN={dsn_name}"
                                display_conn_str = f"DSN={dsn_name}"

                            print(f"Debug: Using corrected connection string: {display_conn_str}")
                        else:
                            print("Error: Could not find matching driver in odbcinst.ini")

            # Connect using pyodbc
            print(f"Debug: Attempting connection with: pyodbc.connect('{conn_str}')")
            try:
                conn = pyodbc.connect(conn_str)
                cursor = conn.cursor()
                
                # Test query
                cursor.execute("SELECT 'Connection OK' AS Status")
                result = cursor.fetchone()
                
                cursor.close()
                conn.close()
                
                if result and result[0] == 'Connection OK':
                    print("✓ iODBC connection successful")
                    return True
                else:
                    print("✗ iODBC connection failed - unexpected result")
                    print(f"Connection string used: {display_conn_str}")
                    return False
                    
            except pyodbc.Error as e:
                print("✗ iODBC connection failed")
                print(f"Connection string used: {display_conn_str}")
                print("\nTroubleshooting tips for OpenLink drivers:")
                print("  1. Check WideAsUTF16=Yes in DSN configuration")
                print("  2. Verify driver is registered in odbcinst.ini")
                print("  3. Check ODBCINI and ODBCINST environment variables")
                print("  4. Ensure database server is running and accessible")
                return False
            except Exception as e:
                print(f"✗ iODBC connection failed: {e}")
                return False
            print(f"Error: {e}")
            return False
        except ImportError:
            print("✗ pyodbc library not found - install with: pip install pyodbc")
            return False
        except Exception as e:
            print(f"✗ iODBC connection failed: {e}")
            print(f"Connection string used: {display_conn_str}")
            return False
    
    def test_custom_dsn(self, dsn_name, manager=None):
        """Test a custom DSN connection - goes straight to testing without showing details"""
        print(f"\nTesting DSN: {dsn_name}")
        print("─" * 63)
        
        # Simple direct connection test
        success = self.simple_dsn_test(dsn_name, manager)
        
        print("─" * 63)
        
        if success:
            print(f"✓ DSN '{dsn_name}' is working")
        else:
            print(f"✗ DSN '{dsn_name}' failed connection tests")
        
        print()
    
    def simple_dsn_test(self, dsn_name, manager=None):
        """Simple direct DSN connection test"""
        try:
            import pyodbc
            
            # Set environment variables
            if self.odbcini:
                import os
                os.environ['ODBCINI'] = self.odbcini
            if self.odbcinst:
                os.environ['ODBCINST'] = self.odbcinst
                os.environ['ODBCINSTINI'] = self.odbcinst
            
            print(f"Attempting connection to DSN: {dsn_name}")
            
            # Try connection
            conn_str = f"DSN={dsn_name}"
            conn = pyodbc.connect(conn_str)
            cursor = conn.cursor()
            
            # Simple test query
            cursor.execute("SELECT 1")
            result = cursor.fetchone()
            
            cursor.close()
            conn.close()
            
            print("Connection successful!")
            return True
            
        except pyodbc.Error as e:
            print(f"Connection failed: {e}")
            return False
        except ImportError:
            print("Error: pyodbc library not found. Install with: pip install pyodbc")
            return False
        except Exception as e:
            print(f"Connection failed: {e}")
            return False
    
    def test_dsn(self, dsn_name, manager=None):
        """Test a DSN connection"""
        dsn_config = self.show_dsn_details(dsn_name)
        
        if not dsn_config:
            print("DSN not found or invalid")
            return
        
        # Ask for credentials
        print("Connection credentials:")
        print("  1) Use credentials from DSN configuration")
        print("  2) Enter custom credentials for this test")
        
        cred_choice = input("\nSelect (1-2, default 1): ").strip() or "1"
        
        username = None
        password = None
        
        if cred_choice == "2":
            username = input("Username: ").strip()
            if not username:
                username = None
            else:
                import getpass
                try:
                    password = getpass.getpass("Password: ")
                except:
                    password = input("Password: ").strip()
        
        print(f"\nTesting DSN: {dsn_name}")
        print("─"*63)
        
        success = False
        
        if manager == 'unixodbc' or (manager is None and self.has_unixodbc):
            success = self.test_dsn_unixodbc(dsn_name, username, password) or success
            print()
        
        if manager == 'iodbc' or (manager is None and self.has_iodbc):
            success = self.test_dsn_iodbc(dsn_name, username, password) or success
        
        print("─"*63)
        
        if success:
            print(f"✓ DSN '{dsn_name}' is working")
            
            # Offer options to continue testing
            print("\nOptions:")
            print("  1) Test the same DSN again")
            print("  2) Test a different DSN")
            print("  3) Test a different driver/manager")
            print("  4) Return to main menu")
            
            continue_choice = input("\nSelect option (1-4, default 4): ").strip() or "4"
            
            if continue_choice == "1":
                # Test the same DSN again
                self.test_dsn(dsn_name, manager)
                return
            elif continue_choice == "2":
                # Test a different DSN - return to main menu which will offer DSN selection
                return
            elif continue_choice == "3":
                # Test a different driver/manager - go to driver testing
                print("\nSwitching to driver testing...")
                self.list_drivers()
                driver_dict = {}
                if self.odbcinst and Path(self.odbcinst).exists():
                    driver_dict = self.read_ini_file(self.odbcinst)
                drivers = list(driver_dict.keys())
                
                if drivers:
                    driver_choice = self.menu_select("Select driver to test:", drivers + ["Enter custom driver name"])
                    if driver_choice == -1:
                        return
                    elif driver_choice < len(drivers):
                        driver_name = drivers[driver_choice]
                    else:
                        driver_name = input("Enter driver name: ").strip()
                else:
                    driver_name = input("Enter driver name: ").strip()
                
                if driver_name:
                    self.show_driver_details(driver_name)
                return
            # else: return to main menu (default)
        else:
            print(f"✗ DSN '{dsn_name}' failed connection tests")
            print("\nTroubleshooting tips:")
            print("  1. Verify the driver is properly installed and registered")
            print("  2. Check connection parameters (host, port, credentials)")
            print("  3. Ensure the database server is running and accessible")
            print("  4. Run 'odbcinst -j' to verify configuration file locations")
            print("  5. Check that driver name in DSN matches driver in odbcinst.ini")
            
            # Offer retry options
            print("\nOptions:")
            print("  1) Try again with different credentials")
            print("  2) Try with a different ODBC manager")
            print("  3) Test a different DSN")
            print("  4) Check driver configuration")
            print("  5) Return to main menu")
            
            retry_choice = input("\nSelect option (1-5, default 5): ").strip() or "5"
            
            if retry_choice == "1":
                # Retry with different credentials
                self.test_dsn(dsn_name, manager)
                return
            elif retry_choice == "2":
                # Try with different manager
                new_manager = self.select_manager()
                if new_manager != -1:
                    self.test_dsn(dsn_name, new_manager)
                return
            elif retry_choice == "3":
                # Test a different DSN - return to main menu which will offer DSN selection
                return
            elif retry_choice == "4":
                # Check driver configuration
                print("\nChecking driver configuration...")
                dsn_config = self.show_dsn_details(dsn_name)
                if dsn_config:
                    driver_name = dsn_config.get('Driver', '').strip()
                    if driver_name:
                        self.show_driver_details(driver_name)
                return
            # else: return to main menu (default)
        print()
    
    def list_drivers(self):
        """List installed ODBC drivers"""
        print("\n" + "="*63)
        print("Installed ODBC Drivers")
        print(f"File: {self.odbcinst}")
        print("="*63)
        
        if not self.odbcinst or not Path(self.odbcinst).exists():
            print("  (odbcinst.ini not found)")
            print("="*63)
            print()
            return []
        
        driver_dict = self.read_ini_file(self.odbcinst)
        drivers = []
        
        for driver_name, driver_config in driver_dict.items():
            drivers.append(driver_name)
            driver_path = driver_config.get('Driver', '<not specified>')
            exists = "✓" if Path(driver_path).exists() else "✗"
            print(f"  {exists} {driver_name}")
            print(f"      {driver_path}")
        
        if not drivers:
            print("  (No drivers registered)")
        
        print("\n" + "="*63)
        print()
        
        return drivers
    
    def show_driver_details(self, driver_name):
        """Show detailed information about a driver"""
        print(f"\nDriver: {driver_name}")
        print("─"*63)
        
        if not self.odbcinst or not Path(self.odbcinst).exists():
            print(f"Error: {self.odbcinst} doesn't exist")
            return
        
        driver_dict = self.read_ini_file(self.odbcinst)
        
        if driver_name not in driver_dict:
            print("Driver not found")
            return
        
        for key, value in driver_dict[driver_name].items():
            print(f"{key} = {value}")
            if key.lower() == 'driver':
                if Path(value).exists():
                    print(f"  Status: ✓ Library exists")
                else:
                    print(f"  Status: ✗ Library NOT FOUND")
        
        print("─"*63)
        print()
    
    def add_dsn(self):
        """Add a new DSN interactively"""
        print("\n" + "="*63)
        print("Add New DSN")
        print("="*63)
        
        # Show available drivers
        print("\nAvailable drivers:")
        drivers = self.list_drivers()
        
        if not drivers:
            print("Warning: No drivers registered. You may need to register a driver first.")
        
        dsn_name = input("\nDSN Name: ").strip()
        if not dsn_name:
            print("Error: DSN name cannot be empty")
            return
        
        # Select driver from list if available
        if drivers:
            print("\nSelect driver:")
            driver_choice = self.menu_select("Select driver:", drivers + ["Enter custom driver name"])
            if driver_choice == -1:
                return
            elif driver_choice < len(drivers):
                driver_name = drivers[driver_choice]
            else:
                driver_name = input("Enter driver name: ").strip()
        else:
            driver_name = input("Driver name: ").strip()
        
        if not driver_name:
            print("Error: Driver name cannot be empty")
            return
        
        # Connection parameters
        print("\nConnection parameters:")
        host = input("Host (default: localhost): ").strip() or "localhost"
        port = input("Port (default: 1111): ").strip() or "1111"
        database = input("Database (default: DB): ").strip() or "DB"
        username = input("Username (default: dba): ").strip() or "dba"
        
        import getpass
        try:
            password = getpass.getpass("Password (default: dba): ") or "dba"
        except:
            password = input("Password (default: dba): ").strip() or "dba"
        
        print(f"\nCreating DSN '{dsn_name}' in {self.odbcini}...")
        
        # Read existing config
        config = configparser.ConfigParser()
        config.optionxform = str
        
        if Path(self.odbcini).exists():
            try:
                config.read(self.odbcini)
            except:
                pass
        
        # Remove existing section if present
        if config.has_section(dsn_name):
            print(f"Removing existing DSN '{dsn_name}'...")
            config.remove_section(dsn_name)
        
        # Add new DSN
        config.add_section(dsn_name)
        config.set(dsn_name, 'Description', f'{dsn_name} DSN')
        config.set(dsn_name, 'Driver', driver_name)
        config.set(dsn_name, 'Address', f'{host}:{port}')
        config.set(dsn_name, 'Database', database)
        config.set(dsn_name, 'UID', username)
        config.set(dsn_name, 'PWD', password)
        
        # Add essential OpenLink driver settings
        print(f"\nAdding essential OpenLink driver settings for '{dsn_name}'...")
        config.set(dsn_name, 'WideAsUTF16', 'Yes')
        config.set(dsn_name, 'Daylight', 'Yes')
        config.set(dsn_name, 'RoundRobin', 'No')
        config.set(dsn_name, 'NoSystemTables', 'No')
        config.set(dsn_name, 'TreatViewsAsTables', 'No')
        config.set(dsn_name, 'PwdClearText', '0')
        
        print("✅ Added essential OpenLink settings:")
        print("   - WideAsUTF16=Yes (critical for Unicode support)")
        print("   - Daylight=Yes (timezone handling)")
        print("   - RoundRobin=No (connection balancing)")
        print("   - NoSystemTables=No (show system tables)")
        print("   - TreatViewsAsTables=No (view handling)")
        print("   - PwdClearText=0 (password encryption)")
        
        # Write config
        if self.write_ini_file(self.odbcini, config):
            print(f"✓ DSN '{dsn_name}' created")
            
            # Test
            test = input("\nTest this DSN now? (y/n): ").strip().lower()
            if test == 'y':
                manager = self.select_manager()
                if manager != -1:
                    self.test_dsn(dsn_name, manager)
    
    def add_driver(self):
        """Register a new ODBC driver"""
        print("\n" + "="*63)
        print("Register New ODBC Driver")
        print("="*63)
        
        driver_name = input("\nDriver name (e.g., 'Virtuoso', 'PostgreSQL'): ").strip()
        if not driver_name:
            print("Error: Driver name cannot be empty")
            return
        
        driver_lib = input("Driver library path (full path to .dylib/.so): ").strip()
        if not driver_lib:
            print("Error: Driver path cannot be empty")
            return
        
        if not Path(driver_lib).exists():
            print(f"Warning: Driver library not found at {driver_lib}")
            cont = input("Continue anyway? (y/n): ").strip().lower()
            if cont != 'y':
                return
        
        driver_desc = input("Description (optional): ").strip() or f"{driver_name} ODBC Driver"
        
        print(f"\nRegistering driver '{driver_name}' in {self.odbcinst}...")
        
        # Read existing config
        config = configparser.ConfigParser()
        config.optionxform = str
        
        if Path(self.odbcinst).exists():
            try:
                config.read(self.odbcinst)
            except:
                pass
        
        # Remove existing section if present
        if config.has_section(driver_name):
            print(f"Driver '{driver_name}' already exists")
            replace = input("Replace? (y/n): ").strip().lower()
            if replace == 'y':
                config.remove_section(driver_name)
            else:
                return
        
        # Add driver
        config.add_section(driver_name)
        config.set(driver_name, 'Description', driver_desc)
        config.set(driver_name, 'Driver', driver_lib)
        config.set(driver_name, 'Setup', driver_lib)
        config.set(driver_name, 'Threading', '1')
        config.set(driver_name, 'UsageCount', '1')
        
        # Write config
        if self.write_ini_file(self.odbcinst, config):
            print(f"✓ Driver '{driver_name}' registered")
    
    def select_manager(self):
        """Ask user to select ODBC manager"""
        if self.has_unixodbc and self.has_iodbc:
            options = ["unixODBC", "iODBC", "Both"]
            choice = self.menu_select("Select ODBC manager:", options)
            return {0: 'unixodbc', 1: 'iodbc', 2: None}.get(choice, -1)
        elif self.has_unixodbc:
            return 'unixodbc'
        else:
            return 'iodbc'
    
    def show_menu(self):
        """Display main menu and return selected option"""
        print("\n╔" + "═"*47 + "╗")
        print("║" + " "*12 + "ODBC DSN Manager" + " "*19 + "║")
        print("╚" + "═"*47 + "╝")
        print()
        print("ODBC Managers:")
        print(f"  {'✓' if self.has_unixodbc else '✗'} unixODBC")
        print(f"  {'✓' if self.has_iodbc else '✗'} iODBC")
        print()
        print(f"DSN File: {self.odbcini}")
        print(f"Driver File: {self.odbcinst}")
        
        menu_options = [
            "Show DSN details",
            "Test a DSN",
            "Test a custom DSN",
            "Add a new DSN",
            "─────────────",
            "List installed drivers",
            "Show driver details",
            "Register a new driver",
            "─────────────",
            "Reconfigure files",
            "Refresh",
            "Exit"
        ]
        
        choice = self.menu_select("Select operation:", menu_options)
        
        # Get DSNs only if needed (lazy loading)
        dsns = []
        if choice in [0, 1]:  # Only operations that actually need DSN list
            # Don't show details when getting DSN list for menu
            dsns = self.list_dsns_grouped(show_details=False)
        
        return choice, dsns
    
    def run(self):
        """Main program loop"""
        self.detect_odbc_managers()
        self.locate_config_files()
        
        while True:
            choice, dsns = self.show_menu()
            
            if choice == -1 or choice == 10:  # Quit or Exit
                print("Goodbye!")
                sys.exit(0)
            
            elif choice == 0:  # Show DSN details
                if dsns:
                    dsn_choice = self.menu_select("Select DSN:", dsns + ["Enter custom DSN name"])
                    if dsn_choice == -1:
                        continue
                    elif dsn_choice < len(dsns):
                        self.show_dsn_details(dsns[dsn_choice])
                    else:
                        dsn_name = input("Enter DSN name: ").strip()
                        if dsn_name:
                            self.show_dsn_details(dsn_name)
                else:
                    dsn_name = input("Enter DSN name: ").strip()
                    if dsn_name:
                        self.show_dsn_details(dsn_name)
                input("\nPress Enter to continue...")
            
            elif choice == 1:  # Test a DSN
                # Get DSN list for circular menu selection (without showing details)
                dsns = self.list_dsns_grouped(show_details=False)
                
                if dsns:
                    # Go straight to circular menu selection
                    dsn_choice = self.menu_select("Select DSN to test:", dsns + ["Enter custom DSN name"])
                    if dsn_choice == -1:
                        continue
                    elif dsn_choice < len(dsns):
                        dsn_name = dsns[dsn_choice]
                    else:
                        dsn_name = input("Enter DSN name: ").strip()
                else:
                    dsn_name = input("Enter DSN name: ").strip()
                
                if dsn_name:
                    manager = self.select_manager()
                    if manager != -1:
                        self.test_dsn(dsn_name, manager)
                        # Wait for user to see results before continuing
                        input("\nPress Enter to continue...")
                # Note: test_dsn now handles its own flow and returns to menu when done

            elif choice == 2:  # Test a custom DSN (direct manual entry)
                dsn_name = input("Enter DSN name to test: ").strip()
                if dsn_name:
                    manager = self.select_manager()
                    if manager != -1:
                        self.test_custom_dsn(dsn_name, manager)
                        # Wait for user to see results before continuing
                        input("\nPress Enter to continue...")
                # Note: test_custom_dsn goes straight to testing without showing details
            
            elif choice == 3:  # Add a new DSN
                self.add_dsn()
                input("\nPress Enter to continue...")
            
            elif choice == 5:  # List installed drivers
                self.list_drivers()
                input("Press Enter to continue...")
            
            elif choice == 6:  # Show driver details
                driver_dict = {}
                if self.odbcinst and Path(self.odbcinst).exists():
                    driver_dict = self.read_ini_file(self.odbcinst)
                drivers = list(driver_dict.keys())
                
                if drivers:
                    driver_choice = self.menu_select("Select driver:", drivers + ["Enter custom driver name"])
                    if driver_choice == -1:
                        continue
                    elif driver_choice < len(drivers):
                        driver_name = drivers[driver_choice]
                    else:
                        driver_name = input("Enter driver name: ").strip()
                else:
                    driver_name = input("Enter driver name: ").strip()
                
                if driver_name:
                    self.show_driver_details(driver_name)
                
                input("\nPress Enter to continue...")
            
            elif choice == 7:  # Register a new driver
                self.add_driver()
                input("\nPress Enter to continue...")
            
            elif choice == 9:  # Reconfigure files
                self.locate_config_files()
                input("Press Enter to continue...")
            
            elif choice == 10:  # Refresh
                continue

if __name__ == '__main__':
    manager = ODBCManager()
    try:
        manager.run()
    except KeyboardInterrupt:
        print("\n\nGoodbye!")
        sys.exit(0)
