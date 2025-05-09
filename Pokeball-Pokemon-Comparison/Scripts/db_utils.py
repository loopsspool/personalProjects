import sqlite3
import os
import importlib
from collections import defaultdict
from contextlib import contextmanager

from file_utils import game_sprite_path
from db_reference_data import *

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
        form_name TEXT NOT NULL UNIQUE
    );
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS poke_forms (
        poke_num INTEGER NOT NULL,
        form_id INTEGER NOT NULL,
        PRIMARY KEY (poke_num, form_id),
        FOREIGN KEY (poke_num) REFERENCES pokemon(num),
        FOREIGN KEY (form_id) REFERENCES forms(id)
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
    CREATE TABLE IF NOT EXISTS form_game_obtainability (
        poke_num INTEGER NOT NULL,
        form_id INTEGER NOT NULL,
        game_id INTEGER NOT NULL,
        obtainable BOOLEAN NOT NULL,
        PRIMARY KEY (poke_num, form_id, game_id),
        FOREIGN KEY (poke_num, form_id) REFERENCES poke_forms (poke_num, form_id),
        FOREIGN KEY (game_id) REFERENCES games(id)
    );
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS sprite_types (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL UNIQUE
    );
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS sprite_obtainability ( 
        poke_num INTEGER NOT NULL,
        form_id INTEGER NOT NULL,
        game_id INTEGER NOT NULL,
        sprite_id INTEGER NOT NULL,
        obtainable BOOLEAN NOT NULL,
        PRIMARY KEY (poke_num, form_id, game_id, sprite_id),
        FOREIGN KEY (poke_num, form_id, game_id) REFERENCES obtainable_forms,
        FOREIGN KEY (sprite_id) REFERENCES sprite_types(id)      
    );
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS all_game_filenames (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        filename TEXT NOT NULL UNIQUE,
        poke_num INTEGER NOT NULL,
        form_id INTEGER NOT NULL,
        game_id INTEGER NOT NULL,
        sprite_id INTEGER NOT NULL,
        obtainable BOOLEAN NOT NULL,
        does_exist BOOLEAN,
        substitution_id INTEGER,
        has_alt BOOLEAN,
        FOREIGN KEY (poke_num, form_id, game_id, sprite_id) REFERENCES sprite_obtainability
    );
    """)

    # Seperating obtainable from all so scraping and RN doesn't have to query and filter unobtainable sprites
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS obtainable_game_filenames (
        id INTEGER PRIMARY KEY,
        filename TEXT NOT NULL UNIQUE,
        poke_num INTEGER NOT NULL,
        form_id INTEGER NOT NULL,
        game_id INTEGER NOT NULL,
        sprite_id INTEGER NOT NULL,
        obtainable BOOLEAN NOT NULL,
        does_exist BOOLEAN,
        substitution_id INTEGER,
        has_alt BOOLEAN,
        FOREIGN KEY (substitution_id) REFERENCES all_game_filenames(id),
        FOREIGN KEY (id) REFERENCES all_game_filenames(id),
        FOREIGN KEY (poke_num, form_id, game_id, sprite_id) REFERENCES sprite_obtainability
    );
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS home_filenames (
        id INTEGER PRIMARY KEY,
        filename TEXT NOT NULL UNIQUE,
        poke_num INTEGER NOT NULL,
        form_id INTEGER NOT NULL,
        sprite_id INTEGER NOT NULL,
        does_exist BOOLEAN,
        FOREIGN KEY (poke_num, form_id) REFERENCES poke_forms,
        FOREIGN KEY (sprite_id) REFERENCES sprite_types(id)
    );
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS home_menu_filenames (
        id INTEGER PRIMARY KEY,
        filename TEXT NOT NULL UNIQUE,
        poke_num INTEGER NOT NULL,
        form_id INTEGER NOT NULL,
        does_exist BOOLEAN,
        FOREIGN KEY (poke_num, form_id) REFERENCES poke_forms
    );
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS drawn_filenames (
        id INTEGER PRIMARY KEY,
        filename TEXT NOT NULL UNIQUE,
        poke_num INTEGER NOT NULL,
        form_id INTEGER NOT NULL,
        does_exist BOOLEAN NOT NULL,
        FOREIGN KEY (poke_num, form_id) REFERENCES poke_forms
    );
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS pokeballs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL UNIQUE,
        gen INGEGER NOT NULL,
        game_exclusive TEXT DEFAULT NULL
    );
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS pokeball_img_types (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL UNIQUE,
        gen INTEGER NOT NULL
    );
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS pokeball_filenames (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        pokeball_id INTEGER NOT NULL,
        img_type_id INTEGER NOT NULL,
        filename TEXT NOT NULL UNIQUE,
        does_exist BOOLEAN NOT NULL,
        FOREIGN KEY (pokeball_id) REFERENCES pokeballs(id),
        FOREIGN KEY (img_type_id) REFERENCES pokeball_img_types(id)
    );
    """)

    connection.commit()
    connection.close()


def insert_into_table(cursor, table, **data):
    cols = ", ".join(data.keys())
    val_placeholders = ", ".join(["?"] * len(data))
    vals = tuple(data.values())

    query = f"INSERT OR IGNORE INTO {table} ({cols}) VALUES ({val_placeholders})"
    cursor.execute(query, vals)
    return cursor.lastrowid


@contextmanager
def get_cursor(passed_cur=None):
    if passed_cur is not None:
        yield passed_cur
    else:
        connection = sqlite3.connect(DB_PATH)
        connection.row_factory = sqlite3.Row
        cur = connection.cursor()
        try:
            yield cur
        finally:
            connection.commit()
            cur.close()
            connection.close()


def get_poke_num(poke_name, cursor=None):
    with get_cursor(cursor) as cur:
        cur.execute("SELECT num FROM pokemon WHERE name=?", (poke_name,))
        form_id = cur.fetchone()
    if form_id: return form_id["num"]
    else: return None


def get_form_id(form_name, cursor=None):
    with get_cursor(cursor) as cur:
        cur.execute("SELECT id FROM forms WHERE form_name=?", (form_name,))
        form_id = cur.fetchone()
    if form_id: return form_id["id"]
    else: return None


def get_form_name(form_id, cursor=None):
    with get_cursor(cursor) as cur:
        cur.execute("SELECT form_name FROM forms WHERE id=?", (form_id,))
        form_name = cur.fetchone()
    if form_name: return form_name["form_name"]
    else: return None


def get_game_id(game_name, cursor=None):
    with get_cursor(cursor) as cur:
        cur.execute("SELECT id FROM games WHERE name=?", (game_name,))
        game_id = cur.fetchone()
    if game_id: return game_id["id"]
    else: return None


