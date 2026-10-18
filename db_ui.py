

import duckdb

# Připojení k databázi
con = duckdb.connect("operations.duckdb")

# Spuštění grafického rozhraní
con.execute("CALL start_ui()")

print("DuckDB UI běží. Pro ukončení stiskni Enter.")

# Udržení programu v chodu
input()

con.close()
