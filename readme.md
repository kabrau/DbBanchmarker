# Db Banchmarker

You need create .env file, you can see "example .env"


> $ python ./run.py

```
Command: SELECT now()
AWS - Times: 0.021s | 0.021s | 0.024s - Rows: 1
GCP - Times: 0.021s | 0.025s | 0.023s - Rows: 1
== Tie
Command: SELECT COUNT(*) FROM logacoes
AWS - Times: 10.817s | 0.765s | 0.797s - Rows: 1
GCP - Times: 0.547s | 0.277s | 0.306s - Rows: 1
== Absolute Winner: GCP
Command: SELECT * FROM analises a ORDER BY a.status DESC LIMIT 100
AWS - Times: 0.094s | 0.075s | 0.084s - Rows: 100
GCP - Times: 0.079s | 0.086s | 0.083s - Rows: 100
== Tie
Command: SELECT * FROM analises LIMIT 10000
AWS - Times: 1.840s | 2.129s | 1.814s - Rows: 10000
GCP - Times: 2.587s | 2.120s | 1.681s - Rows: 10000
== Winners: AWS | Tie | GCP
Command: SELECT * FROM logresponseocrqueue l ORDER BY l.datacadastro DESC LIMIT 1000
AWS - Times: 7.152s | 7.191s | 7.202s - Rows: 1000
GCP - Times: 7.329s | 7.971s | 7.172s - Rows: 1000
== Winners: AWS | AWS | Tie
Command: UPDATE usuarios SET senhasantigas = CONCAT(IFNULL(senhasantigas,""), R...
AWS - Times: 0.250s | 0.156s | 0.188s - Rows: None
GCP - Times: 0.195s | 0.123s | 0.115s - Rows: None
== Tie
Command: SELECT a.EnderecoUf, COUNT(*) FROM analisebmg AS a WHERE a.EnderecoUf ...
AWS - Times: 2.086s | 1.149s | 1.446s - Rows: 29
GCP - Times: 0.635s | 0.611s | 0.617s - Rows: 29
== Absolute Winner: GCP
Command: INSERT INTO logevents (`Level`, `Template`, `Message`, `Exception`) VA...
AWS - Times: 0.072s | 0.072s | 0.135s - Rows: None
GCP - Times: 0.067s | 0.069s | 0.063s - Rows: None
== Tie
Command: SELECT a.id, a.datacadastro, a.cpfcliente, sl.`status`, sl.json->>"$.e...
AWS - Times: 6.554s | 1.977s | 1.496s - Rows: 1000
GCP - Times: 0.857s | 0.871s | 0.805s - Rows: 1000
== Absolute Winner: GCP
Command: SELECT a.id, sl.id, lc.id, ls.id, e.id, r.id FROM analises AS a  LEFT ...
AWS - Times: 3.614s | 0.751s | 0.721s - Rows: 10000
GCP - Times: 0.676s | 0.506s | 0.421s - Rows: 10000
== Absolute Winner: GCP
```