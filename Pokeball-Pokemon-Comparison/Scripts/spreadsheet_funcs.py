from scrape_bulba_translators import bulba_doesnt_have_this_form, determine_bulba_name
from scrape_game_tools import combine_gen_and_game

from globals import *

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

# Performs check to make sure JSON pokedex is up to date
# TODO: Test
# TODO: Add JSON stuff
def check_pokedex_is_up_to_date():
    print("Checking pokedex is up to date...")
    highest_pokedex_number_in_info_file = -1
    row_acc = 2
    # While pokemon number col isn't empty, traverse down to find highest pokemon num
    while (isnt_empty(pokemon_info_sheet, row_acc, poke_info_num_col)):
        row_acc += 1
    highest_pokedex_number_in_info_file = cell_value(pokemon_info_sheet, row_acc-1, poke_info_num_col)  
    # TODO: Check this against last element from JSON
    # If they dont match run generate pokedex from spreadsheet from last highest  

# TODO: Add pokemon start and to go after start, so this isnt running unecessarily
# TODO: This requires adding JSON, which I dont want to do until after I've got things running
def generate_pokedex_from_spreadsheet():
    print("Getting pokemon info from spreadsheet...")
    
    # Getting poke specific relevant info
    for i in range(2, 900):
        name = cell_value(pokemon_info_sheet, i, poke_info_name_col)
        num = cell_value(pokemon_info_sheet, i, poke_info_num_col)
        gen = int(cell_value(pokemon_info_sheet, i, poke_info_gen_col))
        has_f_var = isnt_empty(pokemon_info_sheet, i, poke_info_f_col)
        has_mega = isnt_empty(pokemon_info_sheet, i, poke_info_mega_col)
        has_giganta = isnt_empty(pokemon_info_sheet, i, poke_info_giganta_col)
        reg_forms = cell_value(pokemon_info_sheet, i, poke_info_reg_forms_col)
        has_type_forms = isnt_empty(pokemon_info_sheet, i, poke_info_type_forms_col)
        has_misc_forms = isnt_empty(pokemon_info_sheet, i, poke_info_misc_forms_col)
        is_in_gen8 = isnt_empty(pokemon_info_sheet, i, poke_info_gen8_col)

        # Adding to pokedex
        globals.pokedex.append(globals.Pokemon(name, num, gen, has_f_var, has_mega, has_giganta, reg_forms, has_type_forms, has_misc_forms, is_in_gen8))

# TODO: When JSONs implementation complete, only run this when generating pokedex
# TODO: When this happens this function should be redundant, as the poke

