import javax.swing.*;
import javax.swing.border.EmptyBorder;
import javax.swing.table.DefaultTableModel;
import javax.swing.table.TableCellRenderer;
import java.awt.*;
import java.awt.event.MouseAdapter;
import java.awt.event.MouseEvent;
import java.net.URI;
import java.sql.*;
import java.util.LinkedHashMap;
import java.util.Map;

public class UniversalJDBCTestPro3 extends JFrame {

    // Connection UI
    private JComboBox<String> driverBox;
    private JTextField urlField, userField;
    private JPasswordField passField;
    private JTextArea connLogArea;
    private JButton connectButton, disconnectButton, clearConnLogButton;

    // Query UI
    private JTextArea queryArea;
    private JTable resultTable;
    private JTextArea queryLogArea;
    private JButton runQueryButton, clearQueryLogButton;

    private Connection currentConnection;

    // Driver information
    private static class DriverInfo {
        String className, urlExample, notes, defaultQuery;

        DriverInfo(String c, String u, String n, String dq) {
            className = c;
            urlExample = u;
            notes = n;
            defaultQuery = dq;
        }
    }

    private static final Map<String, DriverInfo> DRIVERS = new LinkedHashMap<>();
    static {
        DRIVERS.put("Virtuoso (OpenLink)", new DriverInfo(
                "virtuoso.jdbc4.Driver",
                "jdbc:virtuoso://localhost:1111/UID=dba/PWD=dba",
                "OpenLink Virtuoso Universal Server",
                "SELECT TOP 10 * FROM DB.DBA.RDF_QUAD"));

        DRIVERS.put("Oracle", new DriverInfo(
                "oracle.jdbc.OracleDriver",
                "jdbc:oracle:thin:@oracle-host:1521:XE",
                "Oracle Database 23c",
                "SELECT 1 FROM DUAL"));

        DRIVERS.put("PostgreSQL", new DriverInfo(
                "org.postgresql.Driver",
                "jdbc:postgresql://localhost:5432/mydb?user=postgres&password=secret",
                "PostgreSQL 42.x",
                "SELECT 1"));

        DRIVERS.put("Microsoft SQL Server", new DriverInfo(
                "com.microsoft.sqlserver.jdbc.SQLServerDriver",
                "jdbc:sqlserver://localhost:1433;databaseName=mydb;user=sa;password=YourStrong!Passw0rd;",
                "SQL Server",
                "SELECT TOP 1 1"));

        DRIVERS.put("Informix", new DriverInfo(
                "com.informix.jdbc.IfxDriver",
                "jdbc:informix-sqli://informix-host:27669/stores_demo:INFORMIXSERVER=YourInformixServer",
                "Informix Connector",
                "SELECT FIRST 1 1 FROM systables"));

        DRIVERS.put("MySQL", new DriverInfo(
                "com.mysql.cj.jdbc.Driver",
                "jdbc:mysql://localhost:3306/mydb?user=root&password=secret",
                "MySQL Connector/J",
                "SELECT 1"));

        DRIVERS.put("OpenLink Generic", new DriverInfo(
                "openlink.jdbc4.Driver",
                "jdbc:openlink://ODBC/DSN=Local Virtuoso;UID=dba;PWD=dba;",
                "OpenLink Multi-Tier JDBC",
                "SELECT 1"));
    }

    public UniversalJDBCTestPro3() {
        super("Universal JDBC Test Utility v3");
        setDefaultCloseOperation(EXIT_ON_CLOSE);
        setSize(1000, 720);
        setLocationRelativeTo(null);

        JTabbedPane tabs = new JTabbedPane();
        tabs.addTab("Connection Setup", buildConnectionPanel());
        tabs.addTab("SQL Query", buildQueryPanel());
        add(tabs);
    }

