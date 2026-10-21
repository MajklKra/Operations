
from database import proved_dotaz

sql = """
SELECT COUNT(*) AS pocet_poruch
FROM udalosti
WHERE zarizeni = 'D'
  AND typ_udalosti = 'Porucha'
"""

vysledek = proved_dotaz(sql)

# print(vysledek.to_string(index=False))


pocet = vysledek[0][0]

print(f"Výsledek dotazu: {pocet}")