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
        regional_form_field = cell_value(pokemon_info_sheet, row, poke_info_reg_forms_col)
        misc_form_field = cell_value(pokemon_info_sheet, row, poke_info_misc_forms_col)
        #misc_forms = [item.strip() for item in misc_form_field.split(",")]

        if has_default_form(poke_num): forms.append("Default")
        if is_x_or_num(pokemon_info_sheet, row, poke_info_f_col): forms.append("f")
        if is_x_or_num(pokemon_info_sheet, row, poke_info_mega_col): forms.append("Mega")
        if is_x_or_num(pokemon_info_sheet, row, poke_info_giganta_col): forms.append("Gigantamax")


def has_default_form(poke_num):
    # TODO: 854, 855, 1012, 1013 might be a bit odd since their default forms may be their front, and their other forms the back...
    # TODO: Write Alcremie forms in spreadsheet... Adjust all
    no_default_form_poke_nums = [201, 412, 413, 421, 422, 423, 492, 493, 550, 555, 585, 586, 641, 642, 645, 647, 648, 666, 669, 670, 671, 681, 710, 711, 716, 718, 720, 741, 745, 746, 773, 774, 778, 849, 869, 875, 877, 888, 889, 892, 905, 925, 931, 964, 978, 982, 999, 1017, 1024]

    if poke_num not in no_default_form_poke_nums: return True


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