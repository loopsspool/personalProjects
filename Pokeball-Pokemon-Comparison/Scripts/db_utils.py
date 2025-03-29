import sqlite3
import os

from spreadsheet_funcs import *

PARENT_DIR = os.path.join(os.getcwd(), os.pardir)
DB_NAME = "pokedex.db"
DB_PATH = os.path.join(PARENT_DIR, DB_NAME)

def create_db():
    print("Creating pokedex database...")

    connection = sqlite3.connect(DB_PATH)
    cursor = connection.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS pokemon (
        num INTEGER PRIMARY KEY,
        num_as_text TEXT NOT NULL UNIQUE,
        name TEXT NOT NULL UNIQUE,
        gen INTEGER NOT NULL
    );
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS forms (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        pokemon_num INTEGER NOT NULL,
        form_name TEXT NOT NULL,
        FOREIGN KEY (pokemon_num) REFERENCES pokemon(num)
    );
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS games (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL UNIQUE,
        gen INTEGER NOT NULL
    );
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS form_gen_availability (
        form_id INTEGER NOT NULL,
        available_from_gen INTEGER NOT NULL,
        available_until_gen INTEGER DEFAULT NULL,
        FOREIGN KEY (form_id) REFERENCES forms(id)
    );
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS form_game_availability (
        form_id INTEGER NOT NULL,
        game_id INTEGER NOT NULL,
        FOREIGN KEY (form_id) REFERENCES forms(id),
        FOREIGN KEY (game_id) REFERENCES games(id)
    );
    """)

    connection.commit()
    connection.close()

def db_exists():
    return os.path.exists(DB_PATH)

def insert_poke(cursor, num, num_as_text, name, gen):
    cursor.execute("""
        INSERT OR IGNORE INTO pokemon (num, num_as_text, name, gen)
        VALUES (?, ?, ?, ?);
    """, (num, num_as_text, name, gen))

def populate_pokes(cursor):
    print("Populating Pokemon into database...")

    # Grabbing information from pokemon info spreadsheet
    for row in range(2, pokemon_info_sheet.max_row + 1):
        num = row - 1
        num_as_str = str(cell_value(pokemon_info_sheet, row, poke_info_num_col))
        name = cell_value(pokemon_info_sheet, row, poke_info_name_col)
        gen = cell_value(pokemon_info_sheet, row, poke_info_gen_col)
        insert_poke(cursor, num, num_as_str, name, gen)

def insert_forms(cursor, poke_num, form_name):
    cursor.execute("""
        INSERT OR IGNORE INTO forms (poke_num, form_name)
        VALUES (?, ?);
    """, (poke_num, form_name))

def populate_forms(cursor):
    print("Populating forms into database...")

    forms = []
    # TODO: Here is where you'll have to import all the hardcoded exceptions and pokemon-by-pokemon individualities
    for row in range(2, pokemon_info_sheet.max_row + 1):
        forms.clear()
        poke_num = int(cell_value(pokemon_info_sheet, row, poke_info_num_col))
        female_field = cell_value(pokemon_info_sheet, row, poke_info_f_col)
        mega_field = cell_value(pokemon_info_sheet, row, poke_info_mega_col)
        giganta_field = cell_value(pokemon_info_sheet, row, poke_info_giganta_col)
        regional_form_field = cell_value(pokemon_info_sheet, row, poke_info_reg_forms_col)
        misc_form_field = cell_value(pokemon_info_sheet, row, poke_info_misc_forms_col)
        #misc_forms = [item.strip() for item in misc_form_field.split(",")]

        if is_x_or_num(female_field): forms.append("f")
        if is_x_or_num(mega_field): forms.append("Mega")
        if is_x_or_num(giganta_field): forms.append("Gigantamax")


def populate_db():
    if not db_exists():
        create_db()

    connection = sqlite3.connect(DB_PATH)
    cursor = connection.cursor()

    try:
        populate_pokes(cursor)
        populate_forms(cursor)

        connection.commit()
    except Exception as e:
        print("Error:", e)
        connection.rollback()
    finally:
        connection.close()

populate_db()