# Reading the filecheck spreadsheet with the end goal of adding missing images
def add_missing_images_to_poke():
    print("Getting missing images from spreadsheet...")

    prev_row_poke_num = -1
    # TODO: Check poke_num_start_from + 1 is accurate (starts at bulbasaur for 1)
    for row in range(poke_num_start_from + 1, pokemon_files_sheet.max_row):
        # TODO: check this works too
        # Haven't reset poke_num yet, so it is the previous rows poke num
        prev_row_poke_num = poke_num
        poke_num = int(cell_value(pokemon_files_sheet, row, poke_files_num_col))
        #TODO: Test
        poke_obj = pokedex[poke_num-1]
        # Only print getting missing images message if its a new pokemon
        if prev_row_poke_num != poke_num:
            poke_name = cell_value(pokemon_files_sheet, row, poke_files_name_col)
            print("Getting ", poke_name, " missing images")
        
        # Tags meaning shiny, animated, back, froms, etc
        tags = cell_value(pokemon_files_sheet, row, poke_files_tags_col)
        # If just regular front image
        if tags == None:
            tags = ""
        # This grabs my translated filename for the image from the spreadsheet
        # Includes all but gen&game, since those cols are to determine what is missing
        filename = cell_value(pokemon_files_sheet, row, poke_files_filename_col)

        if bulba_doesnt_have_this_form(filename):
            continue

        # This is to track generations and skip if it's a back sprite below gen 5
        # To be sifted through to see if they're different by game for the given pokemon
        is_below_gen5 = False

        # Only doing filename_col up because those are where the actual checks need to be made (missing for certain games)
        # And +1 at the end to be inclusive
        for col in range(poke_files_filename_col + 1, pokemon_files_sheet.max_column + 1):
            col_name = get_col_name(pokemon_files_sheet, col)

            # Triggers at Platinum because excel file is reverse chronological, so Plat is first gen 4 game hit
            # Every loop iteration after is_below_gen5 will be true
            if col_name == "Platinum":
                is_below_gen5 = True

            # If pokemon image is unavailable, continue (don't add to missing images obviously)
            if cell_value(pokemon_files_sheet, row, col) == "u":
                continue

            # If it's a back image from a pokemon between gen1 and gen4
            # Put all game images into special missing array
            # This is so another script can go through these images and determine if there were differences in the sprites between games
            # If there were, each file will be named differently
            # Otherwise, they will all be lumped into a single gen# back img
            is_back_below_gen5 = is_below_gen5 and "-Back" in filename
            if is_empty(pokemon_files_sheet, row, col) or is_back_below_gen5:
                # Where to insert the gen in the filename
                gen_insert_index = filename.find(poke_name) + len(poke_name)
                gen_and_game = combine_gen_and_game(col_name, poke_num, tags)
                
                # Back sprites have to be seperated due to:
                # Below gen 5 all back sprites are being downloaded to a seperate folder to be sifted through
                if "-Back" in tags:
                    # Adding space because initially there was no space in spreadsheet
                        # This was for sorting purposes because back sprites start with hyphen immediately after gen
                        # But front sprites follow with a space so they come first in file order
                    # This variable is necessary because bulba uses games to denote which back sprites are from where
                        # In my filenaming convention (gen4 and below excluded due to actual sprite differences between games)
                        # For backs I JUST use gen
                        # But to scrape the image from bulba, I still need the game denoter, which this gets me
                    back_filename_w_game_and_gen_for_bulba = filename[:gen_insert_index] + " " + gen_and_game + filename[gen_insert_index:]
                    bulba_name = determine_bulba_name(back_filename_w_game_and_gen_for_bulba, poke_obj)
                    actual_filename =""
                    gen = ""
                    game = ""
                    if "Gen6" in gen_and_game:
                        # This is because all Gen6 are shared with gen7
                            # So denoter is Gen6-7
                        gen = gen_and_game[:6]
                        # Extra character to skip over space after gen
                        game = gen_and_game[7:]
                    else:
                        gen = gen_and_game[:4]
                        # Extra character to skip over space after gen
                        game = gen_and_game[5:]

                    # filename[:3] gets pokemon number
                    actual_filename = filename[:3] + " " + poke_name + " " + gen + filename[gen_insert_index:]
                    if is_below_gen5:
                        actual_filename += "-" + game
                        poke_obj.missing_gen1_thru_gen4_back_imgs.append((actual_filename, bulba_name))
                    else:
                        poke_obj.missing_imgs.append((actual_filename, bulba_name))
                else:
                    # Going +1 after the insert index because there's a space for non-back sprites
                    # This is to simulate in the spreadsheet the space between generation and games in the filenames
                        # This determines sorting order, so is fairly important
                            # Since the spreadsheet doesn't acknowledge games or gens in the "Filename" column (because each game gets it's own column)
                                # The space must be included to sort the spreadsheet to match filenames
                                    # And thus, must be accounted for here
                    gen_insert_index += 1
                    filename_w_gen = filename[:gen_insert_index] + gen_and_game + filename[gen_insert_index:]
                    bulba_name = determine_bulba_name(filename_w_gen, poke_obj)
                    poke_obj.missing_imgs.append((filename_w_gen, bulba_name))