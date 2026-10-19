

import duckdb
from sqlglot import parse, exp

DB_PATH = "operations.duckdb"

POVOLENE_SLOUPCE = {
    "id", "datum", "zarizeni",
    "typ_udalosti", "popis"
}

POVOLENE_FUNKCE = {
    "count", "sum", "avg", "min", "max",
    "extract", "date_part"
}

def proved_dotaz(sql):
    prikazy = parse(sql, read="duckdb")

    if len(prikazy) != 1:
        raise ValueError("Povolen je pouze jeden SQL dotaz.")

    strom = prikazy[0]

    if not isinstance(strom, exp.Select):
        raise ValueError("Povolen je pouze SELECT.")

    # Zakážeme vnořené dotazy a CTE
    if list(strom.find_all(exp.Subquery, exp.CTE)):
        raise ValueError("Vnořené dotazy nejsou povoleny.")

    # Povolená je pouze jedna tabulka
    tabulky = list(strom.find_all(exp.Table))
    if len(tabulky) != 1 or tabulky[0].name.lower() != "udalosti":
        raise ValueError("Nepovolená tabulka.")

    # Zákaz spojování tabulek
    if list(strom.find_all(exp.Join)):
        raise ValueError("JOIN není povolen.")

    # Kontrola sloupců
    for sloupec in strom.find_all(exp.Column):
        if sloupec.name.lower() not in POVOLENE_SLOUPCE:
            raise ValueError(f"Nepovolený sloupec: {sloupec.name}")

    # Zákaz libovolných funkcí
    
    # Kontrola SQL funkcí
    for funkce in strom.find_all(exp.Func):

        # Logické operátory AND, OR a NOT
        # kontrolujeme odděleně od funkcí.
        if isinstance(funkce, (exp.And, exp.Or, exp.Not)):
            continue

        nazev = funkce.sql_name().lower()

        print("Kontroluji SQL funkci:", nazev)

        if nazev not in POVOLENE_FUNKCE:
            raise ValueError(
                f"Nepovolená SQL funkce: {nazev}"
            )


    con = duckdb.connect(DB_PATH, read_only=True)

    try:
        return con.execute(sql).fetchall()
    finally:
        con.close()
