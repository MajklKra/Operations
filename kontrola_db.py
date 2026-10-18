
import duckdb

# Připojení k existující databázi
con = duckdb.connect("operations.duckdb", read_only=True)

# Načtení všech záznamů
vysledek = con.execute("""
    SELECT *
    FROM udalosti
    ORDER BY id
""").fetchdf()

# Zobrazení dat
print(vysledek.to_string(index=False))

con.close()

print()

con = duckdb.connect("operations.duckdb", read_only=True)

# Zjištění struktury tabulky
vysledek = con.execute("""
    DESCRIBE udalosti;
""").fetchdf()

print(vysledek.to_string(index=False))

con.close()
