import xlsxwriter   # For writing new form rows
import os   # To check for files

from app_globals import pokedex
from spreadsheet_funcs import pokemon_info_sheet, cell_value, is_x_or_num, poke_info_swsh_col, poke_info_bdsp_col, poke_info_la_col, poke_info_sv_col


######################################### TODO: This whole thing needs to be rewritten to use Pokemon objects #########################################
# The redundant checks of already retrieved, available, and stored data is absurd

# TODO: This should always be run at the end of each scrape
# Or, even better, update cells at time of download from scraping file (and delete from their object missing imgs array)
# In that case this should only be run when the pokedex is not up to date (for unobtainables and whatnot, since missing_pokes func relies on that data)
# and only on the newest added pokes
# Also when you run this you could have this run add missing imgs from spreadsheet_funcs as well
# TODO: Add menu sprites, and drawn images

# SPREADSHEET DATA
# pokemon_info = xlrd.open_workbook('C:\\Users\\ejone\\OneDrive\\Desktop\\Code\\Javascript\\p5\\projects\\Pokeball Pokemon Comparison\\Pokemon Info.xls')
# form_sheet = pokemon_info.sheet_by_name("Form Rows")
# info_sheet = pokemon_info.sheet_by_name("Summary")

# TODO: Is this necessary? Can be pulled from pokemon object
def gen_finder(num):
    num = int(num)
    if num <= 151:
        return ("Gen1")
    if num > 151 and num <= 251:
        return ("Gen2")
    if num > 251 and num <= 386:
        return ("Gen3")
    if num > 386 and num <= 493:
        return ("Gen4")
    if num > 493 and num <= 649:
        return ("Gen5")
    if num > 649 and num <= 721:
        return ("Gen6")
    if num > 721 and num <= 809:
        return ("Gen7")
    if num > 809 and num <= 905:
        return ("Gen8")
    if num > 906 and num <= 1025:
        return ("Gen9")

def game_finder_from_gen(gen):
    # Index 3 instead of -1 because on Gen6-7 it would favor Gen7, excluding XY-ORAS
    gen = int(gen[3])

    if gen == 1:
        return(["Yellow", "Red-Green", "Red-Blue"])
    if gen == 2:
        return(["Silver", "Gold", "Crystal"])
    if gen == 3:
        return(["Ruby-Sapphire", "FireRed-LeafGreen", "Emerald"])
    if gen == 4:
        return(["Platinum", "HGSS", "Diamond-Pearl"])
    if gen == 5:
        return(["BW-B2W2"])
    if gen == 6:
        # Including SM-USUM here since gen 7 shared sprites from gen 6
        return(["SM-USUM", "XY-ORAS"])
    if gen == 7:
        return(["LGPE", "SM-USUM"])
    if gen == 8:
        return(["SwSh", "BDSP", "LA"])
    if gen == 9:
        return(["SV"])

# NOTE: 
    #   - TODO: f variants not in mega, giga, or region (except a f hisui sneasel) -- This rule must be applied somewhere other than the unobtainability checker (perhaps a nonexistant checker?)
    #   x No Hisuian variants in any other gen8 game, just LA and up
    #   x No regional variants in BDSP
    #   x No Galarian, alolan forms in LA at all except alolan vulpix, ninetails avail
    #   - Taurus type forms only in Paldea
    #   - Origin Dialga & Palkia only in gen 8-9
    #   - Darmanitan has both regular and galarian zen and standard form
    #   - Reshiram, Zekrom overdrive only in B2W2 ANIMATED (static is normal) & always, there is no non-overdrive animated form 
    #   - Radiant Sun Solgaleo and Full Moon Lunala only available in SMUSUM
    #   - Zenith Marshadow only in USUM
    #   - No default forms checker for certain pokes

# Decided to do tuples here so it's easier to troubleshoot why something was considered unobtainable
    # As oppsed to a bunch of print statements and seeing where it didn't print anymore bc of return
