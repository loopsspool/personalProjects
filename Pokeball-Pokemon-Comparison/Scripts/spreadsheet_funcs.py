import re
import xlsxwriter

from openpyxl import load_workbook

# TODO: Add menu sprites and drawn images sheet to file checklist
# TODO: Run file checklist at end of each scrape? update when image found?
# TODO: Make sure run new file checklist if new pokes added to poke_info sheet


# NOTE: Commented out to prevent circular import before refactoring
#from bulba_translators import bulba_doesnt_have_this_form, determine_bulba_name
from game_tools import combine_gen_and_game


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


def is_poke_in_game(poke_num, game):
    if isinstance(poke_num, int): poke_num = str(poke_num).zfill(4)
    game_availability_col = get_col_number(pokemon_info_sheet, game)
    for row in range(2, POKE_INFO_LAST_ROW+1):
        if str(cell_value(pokemon_info_sheet, row, poke_info_num_col)) == poke_num:
            return isnt_empty(pokemon_info_sheet, row, game_availability_col)
        

def poke_isnt_in_game(poke_num, game):
    return not is_poke_in_game(poke_num, game)


def create_file_checklist_spreadsheet():
    # This will always create a new file that overrides an existing one
    workbook = xlsxwriter.Workbook('C:\\Users\\ethan\\OneDrive\\Desktop\\Code\\Pokeball-Pokemon-Comparison\\Pokemon Images Checklist.xlsx')
    worksheet = workbook.add_worksheet()
    worksheet.freeze_panes(1, 3)

    green = '#40D073'
    red = '#C75451'
    grey = '#404040'
    new_poke_top_border_color = '#D9D9D9'
    formats = {
        # New pokes have strong top border
        "new poke info": workbook.add_format({'top_color': new_poke_top_border_color, 'top': 5}),
        "new poke green": workbook.add_format({'top_color': new_poke_top_border_color, 'top': 5, 'left': 1, 'right': 1, 'bottom': 1, 'align': 'center', 'bg_color': green, 'font_color': green}),
        "new poke red": workbook.add_format({'top_color': new_poke_top_border_color, 'top': 5, 'left': 1, 'right': 1, 'bottom': 1, 'align': 'center', 'bg_color': red, 'font_color': red}),
        "new poke grey": workbook.add_format({'top_color': new_poke_top_border_color, 'top': 5, 'left': 1, 'right': 1, 'bottom': 1, 'align': 'center', 'bg_color': grey, 'font_color': grey}),
        "green": workbook.add_format({'border': 1, 'align': 'center', 'bg_color': green, 'font_color': green}),
        "red": workbook.add_format({'border': 1, 'align': 'center', 'bg_color': red, 'font_color': red}),
        "grey": workbook.add_format({'border': 1, 'align': 'center', 'bg_color': grey, 'font_color': grey})
    }

    game_cols = generate_header_row(workbook, worksheet)
    write_availability(workbook, worksheet, formats, game_cols)

    print("Done!")
    print("Finalizing close...")
    workbook.close()


def generate_header_row(workbook, worksheet):
    print("Generating header row...")
    from db_utils import GAMES
    
    h_format = workbook.add_format({'bold': True, 'align': 'center', 'bg_color': 'gray', 'bottom': 5, 'top': 1, 'left': 1, 'right': 1})
    worksheet.set_row(0, None, h_format)
    worksheet.write(0, 0, "#")
    worksheet.write(0, 1, "Name")
    worksheet.write(0, 2, "Tags")
    col_num = 3
    game_cols = {}
    for game in reversed(GAMES):
        worksheet.write(0, col_num, game[0])
        game_cols[game[0]] = col_num
        col_num += 1

    return game_cols


