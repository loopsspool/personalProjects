import os
import xlsxwriter

from app_globals import PARENT_DIR
from db_reference_data import GAMES, SPRITE_TYPES, HOME_SPRITE_EXCLUDE, POKEBALLS, POKEBALL_IMG_TYPES
from db_utils import get_poke_name, get_all_game_filenames_info, get_all_home_filenames_info, get_all_1D_non_game_filename_info, get_all_pokeball_filename_info

# TODO: Organize into chunks

# TODO: Make class?
# NOTE: Tablenames matching my database only matter if they're going to be a 1 Dimensional spreadsheet and pull from get_all_1D_non_game_filename_info
    # Thats why Game Sprites, HOME, and Pokeballs have more readable table names, they have custom functions in db_utils to pull dimensional data
checklist_sheets = {
    "Game Sprites": {
        "Table": "Games",
        "Is Pokemon": True,
        "New Poke Divider": True,
        "Mult Col List": [game[0] for game in GAMES],
        "Missing Img Getter Callback": get_all_game_filenames_info
    },
    "HOME": {
        "Table": "HOME",
        "Is Pokemon": True,
        "New Poke Divider": False,
        "Mult Col List": [sprite_type for sprite_type in reversed(list(SPRITE_TYPES)) if sprite_type not in HOME_SPRITE_EXCLUDE],  # Reversing bc I like the normal order it's in, so when it gets reversed again in generate headers it will be ordered proper
        "Missing Img Getter Callback": get_all_home_filenames_info
    },
    # "Drawn": {
    #     "Table": "drawn_filenames",
    #     "Is Pokemon": True,
    #     "New Poke Divider": False,
    #     "Mult Col List": None,
    #     "Missing Img Getter Callback": get_all_1D_non_game_filename_info
    # },
    "Home Menu": {
        "Table": "home_menu_filenames",
        "Is Pokemon": True,
        "New Poke Divider": False,
        "Mult Col List": None,
        "Missing Img Getter Callback": get_all_1D_non_game_filename_info
    },
    "Bank": {
        "Table": "bank_filenames",
        "Is Pokemon": True,
        "New Poke Divider": False,
        "Mult Col List": None,
        "Missing Img Getter Callback": get_all_1D_non_game_filename_info    # TODO: Determine if you want Reg col & Shiny Col
    },
    "GO": {
        "Table": "go_filenames",
        "Is Pokemon": True,
        "New Poke Divider": False,
        "Mult Col List": None,
        "Missing Img Getter Callback": get_all_1D_non_game_filename_info    # TODO: Determine if you want Reg col & Shiny Col
    },
    "Pokeballs": {
        "Table": "Pokeballs",
        "Is Pokemon": False,
        "New Poke Divider": False,
        "Mult Col List": None,  # NOTE: This gets defined properly right before workbook writing with recreate_pokeball_list_w_gen5_stills_combined_into_one
        "Missing Img Getter Callback": get_all_pokeball_filename_info
    }
}

#|================================================================================================|
#|~~~~~~~~~~~~~~~~~~~~~~~~~~~[     IMAGE CHECKLIST SPREADSHEET     ]~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~|
#|================================================================================================|

def create_file_checklist_spreadsheet():
    # This will always create a new file that overrides an existing one
    image_checklist_filepath = os.path.join(PARENT_DIR, 'Pokemon Images Checklist.xlsx')
    workbook = xlsxwriter.Workbook(image_checklist_filepath)

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

    checklist_sheets["Pokeballs"]["Mult Col List"] = recreate_pokeball_list_w_gen5_stills_combined_into_one()
    for sheet_name, sheet_properties in checklist_sheets.items():
        sheet = sheet_properties["Sheet Object"] = workbook.add_worksheet(sheet_name)

        is_pokemon_sheet = sheet_properties["Is Pokemon"]
        freeze_cols_to = 3 if is_pokemon_sheet else 1
        sheet.freeze_panes(1, freeze_cols_to)

        write_file_availability(sheet, formats, sheet_properties, is_pokemon_sheet)

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
        col_num = 3 if is_pokemon else 1
        col_map = {}
        mult_col_names = [col_name for col_name in reversed(mult_col_names)]  # Putting names in reverse chronological order so spreadsheet fills with most recent data first
        for col_name in mult_col_names:
            worksheet.write(0, col_num, col_name)
            col_map[col_name] = col_num
            worksheet.set_column(col_num, col_num, len(str(col_name)) + 2)    # Setting column width, 2 is for padding
            col_num += 1
        return col_map
    else:   # 1 Dimensional sheets
        worksheet.write(0, 3, "Available")
        return None
    

def write_file_availability(worksheet, formats, sheet_properties, is_pokemon_sheet):
    if is_pokemon_sheet:
        write_pokemon_availability(worksheet, formats, sheet_properties)
    else:
        write_pokeball_availability(worksheet, formats, sheet_properties)


