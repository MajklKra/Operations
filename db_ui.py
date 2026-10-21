

import duckdb

# Připojení k databázi
con = duckdb.connect("operations.duckdb")

# Spuštění grafického rozhraní
con.execute("CALL start_ui()")

# Udržení programu v chodu
input()

print("DuckDB UI běží. Pro ukončení stiskni Enter.")

con.close()