def get_game_name(game_id, cursor=None):
    with get_cursor(cursor) as cur:
        cur.execute(f"SELECT name FROM games WHERE id={game_id}")
        game_name=cur.fetchone()
    if game_name: return game_name["name"]
    else: return None


def get_poke_name(poke_id, cursor=None):
    with get_cursor(cursor) as cur:
        cur.execute(f"SELECT name FROM pokemon WHERE num={poke_id}")
        poke_name=cur.fetchone()
    if poke_name: return poke_name["name"]
    else: return None


# Using cursor as a parameter here due to how this function is used... not a good way to cleanly commit to db before calling, so passing the connection that has the writes to here
def get_game_filename_id(cursor, filename):
    cursor.execute("SELECT id FROM all_game_filenames WHERE filename=?", (filename,))
    file_id = cursor.fetchone()
    if file_id: return file_id["id"]
    else: return None


def get_pokeball_name(pokeball_id, cursor=None):
    with get_cursor(cursor) as cur:
        cur.execute(f"SELECT name FROM pokeballs WHERE id={pokeball_id}")
        pokeball_name=cur.fetchone()
    if pokeball_name: return pokeball_name["name"]
    else: return None


def get_pokeball_img_type_name(img_type_id, cursor=None):
    with get_cursor(cursor) as cur:
        cur.execute(f"SELECT name FROM pokeball_img_types WHERE id={img_type_id}")
        img_type_name=cur.fetchone()
    if img_type_name: return img_type_name["name"]
    else: return None


def get_all_game_filenames_info():
    connection = sqlite3.connect(DB_PATH)
    connection.row_factory = sqlite3.Row
    cursor = connection.cursor()

    cursor.execute("SELECT * FROM all_game_filenames")
    rows = cursor.fetchall()
    data = defaultdict(lambda: defaultdict(dict))

    # Organizing database in more efficient way for order of processing for checklist spreadsheet
    for row in rows:
        print(f"\rGetting pokemon #{row["poke_num"]} file availability...", end='', flush=True)
        
        main_key = (row["poke_num"], row["form_id"], row["sprite_id"])
        game = get_game_name(row["game_id"], cursor)
        data[main_key][game]["filename"] = row["filename"]
        data[main_key][game]["obtainable"] = True if row["obtainable"] else False
        data[main_key][game]["exists"] = True if row["does_exist"] else False
        data[main_key][game]["has_sub"] = row["substitution_id"] != None
    # Resetting console line after updates from above
    print('\r' + ' '*45 + '\r', end='')

    connection.close()
    return data


def get_non_game_filename_info(table):
    connection = sqlite3.connect(DB_PATH)
    connection.row_factory = sqlite3.Row
    cursor = connection.cursor()

    fields = "poke_num, form_id, filename, does_exist"
    if table == "home_filenames": fields += ", sprite_id"   # Home sprites need sprite_id since they have shinies, animated, etc. Otherwise their identifiers (poke num, form) are non-unique

    cursor.execute(f"SELECT {fields} FROM {table}")
    rows = cursor.fetchall()
    data = {}

    for row in rows:
        key = (row["poke_num"], row["form_id"]) if table != "home_filenames" else (row["poke_num"], row["form_id"], row["sprite_id"])   # Home sprites need sprite_id since they have shinies, animated, etc. Otherwise their identifiers (poke num, form) are non-unique
        data[key] = {"filename": row["filename"], "exists": True if row["does_exist"] else False}

    connection.close()
    return data


def get_missing_poke_imgs_by_table(table, cursor=None):
    data = defaultdict(list)
    print(f"Getting all missing images from {table} by pokemon...")
    
    with get_cursor(cursor) as cur:
        cur.execute(f"SELECT poke_num, form_id, filename FROM {table} WHERE does_exist=0")
        result = cur.fetchall()
        for row in result:
            # { (poke_num, form_id) : [missing imgs list] }
            poke_info = (row["poke_num"], row["form_id"])
            data[poke_info].append(row["filename"])
    return data


def get_missing_pokeball_imgs(cursor=None):
    data = defaultdict(list)
    print("Getting all missing pokeball images...")

    with get_cursor(cursor) as cur:
        cur.execute("SELECT pokeball_id, img_type_id, filename FROM pokeball_filenames WHERE does_exist=0")
        result = cur.fetchall()
        for row in result:
            # { (pokeball_id, img_type_id) : [missing imgs list] }
            # Have to do it as a list because of gen3 ultra ball having two imgs for same ball img type...
            pokeball_info = (row["pokeball_id"], row["img_type_id"])
            data[pokeball_info].append(row["filename"])
    return data


def has_f_form(poke_num, cursor=None):
    with get_cursor(cursor) as cur:
        cur.execute(f"SELECT form_id FROM poke_forms WHERE poke_num={poke_num} AND form_id={get_form_id("-f")}")
        result = cur.fetchone()
    if result: return True
    else: return False


# To cache dynamically imported funcs from spreadsheet_utils so it only imports once
# Necessary to avoid circular import
_module_cache = {}
def lazy_import(module_name):
    if module_name not in _module_cache:
        _module_cache[module_name] = importlib.import_module(module_name)
    return _module_cache[module_name]


def db_exists():
    return os.path.exists(DB_PATH)


def populate_pokes(cursor):
    print("Populating Pokemon into database...")
    from spreadsheet_funcs import POKE_INFO_LAST_ROW, cell_value, pokemon_info_sheet, poke_info_num_col, poke_info_name_col, poke_info_gen_col

    # Grabbing information from pokemon info spreadsheet
    for row in range(2, POKE_INFO_LAST_ROW + 1):
        num = row - 1
        num_as_str = str(cell_value(pokemon_info_sheet, row, poke_info_num_col))
        name = cell_value(pokemon_info_sheet, row, poke_info_name_col)
        gen = cell_value(pokemon_info_sheet, row, poke_info_gen_col)
        insert_into_table(cursor, "pokemon", **{"num": num, "num_as_text": num_as_str, "name": name, "gen": gen})


def insert_into_both_form_tables(cursor, form_name, poke_num):
    insert_into_table(cursor, "forms", **{"form_name": form_name})
    form_id = get_form_id(form_name, cursor)
    insert_into_table(cursor, "poke_forms", **{"poke_num": poke_num, "form_id": form_id})


def denote_forms(forms, denotion):
    forms_arr = forms.split(", ")
    denoted_arr = []
    for form in forms_arr:
        form_no_spaces = form.replace(" ", "_")
        denoted_form = denotion + form_no_spaces
        denoted_arr.append(denoted_form)
    return denoted_arr


