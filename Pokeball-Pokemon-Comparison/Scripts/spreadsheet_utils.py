import xlsxwriter
import os
from openpyxl import load_workbook

from app_globals import PARENT_DIR
from db_utils import GAMES, SPRITE_TYPES, HOME_SPRITE_EXCLUDE, POKEBALL_IMG_TYPES




#|================================================================================================|
#|~~~~~~~~~~~~~~~~~~~~~~~~~~[     GENERAL SPREADSHEET FUNCTIONS     ]~~~~~~~~~~~~~~~~~~~~~~~~~~~~~|
#|================================================================================================|

def normalize_empty_in_sheet(sheet):
    for row in sheet.iter_rows():
        for cell in row:
            if cell.value is None or (isinstance(cell.value, str) and cell.value.strip() == ""):
                cell.value = None


def load_sheet_from_excel(wb_path, sheet_index=0):
    workbook = load_workbook(filename = wb_path, data_only=True)
    sheet = workbook.worksheets[sheet_index]
    normalize_empty_in_sheet(sheet)
    workbook.close()
    return sheet


def cell_value(sheet, row, col):
    return (sheet.cell(row, col).value)


def isnt_empty(sheet, row, col):
    return (cell_value(sheet, row, col) != None)


def is_empty(sheet, row, col):
    return (cell_value(sheet, row, col) == None)


# Returns column number from column name
def get_col_number(sheet, col_name):
    for col in range(1, sheet.max_column):
        if (cell_value(sheet, 1, col) == col_name):
            return col


# Returns column name from column number
def get_col_name(sheet, col_number):
    return(cell_value(sheet, 1, col_number))


def get_last_row(sheet):
    for row in reversed(range(1, sheet.max_row + 1)):
        if any(sheet.cell(row, col).value is not None for col in range(1, sheet.max_column + 1)):
            return row
        

def sheet_pretty_print(sheet):
    for row in sheet.iter_rows(values_only=True):
        print("\t".join(str(cell) if cell is not None else "None" for cell in row))




#|================================================================================================|
#|~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~[     POKEMON FUNCTIONS     ]~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~|
#|================================================================================================|

def is_poke_in_game(poke_num, game):
    if isinstance(poke_num, int): poke_num = str(poke_num).zfill(4)
    game_availability_col = get_col_number(POKEMON_INFO_SHEET, game)
    for row in range(2, POKE_INFO_LAST_ROW+1):
        if str(cell_value(POKEMON_INFO_SHEET, row, POKE_INFO_NUM_COL)) == poke_num:
            return isnt_empty(POKEMON_INFO_SHEET, row, game_availability_col)
        

def poke_isnt_in_game(poke_num, game):
    return not is_poke_in_game(poke_num, game)




#|================================================================================================|
#|~~~~~~~~~~~~~~~~~~~~~~~~~~~[     IMAGE CHECKLIST SPREADSHEET     ]~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~|
#|================================================================================================|

