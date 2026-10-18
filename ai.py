from datetime import datetime

import ollama

# Otázka od uživatele
otazka = input("Zadej otázku: ").strip()

# Struktura databáze Operations
schema = """
Database: DuckDB
Table: udalosti

Columns:
id BIGINT
datum TIMESTAMP
zarizeni VARCHAR
typ_udalosti VARCHAR
popis VARCHAR

Valid values:
zarizeni: A, B, C, D, E
typ_udalosti: Provoz, Údržba, Porucha
"""

aktualni_datum = datetime.now().strftime("%Y-%m-%d")

system_prompt = f"""
You are an expert DuckDB SQL generator.
Convert the user's Czech question into exactly one valid DuckDB SELECT query.

Database schema:
{schema}

Today's date: {aktualni_datum}

Date handling rules:
- The user may ask questions in Czech.
- If the user specifies a month without a year, use the current year.
- If the user specifies a year, always use that year.
- For a whole month, filter from the first day of that month (inclusive)
  to the first day of the following month (exclusive).
- Never include an additional month.
- Do not invent dates. If the date cannot be determined, return CANNOT_ANSWER.


Date range rules:
- The datum column is a TIMESTAMP.
- When the user specifies a date range, include
  the entire first and last day.
- Always use >= for the start date.
- Always use < for the day AFTER the end date.
- Never use BETWEEN for date ranges.
- Example: From October 1 to October 18, 2026:
  datum >= '2026-10-01'
  AND datum < '2026-10-19'


SQL rules:
- Return ONLY SQL, without Markdown or explanations.
- Use only the table udalosti and its listed columns.
- Use single quotes for string values.
- Generate only a SELECT query; never modify the database.
- If the question cannot be answered from the schema, return CANNOT_ANSWER.
"""

if not otazka:
    print("Nezadal jsi žádnou otázku.")
else:
    try:
        response = ollama.chat(
            model="llama3.2:latest",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": otazka},
            ],
            options={"temperature": 0},
        )
        sql = response["message"]["content"].strip()
        print("\nVygenerovaný SQL dotaz:")
        print(sql)
    except Exception as chyba:
        print(f"Nepodařilo se spojit s Ollama nebo získat odpověď: {chyba}")

# Poznámka: SQL zatím pouze zobrazujeme, nespouštíme ho nad databází.