def get_forms_from_excel(row):
    from spreadsheet_funcs import cell_value, isnt_empty, pokemon_info_sheet, poke_info_num_col, poke_info_reg_forms_col, poke_info_misc_forms_col, poke_info_f_col, poke_info_mega_col, poke_info_giganta_col
    forms = []
    poke_num = int(cell_value(pokemon_info_sheet, row, poke_info_num_col))
    regional_form_field = cell_value(pokemon_info_sheet, row, poke_info_reg_forms_col)
    misc_form_field = cell_value(pokemon_info_sheet, row, poke_info_misc_forms_col)

    if has_default_form(poke_num): forms.append("Default")
    if isnt_empty(pokemon_info_sheet, row, poke_info_f_col): forms.append("-f")
    if isnt_empty(pokemon_info_sheet, row, poke_info_mega_col): forms.append("-Mega")
    if isnt_empty(pokemon_info_sheet, row, poke_info_giganta_col): forms.append("-Gigantamax")
    if isnt_empty(pokemon_info_sheet, row, poke_info_reg_forms_col): forms.extend(denote_forms(regional_form_field, "-Region_"))
    if isnt_empty(pokemon_info_sheet, row, poke_info_misc_forms_col): forms.extend(denote_forms(misc_form_field, "-Form_"))

    return forms


# Poke_num: ({"remove_this, "and_this"}, ["replace_with_this", "and_this"])
FORM_EXCEPTION_POKEMON = {
    6: ({"-Mega"}, ["-Mega_X", "-Mega_Y"]),  # Charizard has two mega forms
    128: ({"-Region_Paldea", "-Form_Combat", "-Form_Blaze", "-Form_Aqua"}, ["-Region_Paldea-Form_Combat", "-Region_Paldea-Form_Blaze", "-Region_Paldea-Form_Aqua"]),     # Only Paldean Tauros has misc forms
    150: ({"-Mega"}, ["-Mega_X", "-Mega_Y"]),  # Mewtwo has two mega forms
    215: (set(), ["-Region_Hisui-f"]),   # *Just adding* Sneasel's female Hisuian form 
    555: ({"-Region_Galar"}, ["-Region_Galar-Form_Standard", "-Region_Galar-Form_Zen"]),     # Galarian Darmanitan has his misc forms too
    892: ({"-Gigantamax"}, ["-Gigantamax-Form_Single_Strike", "-Gigantamax-Form_Rapid_Strike"])     # Urshifu forms impact gigantamax appearance
    }

def adjust_forms_for_exceptions(poke_num, forms):
    if poke_num not in FORM_EXCEPTION_POKEMON:
        return forms
    
    to_remove, replacements = FORM_EXCEPTION_POKEMON[poke_num]
    filtered_forms = [form for form in forms if form not in to_remove]
    filtered_forms.extend(replacements)

    return filtered_forms


# Minior and Alcremie have special "shared" forms for their shinies
SHARED_SHINY_FORMS = {  774: ["-Form_Core"], 
                        869: ["-Form_Berry_Sweet", "-Form_Clover_Sweet", "-Form_Flower_Sweet", "-Form_Love_Sweet", "-Form_Ribbon_Sweet", "-Form_Star_Sweet", "-Form_Strawberry_Sweet"]
}
def populate_forms(cursor):
    print("Populating forms into database...")
    from spreadsheet_funcs import POKE_INFO_LAST_ROW

    for row in range(2, POKE_INFO_LAST_ROW + 1): 
        poke_num = row-1
        forms = get_forms_from_excel(row)
        forms = adjust_forms_for_exceptions(row-1, forms)

        for form in forms:
            insert_into_both_form_tables(cursor, form, poke_num)

        # Putting here so poke/forms stay in numerical order for speedy lookups
        if poke_num in SHARED_SHINY_FORMS:
            for form in SHARED_SHINY_FORMS[poke_num]:
                insert_into_both_form_tables(cursor, form, poke_num)
    

# TODO: Group with other gets
def get_poke_form_records(cursor):
    cursor.execute("""
        SELECT p.num, f.id, f.form_name, pf.poke_num, p.name, p.gen
        FROM poke_forms pf
        JOIN forms f ON pf.form_id = f.id
        JOIN pokemon p ON pf.poke_num = p.num
    """)
    forms = {}
    for row in cursor.fetchall():
        # (poke num, form id) maps to form/poke info
        forms[(row["num"], row["id"])] = {  "form name" : row["form_name"],
                                            "poke num" : row["poke_num"],
                                            "poke name" : row["name"],
                                            "poke gen" : row["gen"]
                        }
    return forms


def has_default_form(poke_num):
    no_default_form_poke_nums = {201, 412, 413, 421, 422, 423, 487, 492, 493, 
                                 550, 555, 585, 586, 641, 642, 645, 647, 648, 
                                 666, 669, 670, 671, 681, 710, 711, 716, 718, 
                                 720, 741, 745, 746, 773, 774, 778, 849, 869, 
                                 875, 877, 888, 889, 892, 905, 925, 931, 964, 
                                 978, 982, 999, 1017, 1024}

    if poke_num not in no_default_form_poke_nums: return True


def get_game_records(cursor):
    cursor.execute("SELECT * FROM GAMES")
    games = {}
    for row in cursor.fetchall():
        # Game id maps to game info
        games[row["id"]] = {"name" : row["name"], 
                            "gen" : row["gen"]}
    return games


# NOTE: These are in chronological order and that is IMPORTANT since I rely on game ids sometimes for form filtering (eg mid gen form introductions)
GAMES = (
    ("Red_Green", 1),
    ("Red_Blue", 1),
    ("Yellow", 1),
    ("Gold", 2),
    ("Silver", 2),
    ("Crystal", 2),
    ("Ruby_Sapphire", 3),
    ("FRLG", 3),
    ("Emerald", 3),
    ("Diamond_Pearl", 4),
    ("Platinum", 4),
    ("HGSS", 4),
    ("BW_B2W2", 5),
    ("XY_ORAS", 6),
    ("SM_USUM", 7),
    ("LGPE", 7),
    ("SwSh", 8),
    ("BDSP", 8),
    ("LA", 8),
    ("SV", 9)
)
def populate_games(cursor):
    print("Populating games into database...")

    for game in GAMES:
        insert_into_table(cursor, "games", **{"name": game[0], "gen": game[1]})