def create_file_checklist_spreadsheet():
    # This will always create a new file that overrides an existing one
    image_checklist_filepath = os.path.join(PARENT_DIR, 'Pokemon Images Checklist.xlsx')
    workbook = xlsxwriter.Workbook(image_checklist_filepath)
    game_sprite_availability_sheet = workbook.add_worksheet('Game Sprites')
    home_sprite_availability_sheet = workbook.add_worksheet('Home Sprites')
    drawn_availability_sheet = workbook.add_worksheet('Drawn')
    home_menu_sprite_availability_sheet = workbook.add_worksheet('Home Menu Imgs')
    pokeball_availability_sheet = workbook.add_worksheet('Pokeballs')

    game_sprite_availability_sheet.freeze_panes(1, 3)
    home_sprite_availability_sheet.freeze_panes(1, 3)
    drawn_availability_sheet.freeze_panes(1, 3)
    home_menu_sprite_availability_sheet.freeze_panes(1, 3)
    pokeball_availability_sheet.freeze_panes(1, 1)

    green = '#40D073'
    red = '#C75451'
    grey = '#404040'
    new_poke_top_border_color = '#D9D9D9'
    formats = {
        "header": workbook.add_format({'bold': True, 'align': 'center', 'bg_color': 'gray', 'bottom': 5, 'top': 1, 'left': 1, 'right': 1}),
        # New items have strong top border
        "new info": workbook.add_format({'top_color': new_poke_top_border_color, 'top': 5}),
        "new green": workbook.add_format({'top_color': new_poke_top_border_color, 'top': 5, 'left': 1, 'right': 1, 'bottom': 1, 'align': 'center', 'bg_color': green, 'font_color': green}),
        "new red": workbook.add_format({'top_color': new_poke_top_border_color, 'top': 5, 'left': 1, 'right': 1, 'bottom': 1, 'align': 'center', 'bg_color': red, 'font_color': red}),
        "new grey": workbook.add_format({'top_color': new_poke_top_border_color, 'top': 5, 'left': 1, 'right': 1, 'bottom': 1, 'align': 'center', 'bg_color': grey, 'font_color': grey}),
        "green": workbook.add_format({'border': 1, 'align': 'center', 'bg_color': green, 'font_color': green}),
        "red": workbook.add_format({'border': 1, 'align': 'center', 'bg_color': red, 'font_color': red}),
        "grey": workbook.add_format({'border': 1, 'align': 'center', 'bg_color': grey, 'font_color': grey})
    }

    # NOTE: Tablenames matching my database only matter if they're going to be a 1 Dimensional spreadsheet and pull from get_all_1D_non_game_filename_info
    # Thats why Game Sprites, HOME, and Pokeballs have more readable table names, they have custom functions in db_utils to pull dimensional data
    # Game sprite availability
    write_pokemon_availability(game_sprite_availability_sheet, formats, table="Games")
    # Home sprite availability
    write_pokemon_availability(home_sprite_availability_sheet, formats, table="HOME")
    # Drawn availability
    write_pokemon_availability(drawn_availability_sheet, formats, table="drawn_filenames")
    # Home Menu Imgs availability
    write_pokemon_availability(home_menu_sprite_availability_sheet, formats, table="home_menu_filenames")
    # Pokeball availability
    # TODO: Combine static frames from pokeball gen 5 battle into one col? True if all 9 there, false otherwise
    write_pokeball_availability(pokeball_availability_sheet, formats, table="Pokeballs")

    print("Spreadsheet finished!")
    print("Finalizing spreadsheet close...")
    workbook.close()


def generate_header_row(worksheet, formats, is_pokemon=True, mult_col_names=None):
    worksheet.set_row(0, None, formats["header"])
    if is_pokemon:
        worksheet.write(0, 0, "#")
        worksheet.write(0, 1, "Name")
        worksheet.write(0, 2, "Tags")
    else: # Pokeballs
        worksheet.write(0, 0, "Name")

    if mult_col_names:
        col_num = 3
        col_map = {}
        mult_col_names = [col_name for col_name in reversed(mult_col_names)]  # Putting names in reverse chronological order so spreadsheet fills with most recent data first
        for col_name in mult_col_names:
            worksheet.write(0, col_num, col_name)
            col_map[col_name] = col_num
            worksheet.set_column(col_num, col_num, len(str(col_name)) + 1)    # Setting column width, 1 is for padding
            col_num += 1
        return col_map
    else:   # 1 Dimensional sheets
        worksheet.write(0, 3, "Available")
        return None


def write_pokeball_availability(worksheet, formats):
    from db_utils import get_pokeball_filename_info
    from db_reference_data import POKEBALLS

    col_map = determine_header_cols(worksheet, "Pokeballs", formats)
    pokeball_info = get_pokeball_filename_info()
    longest_pokeball_name = max(POKEBALLS, key=lambda ball: len(ball["name"]))["name"]

    # Starting at 1 to account for header row
    for row, pokeball in enumerate(pokeball_info, start=1):
        worksheet.write(row, 0, pokeball)

        for img_type, exists in pokeball.items():
            exists_format = determine_format_by_boolean_existence(exists)
            worksheet.write(row, col_map[img_type], "X" if exists else "M", formats[exists_format])

    worksheet.set_column(0, 0, longest_pokeball_name + 2)   # +2 for padding


