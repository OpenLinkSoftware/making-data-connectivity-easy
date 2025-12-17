## Generic .NET ODBC Console Application

This document describes a minimal, cross-platform .NET console application that connects to any ODBC-accessible database using an ODBC DSN (Data Source Name).

It is intended to run on any operating system (Windows, macOS, Linux etc) where:

The .NET SDK or runtime is available
A compatible ODBC driver is installed
A working ODBC DSN has been configured

---

### What

This project is a **simple .NET console application** that:

- Uses the `System.Data.Odbc` provider
- Connects to a database via an **ODBC DSN**
- Executes a SQL query
- Prints results to standard output

It serves as a **template** or **reference implementation** for validating `ODBC`connectivity from `.NET` across platforms.

---

### Why

This example is useful when you need to:

- Verify that an `ODBC` driver is correctly installed and configured
- Test database connectivity independently of vendor-specific SDKs
- Create a portable `.NET` database client that works across operating systems
- Use legacy or enterprise databases that expose `ODBC` but not native `.NET` drivers

Using `ODBC` provides a **vendor-neutral abstraction layer**, allowing the same application code to work with many different databases and operating systems simply by changing the `ODBC DSN` and `SQL query`.

---

### How

#### 1. Project File (`ODBCDemo.csproj`)

This project file is intentionally minimal and portable.

```xml
<Project Sdk="Microsoft.NET.Sdk">

  <PropertyGroup>
    <OutputType>Exe</OutputType>
    <TargetFramework>net8.0</TargetFramework>
    <ImplicitUsings>enable</ImplicitUsings>
    <Nullable>enable</Nullable>
  </PropertyGroup>

  <ItemGroup>
    <PackageReference Include="System.Data.Odbc" Version="10.0.1" />
  </ItemGroup>

</Project>
```

**Notes**

* `net8.0` can be replaced with another supported `.NET` version if required
* `System.Data.Odbc` is the only external dependency

#### 2. Application Code (Program.cs)

This version uses placeholders so it can be adapted to any database and ODBC DSN.

```
using System;
using System.Data.Odbc;

namespace ODBCDemo
{
    class Program
    {
        static void Main(string[] args)
        {
            // TODO: Replace with your actual DSN, username, and password
            string connStr = "DSN=<YOUR_DSN_NAME>;UID=<USERNAME>;PWD=<PASSWORD>;";
            Console.WriteLine($"Using connection: {connStr}");

            using (OdbcConnection conn = new OdbcConnection(connStr))
            {
                try
                {
                    conn.Open();
                    Console.WriteLine("Connected to database via ODBC DSN!");

                    // TODO: Replace with a valid SQL query for your database
                    string sql = "SELECT <COLUMNS> FROM <SCHEMA>.<TABLE>";
                    using (OdbcCommand cmd = new OdbcCommand(sql, conn))
                    using (OdbcDataReader reader = cmd.ExecuteReader())
                    {
                        while (reader.Read())
                        {
                            // Example: print first column
                            Console.WriteLine(reader[0].ToString());
                        }
                    }

                    conn.Close();
                }
                catch (Exception ex)
                {
                    Console.WriteLine("Error: " + ex.Message);
                }
            }
        }
    }
}
```

**Customization Points**

* **DSN=<YOUR_DSN_NAME>** → Name of your configured ODBC DSN
* **UID / PWD** → Database authentication credentials
* **SQL query** → Must be valid for your target database dialect

#### 3. ODBC DSN Configuration (OS-Independent Concept)

Although the tools differ by OS, the concept is the same everywhere:

* Install the appropriate `ODBC` driver for your database
* Create a `ODBC DSN` that references that driver
* Test the `ODBC DSN` using the OS-provided ODBC tools

**Important considerations:**

* Driver bitness (32-bit vs 64-bit) must match the .NET runtime
* System ODBC DSNs are recommended for non-interactive applications
* ODBC DSN names are case-sensitive on some platforms

#### 4. Environment & Runtime Requirements

* `.NET` SDK or Runtime installed (dotnet --version to verify)
* `ODBC` driver properly installed and licensed if required
* `ODBC DSN` visible to the user or system context running the application

On non-Windows platforms, ensure:

* `ODBCINI` and `ODBCINSTINI` environment variables (if applicable) point to valid configuration files
* The driver shared libraries are discoverable by the runtime loader

#### 5. Build & Run

From the project directory containing the `ODBCDemo.csproj` and `program.cs` files only, run the following command to build and run the .Net application:

```
dotnet clean
dotnet build -f net8.0
dotnet run -f net8.0
```

**Notes**

* Environment Variables on macOS**

```
export ODBCINI="$HOME/Library/ODBC/odbc.ini"
export ODBCSYSINI="/Library/ODBC"
export DYLD_LIBRARY_PATH="/opt/homebrew/lib"
```

For GUI apps:

```
launchctl setenv ODBCINI "$HOME/Library/ODBC/odbc.ini"
launchctl setenv ODBCSYSINI "/Library/ODBC"
launchctl setenv DYLD_LIBRARY_PATH "/opt/homebrew/lib"
```
#### 6. Expected Output (Example)

```
Using connection: DSN=<YOUR_DSN_NAME>;UID=<USERNAME>;PWD=<PASSWORD>;
Connected to database via ODBC DSN!
<ROW_VALUE_1>
<ROW_VALUE_2>
<ROW_VALUE_3>
...
```

Actual output will depend on:

* The SQL query
* The database contents
* The column(s) selected

#### Summary

This template demonstrates the simplest possible ODBC-based .NET application:

* One project file
* One source file
* One DSN
* One SQL query

By changing only the ODBC DSN and SQL query, the same code can be reused across:

* Databases
* Vendors
* Operating systems

It is intended as a foundation, not a framework—ideal for diagnostics, demos, and integration validation.