FORM_EXCLUSIONS = {
    # Species game availability
    "filtering_for_LGPE_dex_if_needed": lambda poke_form, game: game["name"] == "LGPE" and lazy_import("spreadsheet_funcs").poke_isnt_in_game(poke_form["poke num"], "LGPE"),
    "filtering_for_SwSh_dex_if_needed": lambda poke_form, game: game["name"] == "SwSh" and lazy_import("spreadsheet_funcs").poke_isnt_in_game(poke_form["poke num"], "SwSh"),
    "filtering_for_BDSP_dex_if_needed": lambda poke_form, game: game["name"] == "BDSP" and lazy_import("spreadsheet_funcs").poke_isnt_in_game(poke_form["poke num"], "BDSP"),
    "filtering_for_LA_dex_if_needed": lambda poke_form, game: game["name"] == "LA" and lazy_import("spreadsheet_funcs").poke_isnt_in_game(poke_form["poke num"], "LA"),
    "filtering_for_SV_dex_if_needed": lambda poke_form, game: game["name"] == "SV" and lazy_import("spreadsheet_funcs").poke_isnt_in_game(poke_form["poke num"], "SV"),

    # Universal Rules
    "no_pokemon_with_a_higher_generation_than_game_generation": lambda poke_form, game: poke_form["poke gen"] > game["gen"],
    "no_f_form_visual_differences_before_gen_4": lambda poke_form, game: poke_form["form name"] == "-f" and game["gen"] < 4,
    "no_fairy_forms_before_gen_6": lambda poke_form, game: poke_form["form name"] == "-Form_Fairy" and game["gen"] < 6,
    "no_megas_outside_XY_ORAS_SM_USUM_LGPE": lambda poke_form, game: "-Mega" in poke_form["form name"] and game["name"] not in ("XY_ORAS", "SM_USUM", "LGPE"),
    "no_gigantamax_outside_SwSh": lambda poke_form, game: poke_form["form name"] == "-Gigantamax" and game["name"] != "SwSh",
    "no_regional_forms_before_gen_7": lambda poke_form, game: "-Region" in poke_form["form name"] and game["gen"] < 7,
    "no_alolan_forms_before_SM_USUM": lambda poke_form, game: "-Region_Alola" in poke_form["form name"] and get_game_id(game["name"]) < get_game_id("SM_USUM"),
    "no_galarian_forms_before_SwSh": lambda poke_form, game: "-Region_Galar" in poke_form["form name"] and get_game_id(game["name"]) < get_game_id("SwSh"),
    "no_hisuian_forms_before_LA": lambda poke_form, game: "-Region_Hisui" in poke_form["form name"] and get_game_id(game["name"]) < get_game_id("LA"),
    "no_paldean_forms_before_SV": lambda poke_form, game: "-Region_Paldea" in poke_form["form name"] and get_game_id(game["name"]) < get_game_id("SV"),
    "no_regional_forms_in_BDSP": lambda poke_form, game: game["name"] == "BDSP" and "-Region" in poke_form["form name"],
    "no_regional_forms_in_LA_other_than_hisui_and_alola_kitties": lambda poke_form, game: game["name"] == "LA" and "-Region" in poke_form["form name"] and "-Region_Hisui" not in poke_form["form name"] and not (poke_form["poke name"] in ("Vulpix", "Ninetales") and poke_form["form name"] == "-Region_Alola"),

    # Specific pokemon
    "no_cosplay_pikachu_outside_ORAS": lambda poke_form, game: poke_form["poke num"] == 25 and "-Form_Cosplay" in poke_form["form name"] and game["name"] != "XY_ORAS",
    "no_cap_pikachu_before_gen_7": lambda poke_form, game: poke_form["poke num"] == 25 and "-Form_Cap" in poke_form["form name"] and game["gen"] < 7,
    "no_cap_pikachu_in_these_games": lambda poke_form, game: poke_form["poke num"] == 25 and "-Form_Cap" in poke_form["form name"] and game["name"] in ("LGPE", "BDSP", "LA"),  # Don't have to add earlier games because line above filters out everything below gen 7
    "no_world_cap_pikachu_in_SM_USUM": lambda poke_form, game: poke_form["poke num"] == 25 and poke_form["form name"] == "-Form_Cap_World" and game["name"] == "SM_USUM",
    "no_female_form_eevees_until_gen_8": lambda poke_form, game: poke_form["poke num"] == 133 and poke_form["form name"] == "-f" and game["gen"] < 8,
    "no_spiky_eared_pichu_outside_HGSS": lambda poke_form, game: poke_form["poke num"] == 172 and poke_form["form name"] == "-Form_Spiky_Eared" and game["name"] != "HGSS",
    "no_unown_punctuation_before_gen_3": lambda poke_form, game: poke_form["poke num"] == 201 and poke_form["form name"] in ("-Form_!", "-Form_Qmark") and game["gen"] < 3,
    "no_primal_kyogre_or_groudon_outside_XY_ORAS_and_SM_USUM": lambda poke_form, game: (poke_form["poke num"] in (382, 383)) and poke_form["form name"] == "-Form_Primal" and game["name"] not in ("XY_ORAS", "SM_USUM"),
    "no_deoxys_non_normal_forms_in_ruby_sapphire": lambda poke_form, game: poke_form["poke num"] == 386 and game["name"] == "Ruby_Sapphire" and poke_form["form name"] != "Default",
    "no_deoxys_speed_form_in_FRLG": lambda poke_form, game: poke_form["poke num"] == 386 and game["name"] == "FRLG" and poke_form["form name"] == "-Form_Speed",
    "no_deoxys_attack_and_defense_form_in_emerald": lambda poke_form, game: poke_form["poke num"] == 386 and game["name"] == "Emerald" and poke_form["form name"] in ("-Form_Attack", "-Form_Defense"),
    "no_rotom_forms_until_after_platinum": lambda poke_form, game: poke_form["poke num"] == 479 and poke_form["form name"] != "Default" and get_game_id(game["name"]) < get_game_id("Platinum"),
    "no_origin_dialga_palkia_forms_until_after_LA": lambda poke_form, game: poke_form["poke num"] in (483, 484) and poke_form["form name"] == "-Form_Origin" and get_game_id(game["name"]) < get_game_id("LA"),
    "no_origin_form_giratina_until_after_platinum": lambda poke_form, game: poke_form["poke num"] == 487 and poke_form["form name"] == "-Form_Origin" and get_game_id(game["name"]) < get_game_id("Platinum"),
    "no_sky_form_shaymin_until_after_platinum": lambda poke_form, game: poke_form["poke num"] == 492 and poke_form["form name"] == "-Form_Sky" and get_game_id(game["name"]) < get_game_id("Platinum"),
    "no_???_arceus_form_outside_of_gen_4": lambda poke_form, game: poke_form["poke num"] == 493 and poke_form["form name"] == "-Form_Qmark" and game["gen"] != 4,
    "no_white_striped_basculin_until_LA": lambda poke_form, game: poke_form["poke num"] == 550 and poke_form["form name"] == "-Form_White_Striped" and get_game_id(game["name"]) < get_game_id("LA"),
    "no_ash_greninja_outside_of_SM_USUM": lambda poke_form, game: poke_form["poke num"] == 658 and poke_form["form name"] == "-Form_Ash" and game["name"] != "SM_USUM",
    "no_zygarde_forms_until_gen_7": lambda poke_form, game: poke_form["poke num"] == 718 and poke_form["form name"] != "-Form_50%" and game["gen"] < 7,
    "no_solgaleo_lunala_forms_outside_SM_USUM": lambda poke_form, game: poke_form["poke num"] in (791, 792) and poke_form["form name"] != "Default" and game["name"] != "SM_USUM",
    "no_zenith_marshadow_form_outside_gen_SM_USUM": lambda poke_form, game: poke_form["poke num"] == 802 and poke_form["form name"] != "Default" and game["name"] != "SM_USUM",
    "no_meltan_or_melmetal_until_LGPE": lambda poke_form, game: poke_form["poke num"] in (808, 809) and get_game_id(game["name"]) < get_game_id("LGPE"),    # Technically these are gen 7 pokemon, they just werent introduced until LGPE
    "no_stamped_poke_sprites_in_games": lambda poke_form, game: poke_form["poke num"] in (854, 855, 1012, 1013) and poke_form["form name"] != "Default"     # Both forms look the same except for the stamp, which is really only visible in HOME anyways. This is where the stamp img will be downloaded
}
def is_form_obtainable(form, game):
    for exclusion in FORM_EXCLUSIONS.values():
        if exclusion(form, game):
            return False
    return True