def write_pokemon_availability(worksheet, formats, table):
    from db_utils import get_poke_name

    col_map = determine_header_cols(worksheet, table, formats)  # Returns col name: col num for multi column sheets, else None
    all_file_info = get_file_info(table)    # Gets existence status

    longest_values = {"num": 4, "name": 0, "tags": 0}   # For setting col width later
    prev_poke_num = 0

    # Starting at 1 because row 0 is the header row
    for row, (poke_info, file_info) in enumerate(all_file_info.items(), start=1):
        poke_num = poke_info[0]
        poke_name = get_poke_name(poke_num)
        tags = get_poke_tags(poke_name, file_info, table)

        # Finding longest text to set column width to
        longest_values = determine_if_longest_length_value_yet(longest_values, poke_name, tags)

        # Putting a top border on if its a new poke for tables where I want that (currently just game sprites)
        is_new_poke, sprite_info_format = determine_if_new_poke(prev_poke_num, poke_num, table, formats)
            
        worksheet.write(row, 0, poke_num, sprite_info_format)
        worksheet.write(row, 1, poke_name, sprite_info_format)
        worksheet.write(row, 2, tags, sprite_info_format)
        write_file_existence(worksheet, formats, table, row, col_map, file_info, is_new_poke)
        
        prev_poke_num = poke_num

    # Setting column width
    padding = 2
    worksheet.set_column(0, 0, longest_values["num"] + padding)
    worksheet.set_column(1, 1, longest_values["name"] + padding)
    worksheet.set_column(2, 2, longest_values["tags"] + padding)

    # Resetting console line
    print('\r' + ' '*45 + '\r', end='')


def write_file_existence(worksheet, formats, table, row, col_map, file_info, is_new_poke):
    if col_map: # If has multiple columns
        for col_name, file_status in file_info.items():
            print(col_name, file_status)
            col_num = col_map[col_name]
            # Game sprites are their own beast because they can be substituted
            if table == "Games": write_game_sprite_image_status_for_games(worksheet, formats, is_new_poke, row, col_num, file_status)
            # Everything else is binary, it either exists or it doesn't
            else: 
                file_exists = file_status["exists"]
                print(file_exists)
                format = determine_format_by_boolean_existence(file_exists) 
                worksheet.write(row, col_num, "X" if file_exists else "M", formats[format])
                print(file_exists)
    else:   # 1 Dimensional
        file_exists = file_status["exists"]
        format = determine_format_by_boolean_existence(file_exists) 
        worksheet.write(row, 3, "X" if file_exists else "M", formats[format])


def determine_if_new_poke(prev_poke_num, poke_num, table, formats):
    if prev_poke_num != poke_num:
        is_new_poke = True
        print(f"\rWriting pokemon #{poke_num} file availability...", end='', flush=True)
        sprite_info_format = formats["new info"] if table == "Games" else None
    else:
        is_new_poke = False
        sprite_info_format = None

    return is_new_poke, sprite_info_format


def determine_header_cols(worksheet, table, formats):
    if table == "Games": return generate_header_row(worksheet, formats, mult_col_names=[game[0] for game in GAMES])
    elif table == "HOME": return generate_header_row(worksheet, formats, mult_col_names=[sprite_type for sprite_type in SPRITE_TYPES if sprite_type not in HOME_SPRITE_EXCLUDE])
    elif table == "drawn_filesnames": return generate_header_row(worksheet, formats)
    elif table == "home_menu_filenames": return generate_header_row(worksheet, formats)
    elif table == "Pokeballs": return generate_header_row(worksheet, formats, is_pokemon=False, mult_col_names=POKEBALL_IMG_TYPES)
    else: raise ValueError(f"Table name ({table}) not recognized")


def get_file_info(table):
    from db_utils import get_all_game_filenames_info, get_all_home_filenames_info, get_all_1D_non_game_filename_info, get_all_pokeball_filename_info

    if table == "Games": return get_all_game_filenames_info()
    elif table == "HOME": return get_all_home_filenames_info()
    elif table == "drawn_filesnames": return get_all_1D_non_game_filename_info(table)
    elif table == "home_menu_filenames": return get_all_1D_non_game_filename_info(table)
    elif table == "Pokeballs": return get_all_pokeball_filename_info()