def unobtainability_check(filename, file_gen, poke, game):
    ###################     UNIVERSAL UNOBTAINABILITY     ###################
    # TODO: Run through object dict of games to see if poke avail in that dex
    # If filename is searching gens before pokemon was introduced
    if poke.gen > file_gen:
        return tuple((True, "Pokemon introduced after this gen"))
    # If filename is searching for females before gen4 (no visual difference)
    if "-f" in filename and file_gen < "Gen4":
        return tuple((True, "No female form visual difference before Gen 4"))
    # If filename is searching for animations in games where there weren't any
    if "-Animated" in filename:
        # No animated Back sprites before gen 5
        if "-Back" in filename and file_gen < "Gen5":
            return tuple((True, "No animated back sprites before Gen 5"))
        # No animated sprites in gen 1
        if file_gen == "Gen1":
            return tuple((True, "No animated sprites in Gen 1"))
        # No animated sprites in these games
        # Gen string before game string because stuff like "Gold" is in "Golduck"s name, etc
        no_animation_games = ["Gold", "Silver", "FireRed-LeafGreen", "Ruby-Sapphire"]
        for g in no_animation_games:
            s = file_gen + " " + g
            if s in filename:
                return tuple((True, "No animated sprites in GS, FRLG, or RS"))
    # If searching for a fairy type before gen6
    if "-Form-Fairy" in filename and file_gen < "Gen6":
        return tuple((True, "No fairy types before Gen 6"))
    # If filename is searching for shinies in gen1
    if "-Shiny" in filename and file_gen == "Gen1":
        return tuple((True, "No shinies in Gen 1"))
    # If filename is searching for megas outside of gen 6
    if "-Mega" in filename and file_gen != "Gen6":
        return tuple((True, "No mega forms outside Gen 6"))
    # If filename is searching for regional variants before gen 7
    # By default this will catch Region-Alola
    if "-Region" in filename and file_gen < "Gen7":
        return tuple((True, "No regional forms before Gen 7"))
    if ("-Region" in filename and not "-Rgion-Alola" in filename) and "LGPE" in filename:
        return tuple((True, "Only Alolan regional forms in LGPE")) 
    # No regional variants in BDSP
    if "-Region" in filename and "BDSP" in filename:
        return tuple((True, "No regional forms in BDSP"))
    # If looking for Galar variants before gen 8
    if "-Region-Galar" in filename and file_gen < "Gen8":
        return tuple((True, "No Galar forms before Gen 8"))
    # If looking for Hisuian variants ouside of LA and SV
    if "-Region-Hisui" in filename and not ("LA" in filename or "SV" in filename):
        return tuple((True, "No Hisui forms outside of LA and SV"))
    # If looking for other regional variants in LA
    if "-Region" in filename and "LA" in filename:
        if not "-Region-Hisui" in filename or not (poke.name=="Vulpix" or poke.name=="Ninetails"):
            return tuple((True, "No regional forms in LA except Alolan Vulpix/Ninetails"))
    if "-Gigantamax" in filename and game != "Sword-Shield":
        return tuple((True, "No gigantamax outside of SwSh"))

    ###################     INDIVIDUAL POKEMON     ###################
    # Pikachu Cosplay outside of Gen6
    if "-Form-Cosplay" in filename and file_gen != "Gen6":
        return tuple((True, "No pikachu cosplay outside Gen 6"))
    # Can't be shiny either
    if "-Form-Cosplay" in filename and "Shiny" in filename:
        return tuple((True, "No shiny pikachu cosplay"))
    # Pikachu Hat before Gen7
    if "-Form-Cap" in filename and file_gen < "Gen7":
        return tuple((True, "No pikachu cap below Gen 7"))
    # Pikachu cap in LGPE
    if "-Form-Cap" in filename and (game == "LGPE" or game == "BDSP"):
        return tuple((True, "No pikachu cap in LGPE or BDSP"))
    # Can't be shiny either
    if "-Form-Cap" in filename and "Shiny" in filename:
        return tuple((True, "No shiny pikachu cap"))
    # And World Cap only in Sword-Shield
    if "-Form-Cap-World" in filename and file_gen < "Gen8":
        return tuple((True, "No pikachu world cap below Gen 8"))
    # Unown punctuation before gen 3
    if "201" in filename and ("!" in filename or "Qmark" in filename) and file_gen < "Gen3":
        return tuple((True, "No Unown ! or ? below Gen 3"))
    # Spiky-Eared Pichu outside of gen 4
    if "-Form-Spiky_Eared" in filename and file_gen != "Gen4":
        return tuple((True, "No spiky-eared Pichu outside Gen 4"))
    # Primal Kyogre & Groudon outside of gen 6 & 7
    if "-Primal" in filename and file_gen != "Gen6" and file_gen != "Gen7":
        return tuple((True, "No Primal Groudon or Kyogre outside Gens 6 & 7"))
    # Rotom Forms only available from Platinum on
    if "Rotom" in filename and "Form" in filename and "Diamond-Pearl" in filename:
        return tuple((True, "No Rotom forms before Platinum"))
    # Origin Giratina form only available from Platinum on
    if "Giratina" in filename and "-Form-Origin" in filename and "Diamond-Pearl" in filename:
        return tuple((True, "No Giratina forms before Platinum"))
    # Sky Form Shaymin form only available from Platinum on
    if "Shaymin" in filename and "-Form-Sky" in filename and "Diamond-Pearl" in filename:
        return tuple((True, "No Shaymin forms before Platinum"))
    # ??? Form for Arceus not available after gen4
    if "Arceus" in filename and "Qmark" in filename and file_gen > "Gen4":
        return tuple((True, "??? Type Arceus only available in Gen4"))
    # Ash-Greninja only in SM-USUM
    if "-Form-Ash" in filename and file_gen != "Gen7":
        return tuple((True, "Ash Greninja only available in Gen 7"))
    # 10% and complete Zygarde forms only available in SM
    if ("10%" in filename or "Complete" in filename) and file_gen < "Gen7":
        return tuple((True, "Zygarde 10 percent and Complete forms not available before Gen 7"))
    # Meltan & Melmetal only available in LGPE and above
    if ("Meltan" in filename or "Melmetal" in filename) and game == "SM-USUM":
        return tuple((True, "Meltan and Melmetal only available from LGPE on"))
    
    # Checking if pokemon is available in SwSh
    if game == "Sword-Shield":
        for poke, avail in is_available_in_swsh.items():
            # Adding a space after for pokes like Porygon, whose evolutions contain the name Porygon also
            poke_check = poke + " "
            if poke_check in filename:
                if avail == False:
                    return tuple((True, "Pokemon not in SwSh pokeDex"))

    # If potential filename passes all the checks above, it is considered obtainable
    return tuple((False, "Pokemon is obtainable"))
    