    // ---------- Connection Panel ----------
    private JPanel buildConnectionPanel() {
        JPanel panel = new JPanel(new BorderLayout(10, 10));
        panel.setBorder(new EmptyBorder(15, 15, 15, 15));

        JPanel form = new JPanel(new GridBagLayout());
        GridBagConstraints gbc = new GridBagConstraints();
        gbc.insets = new Insets(5, 5, 5, 5);
        gbc.fill = GridBagConstraints.HORIZONTAL;

        driverBox = new JComboBox<>(DRIVERS.keySet().toArray(new String[0]));
        urlField = new JTextField();
        userField = new JTextField();
        passField = new JPasswordField();

        driverBox.addActionListener(e -> {
            DriverInfo info = DRIVERS.get(driverBox.getSelectedItem());
            urlField.setText(info.urlExample);
            if (queryArea != null) {
                queryArea.setText(info.defaultQuery);
            }
        });

        gbc.gridx = 0;
        gbc.gridy = 0;
        form.add(new JLabel("Driver:"), gbc);
        gbc.gridx = 1;
        gbc.weightx = 1;
        form.add(driverBox, gbc);
        gbc.gridx = 0;
        gbc.gridy = 1;
        gbc.weightx = 0;
        form.add(new JLabel("JDBC URL:"), gbc);
        gbc.gridx = 1;
        gbc.weightx = 1;
        form.add(urlField, gbc);
        gbc.gridx = 0;
        gbc.gridy = 2;
        gbc.weightx = 0;
        form.add(new JLabel("Username:"), gbc);
        gbc.gridx = 1;
        gbc.weightx = 1;
        form.add(userField, gbc);
        gbc.gridx = 0;
        gbc.gridy = 3;
        gbc.weightx = 0;
        form.add(new JLabel("Password:"), gbc);
        gbc.gridx = 1;
        gbc.weightx = 1;
        form.add(passField, gbc);

        JPanel buttons = new JPanel(new FlowLayout(FlowLayout.RIGHT));
        connectButton = new JButton("Connect");
        disconnectButton = new JButton("Disconnect");
        clearConnLogButton = new JButton("Clear Log");
        buttons.add(connectButton);
        buttons.add(disconnectButton);
        buttons.add(clearConnLogButton);

        connLogArea = new JTextArea(15, 80);
        connLogArea.setEditable(false);
        connLogArea.setFont(new Font(Font.MONOSPACED, Font.PLAIN, 12));
        JScrollPane logScroll = new JScrollPane(connLogArea);

        panel.add(form, BorderLayout.NORTH);
        panel.add(logScroll, BorderLayout.CENTER);
        panel.add(buttons, BorderLayout.SOUTH);

        connectButton.addActionListener(e -> connectDB());
        disconnectButton.addActionListener(e -> disconnectDB());
        clearConnLogButton.addActionListener(e -> connLogArea.setText(""));

        driverBox.setSelectedIndex(0);
        return panel;
    }

    // ---------- Query Panel ----------
    private JPanel buildQueryPanel() {
        JPanel panel = new JPanel(new BorderLayout(10, 10));
        panel.setBorder(new EmptyBorder(10, 10, 10, 10));

        DriverInfo info = DRIVERS.get(driverBox.getSelectedItem());
        queryArea = new JTextArea(info.defaultQuery, 5, 80);
        queryArea.setFont(new Font(Font.MONOSPACED, Font.PLAIN, 13));
        JScrollPane queryScroll = new JScrollPane(queryArea);

        resultTable = new JTable();
        JScrollPane resultScroll = new JScrollPane(resultTable);

        queryLogArea = new JTextArea(10, 80);
        queryLogArea.setFont(new Font(Font.MONOSPACED, Font.PLAIN, 12));
        queryLogArea.setEditable(false);
        JScrollPane queryLogScroll = new JScrollPane(queryLogArea);

        runQueryButton = new JButton("Run Query");
        clearQueryLogButton = new JButton("Clear Log");
        JPanel btnPanel = new JPanel(new FlowLayout(FlowLayout.RIGHT));
        btnPanel.add(runQueryButton);
        btnPanel.add(clearQueryLogButton);

        runQueryButton.addActionListener(e -> runQuery());
        clearQueryLogButton.addActionListener(e -> queryLogArea.setText(""));

        JSplitPane splitTop = new JSplitPane(JSplitPane.VERTICAL_SPLIT, queryScroll, resultScroll);
        splitTop.setResizeWeight(0.3);
        JSplitPane splitMain = new JSplitPane(JSplitPane.VERTICAL_SPLIT, splitTop, queryLogScroll);
        splitMain.setResizeWeight(0.7);

        panel.add(splitMain, BorderLayout.CENTER);
        panel.add(btnPanel, BorderLayout.SOUTH);

        resultTable.addMouseListener(new MouseAdapter() {
            public void mouseClicked(MouseEvent evt) {
                int row = resultTable.rowAtPoint(evt.getPoint());
                int col = resultTable.columnAtPoint(evt.getPoint());
                Object val = resultTable.getValueAt(row, col);
                if (val != null && val.toString().matches("https?://.*")) {
                    try {
                        Desktop.getDesktop().browse(new URI(val.toString()));
                    } catch (Exception ex) {
                        logQuery("✗ Failed to open URL: " + ex.getMessage());
                    }
                }
            }
        });

        return panel;
    }

