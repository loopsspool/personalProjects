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

    # This can all be pulled by a join of form game availability and games tables, seeing what games belong to what gen
    # cursor.execute("""
    # CREATE TABLE IF NOT EXISTS form_gen_availability (
    #     form_id INTEGER NOT NULL,
    #     available_from_gen INTEGER NOT NULL,
    #     available_until_gen INTEGER DEFAULT NULL,
    #     PRIMARY KEY (form_id)
    #     FOREIGN KEY (form_id) REFERENCES forms(id)
    # );
    # """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS form_game_availability (
        form_id INTEGER NOT NULL,
        game_id INTEGER NOT NULL,
        is_available BOOLEAN NOT NULL,
        PRIMARY KEY (form_id, game_id)
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
    for row in range(2, POKE_INFO_LAST_ROW + 1):
        num = row - 1
        num_as_str = str(cell_value(pokemon_info_sheet, row, poke_info_num_col))
        name = cell_value(pokemon_info_sheet, row, poke_info_name_col)
        gen = cell_value(pokemon_info_sheet, row, poke_info_gen_col)
        insert_poke(cursor, num, num_as_str, name, gen)


def insert_form(cursor, poke_num, form_name):
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
            insert_form(cursor, row-1, form)

def get_form_records(cursor):
    cursor.execute("""
        SELECT f.id, f.form_name, p.num, p.name, p.gen
        FROM forms f
        JOIN pokemon p ON f.pokemon_num = p.num
    """)
    forms = {}
    for row in cursor.fetchall():
        # form id maps to form info
        forms[row[0]] = { "name" : row[1],
                          "poke num" : row[2],
                          "poke name" : row[3],
                          "poke gen" : row[4]
                        }
    return forms


def has_default_form(poke_num):
    # TODO: 854, 855, 1012, 1013 might be a bit odd since their default forms may be their front, and their other forms the back...
    # TODO: Wishiwashi had some default forms slip through in my saved files... Are they actually alts? Same thing with 849.
        # TODO: Write script to find files that have a default sprite saved that shouldnt, like the above
    # TODO: Minior 774 Form Core is for shiny... no matter core color all shinies are the same
    # TODO: No 854, 855 form sprites saved prolly bc improper scrape script
    # TODO: Be sure Arceus Qmark form only in gen4
    no_default_form_poke_nums = [201, 412, 413, 421, 422, 423, 487, 492, 493, 550, 555, 585, 586, 641, 642, 645, 647, 648, 666, 669, 670, 671, 681, 710, 711, 716, 718, 720, 741, 745, 746, 773, 774, 778, 849, 869, 875, 877, 888, 889, 892, 905, 925, 931, 964, 978, 982, 999, 1017, 1024]

    if poke_num not in no_default_form_poke_nums: return True


def get_game_records(cursor):
    cursor.execute("SELECT * FROM GAMES")
    games = {}
    for row in cursor.fetchall():
        # Game id maps to game info
        games[row[0]] = {"name" : row[1], 
                         "gen" : row[2]}
    return games


def insert_game(cursor, game, gen):
    cursor.execute("""
        INSERT OR IGNORE INTO games (name, gen)
        VALUES (?, ?);
    """, (game, gen))

# TODO: Should I follow my file naming convention or list out each game?
GAMES = (
    ("Red-Green", 1),
    ("Red-Blue", 1),
    ("Yellow", 1),
    ("Gold", 2),
    ("Silver", 2),
    ("Crystal", 2),
    ("Ruby-Sapphire", 3),
    ("Emerald", 3),
    ("FRLG", 3),
    ("Diamond-Pearl", 4),
    ("Platinum", 4),
    ("HGSS", 4),
    ("BW-B2W2", 5),
    ("XY-ORAS", 6),
    ("SM-USUM", 7),
    ("LGPE", 7),
    ("SwSh", 8),
    ("BDSP", 8),
    ("LA", 8),
    ("SV", 9)
)
def populate_games(cursor):
    print("Populating games into database...")

    for game in GAMES:
        insert_game(cursor, game[0], game[1])


def insert_form_game_availability(cursor, form_id, game_id, bool):
    cursor.execute("""
        INSERT OR IGNORE INTO form_game_availability (form_id, game_id, is_available)
        VALUES (?, ?, ?);
    """, (form_id, game_id, bool))


FORM_EXCLUSIONS = {
    "no_f_form_visual_differences_before_gen4": lambda form, game, poke_num: form["name"] == "-f" and game["gen"] < 4
}
def is_form_available(form, game, poke_num):
    for condition in FORM_EXCLUSIONS.values():
        if condition(form, game, poke_num):
            return False
    return True


# TODO: Add ON CONFLICT to INSERT OR IGNORE statements to update values? See where relevant
def populate_form_game_availability(cursor):
    print("Populating game availability for forms into database...")


    forms = get_form_records(cursor)
    games = get_game_records(cursor)

    for form_id, form_info in forms.items():
        for game_id, game_info in games.items():
            if form_info["poke gen"] > game_info["gen"]:
                continue                
            
            available = is_form_available(form_info, game_info, form_info["poke num"])
            if not available: 
                print(form_info["poke name"], form_info["name"], "not available in", game_info["name"])                
   


def populate_db():
    if not db_exists():
        create_db()

    connection = sqlite3.connect(DB_PATH)
    cursor = connection.cursor()

    try:
        populate_pokes(cursor)
        populate_forms(cursor)
        populate_games(cursor)
        populate_form_game_availability(cursor)

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