def prevent_overriding(filename, game):
    # The unobtainability check was blocking all Alolan Regions in the spreadsheeet
        # This was due to SM-USUM being contained in the gen6-7 array (bc they share sprites)
            # And the Region tag for gen 6 was flagged unobtainable
            # This all AFTER it was cleared for being obtainable when SM-USUM was ran perviously as gen7 array (bc reverse chronological order)
    if "Gen6-7" in filename and game == "SM-USUM":
        # Allowing Alola Regions to show
        if "Region-Alola" in filename:
            return True
        # Allowing gen 7 pokemon to show as available
        if gen_finder(filename[:4]) == "Gen7":
            return True
        # Allowing Pikachu Caps through
        if "-Form-Cap" in filename:
            return True
        # REJECTING Cosplay Pikachu for SM-USUM
        if "-Form-Cosplay" in filename:
            return True
        # Allowing Ash Greninja
        if "-Form-Ash" in filename:
            return True
        # Allowing Zygarde forms
        if "10%" in filename or "Complete" in filename:
            return True

    return False

# TODO: tf is this?
form_pokedex = []

# TODO: Depending on how you handle type forms maybe change them back from misc forms for applicable pokes in the spreadsheet?
    

def

# Gets pokemon numbers, names, and forms
# Starting at 1 skips header cell
for i in range(1, len(form_sheet.col(0))):
    # Can do this with length of the first column since the name and number columns should be the same
    # Have to do form name keys so they're unique
        # (Pikachu-f and Pikachu-Cap share the same national dex number so there can't be repeat keys)

    name = cell_value(form_sheet, i, 1)
    number = cell_value(form_sheet, i, 0)
    variation = ""
    # Multiple variations:
        # Urshifu Gigantamax forms
        # Regional Darmanitan forms
    # Actually doesn't matter and they can still be lumped together
        # Because shiny comes before every other tag
        # Both Gigantamax and Regional tags come before form tag (so it's in proper order)
        # And back and animated tags come after variations
    if "-" in name and name != "Jangmo-o" and name != "Hakamo-o" and name != "Kommo-o" and name != "Porygon-Z" and name != "Ho-Oh":
        variation = "-" + name.split("-", 1)[1]
        name = name.split("-", 1)[0]

    form_pokedex.append(Pokemon(name, number, variation))