def populate_form_game_obtainability(cursor, force):
    print("Populating game obtainability for forms into database...")

    poke_forms = get_poke_form_records(cursor)
    games = get_game_records(cursor)
    form_game_obtainability = {}

    # Running all pokemon forms through all games to check if its obtainable
    for poke_form_id, poke_form_info in poke_forms.items():
        for game_id, game_info in games.items():
            print(f"\rChecking #{poke_form_info["poke num"]} form obtainability...", end='', flush=True)
            # Quick workaround to make it run faster, only generating obtainability if forced or the record doesn't exist yet
            if force or not entry_exists(cursor, "form_game_obtainability", {"poke_num": poke_form_id[0], "form_id": poke_form_id[1], "game_id": game_id}):
                obtainable = is_form_obtainable(poke_form_info, game_info)
                form_game_obtainability[(poke_form_id, game_id)] = {"poke_num": poke_form_id[0], "form_id": poke_form_id[1], "game_id": game_id, "obtainable": obtainable}

    # Resetting console line after updates from above
    print('\r' + ' '*60 + '\r', end='')
    for form_info in form_game_obtainability.values(): insert_into_table(cursor, "form_game_obtainability", **form_info)


# TODO: This might not be needed for when you check last entered pokemon in db against highest poke num in info spreadsheet?
    # Especially if you check highest poke_num across all applicable tables!
def entry_exists(cursor, table, cols):
    where_clause = " AND ".join(f"{k} = ?" for k in cols)
    values = tuple(cols.values())

    query = f"SELECT 1 FROM {table} WHERE {where_clause} LIMIT 1"
    cursor.execute(query, values)
    return cursor.fetchone() is not None


# Default meaning front, normal color, static sprite
SPRITE_TYPES = ["Default", "-Animated", "-Shiny", "-Shiny-Animated", "-Back", "-Back-Animated", "-Shiny-Back", "-Shiny-Back-Animated"]
def populate_sprite_types(cursor):
    print("Populating sprite types into database...")
    for type in SPRITE_TYPES:
        cursor.execute("INSERT OR IGNORE INTO sprite_types (name) VALUES (?)", (type,))


def get_sprite_types(cursor):
    cursor.execute("SELECT * FROM sprite_types")
    sprite_types = {}
    for row in cursor.fetchall():
        sprite_types[row["id"]] = row["name"]
    return sprite_types


def get_poke_form_obtainability_records(cursor):
    cursor.execute("""
        SELECT p.num, f.id AS form_id, g.id AS game_id, f.form_name, fgo.poke_num, p.name AS poke_name, g.name AS game_name, g.gen, fgo.obtainable
        FROM form_game_obtainability fgo
        JOIN forms f ON fgo.form_id = f.id
        JOIN pokemon p ON fgo.poke_num = p.num
        JOIN games g ON fgo.game_id = g.id
    """)
    forms = {}
    for row in cursor.fetchall():
        # (poke num, form id, game id) maps to form/poke/game info
        forms[(row["num"], row["form_id"], row["game_id"])] = { "form name" : row["form_name"],
                                                                "poke num" : row["poke_num"],
                                                                "poke name" : row["poke_name"],
                                                                "game name" : row["game_name"],
                                                                "game gen" : row["gen"],
                                                                "obtainable" : row["obtainable"]
        }
    return forms


# Certain rules to be excluded but exist elsewhere, for nonexistant sprites, see NONEXISTANT_SPRITES
SPRITE_EXCLUSIONS = {
    # UNIVERSAL EXCLUSIONS
    "no_sprites_if_form_is_unavailable": lambda pfgo_info, sprite_type: pfgo_info["obtainable"] == 0,
    "no_shiny_sprites_in_gen_1": lambda pfgo_info, sprite_type: pfgo_info["game gen"] == 1 and "Shiny" in sprite_type,
    "no_animated_sprites_in_gen_1": lambda pfgo_info, sprite_type: pfgo_info["game gen"] == 1 and "Animated" in sprite_type,
    "no_animated_back_sprites_below_gen_5": lambda pfgo_info, sprite_type: pfgo_info["game gen"] < 5 and "-Back-Animated" in sprite_type,
    "no_animated_sprites_in_these_games": lambda pfgo_info, sprite_type: pfgo_info["game name"] in ("Gold", "Silver", "FRLG", "Ruby_Sapphire") and "Animated" in sprite_type,

    # INDIVIDUAL POKEMON
    "no_shiny_castform_forms_until_gen_8": lambda pfgo_info, sprite_type: pfgo_info["poke num"] == 351 and pfgo_info["form name"] != "Default" and "Shiny" in sprite_type and pfgo_info["game gen"] < 8
}
def is_sprite_possible(pfgo_info, sprite_type):
    for exclusion in SPRITE_EXCLUSIONS.values():
        if exclusion(pfgo_info, sprite_type):
            return False
    return True


