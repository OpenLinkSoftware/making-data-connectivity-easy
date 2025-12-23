/**
 * basic-odbc-query.ts
 *
 * Executes a single SQL or SPARQL query provided at initialization time.
 *
 * Usage:
 *   node basic-odbc-query.js "<QUERY>"
 *   node basic-odbc-query.js "<QUERY>" [DSN] [UID] [PWD]
 *
 * Examples:
 *   node basic-odbc-query.js "SELECT 1"
 *
 *   node basic-odbc-query.js \
 *     "SPARQL SELECT * WHERE { ?s ?p ?o } LIMIT 10" \
 *     MyVirtuosoDSN dba dba
 */

import * as odbc from 'odbc';

/*
 * Defaults
 */
const DEFAULT_DSN = 'MyVirtuosoDSN';
const DEFAULT_UID = 'dba';
const DEFAULT_PWD = 'dba';

/*
 * CLI arguments
 * argv[2] = query (required)
 * argv[3] = DSN
 * argv[4] = UID
 * argv[5] = PWD
 */
const [, , query, cliDsn, cliUid, cliPwd] = process.argv;

if (!query) {
  console.error('Error: query argument is required.');
  process.exit(1);
}

const DSN = cliDsn || DEFAULT_DSN;
const UID = cliUid || DEFAULT_UID;
const PWD = cliPwd || DEFAULT_PWD;

const connectionString = `DSN=${DSN};UID=${UID};PWD=${PWD};`;

async function main() {
  try {
    console.log(`Connecting via DSN='${DSN}' as UID='${UID}'`);
    console.log(`Executing query:\n${query}\n`);

    const connection = await odbc.connect(connectionString);
    const result = await connection.query(query);

    console.log('Result:');
    console.dir(result, { depth: null });

    await connection.close();
  } catch (err) {
    console.error('Execution failed:', err);
    process.exit(1);
  }
}

main();
