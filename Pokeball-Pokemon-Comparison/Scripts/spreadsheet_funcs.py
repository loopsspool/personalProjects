import re

from openpyxl import load_workbook

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

# Spreadsheet For Pokedex Info
pokemon_info_sheet_path = 'C:\\Users\\ethan\\OneDrive\\Desktop\\Code\\Pokeball-Pokemon-Comparison\\Pokemon Info.xlsx'
pokemon_info_sheet = load_sheet_from_excel(pokemon_info_sheet_path)

pokemon_files = load_workbook(filename = 'C:\\Users\\ethan\\OneDrive\\Desktop\\Code\\Pokeball-Pokemon-Comparison\\Pokemon File-check.xlsx', data_only=True)
pokemon_files_sheet = pokemon_files.worksheets[0]
poke_info_last_row = get_last_row(pokemon_info_sheet)
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


# TODO: Add pokemon start and to go after start, so this isnt running unecessarily
# def generate_pokedex_from_spreadsheet():
#     print("Getting pokemon info from spreadsheet...")
    
#     # Clears pokedex so every pokemon isn't added again if JSON was populated
#     pokedex.clear()
#     index = 0
#     # Getting poke specific relevant info
#     for i in range(2, poke_info_last_row + 1):
#         num = cell_value(pokemon_info_sheet, i, poke_info_num_col)
#         name = cell_value(pokemon_info_sheet, i, poke_info_name_col)
#         gen = int(cell_value(pokemon_info_sheet, i, poke_info_gen_col))
#         has_f_var = isnt_empty(pokemon_info_sheet, i, poke_info_f_col)
#         has_mega = isnt_empty(pokemon_info_sheet, i, poke_info_mega_col)
#         has_giganta = isnt_empty(pokemon_info_sheet, i, poke_info_giganta_col)
#         reg_forms = cell_value(pokemon_info_sheet, i, poke_info_reg_forms_col)
#         misc_forms = isnt_empty(pokemon_info_sheet, i, poke_info_misc_forms_col)
#         is_in_lgpe = isnt_empty(pokemon_info_sheet, i, poke_info_lgpe_col)
#         is_in_swsh = isnt_empty(pokemon_info_sheet, i, poke_info_swsh_col)
#         is_in_bdsp = isnt_empty(pokemon_info_sheet, i, poke_info_bdsp_col)
#         is_in_la = isnt_empty(pokemon_info_sheet, i, poke_info_la_col)
#         is_in_sv = isnt_empty(pokemon_info_sheet, i, poke_info_sv_col)
        
#         is_in_game = {
#             "LGPE": is_in_lgpe,
#             "SwSh": is_in_swsh,
#             "BDSP": is_in_bdsp,
#             "LA": is_in_la,
#             "SV": is_in_sv
#         }

#         # Adding to pokedex
#         # str(num) to preserve 4 digit numbers w/o leading zeros as strings
#         pokedex.append(Pokemon(str(num), name, gen, has_f_var, has_mega, has_giganta, reg_forms, misc_forms, is_in_game))

#         #check_form_availability(pokedex[index])
#         index += 1

#     save_pokedex()

# def find_last_row_for_poke(num):
#     for row in range(1, pokemon_files_sheet.max_row):
#         if cell_value(pokemon_files_sheet, row, poke_files_num_col)==str(num).zfill(4) and cell_value(pokemon_files_sheet, row+1, poke_files_num_col)!=str(num).zfill(4):
#             # +1 so its inclusive
#             return row+1
#     raise ValueError("Something went wrong in find_last_row_for_poke")

# # TODO: This should be obsolete when missing files get added during filecheck spreadsheet operation
# # TODO: Test pokemon_files_sheet.max_row is inclusive (by doing last poke in the dex)
# # Reading the filecheck spreadsheet with the end goal of adding missing images
# def add_missing_images_to_poke():
#     print("Getting missing images from spreadsheet...")

#     prev_row_poke_num = -1
#     stop = find_last_row_for_poke(poke_num_start_from + poke_to_go_after_start)

#     for row in range(poke_num_start_from + 1, stop):
#         poke_num = int(cell_value(pokemon_files_sheet, row, poke_files_num_col))
#         #TODO: Test
#         poke_obj = pokedex[poke_num-1]
#         # Only print getting missing images message if its a new pokemon
#         if prev_row_poke_num != poke_num:
#             print("Getting", poke_obj.name, "missing images...")
#         # TODO: check this works too
#         # Just setting here after the check to not deal with all the exceptions of the loop not continuing
#         # If used farther down placement will have to be modified
#         prev_row_poke_num = poke_num
        
