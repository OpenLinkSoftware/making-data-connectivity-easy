# ODBC DSN Manager for macOS

A comprehensive ODBC Data Source Name (DSN) management tool for macOS with support for both iODBC and unixODBC.

## Features

- **Test DSN Connections**: Directly test ODBC connections with real connection attempts
- **DSN Management**: Add, view, and manage DSN configurations
- **Driver Management**: Register and manage ODBC drivers
- **Circular Menu Navigation**: Easy-to-use cursor-based interface
- **Multi-Manager Support**: Works with both iODBC and unixODBC
- **Comprehensive Configuration**: Full ODBC configuration management

## Installation

### Prerequisites

- Python 3.6+
- pyodbc library
- iODBC or unixODBC installed

### Install Dependencies

```bash
# Install Python if not already installed
brew install python

# Install pyodbc
pip install pyodbc

# Install ODBC manager (choose one)
brew install unixodbc  # For unixODBC
# OR
brew install libiodbc  # For iODBC
```

### Quick Start

```bash
# Clone or download the repository
git clone https://github.com/your-repo/odbc-dsn-manager.git
cd odbc-dsn-manager

# Run the manager
python3 odbc-driver-manager-3.py
```

## Usage

See [USAGE.md](USAGE.md) for detailed usage instructions.

## Configuration

See [CONFIGURATION.md](CONFIGURATION.md) for ODBC configuration setup.

## Troubleshooting

See [TROUBLESHOOTING.md](TROUBLESHOOTING.md) for common issues and solutions.

## License

This project is open source and available under the MIT License.

## Support

For issues, questions, or contributions, please open an issue on the GitHub repository.

## Contributing

Contributions are welcome! Please follow the standard GitHub flow:

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to your branch
5. Open a Pull Request

## Roadmap

- Add support for DSN export/import
- Implement DSN validation
- Add connection pooling options
- Enhance driver configuration
- Add GUI interface option

## Contact

For more information, contact the project maintainers.
