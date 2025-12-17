# Making Data Connectivity Easy
A collection of programs aimed at simplifying and demystifing open standards based data connectivity.

## Java Examples
Here's a Java program that interrogates its host operating enviroment (Java Virtual Machine) for currently installed drivers. The drivers discovered can then be tested for basic connectivity. 

### Why?
Use of our JDBC or ODBC-JDBC bridge drivers depends on an easy to used experience during installation, configuration, and use. 

### How?
1. Determine the location of the JAR files of each of the JDBC drivers of interest. Ideally, place them in a common directory (folder) of your choosing
2. Ensure the CLASSPATH operating system environment variable contains an entry for each of the JAR files of each of the JDBC Drivers of interest. 
3. Save the Java source code to a file e.g., `UniversalJDBCTest.java`
4. Compile the .java source code using: ` javac -cp ".:/{JDBC-JAR-FILES-DIRECTORY}/*" UniversalJDBCTest.java` e.g., ` javac -cp ".:/Library/Java/Extensions/*" UniversalJDBCTest.java`
5. Run the compiled program (.class) using: ` java -cp ".:/{JDBC-JAR-FILES-DIRECTORY}/*" UniversalJDBCTest` e.g., ` java -cp ".:/Library/Java/Extensions/*" UniversalJDBCTest` -- if you don't want to depend on $CLASSPATH for picking up JDBC Driver JAR file locations
6. Run the compiled program (.class) using: ` java UniversalJDBCTest` -- if you are depending on $CLASSPATH for picking up JDBC Driver JAR file locations


#### Usage Examples

##### Virtuoso (multi-model DBMS for supporting both SQL and SPARQL queries via JDBC)

```sh
=== Universal JDBC Connection Test ===

Available JDBC Drivers:

1) com.informix.jdbc.IfxDriver (v4.2)
2) com.informix.jdbc.InformixDriver (v15.0)
3) virtuoso.jdbc4.Driver (v3.120)
4) org.postgresql.Driver (v42.7)
5) oracle.jdbc.OracleDriver (v23.8)
6) openlink.jdbc4.Driver (v4.56)
7) com.amazonaws.athena.jdbc.AthenaDriver (v1.0)
8) com.mysql.cj.jdbc.Driver (v9.3)
9) com.microsoft.sqlserver.jdbc.SQLServerDriver (v12.10)

Select a driver by number: 3

Selected Driver: virtuoso.jdbc4.Driver

Enter JDBC URL (e.g., jdbc:oracle:thin:@host:port:sid): jdbc:virtuoso://localhost/charset=UTF-8/
Enter username: dba
Enter password: 

Connecting...

=== Connection Metadata ===
JDBC Driver Name: OpenLink Virtuoso JDBC pure Java
JDBC Driver Version: 3.120 (for Java 2 platform)
JDBC Spec Version: 3.0
Database Product Name: OpenLink Virtuoso VDBMS
Database Product Version: 08.03.3332

✅ Connection successful!
```

##### Oracle

```sh
=== Universal JDBC Connection Test ===

Available JDBC Drivers:

1) com.informix.jdbc.IfxDriver (v4.2)
2) com.informix.jdbc.InformixDriver (v15.0)
3) virtuoso.jdbc4.Driver (v3.120)
4) org.postgresql.Driver (v42.7)
5) oracle.jdbc.OracleDriver (v23.8)
6) openlink.jdbc4.Driver (v4.56)
7) com.amazonaws.athena.jdbc.AthenaDriver (v1.0)
8) com.mysql.cj.jdbc.Driver (v9.3)
9) com.microsoft.sqlserver.jdbc.SQLServerDriver (v12.10)

Select a driver by number: 5

Selected Driver: oracle.jdbc.OracleDriver

Enter JDBC URL (e.g., jdbc:oracle:thin:@host:port:sid): jdbc:oracle:thin:@54.172.89.18:1521/XE
Enter username: hr
Enter password: 

Connecting...

=== Connection Metadata ===
JDBC Driver Name: Oracle JDBC driver
JDBC Driver Version: 23.8.0.25.04
JDBC Spec Version: 4.3
Database Product Name: Oracle
Database Product Version: Oracle Database 18c Express Edition Release 18.0.0.0.0 - Production
Version 18.4.0.0.0

✅ Connection successful!
```

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