    // ---------- Connect/Disconnect ----------
    private void connectDB() {
        String key = (String) driverBox.getSelectedItem();
        DriverInfo info = DRIVERS.get(key);
        String url = urlField.getText().trim();
        String user = userField.getText().trim();
        String pass = new String(passField.getPassword());

        try {
            logConn("Loading driver: " + info.className);
            Class.forName(info.className);
            currentConnection = DriverManager.getConnection(url, user, pass);
            logConn("✓ Connected successfully to: " + url);
            DatabaseMetaData meta = currentConnection.getMetaData();
            logConn("Product: " + meta.getDatabaseProductName());
            logConn("Version: " + meta.getDatabaseProductVersion());
            logConn("Driver: " + meta.getDriverName() + " (" + meta.getDriverVersion() + ")");
            logConn("User: " + meta.getUserName());
        } catch (Exception ex) {
            logConn("✗ Connection failed: " + ex.getMessage());
        }
    }

    private void disconnectDB() {
        if (currentConnection != null) {
            try {
                currentConnection.close();
                logConn("✓ Connection closed.");
                currentConnection = null;
            } catch (Exception ex) {
                logConn("✗ Error closing connection: " + ex.getMessage());
            }
        } else {
            logConn("No active connection.");
        }

        // --- Reset UI to default ---
        driverBox.setSelectedIndex(0); // first driver
        DriverInfo info = DRIVERS.get(driverBox.getSelectedItem());
        urlField.setText(info.urlExample);
        userField.setText("");
        passField.setText("");
        if (queryArea != null) {
            queryArea.setText(info.defaultQuery);
        }
    }

    // ---------- Query Execution ----------
    private void runQuery() {
        if (currentConnection == null) {
            JOptionPane.showMessageDialog(this, "Please connect to a database first.",
                    "No Connection", JOptionPane.WARNING_MESSAGE);
            return;
        }

        runQueryButton.setEnabled(false);
        runQueryButton.setText("Running...");

        SwingWorker<Void, Void> worker = new SwingWorker<>() {
            @Override
            protected Void doInBackground() {
                String sql = queryArea.getText().trim();
                try (Statement stmt = currentConnection.createStatement()) {
                    boolean hasResult = stmt.execute(sql);
                    if (hasResult) {
                        ResultSet rs = stmt.getResultSet();
                        ResultSetMetaData md = rs.getMetaData();
                        int cols = md.getColumnCount();
                        String[] colNames = new String[cols];
                        for (int i = 1; i <= cols; i++)
                            colNames[i - 1] = md.getColumnLabel(i);

                        DefaultTableModel model = new DefaultTableModel(colNames, 0);
                        while (rs.next()) {
                            Object[] row = new Object[cols];
                            for (int i = 1; i <= cols; i++)
                                row[i - 1] = rs.getObject(i);
                            model.addRow(row);
                        }
                        resultTable.setModel(model);

                        for (int i = 0; i < cols; i++) {
                            resultTable.getColumnModel().getColumn(i).setCellRenderer(new LinkCellRenderer());
                        }
                        logQuery("✓ Query executed successfully. " + model.getRowCount() + " rows returned.");
                    } else {
                        logQuery("✓ Update executed successfully. " + stmt.getUpdateCount() + " rows affected.");
                    }
                } catch (Exception ex) {
                    logQuery("✗ Query failed: " + ex.getMessage());
                }
                return null;
            }

            @Override
            protected void done() {
                runQueryButton.setText("Run Query");
                runQueryButton.setEnabled(true);
            }
        };
        worker.execute();
    }

    private void logConn(String msg) {
        connLogArea.append(msg + "\n");
        connLogArea.setCaretPosition(connLogArea.getDocument().getLength());
    }

    private void logQuery(String msg) {
        queryLogArea.append(msg + "\n");
        queryLogArea.setCaretPosition(queryLogArea.getDocument().getLength());
    }

    // Custom TableCellRenderer to hyperlink URLs
    static class LinkCellRenderer extends JLabel implements TableCellRenderer {
        LinkCellRenderer() {
            setOpaque(true);
            setForeground(Color.BLUE.darker());
        }

        @Override
        public Component getTableCellRendererComponent(JTable table, Object value,
                boolean isSelected, boolean hasFocus,
                int row, int column) {
            setText(value != null ? value.toString() : "");
            if (value != null && value.toString().matches("https?://.*")) {
                setText("<html><u>" + value.toString() + "</u></html>");
            }
            setBackground(isSelected ? table.getSelectionBackground() : table.getBackground());
            return this;
        }
    }

    // ---------- Main ----------
    public static void main(String[] args) {
        SwingUtilities.invokeLater(() -> {
            UniversalJDBCTestPro3 app = new UniversalJDBCTestPro3();
            app.setVisible(true);
        });
    }
}