# for i in range(len(form_pokedex)):
#     print(form_pokedex[i].number, form_pokedex[i].name, "\n", form_pokedex[i].variation, "\n")

file_check_workbook = xlsxwriter.Workbook('C:\\Users\\ethan\\OneDrive\\Desktop\\Code\\Pokeball-Pokemon-Comparison\\Pokemon Images Checklist.xlsx')
file_check_worksheet = file_check_workbook.add_worksheet()


##########################  HEADER ROW  ########################## 
print("Generating header row...")
h_format = file_check_workbook.add_format({'bold': True, 'align': 'center', 'bg_color': 'gray', 'border': 1})
file_check_worksheet.set_row(0, None, h_format)
file_check_worksheet.freeze_panes(1, 0)
file_check_worksheet.write(0, 0, "#")
file_check_worksheet.write(0, 1, "Name")
file_check_worksheet.write(0, 2, "Tags")
file_check_worksheet.write(0, 3, "Filename")
# Games sorted by reverse chronological order for file sorting synchronization between excel and files
    # Also starting with newest game first so excel file doesn't look barren upon opening
games = ["SV", "LA", "BDSP", "SwSh", "LGPE", "SM-USUM", "XY-ORAS", "BW-B2W2", "Platinum", "HGSS", "Diamond-Pearl", "Ruby-Sapphire", "FireRed-LeafGreen", "Emerald", "Silver", "Gold", "Crystal", "Yellow", "Red-Green", "Red-Blue"]
game_cols = {}
for i in range(len(games)):
    # Saving game columns
    game_cols[games[i]] = i + 4
    # i + 4 to write to the next column after filename
    file_check_worksheet.write(0, i + 4, games[i])


##########################  POKEMON FILENAMES   ##########################
print("Creating potential pokemon filenames...")
# To adjust for there only being a single shiny look when in default form these pokemon have multiple forms
alcremie_shiny_forms_done = []
minior_shiny_form_done = False
filenames = []
# 1 because it's below the header row (row 0)
row_i = 1
for i in range(len(form_pokedex)):
    for i_ in range(8):
        # The below follow order of the microsoft alphabetically file order system that I have utilized in my naming structure
        # Normal
        tags_and_variation = form_pokedex[i].variation

        # To adjust for there only being shiny alcremie sweet forms
        if form_pokedex[i].name == "Alcremie" and (i_ == 2 or i_ == 3 or i_ == 6 or i_ == 7):
            # Not restricting by one hyphen so can get only the sweet at the end
            tags_and_variation = tags_and_variation.split("-")
            # Shiny-Form-Sweet
            tags_and_variation = "-Form-" + tags_and_variation[len(tags_and_variation) - 1]
            # If the shiny sweet form has already been done, continue through the other tags
            if tags_and_variation in alcremie_shiny_forms_done:
                continue
            # If it is the final tag iteration for alcremie, add it's shiny sweet forms to the done array to not be done again
            if i_ == 7:
                alcremie_shiny_forms_done.append(tags_and_variation)

        # To adjust for all colored minior core shinies being the same
        if form_pokedex[i].name == "Minior" and "Core" in tags_and_variation and (i_ == 2 or i_ == 3 or i_ == 6 or i_ == 7):
            tags_and_variation = "-Form-Core"
            # If the shiny core has been done, continue
            if minior_shiny_form_done:
                continue
            # If the shiny core hasn't been done and is on it's last iteration, mark it as done
            if i_ == 7:
                minior_shiny_form_done = True

        # Animated
        if i_ == 1:
            tags_and_variation += "-Animated"
        # Shiny
        if i_ == 2:
            tags_and_variation = "-Shiny" + tags_and_variation
        # Shiny-Animated
        if i_ == 3:
            tags_and_variation = "-Shiny" + tags_and_variation + "-Animated"
        # Back
        if i_ == 4:
            tags_and_variation += "-Back"
        # Back-Animated
        if i_ == 5:
            tags_and_variation += "-Back-Animated"
        # Shiny-Back
        if i_ == 6:
            tags_and_variation = "-Shiny" + tags_and_variation + "-Back"
        # Shiny-Back-Animated
        if i_ == 7:
            tags_and_variation = "-Shiny" + tags_and_variation + "-Back-Animated"

        # Assigning to cells
        # Number
        file_check_worksheet.write(row_i, 0, form_pokedex[i].number)
        # Name
        file_check_worksheet.write(row_i, 1, form_pokedex[i].name)
        # Tags & Variation
        file_check_worksheet.write(row_i, 2, tags_and_variation)
        # Filename (excluding gen & game)
            # Important to sort by so excel sheet has same ordering as file names
        filename = str(form_pokedex[i].number) + " " + form_pokedex[i].name

        # Back tags have no space in filename after gen (backs don't have game denotions), but fronts have spaces between gen and game
            # Adding this space simulates this crucial sorting system in the excel file without adding the gen and game (since those are going into columns)
        if "Back" in tags_and_variation:
            filename += tags_and_variation
        else:
            filename += " " + tags_and_variation

        # Adding too filenames array for file checking process later
        filenames.append(filename)
        file_check_worksheet.write(row_i, 3, filename)

        # Move onto next row
        row_i += 1


