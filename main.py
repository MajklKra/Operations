
import pandas as pd
import duckdb

# 1. Načtení Excelu
df = pd.read_excel("Operations.xlsx")

# 2. Přejmenování sloupců
df.columns = ["id","datum","zarizeni","typ_udalosti","popis"]

# 3. Připojení k databázi
con = duckdb.connect("operations.duckdb")

# 4. Vytvoření tabulky z Excelu
con.execute("""
    CREATE OR REPLACE TABLE udalosti AS
    SELECT * FROM df
""")

# 5. Kontrola počtu záznamů
vysledek = con.execute("""
    SELECT COUNT(*) FROM udalosti
""").fetchone()

print("Počet záznamů v databázi:", vysledek[0])

con.close()
