import sqlite3

from spreadsheet_funcs import pokemon_info_sheet, get_col_number, cell_value, is_empty, isnt_empty, is_x_or_num

def create_db():
    connection = sqlite3.connect("pokedex.db")
    cursor = connection.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS pokemon (
        num INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL UNIQUE,
        gen INTEGER NOT NULL,
    );
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS forms (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        pokemon_num INTEGER NOT NULL,
        form_name TEXT NOT NULL,
        FOREIGN KEY (pokemon_num) REFRENCES pokemon(num)
    );
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS games (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL UNIQUE,
        gen INTEGER NOT NULL,
    );
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS form_gen_availability (
        form_id INTEGER NOT NULL,
        available_from INTEGER NOT NULL,
        available_until INTEGER DEFAULT NULL,
        FOREIGN KEY (form_id) REFRENCES forms(id)
    );
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS form_game_availability (
        form_id INTEGER NOT NULL,
        game_id INTEGER NOT NULL,
        FOREIGN KEY (form_id) REFRENCES forms(id),
        FOREIGN KEY (game_id) REFRENCES games(id)
    );
    """)

    connection.commit()
    connection.close()