##########################  CHECKING FOR FILES   ##########################
print("Checking filenames against actual image files...")
# TODO: Incorporate alts
# TODO: Incorporate drawn images (on a different sheet?)
# TODO: Nitpick fixes
    # Deoxys forms game exlusive in gen 3
    # Spiky-eared pichu for all gen 4
    # Female backs that only have differences in the front
# TODO: 201 Unown in FRLG uses RS sprites
# TODO: If platinum animated is missing, but diamond and pearl are there, check off platinum
# TODO: Total missing is incorrect! Refer to missing_imgs_info.py for accurate total

game_sprite_path = "C:\\Users\\ejone\\OneDrive\\Desktop\\Code\\Javascript\\p5\\projects\\Pokeball Pokemon Comparison\\Images\\Pokemon\\Game Sprites\\"
game_sprite_files = os.listdir(game_sprite_path)
for i in range(len(game_sprite_files)):
    # Removes file extension to just check name
    game_sprite_files[i] = game_sprite_files[i][:len(game_sprite_files[i])-4]

# games = ["Sword-Shield", "SM-USUM", "XY-ORAS", "BW-B2W2", "Platinum", "HGSS", "Diamond-Pearl", "Ruby-Sapphire", "FireRed-LeafGreen", "Emerald", "Silver", "Gold", "Crystal", "Yellow", "Red-Green", "Red-Blue"]
game_denotions = ["Gen9 SV", "Gen8 LA", "Gen8 SwSh-BDSP", "Gen7 LGPE", "Gen7 SM-USUM", "Gen6-7 XY-ORAS-SM-USUM", "Gen5 BW-B2W2", "Gen4 Platinum", "Gen4 HGSS", "Gen4 Diamond-Pearl", "Gen3 Ruby-Sapphire", "Gen3 FireRed-LeafGreen", "Gen3 Emerald", "Gen2 Silver", "Gen2 Gold", "Gen2 Crystal", "Gen1 Yellow", "Gen1 Red-Green", "Gen1 Red-Blue"]
back_gen_denotions = ["Gen9", "Gen8", "Gen7", "Gen6-7", "Gen5", "Gen4", "Gen3", "Gen2", "Gen1"]

# Centers "x" in cell and makes fill color green
check_format = file_check_workbook.add_format({'align': 'center', 'bg_color': '#00cf37'})
missing_format = file_check_workbook.add_format({'align': 'center', 'bg_color': '#ff0000'})
unobtainable_format = file_check_workbook.add_format({'align': 'center', 'bg_color': 'black'})
# It's own "Missing" format since only some pokes have different Crystal back sprites
missing_crystal_back_format = file_check_workbook.add_format({'align': 'center', 'bg_color': '#fcba03'})

# This is to hardcode the game name in for sprites that have different backs between games within the same generation
    # Only for backs because front sprites have game in filename