# Sprites that don't exist. Shouldn't even be marked unobtainable, which is why theyre here not SPRITE_EXCLUSIONS
NONEXISTANT_SPRITES={
    "skip_all_shared_shiny_forms_that_arent_adjusted_appropriately": lambda poke_num, form_name, sprite_type: poke_num in SHARED_SHINY_FORMS and "Shiny" in sprite_type and form_name not in SHARED_SHINY_FORMS[poke_num],
    "skip_all_non_shiny_sprites_for_shared_shinies_that_are_adjusted": lambda poke_num, form_name, sprite_type: poke_num in SHARED_SHINY_FORMS and "Shiny" not in sprite_type and form_name in SHARED_SHINY_FORMS[poke_num],

    "no_shiny_cosplay_pikachu": lambda poke_num, form_name, sprite_type: poke_num == 25 and "-Form_Cosplay" in form_name and "Shiny" in sprite_type,
    "no_shiny_cap_pikachu": lambda poke_num, form_name, sprite_type: poke_num == 25 and "-Form_Cap" in form_name and "Shiny" in sprite_type,
    # The below only affects home because (non-default) forms of the stamped pokes were already marked as unobtainable in games (since no way to see stamp in game and all other sprites are identical)
    # Further processing is done in the generate_home_filenames function to exclude default form back sprites (couldn't include here bc would also filter them for games)
    "no_stamped_poke_forms_except_show_stamp_back_sprite": lambda poke_num, form_name, sprite_type: poke_num in (854, 855, 1012, 1013) and form_name != "Default" and sprite_type not in ("-Back", "-Shiny-Back")
}
def should_skip_nonexistant_sprite(poke_num, form_name, sprite_type):
    for nonexistant in NONEXISTANT_SPRITES.values():
        if nonexistant(poke_num, form_name, sprite_type):
            return True
    return False


def populate_sprite_obtainability(cursor):
    print("Populating sprite variations per poke into database...")

    sprite_types = get_sprite_types(cursor)
    poke_form_game_obtainability = get_poke_form_obtainability_records(cursor)
    sprite_obtainability = {}

    for pfgo_id, pfgo_info in poke_form_game_obtainability.items():
        for sprite_id, sprite_type in sprite_types.items():
            if should_skip_nonexistant_sprite(pfgo_info["poke num"], pfgo_info["form name"], sprite_type):
                continue
            sprite_possible = is_sprite_possible(pfgo_info, sprite_type)
            sprite_obtainability[(pfgo_id, sprite_id)] = {"poke_num": pfgo_id[0], "form_id": pfgo_id[1], "game_id": pfgo_id[2], "sprite_id": sprite_id, "obtainable": sprite_possible}

    for spr_obt in sprite_obtainability.values():
        insert_into_table(cursor, "sprite_obtainability", **spr_obt)


def get_sprites_obtainability_records(cursor):
    cursor.execute("""
        SELECT 
            p.num, 
            f.id AS form_id, 
            g.id AS game_id, 
            s.id AS sprite_id, 
            so.poke_num, 
            p.name AS poke_name, 
            p.gen AS poke_gen, 
            g.gen AS game_gen, 
            g.name AS game_name, 
            f.form_name, 
            s.name AS sprite_name, 
            so.obtainable
        FROM sprite_obtainability so
        JOIN forms f ON so.form_id = f.id
        JOIN pokemon p ON so.poke_num = p.num
        JOIN games g ON so.game_id = g.id
        JOIN sprite_types s ON so.sprite_id = s.id
    """)
    sprites = {}
    for row in cursor.fetchall():
        # (poke num, form id, game id, sprite id) maps to form/poke/game/sprite info
        sprites[(row["num"], row["form_id"], row["game_id"], row["sprite_id"])] = { "poke num" : row["poke_num"],
                                                                                    "poke name" : row["poke_name"],
                                                                                    "poke gen" : row["poke_gen"],
                                                                                    "game gen" : row["game_gen"],
                                                                                    "game name" : row["game_name"],
                                                                                    "form name" : row["form_name"],
                                                                                    "sprite type": row["sprite_name"],
                                                                                    "obtainable" : row["obtainable"]
        }
    return sprites


def seperate_sprite_type_if_shiny(sprite_type):
    if sprite_type == "Default": return False, ""
    if "-Shiny" not in sprite_type: return False, sprite_type
    else: return True, sprite_type.replace("-Shiny", "")


def file_does_exist(filename, dir_file_list):
    # Keep .png first since it's most common img type for this
    file_ext = [".png"]
    #  Checking all extensions in path
    for ext in file_ext:
        filename_w_ext = filename + ext
        if filename_w_ext in dir_file_list: return True
    return False
    

def check_for_usable_game_file(filename, sprite_info):
    if not sprite_info["obtainable"]:
        return None, None
    if file_does_exist(filename, ALL_GAME_SPRITE_FILES):
        return True, None
    else:
        exists, substitution = check_for_game_file_substitution(filename)
        return exists, substitution


def check_for_game_file_substitution(filename):
    for game in GAME_FALLBACKS:
        game_adj = game_adjustment_for_back(filename, game)
        if game_adj in filename:
            for repl in GAME_FALLBACKS[game]:
                repl = game_adjustment_for_back(filename, repl)
                replacement_filename = filename.replace(game_adj, repl)
                if file_does_exist(replacement_filename, ALL_GAME_SPRITE_FILES):
                    return True, replacement_filename
    return False, None


def game_adjustment_for_back(filename, game):
    if "-Back" in filename:
        game = game.replace(" ", "_")
    return game


GAME_FALLBACKS = {
    "Gen2 Silver": ["Gen2 Gold", "Gen2 Crystal"],
    "Gen2 Crystal": ["Gen2 Gold"],
    "Gen3 Emerald": ["Gen3 Ruby_Sapphire", "Gen3 FRLG"],
    "Gen3 FRLG": ["Gen3 Ruby_Sapphire"],
    "Gen4 HGSS": ["Gen4 Platinum", "Gen4 Diamond_Pearl"],
    "Gen4 Platinum": ["Gen4 Diamond_Pearl"],
    "Gen6 XY_ORAS": ["Gen7 SM_USUM"],
    "Gen7 SM_USUM": ["Gen6 XY_ORAS"]
}


