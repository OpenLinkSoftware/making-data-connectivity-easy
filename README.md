# Making Data Connectivity Easy
A collection of programs aimed as simplifying and demystifing open standards based data connectivity.

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

