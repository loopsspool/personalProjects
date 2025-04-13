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
    CREATE TABLE IF NOT EXISTS obtainable_filenames (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        filename TEXT NOT NULL,
        poke_num INTEGER NOT NULL,
        form_id INTEGER NOT NULL,
        game_id INTEGER NOT NULL,
        sprite_id INTEGER NOT NULL,
        obtainable BOOLEAN NOT NULL,
        FOREIGN KEY (poke_num, form_id, game_id, sprite_id) REFERENCES sprite_obtainability,
    );
    """)

    connection.commit()
    connection.close()


def get_form_id(cursor, form_name):
    cursor.execute("SELECT id FROM forms WHERE form_name=?", (form_name,))
    form_id = cursor.fetchone()
    if form_id: return form_id[0]
    else: return None

def get_game_id(cursor, game_name):
    cursor.execute("SELECT id FROM games WHERE name=?", (game_name,))
    game_id = cursor.fetchone()
    if game_id: return game_id[0]
    else: return None


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


def insert_form(cursor, form_name):
    cursor.execute("""
        INSERT OR IGNORE INTO forms (form_name)
        VALUES (?);
    """, (form_name,))

def insert_poke_form(cursor, poke_num, form_id):
    cursor.execute("""
        INSERT OR IGNORE INTO poke_forms (poke_num, form_id)
        VALUES (?, ?);
    """, (poke_num, form_id))


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


# Minior and Alcremie have special "shared" forms for their shinies
SHARED_SHINY_FORMS = {  774: ["-Form-Core"], 
                        869: ["-Form-Berry_Sweet", "-Form-Clover_Sweet", "-Form-Flower_Sweet", "-Form-Love_Sweet", "-Form-Ribbon_Sweet", "-Form-Star_Sweet", "-Form-Strawberry_Sweet"]
}
def populate_forms(cursor):
    print("Populating forms into database...")

    # This is to store the forms with their associated pokemon
    # Forms must be committed to the db first before I can retrieve their ID
    poke_form_arr = []

    for row in range(2, POKE_INFO_LAST_ROW + 1): 
        poke_num = row-1
        forms = get_forms_from_excel(row)
        forms = adjust_forms_for_exceptions(row-1, forms)

        for form in forms:
            insert_form(cursor, form)
            form_id = get_form_id(cursor, form)
            insert_poke_form(cursor, poke_num, form_id)

        # Putting here so poke/forms stay in numerical order for speedy lookups
        if poke_num in SHARED_SHINY_FORMS:
            for form in SHARED_SHINY_FORMS[poke_num]:
                insert_form(cursor, form)
                form_id = get_form_id(cursor, form)
                insert_poke_form(cursor, poke_num, form_id)
    

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


def insert_game(cursor, game, gen):
    cursor.execute("""
        INSERT OR IGNORE INTO games (name, gen)
        VALUES (?, ?);
    """, (game, gen))


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


def insert_form_game_obtainability(cursor, poke_num, form_id, game_id, obtainability):
    cursor.execute("""
        INSERT OR IGNORE INTO form_game_obtainability (poke_num, form_id, game_id, obtainable)
        VALUES (?, ?, ?, ?);
    """, (poke_num, form_id, game_id, obtainability))


FORM_EXCLUSIONS = {
    # Species game availability
    "filtering_for_LGPE_dex_if_needed": lambda poke_form, game: game["name"] == "LGPE" and poke_isnt_in_game(poke_form["poke num"], "LGPE"),
    "filtering_for_SwSh_dex_if_needed": lambda poke_form, game: game["name"] == "SwSh" and poke_isnt_in_game(poke_form["poke num"], "SwSh"),
    "filtering_for_BDSP_dex_if_needed": lambda poke_form, game: game["name"] == "BDSP" and poke_isnt_in_game(poke_form["poke num"], "BDSP"),
    "filtering_for_LA_dex_if_needed": lambda poke_form, game: game["name"] == "LA" and poke_isnt_in_game(poke_form["poke num"], "LA"),
    "filtering_for_SV_dex_if_needed": lambda poke_form, game: game["name"] == "SV" and poke_isnt_in_game(poke_form["poke num"], "SV"),

    # Universal Rules
    "no_pokemon_with_a_higher_generation_than_game_generation": lambda poke_form, game: poke_form["poke gen"] > game["gen"],
    "no_f_form_visual_differences_before_gen_4": lambda poke_form, game: poke_form["form name"] == "-f" and game["gen"] < 4,
    "no_fairy_forms_before_gen_6": lambda poke_form, game: poke_form["form name"] == "-Form-Fairy" and game["gen"] < 6,
    "no_megas_outside_gen_6_and_7_excluding_LGPE": lambda poke_form, game: "-Mega" in poke_form["form name"] and (game["gen"] not in (6, 7) or game["name"] == "LGPE"),
    "no_gigantamax_outside_SwSh": lambda poke_form, game: poke_form["form name"] == "-Gigantamax" and game["name"] != "SwSh",
    "no_regional_forms_before_gen_7": lambda poke_form, game: "-Region" in poke_form["form name"] and game["gen"] < 7,
    "no_regional_forms_other_than_alola_allowed_in_LGPE": lambda poke_form, game: game["name"] == "LGPE" and "-Region" in poke_form["form name"] and poke_form["form name"] != "-Region-Alola",
    "no_regional_forms_in_BDSP": lambda poke_form, game: game["name"] == "BDSP" and "-Region" in poke_form["form name"],
    "no_galarian_forms_before_gen_8": lambda poke_form, game: poke_form["form name"] == "-Region-Galar" and game["gen"] < 8,
    "no_hisuian_forms_outside_certain_games": lambda poke_form, game: poke_form["form name"] == "-Region-Hisui" and game["name"] not in ("LA, SV"),
    "no_regional_forms_in_LA_other_than_hisui_and_alola_kitties": lambda poke_form, game: game["name"] == "LA" and "-Region" in poke_form["form name"] and poke_form["form name"] != "-Region-Hisui" and poke_form["poke name"] not in ("Vulpix", "Ninetales"),

    # Specific pokemon
    "no_cosplay_pikachu_outside_ORAS": lambda poke_form, game: poke_form["poke num"] == 25 and "-Form-Cosplay" in poke_form["form name"] and game["name"] != "XY-ORAS",
    "no_cap_pikachu_before_gen_7": lambda poke_form, game: poke_form["poke num"] == 25 and "-Form-Cap" in poke_form["form name"] and game["gen"] < 7,
    "no_cap_pikachu_outside_of_these_games": lambda poke_form, game: poke_form["poke num"] == 25 and "-Form-Cap" in poke_form["form name"] and game["name"] not in ("SM-USUM", "SwSh", "SV"),
    "no_world_cap_pikachu_outside_of_these_games": lambda poke_form, game: poke_form["poke num"] == 25 and poke_form["form name"] == "-Form-Cap-World" and game["name"] not in ("SwSh", "SV"),
    "no_paldean_form_tauros_in_older_games": lambda poke_form, game: poke_form["poke num"] == 128 and poke_form["form name"] != "Default" and game["name"] != "SV",
    "no_female_form_eevees_until_gen_8": lambda poke_form, game: poke_form["poke num"] == 133 and poke_form["form name"] == "-f" and game["gen"] < 8,
    "no_spiky_eared_pichu_outside_gen_4": lambda poke_form, game: poke_form["poke num"] == 172 and poke_form["form name"] == "-Form-Spiky_Eared" and game["gen"] != 4,
    "no_unown_punctuation_before_gen_3": lambda poke_form, game: poke_form["poke num"] == 201 and poke_form["form name"] in ("-Form-!", "-Form-Qmark") and game["gen"] < 3,
    "no_primal_kyogre_or_groudon_outside_gen_6_and_7": lambda poke_form, game: (poke_form["poke num"] in (382, 383)) and poke_form["form name"] == "-Form-Primal" and game["gen"] not in (6, 7),
    "no_rotom_forms_until_after_platinum": lambda poke_form, game: poke_form["poke num"] == 479 and poke_form["form name"] != "Default" and game["name"] == "Diamond-Pearl",
    "no_origin_dialga_palkia_forms_until_after_LA": lambda poke_form, game: poke_form["poke num"] in (483, 484) and poke_form["form name"] == "-Form-Origin" and game["name"] not in ("LA", "SV"),
    "no_origin_form_giratina_until_after_platinum": lambda poke_form, game: poke_form["poke num"] == 487 and poke_form["form name"] == "-Form-Origin" and game["name"] == "Diamond-Pearl",
    "no_sky_form_shaymin_until_after_platinum": lambda poke_form, game: poke_form["poke num"] == 492 and poke_form["form name"] == "-Form-Sky" and game["name"] == "Diamond-Pearl",
    "no_???_arceus_form_outside_of_gen_4": lambda poke_form, game: poke_form["poke num"] == 493 and poke_form["form name"] == "-Form-Qmark" and game["gen"] != 4,
    "no_ash_greninja_outside_of_gen_7": lambda poke_form, game: poke_form["poke num"] == 658 and poke_form["form name"] == "-Form-Ash" and game["gen"] != 7,
    "no_zygarde_forms_until_gen_7": lambda poke_form, game: poke_form["poke num"] == 718 and poke_form["form name"] != "-Form-50%" and game["gen"] < 7,
    "no_solgaleo_lunala_forms_outside_SM-USUM": lambda poke_form, game: poke_form["poke num"] in (791, 792) and poke_form["form name"] != "Default" and game["name"] != "SM-USUM",
    "no_zenith_marshadow_form_outside_gen_SM-USUM": lambda poke_form, game: poke_form["poke num"] == 802 and poke_form["form name"] != "Default" and game["name"] != "SM-USUM",
    "no_meltan_or_melmetal_until_gen_8": lambda poke_form, game: poke_form["poke num"] in (808, 809) and (game["name"] != "LGPE" and game["gen"] < 8)    # Technically these are gen 7 pokemon, that weren't available until gen 8 (excluding LGPE)
}
def is_form_obtainable(form, game):
    for exclusion in FORM_EXCLUSIONS.values():
        if exclusion(form, game):
            return False
    return True


# TODO: Add ON CONFLICT to INSERT OR IGNORE statements to update values? See where relevant
def populate_form_game_obtainability(cursor):
    print("Populating game obtainability for forms into database...")

    poke_forms = get_poke_form_records(cursor)
    games = get_game_records(cursor)
    form_game_obtainability = {}

    # Running all pokemon forms through all games to check if its obtainable
    for poke_form_id, poke_form_info in poke_forms.items():
        for game_id, game_info in games.items():
            # NOTE: Getting dict values in tuples is where things are being slowed down... namedtuples can speed that up with some effort
            obtainable = is_form_obtainable(poke_form_info, game_info)
            form_game_obtainability[(poke_form_id, game_id)] = {"poke_num": poke_form_id[0], "form_id": poke_form_id[1], "game_id": game_id, "obtainable": obtainable}

    for form_info in form_game_obtainability.values(): insert_form_game_obtainability(cursor, form_info["poke_num"], form_info["form_id"], form_info["game_id"], form_info["obtainable"])


# Default meaning front, normal color, static sprite
# Show stamp for the tea/matcha pokemon (854, 855, 1012, 1013)
SPRITE_TYPES = ["Default", "-Shiny", "-Back", "-Animated", "-Shiny-Back", "-Shiny-Animated", "-Shiny-Back-Animated", "-Back-Animated", "-Show_Stamp"]
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
    "no_animated_sprites_in_these_games": lambda pfgo_info, sprite_type: pfgo_info["game name"] in ("Gold", "Silver", "FRLG", "Ruby-Sapphire") and "Animated" in sprite_type
}
def is_sprite_possible(pfgo_info, sprite_type):
    for exclusion in SPRITE_EXCLUSIONS.values():
        if exclusion(pfgo_info, sprite_type):
            return False
    return True


# Sprites that don't exist. Shouldn't even be marked unobtainable, which is why theyre here not SPRITE_EXCLUSIONS
NONEXISTANT_SPRITES={
    "no_shiny_cosplay_pikachu": lambda poke_num, form_name, sprite_type: poke_num == 25 and "-Form-Cosplay" in form_name and "Shiny" in sprite_type,
    "no_shiny_cap_pikachu": lambda poke_num, form_name, sprite_type: poke_num == 25 and "-Form-Cap" in form_name and "Shiny" in sprite_type,
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
            sprite_obtainability[(pfgo_id, sprite_id)] = {"poke num": pfgo_id[0], "form id": pfgo_id[1], "game id": pfgo_id[2], "sprite id": sprite_id, "obtainable": sprite_possible}

    for spr_obt in sprite_obtainability.values():
        insert_sprite_obtainability(cursor, spr_obt["poke num"], spr_obt["form id"], spr_obt["game id"], spr_obt["sprite id"], spr_obt["obtainable"])


def insert_sprite_obtainability(cursor, poke_num, form_id, game_id, sprite_id, obtainability):
    cursor.execute("""
        INSERT OR IGNORE INTO sprite_obtainability (poke_num, form_id, game_id, sprite_id, obtainable)
        VALUES (?, ?, ?, ?, ?);
    """, (poke_num, form_id, game_id, sprite_id, obtainability))


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


# TODO: Glameow only poke sprite change between gen 6&7 (ie, Glameow has its own Gen7 SM-USUM Sprite)
def determine_gen_and_game(cursor, all_sprites, sprite_id, sprite_info):
    gen = sprite_info["game gen"]
    game = sprite_info["game name"]
    # This accounts for Gen7 SM-USUM reusing Gen6 XY-ORAS sprites, and using Gen6 filenames
    if sprite_info["game gen"] == 7 and sprite_info["poke gen"] < 7:
        xy_oras_sprite_equivalent = all_sprites[(sprite_id[0], sprite_id[1], get_game_id(cursor, "XY-ORAS"), sprite_id[3])]
        if xy_oras_sprite_equivalent["obtainable"]:
            gen = 6
            game = "XY-ORAS"
    return gen, game


def seperate_sprite_type_if_shiny(sprite_type):
    if sprite_type == "Default": return False, ""
    if "-Shiny" not in sprite_type: return False, sprite_type
    else: return True, sprite_type.replace("-Shiny", "")


def generate_filename(cursor, all_sprites, sprite_id, sprite_info):
    poke_num = str(sprite_info["poke num"]).zfill(4)
    form_name = "" if sprite_info["form name"] == "Default" else sprite_info["form name"]
    is_shiny, sprite_type = seperate_sprite_type_if_shiny(sprite_info["sprite type"])
    gen, game = determine_gen_and_game(cursor, all_sprites, sprite_id, sprite_info)
    # TODO: Account for gen 1-4 back sprites
        # I'm thinking just add a hyphen between Gen& Game instead of a space
        # Gen 1 all 3, RB, RG, Yellow
        # Gen 2 only Gold & Crystal, Silver should map to Gold
        # Gen 3 it seems RS use the same as emerald, but e animated things, frlg definitely different sometimes, same other times
        # Gen 4 is all over the place... Some use same across DP, Plat, and HGSS, some all different, any combo really
        # Whatever you do with the old files keep the alts if there are any
    filename = f"{poke_num} {sprite_info["poke name"]} Gen{gen}{str(" " + game) if "Back" not in sprite_type else ""}{"-Shiny" if is_shiny else ""}{form_name}{sprite_type}"
    print(sprite_id)
    print(filename)


def populate_filenames(cursor):
    print("Populating filenames into database...")
    all_sprites = get_sprites_obtainability_records(cursor)

    for sprite_id, sprite_info in all_sprites.items():
        if sprite_info["obtainable"]:
            generate_filename(cursor, all_sprites, sprite_id, sprite_info)


# TODO: Determine Alts elsewhere, perhaps in filename table having a boolean field for Alt
def populate_db():
    if not db_exists():
        create_db()

    connection = sqlite3.connect(DB_PATH)
    cursor = connection.cursor()

    try:
        populate_pokes(cursor)
        populate_forms(cursor)
        populate_games(cursor)
        populate_form_game_obtainability(cursor)
        populate_sprite_types(cursor)
        populate_sprite_obtainability(cursor)
        populate_filenames(cursor)

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