def generate_game_filename(sprite_info):
    poke_num = str(sprite_info["poke num"]).zfill(4)
    form_name = "" if sprite_info["form name"] == "Default" else sprite_info["form name"]
    is_shiny, sprite_type = seperate_sprite_type_if_shiny(sprite_info["sprite type"])
    gen = sprite_info["game gen"]
    game = sprite_info["game name"]

    # Hyphen before game allows for alphabetical sorting of back sprites below the front game sprites
    filename = f"{poke_num} {sprite_info["poke name"]} Gen{gen}{str("_" + game) if "-Back" in sprite_type else str(" " + game)}{"-Shiny" if is_shiny else ""}{form_name}{sprite_type}"
    return filename


ALL_GAME_SPRITE_FILES = set(os.listdir(game_sprite_path))
def populate_game_filenames(cursor, force=False):
    print("Populating game filenames into database...")
    all_sprites = get_sprites_obtainability_records(cursor)
    substitutions_to_convert_to_id = []
    
    for sprite_id, sprite_info in all_sprites.items():
        print(f"\rGenerating pokemon #{sprite_info["poke num"]} game filenames...", end='', flush=True)
        filename = generate_game_filename(sprite_info)
        file_exists, substitution = check_for_usable_game_file(filename, sprite_info)
        has_sub = 1 if substitution!=None else None     # Temp marking to set in substitution field until I can get subs file id
        has_alt = file_does_exist(substitution + "-Alt", ALL_GAME_SPRITE_FILES) if has_sub else file_does_exist(filename + "-Alt", ALL_GAME_SPRITE_FILES)
        file_ids = {"filename": filename, "poke_num": sprite_id[0], "form_id": sprite_id[1], "game_id": sprite_id[2], "sprite_id": sprite_id[3], "obtainable": sprite_info["obtainable"], "does_exist": file_exists, "substitution_id": has_sub, "has_alt": has_alt}
        # Inserting into all filenames table
        insert_into_table(cursor, "all_game_filenames", **file_ids)
        filename_id = get_game_filename_id(cursor, filename)
        if has_sub: substitutions_to_convert_to_id.append({"file_id": filename_id, "sub_name": substitution})
        # Inserting into only obtainable filenames table
        if sprite_info["obtainable"]:
            insert_into_table(cursor, "obtainable_game_filenames", **{"id": filename_id, **file_ids})

    # Resetting console line after updates from above
    print('\r' + ' '*60 + '\r', end='')

    # This is pulled out seperate since it depends on file_ids from all_game_filenames table, which may not be present yet
    # This is due to checking if the replacement filename exists in all files
    # But that replacement filename may not be inserted into the database yet, hence it doesn't have an id
    change_substitution_field_from_filename_to_file_id(cursor, substitutions_to_convert_to_id)


def edit_substitution_field(cursor, record):
    substitution_id = get_game_filename_id(cursor, record["sub_name"])
    cursor.execute(f"UPDATE all_game_filenames SET substitution_id = {substitution_id} WHERE id = {record["file_id"]}")
    cursor.execute(f"UPDATE obtainable_game_filenames SET substitution_id = {substitution_id} WHERE id = {record["file_id"]}")


def change_substitution_field_from_filename_to_file_id(cursor, sub_names_to_convert):
    print("Converting substitution game filenames to ids...")
    for record in sub_names_to_convert:
        edit_substitution_field(cursor, record)


def populate_home_filenames(cursor):
    from app_globals import home_save_path
    print("Populating HOME sprite filenames into database...")

    home_sprites_files = set(os.listdir(home_save_path))
    poke_forms = get_poke_form_records(cursor)
    sprite_types = get_sprite_types(cursor)

    for poke_form, poke_info in poke_forms.items():
        for sprite_id, sprite_type in sprite_types.items():
            if should_skip_nonexistant_sprite(poke_info["poke num"], poke_info["form name"], sprite_type):
                continue
            # No home back sprites
            if "-Back" in sprite_type:
                # Except for stamped pokemon formed "back" sprites (showing the stamp)
                if not is_stamped_poke_form(poke_info):
                    continue
            filename = generate_home_filename(poke_info, sprite_type)
            exists = file_does_exist(filename, home_sprites_files)
            file_ids = {"filename": filename, "poke_num": poke_info["poke num"], "form_id": poke_form[1], "sprite_id": sprite_id, "does_exist":exists}
            insert_into_table(cursor, "home_filenames", **file_ids)


def is_stamped_poke_form(poke_info):
    if poke_info["poke num"] in (854, 855, 1012, 1013) and poke_info["form name"] != "Default": return True
    else: return False


def generate_home_filename(poke_info, sprite_type):
    poke_num = str(poke_info["poke num"]).zfill(4)
    form_name = "" if poke_info["form name"] == "Default" else poke_info["form name"]
    is_shiny, sprite_type = seperate_sprite_type_if_shiny(sprite_type)

    # Hyphen before game allows for alphabetical sorting of back sprites below the front game sprites
    filename = f"{poke_num} {poke_info["poke name"]} HOME{"-Shiny" if is_shiny else ""}{form_name}{sprite_type}"
    return filename


def populate_home_menu_filenames(cursor):
    from app_globals import home_menu_sprite_path
    print("Populating home menu sprites into database...")

    home_menu_sprite_files = set(os.listdir(home_menu_sprite_path))
    poke_forms = get_poke_form_records(cursor)
    for poke_form, poke_info in poke_forms.items():
        if should_exclude_menu_poke_form(poke_info): continue
        filename = generate_home_menu_filename(poke_info)
        exists = file_does_exist(filename, home_menu_sprite_files)
        file_ids = {"filename": filename, "poke_num": poke_form[0], "form_id": poke_form[1], "does_exist": exists}
        insert_into_table(cursor, "home_menu_filenames", **file_ids)


def should_exclude_menu_poke_form(poke_info):
    poke_num = poke_info["poke num"]
    form_name = poke_info["form name"]
    # No f menu sprites
    if form_name == "-f": return True     
    # These get excluded from menu sprites too
    if poke_num in NO_DRAWN_FORMS:  
        if form_name in NO_DRAWN_FORMS[poke_num]:
            return True
    # No Kyurem overdrive
    if poke_num == 646 and "Overdrive" in form_name: return True

    return False


def generate_home_menu_filename(poke_info):
    poke_num = str(poke_info["poke num"]).zfill(4)
    form_name = poke_info["form name"]
    # Removing Region, Form, and Default tags, leaving -values
    for excl in ["Region_", "Form_", "Default"]:
        if excl in form_name: form_name = form_name.replace(excl, "")
    filename = f"{poke_num} {poke_info["poke name"]}{form_name}"
    return filename


