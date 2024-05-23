import time
import MySQLdb
from dotenv import load_dotenv
import os

# Load variables from the .env file
load_dotenv()

# Connection parameters for the databases
db1_name = os.getenv('DB1_NAME')
db1_config = {
    "host": os.getenv('DB1_HOST'),
    "user": os.getenv('DB1_USER'),
    "password": os.getenv('DB1_PASS'),
    "database": os.getenv('DB1_DB')
}

db2_name = os.getenv('DB2_NAME')
db2_config = {
    "host": os.getenv('DB2_HOST'),
    "user": os.getenv('DB2_USER'),
    "password": os.getenv('DB2_PASS'),
    "database": os.getenv('DB2_DB')
}

# SQL queries to be executed
queries = [
    "SELECT now()",
    "SELECT COUNT(*) FROM logacoes",
    "SELECT * FROM analises a ORDER BY a.status DESC LIMIT 100",
    "SELECT * FROM analises LIMIT 10000",
    "SELECT * FROM logresponseocrqueue l ORDER BY l.datacadastro DESC LIMIT 1000",
    "UPDATE usuarios SET senhasantigas = CONCAT(IFNULL(senhasantigas,\"\"), ROUND(RAND()*100),\";\") WHERE ativo = 0",
    "SELECT a.EnderecoUf, COUNT(*) FROM analisebmg AS a WHERE a.EnderecoUf IS NOT NULL GROUP BY a.EnderecoUf"
]

# 1000 Inserts
insert_start = "INSERT INTO logevents (`Level`, `Template`, `Message`, `Exception`) VALUES "
value = "('test', NOW(), 'test', 'test')"
values = ", ".join([value] * 1000)
full_insert = insert_start + values + ";"

queries.append(full_insert)

# Various Left Joins
query = """SELECT a.id, a.datacadastro, a.cpfcliente, sl.`status`, sl.json->>"$.error" AS ERROR, sl.json->>"$.version" AS Version, r.enviado,
r.json->>"$.Analise.Sistema", 
r.json->>"$.Analise.OCR.TipoDocumento", 
e.codename,
lc.description,
ls.statuscode,
ls.score
FROM analises AS a 
LEFT JOIN logresponseocrqueue AS sl ON sl.analiseid = a.id AND sl.datacadastro >= a.dataenvio
LEFT JOIN log_calculo_score AS lc ON lc.analiseid = a.id AND lc.datetime >= a.dataenvio AND lc.description NOT LIKE "%>>> PROCESSO PELA PLATAFORMA WEB <<<%"
LEFT JOIN logserpro AS ls ON ls.analiseid = a.id
LEFT JOIN empresas AS e ON e.id = a.empresaid
LEFT JOIN resultadoqueue AS r ON r.analiseid = a.id
WHERE 
sl.masterType = "CNH"
AND a.datacadastro >= "2023-01-01"
ORDER BY a.id DESC
LIMIT 1000
"""

queries.append(query)

query = """SELECT a.id, sl.id, lc.id, ls.id, e.id, r.id
FROM analises AS a 
LEFT JOIN logresponseocrqueue AS sl ON sl.analiseid = a.id AND sl.datacadastro >= a.dataenvio
LEFT JOIN log_calculo_score AS lc ON lc.analiseid = a.id AND lc.datetime >= a.dataenvio AND lc.description NOT LIKE "%>>> PROCESSO PELA PLATAFORMA WEB <<<%"
LEFT JOIN logserpro AS ls ON ls.analiseid = a.id
LEFT JOIN empresas AS e ON e.id = a.empresaid
LEFT JOIN resultadoqueue AS r ON r.analiseid = a.id
WHERE 
a.datacadastro >= "2023-01-01" AND sl.masterType = "CNH" 
LIMIT 10000
"""
queries.append(query)

# Function to execute a query and measure the time
def execute_query(db_config, query):
    try:
        # Connect to the database
        db = MySQLdb.connect(**db_config)
        cursor = db.cursor()

        # Start timer
        start = time.time()

        # Execute query
        cursor.execute(query)

        # Get results
        result = cursor.fetchall()

        # Stop timer
        end = time.time()

        # Calculate execution time
        execution_time = end - start

        # Close cursor and connection
        cursor.close()
        db.close()

        # Return execution time and number of rows (if applicable)
        if result:
            return execution_time, len(result)
        else:
            return execution_time, None
    except Exception as e:
        print(f"Error executing query: {e}")
        return None, None

# Execute benchmark for each database and query
for query in queries:
    print(f"Command: {query[:70] + '...' if len(query) > 75 else query}".replace('\n', ' '))

    # Execute on Database 1
    execution_time1, rows1 = execute_query(db1_config, query)

    # Execute on Database 2
    execution_time2, rows2 = execute_query(db2_config, query)

    # Execute on Database 1
    execution_time1b, rows1b = execute_query(db1_config, query)

    # Execute on Database 2
    execution_time2b, rows2b = execute_query(db2_config, query)

    # Execute on Database 1
    execution_time1c, rows1c = execute_query(db1_config, query)

    # Execute on Database 2
    execution_time2c, rows2c = execute_query(db2_config, query)

    print(f"{db1_name} - Times: {execution_time1:.3f}s | {execution_time1b:.3f}s | {execution_time1c:.3f}s - Rows: {rows1}")
    print(f"{db2_name} - Times: {execution_time2:.3f}s | {execution_time2b:.3f}s | {execution_time2c:.3f}s - Rows: {rows2}")

    tie_threshold = 0.1

    # Compare execution times
    if abs(execution_time1 - execution_time2) < tie_threshold:
        winner = "Tie"    
    elif execution_time1 < execution_time2:
        winner = db1_name
    elif execution_time1 > execution_time2:
        winner = db2_name
    else:
        winner = "Tie"

    # Compare execution times
    if abs(execution_time1b - execution_time2b) < tie_threshold:
        winnerb = "Tie"    
    elif execution_time1b < execution_time2b:
        winnerb = db1_name
    elif execution_time1b > execution_time2b:
        winnerb = db2_name
    else:
        winnerb = "Tie"        

    # Compare execution times
    if abs(execution_time1c - execution_time2c) < tie_threshold:
        winnerc = "Tie"    
    elif execution_time1c < execution_time2c:
        winnerc = db1_name
    elif execution_time1c > execution_time2c:
        winnerc = db2_name
    else:
        winnerc = "Tie"

    if winner == winnerb == winnerc == "Tie":
        print(f"== Tie")
    elif winner == winnerb == winnerc:
        print(f"== Absolute Winner: {winner}")
    else:   
        print(f"== Winners: {winner} | {winnerb} | {winnerc}")
