# **pyODBC Python Example**

This Python script demonstrates how to connect to **ODBC Data Source Name (DSN)** on **macOS, Linux, or Windows** .

---

## **Prerequisites**

### **Python & pyodbc**

1. **Python 3** installed (python3 recommended).
2. **pyodbc** Python package:

```
python3 -m pip install pyodbc
```

---

### **ODBC Driver Manager**

* **macOS:**

```
brew install unixodbc
```

* **Linux (Debian/Ubuntu):**

```
sudo apt update
sudo apt install unixodbc unixodbc-dev
```

* **Linux (RHEL/CentOS/Fedora):**

```
sudo yum install unixODBC unixODBC-devel
```

* **Windows:** Use the built-in **ODBC Data Source Administrator** to configure DSNs.

---

### **Virtuoso ODBC Driver**

1. Install the **Virtuoso ODBC driver** for your platform.
2. Configure a **DSN** pointing to your Virtuoso instance:
  * Example DSN: VirtuosoODBC

---

### **Architecture Considerations**

* **macOS (Apple Silicon):** Python, unixODBC, and Virtuoso ODBC driver should all be **arm64**.
* **Linux:** Ensure Python and ODBC driver architectures match (x86_64 vs arm64).
* **Windows:** Python, ODBC driver, and DSN must be consistent (32-bit vs 64-bit).

---

## **Usage**

1. Edit the script to specify your DSN, username, and password:

```
DSN_NAME = "VirtuosoODBC"
USERNAME = "dba"
PASSWORD = "dba"
```

2. Run the script:

```
python3 basic-odbc-example.py
```

3. Expected output:

```
Connected successfully. Test query returned: 1
```

4. You can replace the test query with your own SQL or SPARQL queries.

---

## **Notes**

* **macOS:** Install Xcode CLI tools if pyodbc needs to build from source:

```
xcode-select --install
```

* **Linux:** Ensure unixodbc-dev is installed to compile pyodbc.
* **Verify ODBC drivers and DSNs** :

```
# List available ODBC drivers
odbcinst -q -d

# List DSNs
odbcinst -q -s
```

* The script works cross-platform if DSN, drivers, and Python are correctly installed and architecturally compatible.