def populate_drawn_filenames(cursor):
    from app_globals import drawn_save_path
    print("Populating drawn filenames into database...")

    drawn_files = set(os.listdir(drawn_save_path))
    poke_forms = get_poke_form_records(cursor)
    for poke_form, poke_info in poke_forms.items():
        filenames = generate_drawn_filenames(poke_info, cursor)    # generate_drawn_filenames actually returns a list, usually len==1, but if its a female it has to generate a male filename too
        for filename in filenames:
            exists = file_does_exist(filename, drawn_files)
            file_ids = {"filename": filename, "poke_num": poke_form[0], "form_id": poke_form[1], "does_exist": exists}
            insert_into_table(cursor, "drawn_filenames", **file_ids)


NO_DRAWN_FORMS = {
    172: {"-Form_Spiky_Eared"},
    493: {"-Form_Qmark"},
    # Only using Average Size for drawn 710-711
    710: {"-Form_Small_Size", "-Form_Large_Size", "-Form_Super_Size"},
    711: {"-Form_Small_Size", "-Form_Large_Size", "-Form_Super_Size"},
    854: {"-Form_Antique", "-Form_Phony"},
    855: {"-Form_Antique", "-Form_Phony"},
    1012: {"-Form_Artisan", "-Form_Counterfeit"},
    1013: {"-Form_Masterpiece", "-Form_Unremarkable"},
}
# Removes forms specifically for being shiny
for k,v in SHARED_SHINY_FORMS.items(): NO_DRAWN_FORMS[k] = set(v)
def generate_drawn_filenames(poke_info, cursor):
    poke_num_leading_zeros = str(poke_info["poke num"]).zfill(4)
    poke_num_int = poke_info["poke num"]
    form_name = poke_info["form name"]
    filenames = []  # Needed bc if its female, I need to create a male filename too
    if poke_num_int in NO_DRAWN_FORMS: 
        if form_name in NO_DRAWN_FORMS[poke_num_int]: 
            return []
    if has_f_form(poke_num_int, cursor=cursor) and form_name == "Default": return []  # In bulba, default drawn for a poke with a female form is a pic of both m and f
    # Removing Region, Form, and Default tags, leaving -values
    for excl in ["Region_", "Form_", "Default"]:
        if excl in form_name: form_name = form_name.replace(excl, "")
    # No drawn females until gen5, and then seperated by -Female/Male denoter
    if poke_info["poke gen"] >= 5 and "-f" in form_name:
        form_name = "-Female"
        filenames.append(f"{poke_num_leading_zeros} {poke_info["poke name"]}-Male")
    elif "-f" in form_name: # Gen < 5
        form_name = ""

    filenames.append(f"{poke_num_leading_zeros} {poke_info["poke name"]}{form_name}")
    return filenames


def populate_pokeballs(cursor):
    for ball in POKEBALLS:
        insert_into_table(cursor, "pokeballs", **ball)


def populate_pokeball_img_types(cursor):
    for img_type in POKEBALL_IMG_TYPES:
        insert_into_table(cursor, "pokeball_img_types", **img_type)


def get_all_pokeballs(cursor):
    cursor.execute("SELECT * FROM pokeballs")
    data = cursor.fetchall()
    pokeballs = {}
    for ball in data:
        # name: {}
        pokeballs[ball["id"]] = {"name": ball["name"], "gen": ball["gen"], "exclusive to": ball["game_exclusive"]}
    return pokeballs


def get_all_pokeball_img_types(cursor):
    cursor.execute("SELECT * FROM pokeball_img_types")
    data = cursor.fetchall()
    pokeball_img_types = {}
    for img_type in data:
        pokeball_img_types[img_type["id"]] = {"name": img_type["name"], "gen": img_type["gen"]}
    return pokeball_img_types


def populate_pokeball_filenames(cursor):
    from app_globals import pokeball_save_path

    print("Populating pokeball filenames into database...")

    pokeballs = get_all_pokeballs(cursor)
    pokeball_img_types = get_all_pokeball_img_types(cursor)

    pokeball_files = set(os.listdir(pokeball_save_path))
    for ball_id, ball_info in pokeballs.items():
        for img_type_id, img_type_info in pokeball_img_types.items():
            filenames = generate_pokeball_filename(ball_info, img_type_info)
            # Iterating bc generate pokeball filename returns a list, because if gen3 Ultra Ball theres inter-gen differences (ie multiple filenames)
            for filename in filenames:
                exists = file_does_exist(filename, pokeball_files)
                file_ids = {"filename": filename, "pokeball_id": ball_id, "img_type_id": img_type_id, "does_exist": exists}
                insert_into_table(cursor, "pokeball_filenames", **file_ids)


# TODO: May have to adapt strange ball since it was like a mid-gen introduction
# TODO: Only has HOME and LA bag sprites if its in LA, and if not strange ball note as hisuian
# TODO: Bag_BDSP Not on all?
# TODO: Change exclusivity to just exclusive to, and checking platformm in exclusive to.split(", ")
def generate_pokeball_filename(ball_info, img_type_info):
    ball_name = ball_info["name"]
    img_type_name = img_type_info["name"]

    # TODO: Run POKEBALL_IMG_EXCEPTIONS
    # Ultra ball difference between Ruby_Sapphire and FRLG/Emerald
    if ball_name == "Ultra Ball" and img_type_name == "Gen3":
        return ["Ultra Ball-Gen3-FRLGE", "Ultra Ball-Gen3-RS"]
    if img_type_info["gen"] <= ball_info["gen"]:
        filename = f"{ball_name}-{img_type_name}"
        return [filename]
    return []


# TODO: Add update function to update existing, sub, and alt status for all imgs
def populate_db(force=False):
    if not db_exists():
        create_db()

    connection = sqlite3.connect(DB_PATH)
    connection.row_factory = sqlite3.Row
    cursor = connection.cursor()

    try:
        populate_pokes(cursor)
        populate_forms(cursor)
        populate_games(cursor)
        connection.commit() # Committing here so form_game_obtainability can get form ids from forms via a different connection
        populate_form_game_obtainability(cursor, force)
        populate_sprite_types(cursor)
        populate_sprite_obtainability(cursor)
        populate_game_filenames(cursor)
        connection.commit() # Committing because database was locked when populate_drawn_filenames trying to access with has_f_form
        populate_home_filenames(cursor)
        populate_home_menu_filenames(cursor)
        populate_drawn_filenames(cursor)
        populate_pokeballs(cursor)
        populate_pokeball_img_types(cursor)
        populate_pokeball_filenames(cursor)

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
    max_num = cursor.fetchone()["num"]
    connection.close()
    return max_num