def determine_if_longest_length_value_yet(longest_values_dict, name, tags):
    name_len = len(str(name))
    tags_len = len(str(tags))
    if name_len > longest_values_dict["name"]: longest_values_dict["name"] = name_len
    if tags_len > longest_values_dict["tags"]: longest_values_dict["tags"] = tags_len
    return longest_values_dict
        

def write_game_sprite_image_status_for_games(worksheet, formats, is_new_poke, row, col_num, file_status):
    text = denote_file_status(file_status["obtainable"], file_status["exists"], file_status["has_sub"])
    format = determine_game_sprite_format(text, is_new_poke)

    worksheet.write(row, col_num, text, formats[format])


def determine_game_sprite_format(text, is_new_poke):
    format = "new " if is_new_poke else ""
    if text == "U": format += "grey"
    elif text in ("S", "X"): format += "green"
    elif text == "M": format += "red"
    return format


# is_new_poke = False allows omission of it to not draw the top border for a new item
def determine_format_by_boolean_existence(is_avail, is_new_poke=False):
    format = "new " if is_new_poke else ""
    if is_avail: format += "green"
    if not is_avail: format += "red"
    return format


def denote_file_status(obtainable, exists, sub):
    text = ""
    if not obtainable:
        text = "U"
    else:
        if exists:
            # If image is substituted, denote that
            if sub:
                # TODO: Put substitution file ID in text
                text = "S"
            else:
                text = "X"
        else:
            text = "M"
    return text


# NOTE: Tags *could* be pulled via form/sprite type but I do reorder them differently (eg changing -Shiny tag placement in filename)
def get_poke_tags(poke_name, file_info, table):
    # TODO: Error here....
    if table == "HOME": filename = file_info["Default"]["filename"]     # Getting default filename will leave me with tags only (no "-Shiny", "-Animated", etc)
    elif table == "Games": filename = file_info["SV"]["filename"]   # Any game would work here for tags, just pulling it out of the next loop so it isn't rewritten for each game
    else: filename = file_info["filename"]  # 1 Dimensional tables
    
    # Getting tags from filename split based off first hyphen
    max_split = 1
    max_split += poke_name.count("-")   # Increasing hyphen split limit if pokemon has hyphen in their name
    split_filename = filename.split("-", max_split)

    # If tags in filename, return those
    if len(split_filename) > max_split:
        tags = "-" + split_filename[len(split_filename)-1]
    else:   # If theres no tags in the filename (Default), return an empty string
        tags = ""
    return tags





#|================================================================================================|
#|~~~~~~~~~~~~~~~~~~~~~~~~~~[     GLOBAL  POKE INFO CONSTANTS     ]~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~|
#|================================================================================================|

# Spreadsheet for Pokedex Info (pokemon, f/region/mega/giganta variants, megas, species forms, game exclusivity, etc)
POKEMON_INFO_SHEET_PATH = os.path.join(PARENT_DIR, 'Pokemon Info.xlsx')
POKEMON_INFO_SHEET = load_sheet_from_excel(POKEMON_INFO_SHEET_PATH)

POKE_INFO_LAST_ROW = get_last_row(POKEMON_INFO_SHEET)
POKE_INFO_NAME_COL = get_col_number(POKEMON_INFO_SHEET, "Name")
POKE_INFO_NUM_COL = get_col_number(POKEMON_INFO_SHEET, "#")
POKE_INFO_GEN_COL = get_col_number(POKEMON_INFO_SHEET, "Gen")
POKE_INFO_F_COL = get_col_number(POKEMON_INFO_SHEET, "Female Variation")
POKE_INFO_MEGA_COL = get_col_number(POKEMON_INFO_SHEET, "Mega")
POKE_INFO_GIGANTA_COL = get_col_number(POKEMON_INFO_SHEET, "Gigantamax")
POKE_INFO_REG_FORMS_COL = get_col_number(POKEMON_INFO_SHEET, "Regional Forms")
POKE_INFO_MISC_FORMS_COL = get_col_number(POKEMON_INFO_SHEET, "Misc Forms")