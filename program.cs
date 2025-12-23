using System;
using System.Data.Odbc;

namespace ODBCDemo
{
    class Program
    {
        static void Main(string[] args)
        {
            // TODO: Replace with your actual DSN, username, and password
            string connStr = "DSN=sqllu-uda10;UID=openlink;PWD=Odbc@mssql;";
            Console.WriteLine($"Using connection: {connStr}");

            using (OdbcConnection conn = new OdbcConnection(connStr))
            {
                try
                {
                    conn.Open();
                    Console.WriteLine("Connected to database via ODBC DSN!");

                    // TODO: Replace with a valid SQL query for your database
                    string sql = "SELECT TOP 5 * FROM Customers";
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