# NOTE: This temporarily removes Crystal back differences on spreadsheet until all info is gathered on gen1-4 back sprites
def check_for_back_game_difference(filename, game):
    # SM-USUM (3DS) sprites differ from LGPE (Switch) models
    # Regional variants not introduced until Gen7, so can't share with XY-ORAS (those sprites denoted as Gen6-7)
    # This is the only check needed since in LGPE you can only get the first 151 pokemon + 808 and 809
    if "-Region-Alola" in filename and (game == "SM-USUM" or game == "LGPE"):
        return (filename + "-" + game)

    # TODO: Be sure to add a back check in the conditional when adding different games
    
    # If no game back differences, simply return the original filename
    return (filename)

def check_for_file(curr_file, game, row, col):
    global missing_count

    # Checking for back sprites that differ between games witin generation
    # Only for backs because front sprites have game in filename
    if "Back" in curr_file:
        curr_file = check_for_back_game_difference(curr_file, game)
    
    if curr_file in game_sprite_files:
        file_check_worksheet.write(row, col, "x", check_format)
    else:
        file_check_worksheet.write(row, col, "", missing_format)
        missing_count += 1

potential_wrong_continues = []
missing_count = 0
row = 1
for i in range(len(filenames)):
    f = filenames[i]
    # Gets pokemon number from filename to find the pokemon name and gen
    poke_num = f[0:3]
    poke_gen = gen_finder(poke_num)
    # Figures character length of number (always 4) and name
    insert_index = 4 + len(pokedex[poke_num])
    # Removes space after name for non-back sprites
        # This was added to mimic the file sorting into the excel file
    if not "Back" in f:
        f = f[:insert_index] + f[(insert_index + 1):]

    col = -1

    if "Back" in f:
        for gen in back_gen_denotions:
            # Adds generation to checking file string
            curr_file = f[:insert_index] + ' ' + gen + f[insert_index:]
            # Getting games in generation to find column
            games_in_gen = game_finder_from_gen(gen)
            # Finding columns of games in gen
            for game in games_in_gen:
                will_override = prevent_overriding(curr_file, game)
                if will_override:
                    # NOTE: Most overrides were intentional, but still making note. Only use for debugging if neeeded (which shouldn't be)
                    #potential_wrong_continues.append(curr_file)
                    continue
                col = game_cols[game]
                # Unobtainability checker
                is_unobtainable = unobtainability_check(curr_file, gen[:4], poke_gen, poke_num, game)
                if is_unobtainable[0]:
                    potential_wrong_continues.append(curr_file)
                    file_check_worksheet.write(row, col, "u", unobtainable_format)
                    continue

                check_for_file(curr_file, game, row, col)
            # print(curr_file)
    else:
        for filegame in game_denotions:
            # Adds game to checking file string
            curr_file = f[:insert_index] + ' ' + filegame + f[insert_index:]
            # Find column of game
            for game in games:
                if game in filegame:
                    will_override = prevent_overriding(curr_file, game)
                    if will_override:
                        # NOTE: Most overrides were intentional, but still making note. Only use for debugging if neeeded (which shouldn't be)
                        #potential_wrong_continues.append(curr_file)
                        continue
                    col = game_cols[game]
                    # Unobtainability checker
                    is_unobtainable = unobtainability_check(curr_file, filegame[:4], poke_gen, poke_num, game)
                    if is_unobtainable[0]:
                        potential_wrong_continues.append(curr_file)
                        file_check_worksheet.write(row, col, "u", unobtainable_format)
                        continue

                    check_for_file(curr_file, game, row, col)

            # print(curr_file)
    row += 1

# TODO: Missing count is wrong
print("Missing:", missing_count, "images")

# NOTE: Most overrides were intentional, but still making note. Only use for debugging if neeeded (which shouldn't be)
# for f in potential_wrong_continues:
#     # Excluding cosplay because the files ARE there, but they include SM-USUM in the name
#         # Instead of creating a XY-ORAS only tag and rewriting code
#         # The exclusion happens here. They are not continued for XY-ORAS, only SM-USUM for non-overwriting purposes of the unobtainability
#     if f in game_sprite_files and not "-Form-Cosplay" in f:
#         print("WRONG CONTINUE FOR:\n", f)

file_check_workbook.close()
print("Done!")
print("Remember to sort by filename column to have the spreadsheet line up with your files")

# Row by poke, column by game

# | Number | Name | Tags (incl. variation) |