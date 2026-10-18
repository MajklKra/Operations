
import pandas as pd

# Načtení Excelu
df = pd.read_excel("Operations.xlsx")

# Výpis prvních pěti záznamů
print(df.head())

# Výpis celkového počtu záznamů
print("Počet záznamů:", len(df))
