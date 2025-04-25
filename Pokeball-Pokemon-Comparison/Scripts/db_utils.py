import sqlite3
import os
import importlib
from collections import defaultdict
from contextlib import contextmanager

from file_utils import game_sprite_path

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
        FOREIGN KEY (substitution_id) REFERENCES all_game_filenames(id)
        FOREIGN KEY (id) REFERENCES all_game_filenames(id),
        FOREIGN KEY (poke_num, form_id, game_id, sprite_id) REFERENCES sprite_obtainability
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

    # TODO: Add Drawn Filename Table
    # TODO: Add Home Filename Table
    # TODO: Add Home Menu Filename Table
        # See whats missing to download from Gen8 (Just gigantamax?)

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
        cur = connection.cursor()
        try:
            yield cur
        finally:
            cur.close()
            connection.close()


def get_poke_num(poke_name, cursor=None):
    with get_cursor(cursor) as cur:
        cur.execute("SELECT num FROM pokemon WHERE name=?", (poke_name,))
        form_id = cur.fetchone()
    if form_id: return form_id[0]
    else: return None


def get_form_id(form_name, cursor=None):
    with get_cursor(cursor) as cur:
        cur.execute("SELECT id FROM forms WHERE form_name=?", (form_name,))
        form_id = cur.fetchone()
    if form_id: return form_id[0]
    else: return None


def get_game_id(game_name, cursor=None):
    with get_cursor(cursor) as cur:
        cur.execute("SELECT id FROM games WHERE name=?", (game_name,))
        game_id = cur.fetchone()
    if game_id: return game_id[0]
    else: return None


def get_game_name(game_id, cursor=None):
    with get_cursor(cursor) as cur:
        cur.execute(f"SELECT name FROM games WHERE id={game_id}")
        game_name=cur.fetchone()
    if game_name: return game_name[0]
    else: return None


def get_poke_name(poke_id, cursor=None):
    with get_cursor(cursor) as cur:
        cur.execute(f"SELECT name FROM pokemon WHERE num={poke_id}")
        poke_name=cur.fetchone()
    if poke_name: return poke_name[0]
    else: return None


# Using cursor as a parameter here due to how this function is used... not a good way to cleanly commit to db before calling, so passing the connection that has the writes to here
def get_game_filename_id(cursor, filename):
    cursor.execute("SELECT id FROM all_game_filenames WHERE filename=?", (filename,))
    file_id = cursor.fetchone()
    if file_id: return file_id[0]
    else: return None


def get_all_game_filenames_info():
    print("Fetching file info from database...")
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


