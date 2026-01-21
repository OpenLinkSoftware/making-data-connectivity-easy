# ODBC DSN Manager - Troubleshooting Guide

This guide helps resolve common issues with the ODBC DSN Manager.

## Table of Contents

- [General Issues](#general-issues)
- [Connection Issues](#connection-issues)
- [Configuration Issues](#configuration-issues)
- [Driver Issues](#driver-issues)
- [Performance Issues](#performance-issues)
- [Error Messages](#error-messages)

## General Issues

### Program won't start

**Symptoms**:
- Error when running `python3 odbc-driver-manager-3.py`
- Python or module import errors

**Solutions**:

1. **Check Python installation**:
   ```bash
   python3 --version
   ```
   Should show Python 3.6 or higher

2. **Install missing dependencies**:
   ```bash
   pip install pyodbc
   ```

3. **Check file permissions**:
   ```bash
   chmod +x odbc-driver-manager-3.py
   ```

### No DSNs appear in the list

**Symptoms**:
- Empty DSN list
- "No DSNs configured" message

**Solutions**:

1. **Check ODBCINI environment variable**:
   ```bash
   echo $ODBCINI
   ```
   Should point to your odbc.ini file

2. **Verify odbc.ini file**:
   ```bash
   cat $ODBCINI
   ```
   Should contain DSN definitions

3. **Check file location**:
   - Try common locations: `~/.odbc.ini`, `/etc/odbc.ini`
   - Use "Reconfigure files" option to select correct file

### Menu navigation not working

**Symptoms**:
- Arrow keys don't work
- Can't select menu options

**Solutions**:

1. **Check terminal compatibility**:
   - Use standard terminal (Terminal.app, iTerm2)
   - Avoid remote terminals with limited support

2. **Try alternative keys**:
   - Use `j`/`k` for down/up if arrow keys fail
   - Use `Tab` to cycle through options

3. **Check curses library**:
   ```bash
   python3 -c "import curses; print('curses OK')"
   ```

## Connection Issues

### Connection failed: Data source name not found (IM002)

**Symptoms**:
- Error: `IM002 [unixODBC][Driver Manager]Data source name not found`
- DSN exists but connection fails

**Solutions**:

1. **Check DSN name spelling**:
   - Verify exact DSN name in odbc.ini
   - Check for typos or case sensitivity

2. **Verify driver registration**:
   ```bash
   odbcinst -j  # For unixODBC
   iodbctest    # For iODBC
   ```

3. **Check driver path in odbcinst.ini**:
   - Ensure driver library path is correct
   - Verify library file exists

### Connection failed: Invalid credentials

**Symptoms**:
- Authentication failed
- Invalid username/password

**Solutions**:

1. **Verify credentials**:
   - Double-check username and password
   - Try connecting with other tools first

2. **Check DSN configuration**:
   - Verify host, port, database name
   - Check for special characters in credentials

3. **Test with DSN credentials**:
   - Use option "Use credentials from DSN configuration"
   - Check if credentials are stored in DSN

### Connection failed: Driver not found

**Symptoms**:
- Driver library not found
- Invalid driver path

**Solutions**:

1. **Check driver library path**:
   ```bash
   ls -la /path/to/driver.so
   ```

2. **Verify driver in odbcinst.ini**:
   - Check Driver= path in odbcinst.ini
   - Ensure path is absolute and correct

3. **Reinstall driver**:
   - Reinstall ODBC driver package
   - Verify installation with package manager

## Configuration Issues

### ODBCINI environment variable not set

**Symptoms**:
- Configuration file not found
- Default locations not working

**Solutions**:

1. **Set environment variable**:
   ```bash
   export ODBCINI=/path/to/odbc.ini
   ```

2. **Add to shell profile**:
   ```bash
   echo 'export ODBCINI=/path/to/odbc.ini' >> ~/.bashrc
   source ~/.bashrc
   ```

3. **Use Reconfigure option**:
   - Select "Reconfigure files" from main menu
   - Choose correct configuration files

### Wrong configuration file selected

**Symptoms**:
- DSNs not appearing
- Drivers not found

**Solutions**:

1. **Check current files**:
   - Main menu shows "DSN File" and "Driver File"
   - Verify these are correct

2. **Reconfigure files**:
   - Select "Reconfigure files" from main menu
   - Choose correct odbc.ini and odbcinst.ini

3. **Check file contents**:
   ```bash
   cat /path/to/odbc.ini
   cat /path/to/odbcinst.ini
   ```

### Configuration file permissions

**Symptoms**:
- Permission denied errors
- Can't write configuration

**Solutions**:

1. **Check file permissions**:
   ```bash
   ls -la /path/to/odbc.ini
   ```

2. **Fix permissions**:
   ```bash
   chmod 644 /path/to/odbc.ini
   chown $USER /path/to/odbc.ini
   ```

3. **Use user-level files**:
   - Use `~/.odbc.ini` instead of system files
   - No sudo required for user files

## Driver Issues

### Driver not registered

**Symptoms**:
- Driver not in list
- Can't select driver when adding DSN

**Solutions**:

1. **Register driver manually**:
   - Select "Register a new driver" from main menu
   - Enter driver name and library path

2. **Check odbcinst.ini**:
   ```bash
   cat /path/to/odbcinst.ini
   ```
   - Verify driver section exists
   - Check Driver= path is correct

3. **Reinstall driver package**:
   ```bash
   brew reinstall unixodbc  # or libiodbc
   ```

### Driver library not found

**Symptoms**:
- Driver path invalid
- Library file missing

**Solutions**:

1. **Verify library path**:
   ```bash
   ls -la /path/to/driver.so
   ```

2. **Find correct path**:
   ```bash
   find / -name "driver.so" 2>/dev/null
   ```

3. **Update odbcinst.ini**:
   - Correct the Driver= path
   - Use absolute paths

### Driver version mismatch

**Symptoms**:
- Driver works with other tools but not this manager
- Version compatibility issues

**Solutions**:

1. **Check driver version**:
   ```bash
   strings /path/to/driver.so | grep version
   ```

2. **Update driver**:
   - Install latest driver version
   - Check vendor website for updates

3. **Try different driver**:
   - Some vendors provide multiple driver versions
   - Try alternative drivers for same database

## Performance Issues

### Slow DSN listing

**Symptoms**:
- Delay when loading DSN list
- Slow menu navigation

**Solutions**:

1. **Reduce DSN count**:
   - Remove unused DSNs from odbc.ini
   - Archive old configurations

2. **Optimize configuration files**:
   - Remove comments and whitespace
   - Simplify complex configurations

3. **Use user-level files**:
   - User-level files are faster than system files
   - `~/.odbc.ini` instead of `/etc/odbc.ini`

### Connection timeout

**Symptoms**:
- Connection attempts take too long
- Timeout errors

**Solutions**:

1. **Check network connectivity**:
   - Verify database server is reachable
   - Test with ping or telnet

2. **Adjust timeout settings**:
   - Add timeout parameters to DSN
   - Check database-specific settings

3. **Test locally first**:
   - Verify local connections work
   - Rule out network issues

## Error Messages

### IM002 - Data source name not found

**Cause**: DSN not found in odbc.ini or driver not registered

**Solution**:
- Verify DSN exists in odbc.ini
- Check driver registration in odbcinst.ini
- Use exact DSN name (case-sensitive)

### IM003 - Specified driver could not be loaded

**Cause**: Driver library not found or invalid

**Solution**:
- Verify driver library path in odbcinst.ini
- Check file permissions on driver library
- Reinstall ODBC driver

### IM004 - Driver's SQLAllocHandle on SQL_HANDLE_ENV failed

**Cause**: Driver initialization failed

**Solution**:
- Check driver compatibility
- Update to latest driver version
- Verify driver dependencies

### 08001 - Unable to connect

**Cause**: Network or authentication issue

**Solution**:
- Verify database server is running
- Check network connectivity
- Verify credentials
- Test with other ODBC tools

### 08004 - Server rejected connection

**Cause**: Server-side connection limit or firewall

**Solution**:
- Check database server logs
- Verify firewall settings
- Check connection limits

### HY000 - General error

**Cause**: Various driver-specific issues

**Solution**:
- Check driver documentation
- Enable driver logging
- Test with minimal configuration

## Additional Resources

### ODBC Configuration Tools

```bash
# unixODBC tools
odbcinst -j        # Show configuration
isbql             # Interactive SQL tool

# iODBC tools  
iodbctest         # Test tool
iodbc-config      # Configuration info
```

### Debugging ODBC

```bash
# Enable ODBC tracing
export ODBCTRACE=1
export ODBCTRACEFILE=/tmp/odbc.log

# Run your application
python3 odbc-driver-manager-3.py

# Check trace log
tail -f /tmp/odbc.log
```

### Checking ODBC Installation

```bash
# Check unixODBC installation
which odbcinst
odbcinst -j

# Check iODBC installation
which iodbctest
iodbctest

# Check Python ODBC support
python3 -c "import pyodbc; print(pyodbc.version)"
```

## Getting Help

### Common Commands

```bash
# Show ODBC configuration
odbcinst -j

# Test ODBC connection
isbql -v DSN=YourDSN

# List ODBC drivers
iodbctestw

# Check Python environment
python3 -c "import sys; print(sys.version)"
```

### Support Resources

- **unixODBC Documentation**: http://www.unixodbc.org/
- **iODBC Documentation**: http://www.iodbc.org/
- **pyodbc Documentation**: https://github.com/mkleehammer/pyodbc
- **ODBC Specification**: https://docs.microsoft.com/en-us/sql/odbc/

### Troubleshooting Steps

1. **Verify basic connectivity**
2. **Check configuration files**
3. **Test with simple tools first**
4. **Enable logging/tracing**
5. **Isolate the issue**
6. **Search for specific error messages**

This troubleshooting guide should help resolve most common issues with the ODBC DSN Manager. If you encounter issues not covered here, please check the project documentation or open an issue with specific error details.