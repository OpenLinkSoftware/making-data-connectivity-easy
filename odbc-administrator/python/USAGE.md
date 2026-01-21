# ODBC DSN Manager - Usage Guide

This guide provides detailed instructions for using the ODBC DSN Manager.

## Table of Contents

- [Getting Started](#getting-started)
- [Main Menu Options](#main-menu-options)
- [Testing DSN Connections](#testing-dsn-connections)
- [Managing DSNs](#managing-dsns)
- [Driver Management](#driver-management)
- [Configuration Management](#configuration-management)
- [Keyboard Navigation](#keyboard-navigation)

## Getting Started

1. **Launch the Manager**:
   ```bash
   python3 odbc-driver-manager-3.py
   ```

2. **Initial Setup**:
   - On first run, you'll be prompted to select configuration files
   - Choose your `odbc.ini` and `odbcinst.ini` files
   - These settings are saved for future sessions

3. **Main Menu**:
   - Use arrow keys to navigate
   - Press Enter to select
   - Press 'q' or ESC to cancel

## Main Menu Options

### 1. Show DSN Details

View comprehensive configuration for existing DSNs:

```
1. Select "Show DSN details" from main menu
2. Choose a DSN from the detailed list
3. View all configuration parameters
4. Press Enter to return to main menu
```

**Features**:
- Shows driver information
- Displays all connection parameters
- Groups DSNs by driver type
- Paginated display for large DSN lists

### 2. Test a DSN

Test connection to an existing DSN:

```
1. Select "Test a DSN" from main menu
2. Choose a DSN from the simple circular menu
3. Select ODBC manager (unixODBC/iODBC/Both)
4. Choose credential options
5. View connection test results
6. Select continuation options
```

**Features**:
- Simple circular menu selection
- No unnecessary configuration displays
- Clear connection status messages
- Options to retry or test different DSNs

### 3. Test a Custom DSN

Directly test any DSN by name:

```
1. Select "Test a custom DSN" from main menu
2. Enter the DSN name
3. Select ODBC manager
4. View connection test results
```

**Features**:
- Direct input without browsing
- Fast connection testing
- Clear success/failure messages
- Immediate results display

### 4. Add a New DSN

Create a new DSN configuration:

```
1. Select "Add a new DSN" from main menu
2. Enter DSN name
3. Select driver from available drivers
4. Enter connection parameters
5. Configure essential OpenLink settings
6. Option to test immediately
```

**Features**:
- Step-by-step DSN creation
- Driver selection from registered drivers
- Essential OpenLink settings included
- Immediate testing option

### 5. List Installed Drivers

View all registered ODBC drivers:

```
1. Select "List installed drivers" from main menu
2. View driver list with status
3. Press Enter to return to main menu
```

**Features**:
- Shows driver names and library paths
- Indicates driver file existence
- Simple list format

### 6. Show Driver Details

View detailed driver configuration:

```
1. Select "Show driver details" from main menu
2. Choose a driver from the list
3. View complete driver configuration
4. Press Enter to return to main menu
```

**Features**:
- Shows all driver parameters
- Displays library paths
- Shows driver configuration details

### 7. Register a New Driver

Add a new ODBC driver:

```
1. Select "Register a new driver" from main menu
2. Enter driver name
3. Enter driver library path
4. Add optional description
5. Driver is registered in odbcinst.ini
```

**Features**:
- Driver name validation
- Library path verification
- Automatic odbcinst.ini updates

### 8. Reconfigure Files

Change ODBC configuration files:

```
1. Select "Reconfigure files" from main menu
2. Go through configuration setup again
3. Select new odbc.ini and odbcinst.ini files
4. Settings are updated for current session
```

**Features**:
- Change configuration files anytime
- Updates environment variables
- Immediate effect

### 9. Refresh

Reload current configuration:

```
1. Select "Refresh" from main menu
2. Configuration is reloaded
3. Returns to main menu
```

**Features**:
- Reloads DSN and driver lists
- Updates configuration settings
- Quick refresh option

### 10. Exit

Quit the application:

```
1. Select "Exit" from main menu
2. Application closes cleanly
```

## Testing DSN Connections

### Connection Testing Process

1. **Connection Attempt**: The manager uses `pyodbc.connect()` for real connection testing
2. **Test Query**: Executes `SELECT 1` to verify connection works
3. **Result Display**: Shows "Connection successful!" or specific error messages
4. **Environment Setup**: Automatically sets `ODBCINI` and `ODBCINST` environment variables

### Connection Test Results

**Successful Connection**:
```
Testing DSN: MySQL_Production
─────────────────────────────────────────────────────────────────
Attempting connection to DSN: MySQL_Production
Connection successful!
─────────────────────────────────────────────────────────────────
✓ DSN 'MySQL_Production' is working

Press Enter to continue...
```

**Failed Connection**:
```
Testing DSN: NonExistentDSN
─────────────────────────────────────────────────────────────────
Attempting connection to DSN: NonExistentDSN
Connection failed: ('IM002', '[IM002] [unixODBC][Driver Manager]Data source name not found and no default driver specified (0) (SQLDriverConnect)')
─────────────────────────────────────────────────────────────────
✗ DSN 'NonExistentDSN' failed connection tests

Press Enter to continue...
```

## Managing DSNs

### DSN Configuration Files

The manager works with standard ODBC configuration files:

- **odbc.ini**: Contains DSN definitions
- **odbcinst.ini**: Contains driver definitions

### DSN Creation Best Practices

1. **Use Descriptive Names**: Choose meaningful DSN names
2. **Include Essential Settings**: Add required OpenLink settings
3. **Test Immediately**: Verify the DSN works after creation
4. **Document Configuration**: Note connection parameters

### Essential OpenLink Settings

The manager automatically includes these essential settings:
- `WideAsUTF16=Yes` - Critical for Unicode support
- `Daylight=Yes` - Timezone handling
- `RoundRobin=No` - Connection balancing
- `NoSystemTables=No` - Show system tables
- `TreatViewsAsTables=No` - View handling
- `PwdClearText=0` - Password encryption

## Driver Management

### Driver Requirements

- Driver library must be properly installed
- Library path must be correct in odbcinst.ini
- Driver must support the target database

### Common Drivers

- **MySQL**: `libmyodbc8.so` or `libmysqlodbc8.so`
- **PostgreSQL**: `psqlodbcw.so` or `psqlodbc.so`
- **SQL Server**: `libmsodbcsql.so`
- **Oracle**: `libsqora.so`
- **Snowflake**: `libSnowflake.dylib`

## Configuration Management

### Configuration File Locations

Standard ODBC configuration file locations:

**odbc.ini**:
- `~/.odbc.ini` (user-level)
- `~/Library/ODBC/odbc.ini` (user-level)
- `/etc/odbc.ini` (system-level)
- `/usr/local/etc/odbc.ini` (system-level)

**odbcinst.ini**:
- `~/.odbcinst.ini` (user-level)
- `~/Library/ODBC/odbcinst.ini` (user-level)
- `/Library/ODBC/odbcinst.ini` (system-level)
- `/etc/odbcinst.ini` (system-level)
- `/usr/local/etc/odbcinst.ini` (system-level)

### Environment Variables

Key environment variables:
- `ODBCINI`: Path to odbc.ini file
- `ODBCINST`: Path to odbcinst.ini file
- `ODBCINSTINI`: Alternative path to odbcinst.ini (for iODBC)

## Keyboard Navigation

### Menu Navigation

- **↑/↓ Arrow Keys**: Navigate menu options
- **Enter**: Select highlighted option
- **q or ESC**: Cancel/quit current operation
- **Tab**: Move between input fields (where applicable)

### Circular Menu Features

- **Wraparound Navigation**: Arrow keys wrap around menu options
- **Highlighted Selection**: Current selection is clearly marked with `►`
- **Consistent Behavior**: Same navigation in all menus

### Input Fields

- **Text Input**: Type directly in input fields
- **Password Input**: Hidden input for passwords
- **Confirmation**: Clear confirmation prompts

## Troubleshooting

See [TROUBLESHOOTING.md](TROUBLESHOOTING.md) for common issues and solutions.
