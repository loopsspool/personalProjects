import openpyxl     # For reading excel workbook
# Must explicitly state this...
from openpyxl import load_workbook

import globals

# For Pokedex Info
pokemon_info = load_workbook(filename = 'C:\\Users\\ejone\\OneDrive\\Desktop\\Code\\Javascript\\p5\\projects\\Pokeball Pokemon Comparison\\Pokemon Info.xlsx', data_only=True)
pokemon_info_sheet = pokemon_info.worksheets[0]
# For file tracking (what images I do/dont have)
pokemon_files = load_workbook(filename = 'C:\\Users\\ejone\\OneDrive\\Desktop\\Code\\Javascript\\p5\\projects\\Pokeball Pokemon Comparison\\Pokemon File-check.xlsx', data_only=True)
pokemon_files_sheet = pokemon_files.worksheets[0]

# TODO: Change these so sheet is first variable
def cell_value(row, col, sheet):
    return (sheet.cell(row, col).value)

def isnt_empty(row, col, sheet):
    return (cell_value(row, col, sheet) != None)

def is_empty(row, col, sheet):
    return (cell_value(row, col, sheet) == None)

# Returns column number from column name
def get_col_number(col_name, sheet):
    for col in range(1, sheet.max_column):
        if (cell_value(1, col, sheet) == col_name):
            return col

# Returns column name from column number
def get_col_name(col_number, sheet):
    return(cell_value(1, col_number, sheet))

def generate_pokedex_from_spreadsheet():
    print("Getting pokemon info from spreadsheet...")

    # Gets column numbers from spreadsheet
    name_col = get_col_number("Name", pokemon_info_sheet)
    num_col = get_col_number("#", pokemon_info_sheet)
    gen_col = get_col_number("Gen", pokemon_info_sheet)
    f_col = get_col_number("Female Variation", pokemon_info_sheet)
    mega_col = get_col_number("Mega", pokemon_info_sheet)
    giganta_col = get_col_number("Gigantamax", pokemon_info_sheet)
    reg_forms_col = get_col_number("Regional Forms", pokemon_info_sheet)
    type_forms_col = get_col_number("Type Forms", pokemon_info_sheet)
    misc_forms_col = get_col_number("Misc Forms", pokemon_info_sheet)
    gen8_col = get_col_number("Available in Gen 8", pokemon_info_sheet)
    
    # Getting poke specific relevant info
    for i in range(2, 900):
        name = cell_value(i, name_col, pokemon_info_sheet)
        num = cell_value(i, num_col, pokemon_info_sheet)
        gen = int(cell_value(i, gen_col, pokemon_info_sheet))
        has_f_var = isnt_empty(i, f_col, pokemon_info_sheet)
        has_mega = isnt_empty(i, mega_col, pokemon_info_sheet)
        has_giganta = isnt_empty(i, giganta_col, pokemon_info_sheet)
        reg_forms = cell_value(i, reg_forms_col, pokemon_info_sheet)
        has_type_forms = isnt_empty(i, type_forms_col, pokemon_info_sheet)
        has_misc_forms = isnt_empty(i, misc_forms_col, pokemon_info_sheet)
        is_in_gen8 = isnt_empty(i, gen8_col, pokemon_info_sheet)

        # Adding to pokedex
        globals.pokedex.append(globals.Pokemon(name, num, gen, has_f_var, has_mega, has_giganta, reg_forms, has_type_forms, has_misc_forms, is_in_gen8))

# TODO: Break this into a shitload of functions so I can actually read it
# TODO: This function is stupid slow
# TODO: Add param for which poke num to start from
# Reading the filecheck spreadsheet with the end goal of adding missing images
def add_missing_images_to_poke(start_num):
    prev_row_poke_num = -1
    # TODO: Check start_num + 1 is accurate (starts at bulbasaur for 1)
    for row in range(start_num + 1, pokemon_files_sheet.max_row):
        # TODO: check this works too
        if row > start_num + 1:
            prev_row_poke_num = poke_num
        poke_num = int(cell_value(row, poke_num_col, pokemon_files_sheet))
        poke_name = cell_value(row, poke_name_col, pokemon_files_sheet)
        # Only print getting missing images message if its a new pokemon
        if prev_row_poke_num != poke_num:
            print("Getting ", poke_name, " missing images")

        poke_obj = -1
        #TODO: Grab pokemon by number in array -1, not checking each poke object
        # Getting pokemon object
        for pokemon in pokedex:
            # Num, not name for the likes of Flabebe (has apostrophe over e), Type: Null, etc
            if int(pokemon.number) == poke_num:
                poke_obj = pokemon
                break
        # Tags meaning shiny, animated, back, froms, etc
        tags = cell_value(row, tags_col, pokemon_files_sheet)
        # If just regular front image
        if tags == None:
            tags = ""
        # This grabs my translated filename for the image from the spreadsheet
        # Includes all but gen&game, since those cols are to determine what is missing
        filename = cell_value(row, filename_col, pokemon_files_sheet)

        # For only going after certain pokemon
            # If the server kicks me, this'll pick up my place
        # TODO: Uncomment
        # if poke_name != only_get_on_and_after() and (pokemon_not_reached_yet or pokemon_after >= pokemon_after_limit):
        #     continue
        # else:
        #     pokemon_not_reached_yet = False
        #     # This is to speed up the file each time I have to run it because of a server boot
        #     # Only goes n number after the starter poke
        #     # Checking if the previous pokemon name was different than the last
        #     if poke_name != cell_value(row-1, poke_name_col, pokemon_files_sheet):
        #         pokemon_after += 1
        # NOTE: Change the last number to pick up where last left off
        if not poke_obj.has_f_var or int(poke_obj.number) > 493 or int(poke_obj.number) <= back_start:
            continue

        if bulba_doesnt_have_this_form(filename):
            continue

        # TODO: Should I skip gen1? Why?  Are the gen1 back sprites all the same?
        # This is to track generations and skip if it's a back sprite below gen 5
        # Those sprites are being pulled seperately in the row only loop above
        # To be sifted through to see if they're different by game for the given pokemon
        is_below_gen5 = False
        # TODO: Is this still needed?
        # This is to download anything from Sword and Shield
        # Realized after bulba has higher quality gen8 models than wikidex
        is_swsh = False
        # Only doing filename_col up because those are where the actual checks need to be made (missing for certain games)
        # And +1 at the end to be inclusive
        for col in range(filename_col + 1, pokemon_files_sheet.max_column + 1):
            col_name = get_col_name(col, pokemon_files_sheet)

            # Triggers at Platinum because excel file is reverse chronological, so Plat is first gen 4 game hit
            # Every loop iteration after is_below_gen5 will be true
            if col_name == "Platinum":
                is_below_gen5 = True

            if col_name == "Sword-Shield":
                is_swsh = True
            else:
                is_swsh = False
            
            # If pokemon image is unavailable, continue (don't add to missing images obviously)
            if cell_value(row, col, pokemon_files_sheet) == "u":
                continue

            # If it's a back image from a pokemon between gen1 and gen4
            # Put all game images into special missing array
            # This is so another script can go through these images and determine if there were differences in the sprites between games
            # If there were, each file will be named differently
            # Otherwise, they will all be lumped into a single gen# back img
            is_back_below_gen5 = is_below_gen5 and "-Back" in filename
            if is_empty(row, col, pokemon_files_sheet) or is_back_below_gen5 or is_swsh:
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
                    #print(actual_filename, "     changed to     ", bulba_name)
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