# TODO: I think you can combine pokemon & pokeball availability functions into one and base differenced on Is Pokemon Sheet
def write_pokeball_availability(worksheet, formats, sheet_properties):
    col_map = generate_header_row(worksheet, formats, is_pokemon=False, mult_col_names=sheet_properties["Mult Col List"])  # Returns col name: col num for multi column sheets, else None
    pokeball_info = sheet_properties["Missing Img Getter Callback"]()    # Gets existence status
    longest_pokeball_name = len(max(POKEBALLS, key=lambda ball: len(ball["name"]))["name"])

    # Starting at 1 to account for header row
    for row, (pokeball, img_type) in enumerate(pokeball_info.items(), start=1):
        worksheet.write(row, 0, pokeball)

        for img_type_name, file_status in img_type.items():
            col_num = col_map[img_type_name]
            write_image_status_where_can_be_unobtainable(worksheet, formats, row, col_num, file_status, is_new_poke=False, has_new_poke_divider=False)

    worksheet.set_column(0, 0, longest_pokeball_name + 2)   # +2 for padding


def write_pokemon_availability(worksheet, formats, sheet_properties):
    table = sheet_properties["Table"]
    has_new_poke_divider = sheet_properties["New Poke Divider"]
    get_missing_imgs_callback = sheet_properties["Missing Img Getter Callback"]

    col_map = generate_header_row(worksheet, formats, is_pokemon=True, mult_col_names=sheet_properties["Mult Col List"])  # Returns col name: col num for multi column sheets, else None
    all_file_info = get_missing_imgs_callback() if get_missing_imgs_callback is not get_all_1D_non_game_filename_info else get_missing_imgs_callback(table)    # Gets existence status, 1D sheets require table name

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
        is_new_poke, sprite_info_format = determine_if_new_poke(prev_poke_num, poke_num,has_new_poke_divider , formats)
            
        # Writing file info
        worksheet.write(row, 0, poke_num, sprite_info_format)
        worksheet.write(row, 1, poke_name, sprite_info_format)
        worksheet.write(row, 2, tags, sprite_info_format)
        # Writing if file actually exists
        write_file_existence(worksheet, formats, row, col_map, file_info, is_new_poke, has_new_poke_divider)
        
        prev_poke_num = poke_num

    # Setting column width
    padding = 2
    worksheet.set_column(0, 0, longest_values["num"] + padding)
    worksheet.set_column(1, 1, longest_values["name"] + padding)
    worksheet.set_column(2, 2, longest_values["tags"] + padding)

    # Resetting console line
    print('\r' + ' '*45 + '\r', end='')


def write_file_existence(worksheet, formats, row, col_map, file_info, is_new_poke, has_new_poke_divider):
    if col_map: # If has multiple columns
        for col_name, file_status in file_info.items():
            col_num = col_map[col_name]
            write_image_status_where_can_be_unobtainable(worksheet, formats, row, col_num, file_status, is_new_poke, has_new_poke_divider)
    else:   # 1 Dimensional
        file_exists = file_info["exists"]
        format = determine_format_by_boolean_existence(file_exists, is_new_poke, has_new_poke_divider) 
        worksheet.write(row, 3, "X" if file_exists else "M", formats[format])


def determine_if_new_poke(prev_poke_num, poke_num, has_new_poke_divider, formats):
    if prev_poke_num != poke_num:
        is_new_poke = True
        print(f"\rWriting pokemon #{poke_num} file availability...", end='', flush=True)
        sprite_info_format = formats["new info"] if has_new_poke_divider else None
    else:
        is_new_poke = False
        sprite_info_format = None

    return is_new_poke, sprite_info_format


def recreate_pokeball_list_w_gen5_stills_combined_into_one():
    pokeball_cols = [pokeball["name"] for pokeball in POKEBALL_IMG_TYPES]
    # Combining statics 0-8 into one column, logic for if they all exist or not is in get_all_pokeball_filename_info in db_utils
    gen5_static_0_index = pokeball_cols.index("Gen5_Battle-Static_0")
    pokeball_cols[gen5_static_0_index] = "Gen5_Battle-Statics"
    pokeball_cols = [ball for ball in pokeball_cols if not ball.startswith("Gen5_Battle-Static_")]  # Excludes my combined element because of the underscore
    return pokeball_cols


def determine_if_longest_length_value_yet(longest_values_dict, name, tags):
    name_len = len(str(name))
    tags_len = len(str(tags))
    if name_len > longest_values_dict["name"]: longest_values_dict["name"] = name_len
    if tags_len > longest_values_dict["tags"]: longest_values_dict["tags"] = tags_len
    return longest_values_dict
        

def write_image_status_where_can_be_unobtainable(worksheet, formats, row, col_num, file_status, is_new_poke, has_new_poke_divider):
    has_sub = None if "has_sub" not in file_status else file_status["has_sub"]
    text = denote_file_status(file_status["obtainable"], file_status["exists"], has_sub)
    format = determine_format_w_unobtainable(text, is_new_poke, has_new_poke_divider)

    worksheet.write(row, col_num, text, formats[format])


def determine_format_w_unobtainable(text, is_new_poke, has_new_poke_divider):
    format = "new " if has_new_poke_divider and is_new_poke else ""
    if text == "U": format += "grey"
    elif text in ("S", "X"): format += "green"
    elif text == "M": format += "red"
    return format


# is_new_poke = False allows omission of it to not draw the top border for a new item
def determine_format_by_boolean_existence(is_avail, is_new_poke, has_new_poke_divider):
    format = "new " if has_new_poke_divider and is_new_poke else ""
    if is_avail: format += "green"
    if not is_avail: format += "red"
    return format


def denote_file_status(obtainable, exists, sub=None):
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