## **Usage**

This project provides a simple Node.js / TypeScript example for executing SQL or SPARQL queries against an ODBC Data Source Name (DSN), such as a Virtuoso server, using the odbc package and unixODBC.

### **Prerequisites **

* Node.js (arm64 on Apple Silicon recommended) -- if running from macOS
* unixODBC installed and configured
* An ODBC DSN registered in odbc.ini
* The odbc npm package installed
* TypeScript (if using the .ts variant)

Verify DSN availability:

```
odbcinst -q -s
```

---

### **Build (TypeScript only)**

Compile the TypeScript source to JavaScript:

```
npx tsc basic-odbc-query.ts
```

This produces:

```
basic-odbc-query.js
```

> If you are using the JavaScript-only version, no build step is required.

---

### **Run**

The script executes **one query provided at startup** .

#### **Basic usage**

```
node basic-odbc-query.js "<QUERY>"
```

Example:

```
node basic-odbc-query.js "SELECT 1"
```

---

### **Override connection parameters**

By default, the script uses built-in values for DSN, UID, and PWD.

These can be overridden via command-line arguments.

```
node basic-odbc-query.js "<QUERY>" [DSN] [UID] [PWD]
```

Example:

```
node basic-odbc-query.js \
  "SELECT * FROM DB.DBA.SYS_USERS" \
  VirtuosoLocal dba dba
```

---

### **SPARQL queries**

Virtuoso accepts SPARQL over ODBC when the query is prefixed with SPARQL.

Example:

```
node basic-odbc-query.js \
  "SPARQL SELECT ?s ?p ?o WHERE { ?s ?p ?o } LIMIT 10" \
  VirtuosoLocal dba dba
```

---

### **Notes**

* The DSN **must** be registered with unixODBC (odbc.ini)
* The associated ODBC driver **must** be registered (odbcinst.ini)
* The script mirrors the invocation model of isql:

```
isql DSN UID PWD
```

* Any IM002 error indicates a DSN or driver configuration issue, not a code issue

---

### **Troubleshooting**

Verify connectivity outside Node.js:

```
isql VirtuosoLocal dba dba
```

If this fails, fix the ODBC configuration before running the script.

