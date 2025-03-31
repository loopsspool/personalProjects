import sqlite3
import os

from spreadsheet_funcs import *

PARENT_DIR = os.path.join(os.getcwd(), os.pardir)
DB_NAME = "pokedex.db"
DB_PATH = os.path.join(PARENT_DIR, DB_NAME)

# TODO: For React Native, if certain forms are available outside of the game/gen selected, still display them and go to the first sprite instance, for example see below
# Deoxys forms technically are one for each game in gen3, but just make all forms show
# TODO: Also in RN will have to visually change 710 & 711 forms so gets rid of sorting number

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
    for row in range(2, POKE_INFO_LAST_ROW):
        num = row - 1
        num_as_str = str(cell_value(pokemon_info_sheet, row, poke_info_num_col))
        name = cell_value(pokemon_info_sheet, row, poke_info_name_col)
        gen = cell_value(pokemon_info_sheet, row, poke_info_gen_col)
        insert_poke(cursor, num, num_as_str, name, gen)


def insert_forms(cursor, poke_num, form_name):
    cursor.execute("""
        INSERT OR IGNORE INTO forms (pokemon_num, form_name)
        VALUES (?, ?);
    """, (poke_num, form_name))


def denote_forms(forms, denotion):
    forms_arr = forms.split(", ")
    denoted_arr = []
    for form in forms_arr:
        form_no_spaces = form.replace(" ", "_")
        denoted_form = denotion + form_no_spaces
        denoted_arr.append(denoted_form)
    return denoted_arr


def get_forms_from_excel(row):
    forms = []
    poke_num = int(cell_value(pokemon_info_sheet, row, poke_info_num_col))
    regional_form_field = cell_value(pokemon_info_sheet, row, poke_info_reg_forms_col)
    misc_form_field = cell_value(pokemon_info_sheet, row, poke_info_misc_forms_col)

    if has_default_form(poke_num): forms.append("Default")
    if isnt_empty(pokemon_info_sheet, row, poke_info_f_col): forms.append("-f")
    if isnt_empty(pokemon_info_sheet, row, poke_info_mega_col): forms.append("-Mega")
    if isnt_empty(pokemon_info_sheet, row, poke_info_giganta_col): forms.append("-Gigantamax")
    if isnt_empty(pokemon_info_sheet, row, poke_info_reg_forms_col): forms.extend(denote_forms(regional_form_field, "-Region-"))
    if isnt_empty(pokemon_info_sheet, row, poke_info_misc_forms_col): forms.extend(denote_forms(misc_form_field, "-Form-"))

    return forms


# Poke_num: ({"remove_this, "and_this"}, ["replace_with_this", "and_this"])
FORM_EXCEPTION_POKEMON = {
    6: ({"-Mega"}, ["-Mega_X", "-Mega_Y"]),  # Charizard has two mega forms
    128: ({"-Region-Paldea", "-Form-Combat", "-Form-Blaze", "-Form-Aqua"}, ["-Region-Paldea-Form-Combat", "-Region-Paldea-Form-Blaze", "-Region-Paldea-Form-Aqua"]),     # Only Paldean Tauros has misc forms
    150: ({"-Mega"}, ["-Mega_X", "-Mega_Y"]),  # Mewtwo has two mega forms
    215: (set(), ["-Region-Hisui-f"]),   # *Just adding* Sneasel's female Hisuian form 
    555: ({"-Region-Galar"}, ["-Region-Galar-Form-Standard", "-Region-Galar-Form-Zen"]),     # Galarian Darmanitan has his misc forms too
    892: ({"-Gigantamax"}, ["-Gigantamax-Form-Single_Strike", "-Gigantamax-Form-Rapid_Strike"])     # Urshifu forms impact gigantamax appearance
    }

def adjust_forms_for_exceptions(poke_num, forms):
    if poke_num not in FORM_EXCEPTION_POKEMON:
        return forms
    
    to_remove, replacements = FORM_EXCEPTION_POKEMON[poke_num]
    filtered_forms = [form for form in forms if form not in to_remove]
    filtered_forms.extend(replacements)

    return filtered_forms


def populate_forms(cursor):
    print("Populating forms into database...")

    for row in range(2, POKE_INFO_LAST_ROW + 1): 
        forms = get_forms_from_excel(row)
        forms = adjust_forms_for_exceptions(row-1, forms)
        for form in forms:
            insert_forms(cursor, row-1, form)            


def has_default_form(poke_num):
    # TODO: 854, 855, 1012, 1013 might be a bit odd since their default forms may be their front, and their other forms the back...
    # TODO: Wishiwashi had some default forms slip through in my saved files... Are they actually alts? Same thing with 849.
        # TODO: Write script to find files that have a default sprite saved that shouldnt, like the above
    # TODO: Minior 774 Form Core is for shiny... no matter core color all shinies are the same
    # TODO: No 854, 855 form sprites saved prolly bc improper scrape script
    # TODO: Be sure Arceus Qmark form only in gen4
    no_default_form_poke_nums = [201, 412, 413, 421, 422, 423, 487, 492, 493, 550, 555, 585, 586, 641, 642, 645, 647, 648, 666, 669, 670, 671, 681, 710, 711, 716, 718, 720, 741, 745, 746, 773, 774, 778, 849, 869, 875, 877, 888, 889, 892, 905, 925, 931, 964, 978, 982, 999, 1017, 1024]

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

def get_last_poke_num():
    connection = sqlite3.connect(DB_PATH)
    cursor = connection.cursor()
    cursor.execute("SELECT MAX(num) FROM pokemon")
    max_num = cursor.fetchone()[0]
    connection.close()
    return max_num

populate_db()