#         # Tags meaning shiny, animated, back, froms, etc
#         tags = cell_value(pokemon_files_sheet, row, poke_files_tags_col)
#         # If just regular front image
#         if tags == None:
#             tags = ""
#         # This grabs my translated filename for the image from the spreadsheet
#         # Includes all but gen&game, since those cols are to determine what is missing
#         filename = cell_value(pokemon_files_sheet, row, poke_files_filename_col)

        
#         # NOTE: Commented out to prevent circular import before refactoring
#         #if bulba_doesnt_have_this_form(filename):
#         #    continue

#         check_each_game_for_missing(row, poke_obj, filename, tags)

        
# # TODO: Make sure poke_obj pulls correct
# def check_each_game_for_missing(row, poke_obj, filename, tags):
#     # This is to track generations and skip if it's a back sprite below gen 5
#     # To be sifted through to see if they're different by game for the given pokemon
#     is_below_gen5 = False

#     # Only doing filename_col up because those are where the actual checks need to be made (missing for certain games)
#     # And +1 at the end to be inclusive
#     for col in range(poke_files_filename_col + 1, pokemon_files_sheet.max_column + 1):
#         col_name = get_col_name(pokemon_files_sheet, col)

#         # Triggers at Platinum because excel file is reverse chronological, so Plat is first gen 4 game hit
#         # Every loop iteration after is_below_gen5 will be true
#         if col_name == "Platinum":
#             is_below_gen5 = True

#         # If pokemon image is unavailable, continue (don't add to missing images obviously)
#         if cell_value(pokemon_files_sheet, row, col) == "u":
#             continue

#         # If it's a back image from a pokemon between gen1 and gen4
#         # Put all game images into special missing array
#         # This is so another script can go through these images and determine if there were differences in the sprites between games
#         # If there were, each file will be named differently
#         # Otherwise, they will all be lumped into a single gen# back img
#         is_back_below_gen5 = is_below_gen5 and "-Back" in filename
#         # If image is missing or is a gen 1-4 back sprite
#         if is_empty(pokemon_files_sheet, row, col) or is_back_below_gen5:
#             # Where to insert the gen in the filename
#             gen_insert_index = filename.find(poke_obj.name) + len(poke_obj.name)
#             gen_and_game = combine_gen_and_game(col_name, poke_obj.number, tags)
            
#             # Back sprites have to be seperated due to:
#             # Below gen 5 all back sprites are being downloaded to a seperate folder to be sifted through
#             if "-Back" in tags:
#                 determine_missing_back_filename(poke_obj, filename, gen_and_game, gen_insert_index, is_below_gen5)
#             else:
#                 # Going +1 after the insert index because there's a space for non-back sprites
#                 # This is to simulate in the spreadsheet the space between generation and games in the filenames
#                     # This determines sorting order, so is fairly important
#                         # Since the spreadsheet doesn't acknowledge games or gens in the "Filename" column (because each game gets it's own column)
#                             # The space must be included to sort the spreadsheet to match filenames
#                                 # And thus, must be accounted for here
#                 gen_insert_index += 1
#                 filename_w_gen = filename[:gen_insert_index] + gen_and_game + filename[gen_insert_index:]
#                 bulba_name = determine_bulba_name(filename_w_gen, poke_obj)
#                 poke_obj.missing_imgs.append((filename_w_gen, bulba_name))


# def determine_missing_back_filename(poke_obj, filename, gen_and_game, gen_insert_index, is_below_gen5):
#     # Adding space because initially there was no space in spreadsheet
#         # This was for sorting purposes because back sprites start with hyphen immediately after gen
#         # But front sprites follow with a space so they come first in file order
#     # This variable is necessary because bulba uses games to denote which back sprites are from where
#         # In my filenaming convention (gen4 and below excluded due to actual sprite differences between games)
#         # For backs I JUST use gen
#         # But to scrape the image from bulba, I still need the game denoter, which this gets me
#     back_filename_w_game_and_gen_for_bulba = filename[:gen_insert_index] + " " + gen_and_game + filename[gen_insert_index:]
#     bulba_name = determine_bulba_name(back_filename_w_game_and_gen_for_bulba, poke_obj)
#     actual_filename =""
#     # TODO: This could probably be simplified by not initially combining gen and game? Or having a function that pulls gen from game?
#     gen = ""
#     game = ""
#     if "Gen6" in gen_and_game:
#         # This is because all Gen6 are shared with gen7
#             # So denoter is Gen6-7
#         gen = gen_and_game[:6]
#         # Extra character to skip over space after gen
#         game = gen_and_game[7:]
#     else:
#         gen = gen_and_game[:4]
#         # Extra character to skip over space after gen
#         game = gen_and_game[5:]

#     # filename[:3] gets pokemon number
#     actual_filename = filename[:3] + " " + poke_obj.name + " " + gen + filename[gen_insert_index:]
#     if is_below_gen5:
#         actual_filename += "-" + game
#         poke_obj.missing_gen1_thru_gen4_back_imgs.append((actual_filename, bulba_name))
#     else:
#         poke_obj.missing_imgs.append((actual_filename, bulba_name))