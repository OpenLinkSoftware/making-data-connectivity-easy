import java.sql.Connection;
import java.sql.DatabaseMetaData;
import java.sql.DriverManager;
import java.sql.SQLException;
import java.sql.Driver;
import java.util.Enumeration;
import java.util.ArrayList;
import java.util.List;
import java.util.Scanner;
import java.io.Console;

public class UniversalJDBCTest {

    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);
        Console console = System.console();

        System.out.println("=== Universal JDBC Connection Test ===\n");

        // Collect registered JDBC drivers
        List<Driver> driverList = new ArrayList<>();
        Enumeration<Driver> drivers = DriverManager.getDrivers();
        System.out.println("Available JDBC Drivers:\n");

        int index = 1;
        while (drivers.hasMoreElements()) {
            Driver driver = drivers.nextElement();
            driverList.add(driver);
            System.out.printf("%d) %s (v%d.%d)\n",
                    index++, driver.getClass().getName(),
                    driver.getMajorVersion(), driver.getMinorVersion());
        }

        if (driverList.isEmpty()) {
            System.out.println("⚠️ No JDBC drivers are registered with DriverManager.");
            System.out.println("Make sure your driver JARs are on the classpath.");
            scanner.close();
            return;
        }

        // Prompt user to select a driver
        System.out.print("\nSelect a driver by number: ");
        int driverChoice = -1;
        while (driverChoice < 1 || driverChoice > driverList.size()) {
            if (scanner.hasNextInt()) {
                driverChoice = scanner.nextInt();
                if (driverChoice < 1 || driverChoice > driverList.size()) {
                    System.out.print("Invalid choice. Please enter a valid driver number: ");
                }
            } else {
                System.out.print("Please enter a number: ");
                scanner.next(); // discard invalid input
            }
        }
        scanner.nextLine(); // consume newline

        Driver selectedDriver = driverList.get(driverChoice - 1);
        System.out.println("\nSelected Driver: " + selectedDriver.getClass().getName());

        // Prompt for connection parameters
        System.out.print("\nEnter JDBC URL (e.g., jdbc:oracle:thin:@host:port:sid): ");
        String jdbcUrl = scanner.nextLine().trim();

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

        // Attempt connection
        System.out.println("\nConnecting...");
        try (Connection conn = DriverManager.getConnection(jdbcUrl, username, password)) {
            DatabaseMetaData metaData = conn.getMetaData();

            System.out.println("\n=== Connection Metadata ===");
            System.out.println("JDBC Driver Name: " + metaData.getDriverName());
            System.out.println("JDBC Driver Version: " + metaData.getDriverVersion());
            System.out.println("JDBC Spec Version: " +
                    metaData.getJDBCMajorVersion() + "." + metaData.getJDBCMinorVersion());
            System.out.println("Database Product Name: " + metaData.getDatabaseProductName());
            System.out.println("Database Product Version: " + metaData.getDatabaseProductVersion());
            System.out.println("\n✅ Connection successful!");
        } catch (SQLException e) {
            System.err.println("\n❌ SQL Error: " + e.getMessage());
            e.printStackTrace();
        } finally {
            scanner.close();
        }
    }
}