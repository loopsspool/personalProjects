import sqlite3
import os
from collections import defaultdict
from contextlib import contextmanager

from app_globals import *
from db_reference_data import *
from spreadsheet_utils import *
from translation_utils import get_game_needing_special_translation_for_mid_gen_pokes


#|================================================================================================|
#|~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~[     DATABASE INFO     ]~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~|
#|================================================================================================|

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
    CREATE TABLE IF NOT EXISTS costumes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        costume_name TEXT NOT NULL UNIQUE
    );
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS poke_costumes (
        poke_num INTEGER NOT NULL,
        costume_id INTEGER NOT NULL,
        PRIMARY KEY (poke_num, costume_id),
        FOREIGN KEY (poke_num) REFERENCES pokemon(num),
        FOREIGN KEY (costume_id) REFERENCES costumes(id)
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
        does_exist BOOLEAN NOT NULL,
        substitution_id INTEGER,
        has_alt BOOLEAN,
        FOREIGN KEY (substitution_id) REFERENCES all_game_filenames(id),
        FOREIGN KEY (id) REFERENCES all_game_filenames(id),
        FOREIGN KEY (poke_num, form_id, game_id, sprite_id) REFERENCES sprite_obtainability
    );
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS all_home_filenames (
        id INTEGER PRIMARY KEY,
        filename TEXT NOT NULL UNIQUE,
        poke_num INTEGER NOT NULL,
        form_id INTEGER NOT NULL,
        sprite_id INTEGER NOT NULL,
        obtainable BOOLEAN NOT NULL,
        does_exist BOOLEAN,
        FOREIGN KEY (poke_num, form_id) REFERENCES poke_forms,
        FOREIGN KEY (sprite_id) REFERENCES sprite_types(id)
    );
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS obtainable_home_filenames (
        id INTEGER PRIMARY KEY,
        filename TEXT NOT NULL UNIQUE,
        poke_num INTEGER NOT NULL,
        form_id INTEGER NOT NULL,
        sprite_id INTEGER NOT NULL,
        does_exist BOOLEAN NOT NULL,
        FOREIGN KEY (poke_num, form_id) REFERENCES poke_forms,
        FOREIGN KEY (sprite_id) REFERENCES sprite_types(id)
    );
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS all_bank_filenames (
        id INTEGER PRIMARY KEY,
        filename TEXT NOT NULL UNIQUE,
        poke_num INTEGER NOT NULL,
        form_id INTEGER NOT NULL,
        sprite_id INTEGER NOT NULL,
        obtainable BOOLEAN NOT NULL,
        does_exist BOOLEAN,
        FOREIGN KEY (poke_num, form_id) REFERENCES poke_forms,
        FOREIGN KEY (sprite_id) REFERENCES sprite_types(id)
    );
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS obtainable_bank_filenames (
        id INTEGER PRIMARY KEY,
        filename TEXT NOT NULL UNIQUE,
        poke_num INTEGER NOT NULL,
        form_id INTEGER NOT NULL,
        sprite_id INTEGER NOT NULL,
        does_exist BOOLEAN NOT NULL,
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
    CREATE TABLE IF NOT EXISTS all_go_filenames (
        id INTEGER PRIMARY KEY,
        filename TEXT NOT NULL UNIQUE,
        poke_num INTEGER NOT NULL,
        form_id INTEGER NOT NULL,
        costume_id INTEGER NOT NULL,
        sprite_id INTEGER NOT NULL,
        obtainable BOOLEAN NOT NULL,
        does_exist BOOLEAN,
        FOREIGN KEY (poke_num, form_id) REFERENCES poke_forms,
        FOREIGN KEY (poke_num, costume_id) REFERENCES poke_costumes,
        FOREIGN KEY (sprite_id) REFERENCES sprite_types(id)
    );
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS obtainable_go_filenames (
        id INTEGER PRIMARY KEY,
        filename TEXT NOT NULL UNIQUE,
        poke_num INTEGER NOT NULL,
        form_id INTEGER NOT NULL,
        costume_id INTEGER NOT NULL,
        sprite_id INTEGER NOT NULL,
        does_exist BOOLEAN NOT NULL,
        FOREIGN KEY (poke_num, form_id) REFERENCES poke_forms,
        FOREIGN KEY (poke_num, costume_id) REFERENCES poke_costumes,
        FOREIGN KEY (sprite_id) REFERENCES sprite_types(id)
    );
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS pokeballs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL UNIQUE,
        gen INGEGER NOT NULL,
        exclusive_to TEXT DEFAULT NULL
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
    CREATE TABLE IF NOT EXISTS all_pokeball_filenames (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        pokeball_id INTEGER NOT NULL,
        img_type_id INTEGER NOT NULL,
        filename TEXT NOT NULL UNIQUE,
        obtainable BOOLEAN NOT NULL,
        does_exist BOOLEAN,
        FOREIGN KEY (pokeball_id) REFERENCES pokeballs(id),
        FOREIGN KEY (img_type_id) REFERENCES pokeball_img_types(id)
    );
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS obtainable_pokeball_filenames (
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


def populate_db(force=False):
    if not db_exists():
        create_db()

    connection = sqlite3.connect(DB_PATH)
    connection.row_factory = sqlite3.Row
    cursor = connection.cursor()

    try:
        populate_pokes(cursor)
        populate_forms(cursor)
        populate_costumes(cursor)
        populate_games(cursor)
        connection.commit() # Committing here so form_game_obtainability can get form ids from forms via a different connection
        populate_form_game_obtainability(cursor, force)
        populate_sprite_types(cursor)
        populate_sprite_obtainability(cursor)
        populate_game_filenames(cursor)
        connection.commit() # Committing because database was locked when populate_drawn_filenames trying to access with has_f_form
        populate_home_filenames(cursor)
        populate_home_menu_filenames(cursor)
        populate_bank_filenames(cursor)
        connection.commit() # Db locked again
        populate_go_filenames(cursor)
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


# TODO: After adding all/obtainable HOME filenames this updated a bunch of files?
def update_file_existence(cursor=None):
    print("Updating database if there were any downloads...")

    update_save_dir_existing_files()

    # Updating database
    with get_cursor(cursor) as cur:
        update_game_files_existence(cur)
        update_non_game_files_existence("all_home_filenames", save_directories["HOME"]["files"], cur)
        update_non_game_files_existence("obtainable_home_filenames", save_directories["HOME"]["files"], cur)

        update_non_game_files_existence("all_bank_filenames", save_directories["BANK"]["files"], cur)
        update_non_game_files_existence("obtainable_bank_filenames", save_directories["BANK"]["files"], cur)

        update_non_game_files_existence("all_go_filenames", save_directories["GO"]["files"], cur)
        update_non_game_files_existence("obtainable_go_filenames", save_directories["GO"]["files"], cur)

        update_non_game_files_existence("home_menu_filenames", save_directories["HOME Menu"]["files"], cur)
        update_non_game_files_existence("drawn_filenames", save_directories["Drawn"]["files"], cur)

        update_non_game_files_existence("all_pokeball_filenames", save_directories["Pokeball"]["files"], cur)
        update_non_game_files_existence("obtainable_pokeball_filenames", save_directories["Pokeball"]["files"], cur)

    


#|================================================================================================|
#|~~~~~~~~~~~~~~~~~~~~~~~~~~[     DATABASE UNIVERSAL COMMANDS     ]~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~|
#|================================================================================================|

@contextmanager
def get_cursor(passed_cur=None):
    if passed_cur is not None:
        yield passed_cur
        passed_cur.connection.commit()
    else:
        connection = sqlite3.connect(DB_PATH)
        connection.row_factory = sqlite3.Row
        cur = connection.cursor()
        try:
            yield cur
            connection.commit()
        finally:            
            connection.close()


def insert_into_table(cursor, table, **data):
    cols = ", ".join(data.keys())
    val_placeholders = ", ".join(["?"] * len(data))
    vals = tuple(data.values())

    query = f"INSERT OR IGNORE INTO {table} ({cols}) VALUES ({val_placeholders})"
    cursor.execute(query, vals)
    return cursor.lastrowid


def insert_into_table_w_unobtainables(cursor, obtainable, table, **data):
    data_w_obtainable = {**data, "obtainable": obtainable}
    insert_into_table(cursor, table, **data_w_obtainable)


def insert_into_both_form_tables(cursor, form_name, poke_num):
    insert_into_table(cursor, "forms", **{"form_name": form_name})
    form_id = get_form_id(form_name, cursor)
    insert_into_table(cursor, "poke_forms", **{"poke_num": poke_num, "form_id": form_id})


def insert_into_both_costume_tables(cursor, costume_name, poke_num):
    insert_into_table(cursor, "costumes", **{"costume_name": costume_name})
    costume_id = get_costume_id(costume_name, cursor)
    insert_into_table(cursor, "poke_costumes", **{"poke_num": poke_num, "costume_id": costume_id})


# TODO: Change all execute statements to parameter substition instead of inserting into f string (this converts None <-> Null properly)
def update_game_files_existence(cursor):
    cursor.execute("SELECT * FROM obtainable_game_filenames")
    obtainable_game_filename_data = cursor.fetchall()
    for record in obtainable_game_filename_data:
        does_exist, substitution = check_for_usable_game_file(record["filename"], True)     # True parameter bc obtainable game sprites will always be obtainable (duh)
        sub_id = get_game_filename_id(cursor, substitution) if substitution!=None else None
        has_alt = file_exists(substitution + "-Alt", save_directories["Game Sprites"]["files"]) if sub_id!=None else file_exists(record["filename"] + "-Alt", save_directories["Game Sprites"]["files"])
        if does_exist != record["does_exist"] or sub_id != record["substitution_id"] or has_alt != record["has_alt"]:
            print(f"File updated: {record["filename"]}")
            # Updating obtainable game filenames table
            cursor.execute("""
                            UPDATE obtainable_game_filenames 
                            SET does_exist = ?, substitution_id = ?, has_alt = ?
                            WHERE id = ?
            """, (does_exist, sub_id, has_alt, record["id"]))
            # Updating all game filenames table
            cursor.execute("""
                            UPDATE all_game_filenames 
                            SET does_exist = ?, substitution_id = ?, has_alt = ?
                            WHERE id = ?
            """, (does_exist, sub_id, has_alt, record["id"]))


def update_non_game_files_existence(table, set_of_saved_imgs, cursor):
    cursor.execute(f"SELECT * FROM {table}")
    table_data = cursor.fetchall()
    for record in table_data:
        does_exist = file_exists(record["filename"], set_of_saved_imgs)
        db_existence_value = False if record["does_exist"]==None else record["does_exist"]    # This protects tables with unobtainable filenames, so the None existence value for unobtainable files wont get changed to False
        if does_exist != db_existence_value:
            print(f"In table {table}, file updated: {record["filename"]}")
            cursor.execute(f"""
                            UPDATE {table} 
                            SET does_exist = ?
                            WHERE id = ?
            """, (does_exist, record["id"]))




#|================================================================================================|
#|~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~[     GETTERS     ]~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~|
#|================================================================================================|


#|~~~~~~~~~~~~~~~~~~~~~~~~~~~~[     FIELD GETTERS     ]~~~~~~~~~~~~~~~~~~~~~~~~~~~~|

def get_last_poke_num():
    connection = sqlite3.connect(DB_PATH)
    cursor = connection.cursor()
    cursor.execute("SELECT MAX(num) FROM pokemon")
    max_num = cursor.fetchone()[0]
    connection.close()
    return max_num


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


def get_costume_id(costume_name, cursor=None):
    with get_cursor(cursor) as cur:
        cur.execute("SELECT id FROM costumes WHERE costume_name=?", (costume_name,))
        costume_id = cur.fetchone()
    if costume_id: return costume_id["id"]
    else: return None


def get_costume_name(costume_id, cursor=None):
    with get_cursor(cursor) as cur:
        cur.execute("SELECT costume_name FROM costumes WHERE id=?", (costume_id,))
        costume_name = cur.fetchone()
    if costume_name: return costume_name["costume_name"]
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


def external_get_game_filename_id(filename, cursor=None):
    with get_cursor(cursor) as cur:
        cur.execute("SELECT id FROM all_game_filenames WHERE filename=?", (filename,))
        file_id = cur.fetchone()
    if file_id: return file_id["id"]
    else: return None


def get_HOME_filename_id(filename, cursor=None):
    with get_cursor(cursor) as cur:
        cur.execute("SELECT id FROM all_home_filenames WHERE filename=?", (filename,))
        file_id = cur.fetchone()
    if file_id: return file_id["id"]
    else: return None


def get_sprite_type_id(sprite_type_name, cursor=None):
    with get_cursor(cursor) as cur:
        cur.execute("SELECT id FROM sprite_types WHERE name=?", (sprite_type_name,))
        sprite_type_id=cur.fetchone()
    if sprite_type_id: return sprite_type_id["id"]
    else: return None


def get_sprite_type_name(sprite_type_id, cursor=None):
    with get_cursor(cursor) as cur:
        cur.execute(f"SELECT name FROM sprite_types WHERE id={sprite_type_id}")
        sprite_type_name=cur.fetchone()
    if sprite_type_name: return sprite_type_name["name"]
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




#|~~~~~~~~~~~~~~~~~~~~~~~~~~~~[     RECORD GETTERS     ]~~~~~~~~~~~~~~~~~~~~~~~~~~~~|

def get_game_records(cursor):
    cursor.execute("SELECT * FROM GAMES")
    games = {}
    for row in cursor.fetchall():
        # Game id maps to game info
        games[row["id"]] = {"name" : row["name"], 
                            "gen" : row["gen"]}
    return games


def get_all_pokeballs(cursor):
    cursor.execute("SELECT * FROM pokeballs")
    data = cursor.fetchall()
    pokeballs = {}
    for ball in data:
        # name: {}
        pokeballs[ball["id"]] = {"name": ball["name"], "gen": ball["gen"], "exclusive_to": ball["exclusive_to"]}
    return pokeballs


def get_all_pokeball_img_types(cursor):
    cursor.execute("SELECT * FROM pokeball_img_types")
    data = cursor.fetchall()
    pokeball_img_types = {}
    for img_type in data:
        pokeball_img_types[img_type["id"]] = {"name": img_type["name"], "gen": img_type["gen"]}
    return pokeball_img_types


def get_sprite_types(cursor):
    cursor.execute("SELECT * FROM sprite_types")
    sprite_types = {}
    for row in cursor.fetchall():
        sprite_types[row["id"]] = row["name"]
    return sprite_types


def get_all_form_names_for_poke(poke_num, cursor=None):
    with get_cursor(cursor) as cur:
        cur.execute("""
            SELECT f.form_name
            FROM poke_forms pf
            JOIN forms f ON pf.form_id = f.id
            WHERE pf.poke_num = ?
        """, (poke_num,))
        form_names = cur.fetchall()

    if form_names: return [row["form_name"] for row in form_names]
    else: return None


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


def get_poke_costume_records(cursor):
    cursor.execute("SELECT poke_num, costume_id FROM poke_costumes")

    costumes = defaultdict(list)
    for row in cursor.fetchall():
        costumes[row["poke_num"]].append(row["costume_id"])

    return costumes


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




# TODO: Note (in func name?) that these filenames_info funcs are for spreadsheet checklist
#|~~~~~~~~~~~~~~~~~~~~~~~~~~~~[     FILENAME GETTERS     ]~~~~~~~~~~~~~~~~~~~~~~~~~~~~|

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


def get_all_1D_non_game_filename_info(table):
    connection = sqlite3.connect(DB_PATH)
    connection.row_factory = sqlite3.Row
    cursor = connection.cursor()

    cursor.execute(f"SELECT poke_num, form_id, filename, does_exist FROM {table}")
    rows = cursor.fetchall()
    data = {}

    for row in rows:
        key = (row["poke_num"], row["form_id"])
        data[key] = {"filename": row["filename"], "exists": True if row["does_exist"] else False}

    connection.close()
    return data


# Used where want spreadsheet cols of Default and Shiny based off table
def get_all_default_and_shiny_filenames_info(table):
    connection = sqlite3.connect(DB_PATH)
    connection.row_factory = sqlite3.Row
    cursor = connection.cursor()

    cursor.execute(f"SELECT * FROM {table}")
    rows = cursor.fetchall()
    data = defaultdict(lambda: defaultdict(dict))

    for row in rows:
        main_key = (row["poke_num"], row["form_id"]) if table != "all_go_filenames" else (row["poke_num"], row["form_id"], row["costume_id"])
        sprite_type_name = get_sprite_type_name(row["sprite_id"], cursor)
        data[main_key][sprite_type_name]["filename"] = row["filename"]  # Necessary to get tags
        if "obtainable" in row.keys():     # This allows this function to be called from a table regardless if it contains unobtainable filenames
            data[main_key][sprite_type_name]["obtainable"] = True if row["obtainable"] else False  
        data[main_key][sprite_type_name]["exists"] = True if row["does_exist"] else False        

    # for k,v in data.items(): print(f"{k}: {v}")
    # print(table == "all_go_filenames")
    connection.close()
    return data


def get_all_home_filenames_info():
    connection = sqlite3.connect(DB_PATH)
    connection.row_factory = sqlite3.Row
    cursor = connection.cursor()

    cursor.execute("SELECT * FROM all_home_filenames")
    rows = cursor.fetchall()
    data = defaultdict(lambda: defaultdict(dict))

    for row in rows:
        main_key = (row["poke_num"], row["form_id"])
        sprite_type_name = get_sprite_type_name(row["sprite_id"], cursor)
        data[main_key][sprite_type_name]["filename"] = row["filename"]  # Necessary to get tags
        data[main_key][sprite_type_name]["obtainable"] = True if row["obtainable"] else False
        data[main_key][sprite_type_name]["exists"] = True if row["does_exist"] else False

    connection.close()
    return data


def get_all_pokeball_filename_info():
    connection = sqlite3.connect(DB_PATH)
    connection.row_factory = sqlite3.Row
    cursor = connection.cursor()

    cursor.execute("SELECT pokeball_id, img_type_id, obtainable, does_exist FROM all_pokeball_filenames")
    rows = cursor.fetchall()
    data = defaultdict(lambda: defaultdict(dict))

    for row in rows:
        pokeball = get_pokeball_name(row["pokeball_id"], cursor)
        img_type = get_pokeball_img_type_name(row["img_type_id"], cursor)
        
        data[pokeball][img_type] = {
            "obtainable": row["obtainable"],
            "exists": row["does_exist"]
        }

    # TODO: Dream Ball not registering as True
    # Converting Gen5 battle statics into one element
    battle_statics_obtainable = True
    battle_statics_all_exist = True
    # Below necessary bc I can't change dict size while iterating
    add_dict = {}
    del_key_list = []
    # Grabbing data for condensing
    for pokeball, img_type in data.items():
        for i in range(9):
            img_key = f"Gen5_Battle-Static_{i}"
            if img_key not in del_key_list: del_key_list.append(img_key)

            if not img_type[img_key]["obtainable"]:
                battle_statics_obtainable = False
                battle_statics_all_exist = False
                break
            if not img_type[img_key]["exists"]:
                battle_statics_all_exist = False
                break

        add_dict[pokeball] = {"Gen5_Battle-Statics": {"obtainable": battle_statics_obtainable, "exists": battle_statics_all_exist}}

    # Updating data dict
    for pokeball in list(data.keys()):  # Creating list of keys so I can iterate over dict while deleting/adding
        # Deleting 0-9 labeled static file info
        for img_type_key in del_key_list:
            del data[pokeball][img_type_key]
        # Adding singular condensed element that will say if ALL do or dont exist/obtainable
        data[pokeball]["Gen5_Battle-Statics"] = add_dict[pokeball]["Gen5_Battle-Statics"]


    # Updating Gen3 Ultra Ball differences
    # Doing this way since I split it off when generating filenames, not in dict I generate img_types from. These are both Gen3 Img type
    # Initially in row in rows loop it gets overwritten, this ensures if both exist it will appear that way, otherwise they will appear missing
    if "Ultra Ball-Gen3-FRLGE.png" in save_directories["Pokeball"]["files"] and "Ultra Ball-Gen3-RS.png" in save_directories["Pokeball"]["files"]:
        data["Ultra Ball"]["Gen3"]["exists"] = True
    else: data["Ultra Ball"]["Gen3"]["exists"] = False

    connection.close()
    return data


def get_missing_poke_imgs_by_table(poke_num, table, cursor=None):
    data = defaultdict(list)
    
    with get_cursor(cursor) as cur:
        fields = "poke_num, form_id, filename"
        if table == "obtainable_go_filenames": fields += ", costume_id"
        cur.execute(f"SELECT {fields} FROM {table} WHERE poke_num={poke_num} AND does_exist=0")
        result = cur.fetchall()
        for row in result:
            # { (poke_num, form_id) : [missing imgs list] }
            poke_info = (row["poke_num"], row["form_id"]) if table != "obtainable_go_filenames" else (row["poke_num"], row["form_id"], row["costume_id"])
            data[poke_info].append(row["filename"])
    return data


def get_missing_pokeball_imgs(cursor=None):
    data = defaultdict(list)
    print("Getting all missing pokeball images...")

    with get_cursor(cursor) as cur:
        cur.execute("SELECT pokeball_id, img_type_id, filename FROM obtainable_pokeball_filenames WHERE does_exist=0")
        result = cur.fetchall()
        for row in result:
            # { (pokeball_id, img_type_id) : [missing imgs list] }
            # Have to do it as a list because of gen3 ultra ball having two imgs for same ball img type...
            pokeball_info = (row["pokeball_id"], row["img_type_id"])
            data[pokeball_info].append(row["filename"])
    return data




#|================================================================================================|
#|~~~~~~~~~~~~~~~~~~~~~~~~~~~~[     VERIFICATION FUNCTIONS     ]~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~|
#|================================================================================================|

def db_exists():
    return os.path.exists(DB_PATH)


def record_exists(cursor, table, cols):
    where_clause = " AND ".join(f"{k} = ?" for k in cols)
    values = tuple(cols.values())

    query = f"SELECT 1 FROM {table} WHERE {where_clause} LIMIT 1"
    cursor.execute(query, values)
    return cursor.fetchone() is not None


# TODO: When applicable, should only be webp
def file_exists(filename, dir_file_list):
    # Keep .png first since it's most common img type for this
    file_ext = [".png", ".gif", ".webm"]
    #  Checking all extensions in path
    for ext in file_ext:
        filename_w_ext = filename + ext
        if filename_w_ext in dir_file_list: return True
    return False


def has_f_form(poke_num, cursor=None):
    with get_cursor(cursor) as cur:
        cur.execute(f"SELECT form_id FROM poke_forms WHERE poke_num={poke_num} AND form_id={get_form_id("-f")}")
        result = cur.fetchone()
    if result: return True
    else: return False


def has_regional_form(poke_num, region, cursor=None):
    with get_cursor(cursor) as cur:
        cur.execute(f"SELECT form_id FROM poke_forms WHERE poke_num={poke_num} AND form_id={get_form_id(f"-Region_{region}")}")
        result = cur.fetchone()
    if result: return True
    else: return False


def has_default_form(poke_num):
    if poke_num not in NO_DEFAULT_FORM_POKE_NUMS: return True
    else: return False


def is_stamped_poke_form(poke_num, form_name):
    if poke_num in STAMPED_FORM_POKES and form_name != "Default": return True
    else: return False




#|================================================================================================|
#|~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~[     GAME TABLE     ]~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~|
#|================================================================================================|

def populate_games(cursor):
    print("Populating games into database...")

    for game in GAMES:
        insert_into_table(cursor, "games", **{"name": game[0], "gen": game[1]})




#|================================================================================================|
#|~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~[     POKEMON TABLE     ]~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~|
#|================================================================================================|

def populate_pokes(cursor):
    print("Populating Pokemon into database...")

    # Grabbing information from pokemon info spreadsheet
    for row in range(2, POKE_INFO_LAST_ROW + 1):
        num = row - 1
        num_as_str = str(cell_value(POKEMON_INFO_SHEET, row, POKE_INFO_NUM_COL))
        name = cell_value(POKEMON_INFO_SHEET, row, POKE_INFO_NAME_COL)
        gen = cell_value(POKEMON_INFO_SHEET, row, POKE_INFO_GEN_COL)
        insert_into_table(cursor, "pokemon", **{"num": num, "num_as_text": num_as_str, "name": name, "gen": gen})




#|================================================================================================|
#|~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~[     FORM & POKE_FORM TABLES     ]~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~|
#|================================================================================================|

def populate_forms(cursor):
    print("Populating forms and poke_forms into database...")

    for row in range(2, POKE_INFO_LAST_ROW + 1): 
        poke_num = row-1
        forms = get_forms_from_excel(row)
        forms = adjust_forms_for_exceptions(row-1, forms)

        # Inserting into BOTH tables means forms table (just id and name) and poke_forms table (id, name, and poke it applies to)
        for form in forms:
            insert_into_both_form_tables(cursor, form, poke_num)

        # Putting here so poke/forms stay in numerical order for speedy lookups
        if poke_num in SHARED_SHINY_FORMS:
            for form in SHARED_SHINY_FORMS[poke_num]:
                insert_into_both_form_tables(cursor, form, poke_num)



def get_forms_from_excel(row):
    forms = []
    poke_num = int(cell_value(POKEMON_INFO_SHEET, row, POKE_INFO_NUM_COL))
    regional_form_field = cell_value(POKEMON_INFO_SHEET, row, POKE_INFO_REG_FORMS_COL)
    misc_form_field = cell_value(POKEMON_INFO_SHEET, row, POKE_INFO_MISC_FORMS_COL)

    if has_default_form(poke_num): forms.append("Default")
    if isnt_empty(POKEMON_INFO_SHEET, row, POKE_INFO_F_COL): forms.append("-f")
    if isnt_empty(POKEMON_INFO_SHEET, row, POKE_INFO_MEGA_COL): forms.append("-Mega")
    if isnt_empty(POKEMON_INFO_SHEET, row, POKE_INFO_GIGANTA_COL): forms.append("-Gigantamax")
    if isnt_empty(POKEMON_INFO_SHEET, row, POKE_INFO_REG_FORMS_COL): forms.extend(denote_forms(regional_form_field, "-Region_"))
    if isnt_empty(POKEMON_INFO_SHEET, row, POKE_INFO_MISC_FORMS_COL): forms.extend(denote_forms(misc_form_field, "-Form_"))

    return forms


def denote_forms(forms, denotion):
    forms_arr = forms.split(", ")
    denoted_arr = []
    for form in forms_arr:
        form_no_spaces = form.replace(" ", "_")
        denoted_form = denotion + form_no_spaces
        denoted_arr.append(denoted_form)
    return denoted_arr


def adjust_forms_for_exceptions(poke_num, forms):
    if poke_num not in FORM_EXCEPTION_POKEMON:
        return forms
    
    to_remove, replacements = FORM_EXCEPTION_POKEMON[poke_num]
    filtered_forms = [form for form in forms if form not in to_remove]
    filtered_forms.extend(replacements)

    return filtered_forms




#|================================================================================================|
#|~~~~~~~~~~~~~~~~~~~~~~~~~[     COSTUME & POKE_COSTUME TABLES     ]~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~|
#|================================================================================================|

def populate_costumes(cursor):
    print("Populating costumes and poke_costumes into database...")

    for row in range(2, POKE_INFO_LAST_ROW + 1): 
        poke_num = row-1
        insert_into_both_costume_tables(cursor, "None", poke_num)

        if isnt_empty(POKEMON_INFO_SHEET, row, POKE_INFO_COSTUMES_COL):
            costumes = denote_forms(cell_value(POKEMON_INFO_SHEET, row, POKE_INFO_COSTUMES_COL), "-Costume_")

            # Inserting into BOTH tables means forms table (just id and name) and poke_forms table (id, name, and poke it applies to)
            for costume in costumes:
                insert_into_both_costume_tables(cursor, costume, poke_num)




#|================================================================================================|
#|~~~~~~~~~~~~~~~~~~~~~~~~~[     FORM GAME OBTAINABILITY TABLE     ]~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~|
#|================================================================================================|

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
            if force or not record_exists(cursor, "form_game_obtainability", {"poke_num": poke_form_id[0], "form_id": poke_form_id[1], "game_id": game_id}):
                obtainable = is_form_obtainable(poke_form_info, game_info)
                form_game_obtainability[(poke_form_id, game_id)] = {"poke_num": poke_form_id[0], "form_id": poke_form_id[1], "game_id": game_id, "obtainable": obtainable}

    # Resetting console line after updates from above
    print('\r' + ' '*60 + '\r', end='')
    for form_info in form_game_obtainability.values(): insert_into_table(cursor, "form_game_obtainability", **form_info)


def is_form_obtainable(form, game):
    for exclusion in FORM_EXCLUSIONS.values():
        if exclusion(form, game):
            return False
    return True




#|================================================================================================|
#|~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~[     SPRITE TYPES TABLE     ]~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~|
#|================================================================================================|

def populate_sprite_types(cursor):
    print("Populating sprite types into database...")
    for type in SPRITE_TYPES:
        cursor.execute("INSERT OR IGNORE INTO sprite_types (name) VALUES (?)", (type,))




#|================================================================================================|
#|~~~~~~~~~~~~~~~~~~~[     POKE_FORM GAME SPRITE OBTAINABILITY TABLE     ]~~~~~~~~~~~~~~~~~~~~~~~~|
#|================================================================================================|

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


def is_sprite_possible(pfgo_info, sprite_type):
    for exclusion in SPRITE_EXCLUSIONS.values():
        if exclusion(pfgo_info, sprite_type):
            return False
    return True


def should_skip_nonexistant_sprite(poke_num, form_name, sprite_type):
    for nonexistant in NONEXISTANT_SPRITES.values():
        if nonexistant(poke_num, form_name, sprite_type):
            return True
    return False




#|================================================================================================|
#|~~~~~~~~~~~~~~~~~~~~~~~~~[     GAME SPRITES FILENAME TABLE     ]~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~|
#|================================================================================================|

#|~~~~~~~~~~~~~~~~~~~~~~~~~[     GAME SPRITE DB FUNCTIONS     ]~~~~~~~~~~~~~~~~~~~~~~~~~|

def populate_game_filenames(cursor, force=False):
    print("Populating game filenames into database...")
    all_sprites = get_sprites_obtainability_records(cursor)
    substitutions_to_convert_to_id = []
    
    for sprite_id, sprite_info in all_sprites.items():
        print(f"\rGenerating pokemon #{sprite_info["poke num"]} game filenames...", end='', flush=True)
        filename = generate_game_filename(sprite_info)
        does_exist, substitution = check_for_usable_game_file(filename, sprite_info["obtainable"])
        has_sub = 1 if substitution!=None else None     # Temp marking to set in substitution field until I can get subs file id
        has_alt = file_exists(substitution + "-Alt", save_directories["Game Sprites"]["files"]) if has_sub else file_exists(filename + "-Alt", save_directories["Game Sprites"]["files"])

        file_ids = {"filename": filename, "poke_num": sprite_id[0], "form_id": sprite_id[1], "game_id": sprite_id[2], "sprite_id": sprite_id[3], "obtainable": sprite_info["obtainable"], "does_exist": does_exist, "substitution_id": has_sub, "has_alt": has_alt}
        # Inserting into all filenames table
        insert_into_table(cursor, "all_game_filenames", **file_ids)

        filename_id = get_game_filename_id(cursor, filename)
        # Tracking substited files to update substitution file id after all files are inserted into table
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


def change_substitution_field_from_filename_to_file_id(cursor, sub_names_to_convert):
    print("Converting substitution game filenames to ids...")
    for record in sub_names_to_convert:
        edit_substitution_field(cursor, record)


def edit_substitution_field(cursor, record):
    substitution_id = get_game_filename_id(cursor, record["sub_name"])
    # Can safely update both since if a sprite has a substitution, we know it has to be obtainable
    cursor.execute(f"UPDATE all_game_filenames SET substitution_id = {substitution_id} WHERE id = {record["file_id"]}")
    cursor.execute(f"UPDATE obtainable_game_filenames SET substitution_id = {substitution_id} WHERE id = {record["file_id"]}")


def check_for_usable_game_file(filename, obtainable):
    if not obtainable:
        return None, None
    if file_exists(filename, save_directories["Game Sprites"]["files"]):
        return True, None
    else:
        exists, substitution = check_for_game_file_substitution(filename)
        return exists, substitution


def check_for_game_file_substitution(filename):
    for game in GAME_FALLBACKS:
        game_adj = game_adjustment_for_back(filename, game)
        # The latter performs a check if the pokemon was a mid-gen introduction, therefore may have been denoted as a different game on previous scrapes. No need to substitute these sprites with others if they exist
        if game_adj in filename and not get_game_needing_special_translation_for_mid_gen_pokes(filename):
            for repl in GAME_FALLBACKS[game]:
                repl = game_adjustment_for_back(filename, repl)
                replacement_filename = filename.replace(game_adj, repl)
                if file_exists(replacement_filename, save_directories["Game Sprites"]["files"]):
                    return True, replacement_filename
    return False, None


def game_adjustment_for_back(filename, game):
    if "-Back" in filename:
        game = game.replace(" ", "_")
    return game




#|~~~~~~~~~~~~~~~~~~~~~~~[     GAME SPRITE FILENAME FUNCTIONS     ]~~~~~~~~~~~~~~~~~~~~~~~~|

def generate_game_filename(sprite_info):
    poke_num = str(sprite_info["poke num"]).zfill(4)
    form_name = "" if sprite_info["form name"] == "Default" else sprite_info["form name"]
    is_shiny, sprite_type = seperate_sprite_type_if_shiny(sprite_info["sprite type"])
    gen = sprite_info["game gen"]
    game = sprite_info["game name"]

    # Hyphen before game allows for alphabetical sorting of back sprites below the front game sprites
    filename = f"{poke_num} {sprite_info["poke name"]} Gen{gen}{str("_" + game) if "-Back" in sprite_type else str(" " + game)}{"-Shiny" if is_shiny else ""}{form_name}{sprite_type}"
    return filename


def seperate_sprite_type_if_shiny(sprite_type):
    if sprite_type == "Default": return False, ""
    if "-Shiny" not in sprite_type: return False, sprite_type
    else: return True, sprite_type.replace("-Shiny", "")




#|================================================================================================|
#|~~~~~~~~~~~~~~~~~~~~~~~~~[     HOME SPRITES FILENAME TABLE     ]~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~|
#|================================================================================================|

def populate_home_filenames(cursor):
    print("Populating HOME sprite filenames into database...")

    poke_forms = get_poke_form_records(cursor)
    sprite_types = get_sprite_types(cursor)

    for poke_form, poke_info in poke_forms.items():
        for sprite_id, sprite_type in sprite_types.items():
            if "-Back-Animated" in sprite_type: continue    # Animated back sprites are excluded for all HOME pokes, so excluding even them from all_home_filenames'. This formatting also excludes shiny animated back sprites

            poke_num = poke_info["poke num"]
            form_id = poke_form[1]
            form_name = get_form_name(form_id, cursor)

            filename = generate_home_filename(poke_info, sprite_type)
            file_ids = {"filename": filename, "poke_num": poke_num, "form_id": form_id, "sprite_id": sprite_id, "does_exist": None}

            if poke_is_unobtainable_in_home_and_bank(poke_num, form_name, sprite_type):
                insert_into_table_w_unobtainables(cursor, obtainable=False, table="all_home_filenames", **file_ids)
            else:
                file_ids["does_exist"] = file_exists(filename, save_directories["HOME"]["files"])
                insert_into_table(cursor, "obtainable_home_filenames", **file_ids)
                insert_into_table_w_unobtainables(cursor, obtainable=True, table="all_home_filenames", **file_ids)


def generate_home_filename(poke_info, sprite_type):
    poke_num = str(poke_info["poke num"]).zfill(4)
    form_name = "" if poke_info["form name"] == "Default" else poke_info["form name"]
    is_shiny, sprite_type = seperate_sprite_type_if_shiny(sprite_type)

    # Hyphen before game allows for alphabetical sorting of back sprites below the front game sprites
    filename = f"{poke_num} {poke_info["poke name"]} HOME{"-Shiny" if is_shiny else ""}{form_name}{sprite_type}"
    return filename


def poke_is_unobtainable_in_home_and_bank(poke_num, form_name, sprite_type):
    if should_skip_nonexistant_sprite(poke_num, form_name, sprite_type):
        return True
    
    if "-Back" in sprite_type and not is_stamped_poke_form(poke_num, form_name):    # No home back sprites, except for stamped pokemon to show stamp
        return True
    
    # NOTE: If this function is too slow, only the below applies to bank
    for exclusion in UNOBTAINABLE_IN_HOME_AND_BANK.values():
        if exclusion(poke_num, form_name, sprite_type):
            return True
    return False



#|================================================================================================|
#|~~~~~~~~~~~~~~~~~~~~~~~[     HOME MENU IMAGES FILENAME TABLE     ]~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~|
#|================================================================================================|

def populate_home_menu_filenames(cursor):
    print("Populating home menu sprites into database...")

    poke_forms = get_poke_form_records(cursor)
    for poke_form, poke_info in poke_forms.items():
        if should_exclude_menu_poke_form(poke_info): continue
        filename = generate_home_menu_filename(poke_info)
        exists = file_exists(filename, save_directories["HOME Menu"]["files"])
        file_ids = {"filename": filename, "poke_num": poke_form[0], "form_id": poke_form[1], "does_exist": exists}
        insert_into_table(cursor, "home_menu_filenames", **file_ids)


def generate_home_menu_filename(poke_info):
    poke_num = str(poke_info["poke num"]).zfill(4)
    form_name = poke_info["form name"]
    # Removing Region, Form, and Default tags, leaving -values
    for excl in ["Region_", "Form_", "Default"]:
        if excl in form_name: form_name = form_name.replace(excl, "")
    filename = f"{poke_num} {poke_info["poke name"]}{form_name}"
    return filename


def should_exclude_menu_poke_form(poke_info):
    poke_num = poke_info["poke num"]
    form_name = poke_info["form name"]

    # TODO: Can turn each of these into a function
    for exclusion in HOME_MENU_IMG_DOESNT_EXIST.values():
        if exclusion(poke_num, form_name):
            return True
    return False




#|================================================================================================|
#|~~~~~~~~~~~~~~~~~~~~~~~~~~[     POKEMON BANK FILENAME TABLE     ]~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~|
#|================================================================================================|

def populate_bank_filenames(cursor):
    print("Populating BANK sprite filenames into database...")

    # NOTE: While generally probably not the best idea to rely on game filenames instead of building new ones, if its not available in the game, it wont be in BANK either
    # TODO: Probably have to limit query by poke num up to gen7 and exclude things like cosplay pikchu -- better to build off home instead?
    cursor.execute("""
        SELECT filename, poke_num, form_id, sprite_id, obtainable FROM all_game_filenames
        WHERE game_id = ? 
          AND sprite_id IN (?, ?)
    """, (get_game_id("SM_USUM", cursor), get_sprite_type_id("Default", cursor), get_sprite_type_id("-Shiny", cursor)))
    rows = cursor.fetchall()

    for row in rows:
        poke_num = row["poke_num"]
        form_id = row["form_id"]
        form_name = get_form_name(form_id, cursor)
        sprite_id = row["sprite_id"]
        sprite_type = get_sprite_type_name(sprite_id, cursor)
        filename = row["filename"].replace("Gen7 SM_USUM", "BANK")

        
        file_ids = {"filename": filename, "poke_num": poke_num, "form_id": form_id, "sprite_id": sprite_id, "does_exist": None}

        if poke_is_unobtainable_in_home_and_bank(poke_num, form_name, sprite_type):
            insert_into_table_w_unobtainables(cursor, obtainable=False, table="all_bank_filenames", **file_ids)
        else:
            file_ids["does_exist"] = file_exists(filename, save_directories["BANK"]["files"])
            insert_into_table(cursor, "obtainable_go_filenames", **file_ids)
            insert_into_table_w_unobtainables(cursor, obtainable=True, table="all_bank_filenames", **file_ids)




#|================================================================================================|
#|~~~~~~~~~~~~~~~~~~~~~~~~~~[     DRAWN POKES FILENAME TABLE     ]~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~|
#|================================================================================================|

def populate_drawn_filenames(cursor):
    print("Populating drawn filenames into database...")

    poke_forms = get_poke_form_records(cursor)
    for poke_form, poke_info in poke_forms.items():
        filenames = generate_drawn_filenames(poke_info, cursor)    # generate_drawn_filenames actually returns a list, usually len==1, but if its a female it has to generate a male filename too
        for filename in filenames:
            exists = file_exists(filename, save_directories["Drawn"]["files"])
            file_ids = {"filename": filename, "poke_num": poke_form[0], "form_id": poke_form[1], "does_exist": exists}
            insert_into_table(cursor, "drawn_filenames", **file_ids)


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




#|================================================================================================|
#|~~~~~~~~~~~~~~~~~~~~~~~~~~~[     POKEMON GO FILENAME TABLE     ]~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~|
#|================================================================================================|

def populate_go_filenames(cursor):
    print("Populating GO filenames into database...")
    
    poke_forms = get_poke_form_records(cursor)  # (poke num, form id) maps to form/poke info
    sprite_types = get_sprite_types(cursor)
    poke_costumes = get_poke_costume_records(cursor)

    for poke_form, poke_info in poke_forms.items():
        poke_num = poke_info["poke num"]
        form_name = poke_info["form name"]
        print(f"\rGenerating pokemon #{poke_num} GO filenames...", end='', flush=True)

        for costume_id in poke_costumes[poke_num]:
            costume_name = get_costume_name(costume_id)
            if costume_cant_be_equipped(poke_num, form_name, costume_name): continue

            for sprite_id, sprite_type in sprite_types.items():
                if "-Back" in sprite_type or "-Animated" in sprite_type: continue   # GO only has front static sprites

                filename = generate_go_filename(poke_info, sprite_type, costume_name)
                file_ids = {"filename": filename, "poke_num": poke_num, "form_id": poke_form[1], "sprite_id": sprite_id, "costume_id": costume_id, "does_exist": None}

                if unobtainable_in_go(poke_num, form_name, costume_name, sprite_type):
                    insert_into_table_w_unobtainables(cursor, obtainable=False, table="all_go_filenames", **file_ids)
                else:
                    file_ids["does_exist"] = file_exists(filename, save_directories["GO"]["files"])
                    insert_into_table(cursor, "obtainable_go_filenames", **file_ids)
                    insert_into_table_w_unobtainables(cursor, obtainable=True, table="all_go_filenames", **file_ids)

    # Resetting console line after updates from above
    print('\r' + ' '*60 + '\r', end='')


def generate_go_filename(poke_info, sprite_type, costume_name):
    poke_num = poke_info["poke num"]
    poke_num_leading_zeros = str(poke_num).zfill(4)
    poke_name = poke_info["poke name"]
    form_name = "" if poke_info["form name"] == "Default" else poke_info["form name"] 
    costume_name = "" if costume_name == "None" else costume_name
    shiny_tag = "-Shiny" if "-Shiny" in sprite_type else ""

    filename = f"{poke_num_leading_zeros} {poke_name} GO{shiny_tag}{form_name}{costume_name}"
    return filename


def costume_cant_be_equipped(poke_num, form_name, costume_name):
    for exclusion in NO_COSTUMES_EXIST_WITH_THESE_FORMS.values():
        if exclusion(poke_num, form_name, costume_name):
            return True
    return False


def unobtainable_in_go(poke_num, form_name, costume_name, sprite_type):
    for exclusion in UNOBTAINABLE_IN_GO.values():
        if exclusion(poke_num, form_name, costume_name, sprite_type):
            return True
    return False



#|================================================================================================|
#|~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~[     POKEBALL TABLES     ]~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~|
#|================================================================================================|

def populate_pokeballs(cursor):
    for ball in POKEBALLS:
        insert_into_table(cursor, "pokeballs", **ball)


def populate_pokeball_img_types(cursor):
    for img_type in POKEBALL_IMG_TYPES:
        insert_into_table(cursor, "pokeball_img_types", **img_type)




#|================================================================================================|
#|~~~~~~~~~~~~~~~~~~~~~~~~~~~~[     POKEBALLS FILENAME TABLE     ]~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~|
#|================================================================================================|

def populate_pokeball_filenames(cursor):
    print("Populating pokeball filenames into database...")

    pokeballs = get_all_pokeballs(cursor)
    pokeball_img_types = get_all_pokeball_img_types(cursor)

    for ball_id, ball_info in pokeballs.items():
        for img_type_id, img_type_info in pokeball_img_types.items():
            filenames = generate_pokeball_filename(ball_info, img_type_info)
            # Iterating bc generate pokeball filename returns a list, because if gen3 Ultra Ball theres inter-gen differences (ie multiple filenames)
            for filename in filenames:
                file_ids = {"filename": filename, "pokeball_id": ball_id, "img_type_id": img_type_id, "does_exist": None}

                if should_exclude_pokeball_img(ball_info, img_type_info):
                    insert_into_table_w_unobtainables(cursor, obtainable=False, table="all_pokeball_filenames", **file_ids)
                    continue

                file_ids["does_exist"] = file_exists(filename, save_directories["Pokeball"]["files"])
                insert_into_table(cursor, "obtainable_pokeball_filenames", **file_ids)
                insert_into_table_w_unobtainables(cursor, obtainable=True, table="all_pokeball_filenames", **file_ids)


def generate_pokeball_filename(ball_info, img_type_info):
    ball_name = ball_info["name"]
    img_type_name = img_type_info["name"]
    bulba_filename = f"{ball_name}-{img_type_name}"
    # Ultra ball difference between Ruby_Sapphire and FRLG/Emerald
    if ball_name == "Ultra Ball" and img_type_name == "Gen3":
        return [bulba_filename+"_FRLGE", bulba_filename+"_RS"]
    
    return [bulba_filename]


def should_exclude_pokeball_img(ball_info, img_type_info):
    for reason, exclusion in POKEBALL_IMG_EXCLUSIONS.items():
        if exclusion(ball_info, img_type_info): return True
    return False