def write_availability(workbook, worksheet, formats, game_cols):
    from db_utils import get_all_filenames_info, get_poke_name, get_game_name
    
    all_file_info = get_all_filenames_info()

    print("Writing availability of files...")
    prev_poke_num = 0
    is_new_poke = True
    # Starting at 1 because row 0 is the header row
    for i, (poke_sprite_form_id, games) in enumerate(all_file_info.items(), start=1):
        poke_num = poke_sprite_form_id[0]
        poke_name = get_poke_name(poke_num)
        # Any game would work here for tags, just pulling it out of the next loop so it isn't rewritten for each game
        tags = get_poke_tags(poke_name, games["SV"]["filename"])
        # Putting a top border on if its a new poke
        if prev_poke_num != poke_num:
            is_new_poke = True
            print(f"\rWriting pokemon #{poke_num} file availability...", end='', flush=True)
            sprite_info_format = formats["new poke info"]
        else:
            is_new_poke = False
            sprite_info_format = None
        worksheet.write(i, 0, poke_num, sprite_info_format)
        worksheet.write(i, 1, poke_name, sprite_info_format)
        worksheet.write(i, 2, tags, sprite_info_format)
        for game_name, sprite_data in games.items():
            write_sprite_status_for_game(workbook, worksheet, formats, is_new_poke, i, game_cols, game_name, sprite_data["obtainable"], sprite_data["exists"], sprite_data["has_sub"])
        
        prev_poke_num = poke_num
    # Resetting console line after updates from above
    print('\r' + ' '*45 + '\r', end='')
        

def write_sprite_status_for_game(workbook, worksheet, formats, is_new_poke, row, game_cols, game, obtainable, exists, sub):
    game_col = game_cols[game]
    text = denote_file_status(obtainable, exists, sub)
    format = determine_format(text, is_new_poke)

    worksheet.write(row, game_col, text, formats[format])


def determine_format(text, is_new_poke):
    format = "new poke " if is_new_poke else ""
    if text == "U": format += "grey"
    elif text in ("S", "X"): format += "green"
    elif text == "M": format += "red"
    return format


def denote_file_status(obtainable, exists, sub):
    text = ""
    if not obtainable:
        text = "U"
    else:
        if exists:
            # If image is substituted, denote that
            if sub:
                text = "S"
            else:
                text = "X"
        else:
            text = "M"
    return text


def get_poke_tags(poke_name, filename):
    max_split = 1
    if "-" in poke_name:
        max_split = 2
    split_filename = filename.split("-", max_split)
    # If theres no tags in the filename, return an empty string
    if len(split_filename) > 1:
        tags = "-" + split_filename[len(split_filename)-1]
        # Getting rid of file extenstion
        tags = tags[:-4]
    else:
        tags = ""
    return tags

create_file_checklist_spreadsheet()
# TODO: Capitalize constants
# TODO: Verify poke_info_last_row used instead of pokemon_files_sheet.max_row
# Spreadsheet For Pokedex Info
pokemon_info_sheet_path = 'C:\\Users\\ethan\\OneDrive\\Desktop\\Code\\Pokeball-Pokemon-Comparison\\Pokemon Info.xlsx'
pokemon_info_sheet = load_sheet_from_excel(pokemon_info_sheet_path)

pokemon_files = load_workbook(filename = 'C:\\Users\\ethan\\OneDrive\\Desktop\\Code\\Pokeball-Pokemon-Comparison\\Pokemon Images Checklist.xlsx', data_only=True)
pokemon_files_sheet = pokemon_files.worksheets[0]
POKE_INFO_LAST_ROW = get_last_row(pokemon_info_sheet)
poke_info_name_col = get_col_number(pokemon_info_sheet, "Name")
poke_info_num_col = get_col_number(pokemon_info_sheet, "#")
poke_info_gen_col = get_col_number(pokemon_info_sheet, "Gen")
poke_info_f_col = get_col_number(pokemon_info_sheet, "Female Variation")
poke_info_mega_col = get_col_number(pokemon_info_sheet, "Mega")
poke_info_giganta_col = get_col_number(pokemon_info_sheet, "Gigantamax")
poke_info_reg_forms_col = get_col_number(pokemon_info_sheet, "Regional Forms")
poke_info_misc_forms_col = get_col_number(pokemon_info_sheet, "Misc Forms")
poke_info_lgpe_col = get_col_number(pokemon_info_sheet, "LGPE")
poke_info_swsh_col = get_col_number(pokemon_info_sheet, "SwSh")
poke_info_bdsp_col = get_col_number(pokemon_info_sheet, "BDSP")
poke_info_la_col = get_col_number(pokemon_info_sheet, "LA")
poke_info_sv_col = get_col_number(pokemon_info_sheet, "SV")
# TODO: Add drawn and menu sprites
poke_files_num_col = get_col_number(pokemon_files_sheet, "#")
poke_files_name_col = get_col_number(pokemon_files_sheet, "Name")
poke_files_tags_col = get_col_number(pokemon_files_sheet, "Tags")
poke_files_filename_col = get_col_number(pokemon_files_sheet, "Filename")