def get_missing_game_imgs_by_poke(cursor=None):
    data = defaultdict(list)
    print("Getting all missing images by pokemon...")
    
    with get_cursor(cursor) as cur:
        cur.execute("SELECT poke_num, filename FROM obtainable_game_filenames WHERE does_exist=0")
        result = cur.fetchall()
        for row in result:
            poke_num = row[0]
            data[poke_num].append(row[1])
    # { poke_num : [missing imgs list] }
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
        forms[(row[0], row[1])] = { "form name" : row[2],
                                    "poke num" : row[3],
                                    "poke name" : row[4],
                                    "poke gen" : row[5]
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
        games[row[0]] = {"name" : row[1], 
                         "gen" : row[2]}
    return games


# NOTE: These are in chronological order and that is IMPORTANT since I rely on game ids sometimes for form filtering (eg mid gen form introductions)
# TODO: If putting pokemon HOME sprites here (which I recommend against, since it isnt a game), make sure its listed last so it can have all the forms available
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
    "no_megas_outside_XY_ORAS_and_SM_USUM": lambda poke_form, game: "-Mega" in poke_form["form name"] and game["name"] not in ("XY_ORAS", "SM_USUM"),
    "no_gigantamax_outside_SwSh": lambda poke_form, game: poke_form["form name"] == "-Gigantamax" and game["name"] != "SwSh",
    "no_regional_forms_before_gen_7": lambda poke_form, game: "-Region" in poke_form["form name"] and game["gen"] < 7,
    "no_alolan_forms_before_SM_USUM": lambda poke_form, game: "-Region_Alola" in poke_form["form name"] and get_game_id(game["name"]) < get_game_id("SM_USUM"),
    "no_galarian_forms_before_SwSh": lambda poke_form, game: "-Region_Galar" in poke_form["form name"] and get_game_id(game["name"]) < get_game_id("SwSh"),
    "no_hisuian_forms_before_LA": lambda poke_form, game: "-Region_Hisui" in poke_form["form name"] and get_game_id(game["name"]) < get_game_id("LA"),
    "no_paldean_forms_before_SV": lambda poke_form, game: "-Region_Paldea" in poke_form["form name"] and get_game_id(game["name"]) < get_game_id("SV"),
    "no_regional_forms_in_BDSP": lambda poke_form, game: game["name"] == "BDSP" and "-Region" in poke_form["form name"],
    "no_regional_forms_in_LA_other_than_hisui_and_alola_kitties": lambda poke_form, game: game["name"] == "LA" and "-Region" in poke_form["form name"] and poke_form["form name"] != "-Region_Hisui" and not (poke_form["poke name"] in ("Vulpix", "Ninetales") and poke_form["form name"] == "-Region_Alola"),

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
    "no_meltan_or_melmetal_until_LGPE": lambda poke_form, game: poke_form["poke num"] in (808, 809) and get_game_id(game["name"]) < get_game_id("LGPE")    # Technically these are gen 7 pokemon, they just werent introduced until LGPE
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
            print(f"\rChecking {poke_form_info["poke num"]} form obtainability...", end='', flush=True)
            # Quick workaround to make it run faster, only generating obtainability if forced or the record doesn't exist yet
            if force or not entry_exists(cursor, "form_game_obtainability", {"poke_num": poke_form_id[0], "form_id": poke_form_id[1], "game_id": game_id}):
                obtainable = is_form_obtainable(poke_form_info, game_info)
                form_game_obtainability[(poke_form_id, game_id)] = {"poke_num": poke_form_id[0], "form_id": poke_form_id[1], "game_id": game_id, "obtainable": obtainable}

    # Resetting console line after updates from above
    print('\r' + ' '*60 + '\r', end='')
    for form_info in form_game_obtainability.values(): insert_into_table(cursor, "form_game_obtainability", **form_info)


def entry_exists(cursor, table, cols):
    where_clause = " AND ".join(f"{k} = ?" for k in cols)
    values = tuple(cols.values())

    query = f"SELECT 1 FROM {table} WHERE {where_clause} LIMIT 1"
    cursor.execute(query, values)
    return cursor.fetchone() is not None


# Default meaning front, normal color, static sprite
# Show stamp for the tea/matcha pokemon (854, 855, 1012, 1013)
SPRITE_TYPES = ["Default", "-Animated", "-Shiny", "-Shiny-Animated", "-Back", "-Back-Animated", "-Shiny-Back", "-Shiny-Back-Animated", "-Show_Stamp"]
def populate_sprite_types(cursor):
    print("Populating sprite types into database...")
    for type in SPRITE_TYPES:
        cursor.execute("INSERT OR IGNORE INTO sprite_types (name) VALUES (?)", (type,))


def get_sprite_types(cursor):
    cursor.execute("SELECT * FROM sprite_types")
    sprite_types = {}
    for row in cursor.fetchall():
        sprite_types[row[0]] = row[1]
    return sprite_types


def get_poke_form_obtainability_records(cursor):
    cursor.execute("""
        SELECT p.num, f.id, g.id, f.form_name, fgo.poke_num, p.name, g.name, g.gen, fgo.obtainable
        FROM form_game_obtainability fgo
        JOIN forms f ON fgo.form_id = f.id
        JOIN pokemon p ON fgo.poke_num = p.num
        JOIN games g ON fgo.game_id = g.id
    """)
    forms = {}
    for row in cursor.fetchall():
        # (poke num, form id, game id) maps to form/poke/game info
        forms[(row[0], row[1], row[2])] = { "form name" : row[3],
                                            "poke num" : row[4],
                                            "poke name" : row[5],
                                            "game name" : row[6],
                                            "game gen" : row[7],
                                            "obtainable" : row[8]
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
    "no_shiny_cosplay_pikachu": lambda poke_num, form_name, sprite_type: poke_num == 25 and "-Form_Cosplay" in form_name and "Shiny" in sprite_type,
    "no_shiny_cap_pikachu": lambda poke_num, form_name, sprite_type: poke_num == 25 and "-Form_Cap" in form_name and "Shiny" in sprite_type,
    "skip_all_shared_shiny_forms_that_arent_adjusted_appropriately": lambda poke_num, form_name, sprite_type: poke_num in SHARED_SHINY_FORMS and "Shiny" in sprite_type and form_name not in SHARED_SHINY_FORMS[poke_num],
    "skip_all_non_shiny_sprites_for_shared_shinies_that_are_adjusted": lambda poke_num, form_name, sprite_type: poke_num in SHARED_SHINY_FORMS and "Shiny" not in sprite_type and form_name in SHARED_SHINY_FORMS[poke_num],
    "skip_show_stamp_sprite_if_not_applicable": lambda poke_num, form_name, sprite_type: poke_num not in (854, 855, 1012, 1013) and sprite_type == "-Show_Stamp"
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
        SELECT p.num, f.id, g.id, s.id, so.poke_num, p.name, p.gen, g.gen, g.name, f.form_name, s.name, so.obtainable
        FROM sprite_obtainability so
        JOIN forms f ON so.form_id = f.id
        JOIN pokemon p ON so.poke_num = p.num
        JOIN games g ON so.game_id = g.id
        JOIN sprite_types s ON so.sprite_id = s.id
    """)
    sprites = {}
    for row in cursor.fetchall():
        # (poke num, form id, game id, sprite id) maps to form/poke/game/sprite info
        sprites[(row[0], row[1], row[2], row[3])] = {   "poke num" : row[4],
                                                        "poke name" : row[5],
                                                        "poke gen" : row[6],
                                                        "game gen" : row[7],
                                                        "game name" : row[8],
                                                        "form name" : row[9],
                                                        "sprite type": row[10],
                                                        "obtainable" : row[11]
        }
    return sprites


def seperate_sprite_type_if_shiny(sprite_type):
    if sprite_type == "Default": return False, ""
    if "-Shiny" not in sprite_type: return False, sprite_type
    else: return True, sprite_type.replace("-Shiny", "")


def file_does_exist(filename, path):
    file_ext = [".png"]
    for ext in file_ext:
        filename_w_ext = filename + ext
        if filename_w_ext in path: return True
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
    # TODO: Gen1?
    "Gen2 Silver": ["Gen2 Gold", "Gen2 Crystal"],
    "Gen2 Crystal": ["Gen2 Gold"],
    "Gen3 Emerald": ["Gen3 Ruby_Sapphire", "Gen3 FRLG"],
    "Gen3 FRLG": ["Gen3 Ruby_Sapphire"],
    "Gen4 HGSS": ["Gen4 Platinum", "Gen4 Diamond_Pearl"],
    "Gen4 Platinum": ["Gen4 Diamond_Pearl"],
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
def populate_game_filenames(cursor):
    print("Populating filenames into database...")
    all_sprites = get_sprites_obtainability_records(cursor)
    substitutions_to_convert_to_id = []
    
    for sprite_id, sprite_info in all_sprites.items():
        print(f"\rGenerating pokemon #{sprite_info["poke num"]} filenames...", end='', flush=True)
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
    print('\r' + ' '*50 + '\r', end='')

    # This is pulled out seperate since it depends on file_ids from all_game_filenames table, which may not be present yet
    # This is due to checking if the replacement filename exists in all files
    # But that replacement filename may not be inserted into the database yet, hence it doesn't have an id
    change_substitution_field_from_filename_to_file_id(cursor, substitutions_to_convert_to_id)


def edit_substitution_field(cursor, record):
    substitution_id = get_game_filename_id(cursor, record["sub_name"])
    cursor.execute(f"UPDATE all_game_filenames SET substitution_id = {substitution_id} WHERE id = {record["file_id"]}")
    cursor.execute(f"UPDATE obtainable_game_filenames SET substitution_id = {substitution_id} WHERE id = {record["file_id"]}")


def change_substitution_field_from_filename_to_file_id(cursor, sub_names_to_convert):
    print("Converting substitution filenames to ids...")
    for record in sub_names_to_convert:
        edit_substitution_field(cursor, record)


def populate_drawn_filenames(cursor):
    from app_globals import drawn_save_path
    print("Populating drawn filenames into database...")

    poke_forms = get_poke_form_records(cursor)
    for poke_form, poke_info in poke_forms.items():
        for filename in generate_drawn_filenames(poke_info):
            exists = file_does_exist(filename, drawn_save_path)
            file_ids = {"filename": filename, "poke_num": poke_form[0], "form_id": poke_form[1], "does_exist": exists}
            insert_into_table(cursor, "drawn_filenames", **file_ids)
            print(filename)


def generate_drawn_filenames(poke_info):
    poke_num = str(poke_info["poke num"]).zfill(4)
    form_name = poke_info["form name"]
    filenames = []  # Needed bc if its female, I need to create a male filename too
    # Removing Region and Form tags, leaving -values. And removing default
    exclude_from_form = ["Region_", "Form_", "Default"]
    for excl in exclude_from_form:
        if excl in form_name: 
            form_name = form_name.replace(excl, "")
    # No drawn females until gen5, and then seperated by -Female/Male denoter
    if poke_info["poke gen"] >= 5 and form_name == "-f":
        form_name = "-Female"
        filenames.append(f"{poke_num} {poke_info["poke name"]}-Male.png")
    elif form_name == "-f":
        form_name = ""

    filenames.append(f"{poke_num} {poke_info["poke name"]}{form_name}.png")
    return filenames


def populate_db(force=False):
    if not db_exists():
        create_db()

    connection = sqlite3.connect(DB_PATH)
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
        # TODO: This says db is locked for some reason
        #populate_drawn_filenames(cursor)

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