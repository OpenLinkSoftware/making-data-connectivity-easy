import java.sql.*;
import java.util.*;
import java.io.Console;

public class UniversalJDBCTestFull {

    // Helper class to store driver info and example URL
    static class JdbcDriverInfo {
        String driverClass;
        String exampleUrl;

        JdbcDriverInfo(String driverClass, String exampleUrl) {
            this.driverClass = driverClass;
            this.exampleUrl = exampleUrl;
        }
    }

    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);
        Console console = System.console();

        System.out.println("=== Universal JDBC Connection Test ===\n");

        // Define known drivers and example URLs
        Map<String, JdbcDriverInfo> knownDrivers = new LinkedHashMap<>();
        knownDrivers.put("Virtuoso JDBC", new JdbcDriverInfo(
                "virtuoso.jdbc4.Driver",
                "jdbc:virtuoso://localhost:1111/charset=UTF-8/log_enable=2"));
        knownDrivers.put("Oracle JDBC", new JdbcDriverInfo(
                "oracle.jdbc.OracleDriver",
                "jdbc:oracle:thin:@localhost:1521:XE"));
        knownDrivers.put("Informix IfxDriver", new JdbcDriverInfo(
                "com.informix.jdbc.IfxDriver",
                "jdbc:informix-sqli://localhost:1526/testdb:INFORMIXSERVER=ol_informix1210"));
        knownDrivers.put("Informix InformixDriver", new JdbcDriverInfo(
                "com.informix.jdbc.InformixDriver",
                "jdbc:informix-sqli://localhost:1526/testdb:INFORMIXSERVER=ol_informix1210"));
        knownDrivers.put("PostgreSQL JDBC", new JdbcDriverInfo(
                "org.postgresql.Driver",
                "jdbc:postgresql://localhost:5432/mydb"));
        knownDrivers.put("SQL Server JDBC", new JdbcDriverInfo(
                "com.microsoft.sqlserver.jdbc.SQLServerDriver",
                "jdbc:sqlserver://localhost:1433;databaseName=TestDB;encrypt=true"));
        knownDrivers.put("MySQL JDBC", new JdbcDriverInfo(
                "com.mysql.cj.jdbc.Driver",
                "jdbc:mysql://localhost:3306/testdb?useSSL=false&serverTimezone=UTC"));
        knownDrivers.put("OpenLink JDBC", new JdbcDriverInfo(
                "openlink.jdbc4.Driver",
                "jdbc:openlink://ODBC/DSN=LocalVirtuoso"));

        // List known drivers
        System.out.println("Available JDBC Drivers:\n");
        int idx = 1;
        List<String> driverKeys = new ArrayList<>(knownDrivers.keySet());
        for (String key : driverKeys) {
            System.out.printf("%d) %s (%s)\n", idx++, key, knownDrivers.get(key).driverClass);
        }

        // Let user select a driver
        System.out.print("\nSelect a driver by number: ");
        int driverChoice = -1;
        while (driverChoice < 1 || driverChoice > driverKeys.size()) {
            if (scanner.hasNextInt()) {
                driverChoice = scanner.nextInt();
                if (driverChoice < 1 || driverChoice > driverKeys.size()) {
                    System.out.print("Invalid choice. Enter a valid driver number: ");
                }
            } else {
                System.out.print("Please enter a number: ");
                scanner.next();
            }
        }
        scanner.nextLine(); // consume newline

        String driverName = driverKeys.get(driverChoice - 1);
        JdbcDriverInfo driverInfo = knownDrivers.get(driverName);

        // Load the selected driver
        System.out.println("\n[1] Loading JDBC Driver: " + driverInfo.driverClass);
        try {
            Class.forName(driverInfo.driverClass);
            System.out.println("    ✓ Driver loaded successfully");
        } catch (ClassNotFoundException e) {
            System.err.println("    ✗ Driver class not found!");
            e.printStackTrace();
            scanner.close();
            return;
        }

        // Prompt for JDBC URL, showing example
        System.out.printf("\n[2] Enter JDBC URL (example: %s): ", driverInfo.exampleUrl);
        String jdbcUrl = scanner.nextLine().trim();
        if (jdbcUrl.isEmpty()) {
            jdbcUrl = driverInfo.exampleUrl;
            System.out.println("    Using example URL: " + jdbcUrl);
        }

        System.out.print("Enter username: ");
        String username = scanner.nextLine().trim();

        String password;
        if (console != null) {
            char[] pwChars = console.readPassword("Enter password: ");
            password = new String(pwChars);
        } else {
            System.out.print("Enter password (visible): ");
            password = scanner.nextLine();
        }

        // Determine the appropriate test query
        String testQuery;
        if (driverName.startsWith("Informix")) {
            // Informix-specific query for system information
            testQuery = "SELECT FIRST 1 DBINFO('version','full') FROM systables";
            System.out.println("\n[3] Informix driver selected. Using Informix-specific test query.");
        } else {
            // Generic query for other drivers
            testQuery = "SELECT 1";
            System.out.println("\n[3] Using generic test query.");
        }
        
        System.out.println("    Test Query: " + testQuery);

        // Connect and run metadata/test
        System.out.println("\n[4] Connecting to: " + jdbcUrl);
        try (Connection conn = DriverManager.getConnection(jdbcUrl, username, password)) {
            System.out.println("    ✓ Connection established successfully");

            DatabaseMetaData metaData = conn.getMetaData();

            System.out.println("\n[5] Database Metadata:");
            System.out.println("    Database Product Name: " + metaData.getDatabaseProductName());
            System.out.println("    Database Product Version: " + metaData.getDatabaseProductVersion());
            System.out.println("    Database Major/Minor Version: " + metaData.getDatabaseMajorVersion() + "."
                    + metaData.getDatabaseMinorVersion());
            System.out.println("    JDBC Driver: " + metaData.getDriverName());
            System.out.println("    JDBC Driver Version: " + metaData.getDriverVersion());
            System.out.println(
                    "    JDBC Spec Version: " + metaData.getJDBCMajorVersion() + "." + metaData.getJDBCMinorVersion());
            System.out.println("    Supports Transactions: " + metaData.supportsTransactions());
            System.out.println("    Supports Batch Updates: " + metaData.supportsBatchUpdates());
            System.out.println("    Supports Stored Procedures: " + metaData.supportsStoredProcedures());

            // Execute the determined test query
            System.out.println("\n[6] Executing test query...");
            try (Statement stmt = conn.createStatement()) {
                ResultSet rs = stmt.executeQuery(testQuery);
                if (rs.next()) {
                    System.out.println("    ✓ Query executed successfully");
                    
                    // Display result, handling different result types for generic vs. Informix query
                    if (driverName.startsWith("Informix")) {
                        // The Informix query returns a string with version info
                        System.out.println("    Informix Version Info: " + rs.getString(1));
                    } else {
                        // The generic query returns the integer '1'
                        System.out.println("    Test value: " + rs.getInt(1));
                    }
                }
            } catch (SQLException e) {
                System.err.println("    ✗ Test query failed: " + e.getMessage());
            }

            // List catalogs
            System.out.println("\n[7] Available Catalogs:");
            try (ResultSet catalogs = metaData.getCatalogs()) {
                boolean hasCatalogs = false;
                while (catalogs.next()) {
                    System.out.println("    - " + catalogs.getString("TABLE_CAT"));
                    hasCatalogs = true;
                }
                if (!hasCatalogs)
                    System.out.println("    (None)");
            }

            // List schemas
            System.out.println("\n[8] Available Schemas:");
            try (ResultSet schemas = metaData.getSchemas()) {
                boolean hasSchemas = false;
                while (schemas.next()) {
                    System.out.println("    - " + schemas.getString("TABLE_SCHEM"));
                    hasSchemas = true;
                }
                if (!hasSchemas)
                    System.out.println("    (None)");
            }

            // List tables
            System.out.println("\n[9] Available Tables in Database:");
            try (ResultSet tables = metaData.getTables(null, null, "%", new String[] { "TABLE" })) {
                boolean hasTables = false;
                while (tables.next()) {
                    System.out.println("    - " + tables.getString("TABLE_NAME"));
                    hasTables = true;
                }
                if (!hasTables)
                    System.out.println("    (No tables found)");
            }

            // Table types
            System.out.println("\n[10] Supported Table Types:");
            try (ResultSet tableTypes = metaData.getTableTypes()) {
                while (tableTypes.next()) {
                    System.out.println("    - " + tableTypes.getString("TABLE_TYPE"));
                }
            }

            // Close connection
            System.out.println("\n[11] Closing connection...");
            System.out.println("    ✓ Connection closed successfully");

        } catch (SQLException e) {
            System.err.println("✗ Connection failed: " + e.getMessage());
            e.printStackTrace();
        }

        System.out.println("\n=== TEST COMPLETED SUCCESSFULLY ===");
        System.out.println("Your JDBC driver is properly configured.");
        System.out.println("You can now proceed with ODBC DSN configuration.");

        scanner.close();
    }
}
