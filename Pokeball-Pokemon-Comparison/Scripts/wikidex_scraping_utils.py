import requests     # For fetching HTML
from bs4 import BeautifulSoup   # For parsing HTML
import xlrd     # For reading excel data (female, forms, etc)
import urllib.request      # For saving images
import re   # To check each name is formatted properly
import time     # To simulate a pause between each page opening
import os.path   # To skip a file if it already exists


# ===============================================================================================================================================================================================
# ===============================================================================================================================================================================================

#   N   N    OOO   TTTTT  EEEEE
#   NN  N   O   O    T    E       ::
#   N N N   O   O    T    EEEE           This is a really old file, broken off from a longer script I wrote... Not updated yet to reflect best practice/work with other scripts
#   N  NN   O   O    T    E       ::
#   N   N    OOO     T    EEEEE 

# ===============================================================================================================================================================================================
# ===============================================================================================================================================================================================

# TODO: Wikidex has 2 images for each back sprite in gen4, see if there are any other games like this and figure out how to get them
# TODO: Wikidex animateds are all gifs, gen9 is webm.... determine if worthwhile to convert and color correct or keep as is. Consider RN and device compatibility


# WEB DATA
sprite_page = requests.get("https://www.wikidex.net/wiki/Categor%C3%ADa:Sprites_de_Pok%C3%A9mon")
sprite_page_soup = BeautifulSoup(sprite_page.content, 'html.parser')

game_sprites_link_table = sprite_page_soup.find("table")
games_by_gen = []


def get_game(a):
    # From titles, not text, so shiny pokemon (who's text is V) can still get the game
    title = a["title"].split("Pokémon ", 1)[1]
    title = game_translate(title)
    return(title)

def game_title_replace(old, new):
    global game
    global game_str

    if old in game:
        game_str = game_str.replace(old, new)

def form_translate_split(pokemon, spanish_form, translated_form):
    global form
    global split_name

    if pokemon in split_name and pokemon != split_name:
        if spanish_form in split_name:
            form = " " + translated_form
            split_name = split_name.split(" " + spanish_form)[0]



sprites_link_dict = {}
# Template for file naming, also easy access to each game sprites link


    keyname = ""
    # No animated sprites below gen 5 on this website
        # Except for Crystal, which the tag was added in game_translate
    if gen < 5:
        if back == False and shiny == False:
            keyname = "Gen" + str(gen) + " " + game
        if back == False and shiny == True:
            keyname = "Gen" + str(gen) + " " + game + " Shiny"
        if back == True and shiny == False:
            keyname = "Gen" + str(gen) + "-Back"
        if back == True and shiny == True:
            keyname = "Gen" + str(gen) + "-Back Shiny"
    else:
        if animated == True:
            if back == False and shiny == False:
                keyname = "Gen" + str(gen) + " " + game + " Animated"
            if back == False and shiny == True:
                keyname = "Gen" + str(gen) + " " + game + " Animated" + " Shiny"
            if back == True and shiny == False:
                keyname = "Gen" + str(gen) + "-Back" + " Animated"
            if back == True and shiny == True:
                keyname = "Gen" + str(gen) + "-Back Animated Shiny"
        if animated == False:
            if back == False and shiny == False:
                keyname = "Gen" + str(gen) + " " + game + " Static"
            if back == False and shiny == True:
                keyname = "Gen" + str(gen) + " " + game + " Static" + " Shiny"
            if back == True and shiny == False:
                keyname = "Gen" + str(gen) + "-Back" + " Static"
            if back == True and shiny == True:
                keyname = "Gen" + str(gen) + "-Back Static Shiny"

    # Excludes Let's Go because there's not enough sprites to justify it's inclusion
    # And Gen8 Shiny Back sprites because the page isn't uploaded yet
    if not "Let's Go" in keyname and not keyname == "Gen8-Back Static Shiny":
        sprites_link_dict[keyname] = "https://www.wikidex.net" + link.get("href")

# Gets rows (games) of sprite link table
print("Adding games to dict...")
for games in game_sprites_link_table.findAll("td"):
    games_by_gen.append(games)

for i in range(len(games_by_gen)):
    current_gen = i + 1
    current_game = ""
    # No animated sprites below gen5, so just get statics
    if (current_gen < 5):
        # Grabbing links and adding them to the dict
        for link in games_by_gen[i].findAll("a"):
            sprite_link_dict_entry(current_gen, link)

    # Seperates static and animated sprite pages gen 5 and above
    else:
        for image_type in games_by_gen[i].findAll('b'):
            # Excludes game seperators
            if not image_type.text == '|':
                # Gets animated or static
                if image_type.text == "Estáticos:":
                    is_animated = False
                if image_type.text == "Animados:":
                    is_animated = True
                # Grabbing links and adding them to the dict
                for link in image_type.find_next_siblings("a"):
                    sprite_link_dict_entry(current_gen, link, is_animated)


game_hit = False
outlier_sprites = []
for game, link in sprites_link_dict.items():
    # Running only specific games
    # Multiple after game
    # if game != "Gen8 Sword-Shield Animated Shiny":
    #     # If the game hasn't been hit yet, continue on to next game
    #     # If it HAS been hit, run the script
    #     if not game_hit:
    #         print("Skipping game...")
    #         continue
    # else:
    #     # If the game equals the one specified, run script
    #     print("Found game...")
    #     game_hit = True
    
    # Single game
    # if game != "Gen4 Diamond-Pearl Static":
    #     continue

    # Getting soup of the corresponding sprite page
    game_page = requests.get(link, headers = {'User-Agent': "Chrome/89.0.4389.82"})
    game_page_soup = BeautifulSoup(game_page.content, 'html.parser')
    print("Opening", game, "First Page...")
    start_time = time.time()

    # Inside for loop to clear for each game
    pokemon_img_dict = {}

    current_gen = re.findall("Gen\d", game)[0][-1]
    # Loops through pages of sprites collecting image links to download
    # No do-while loop in python, so running a while True loop with a break condition
        # This break condition being if there is not a next page
    while True:
        print("Reading pokemon...")
        # Gets images and captions on page
        names = game_page_soup.find_all(class_="gallerytext")
        imgs = game_page_soup.find_all(class_="gallerybox")
        for i in range(len(names)):
            # If japanese sprites, 3d ones, or game blocks skip em
            if "\(CV\)" in names[i].text or "Japón" in names[i].text or "3D" in names[i].text or "Bloque" in names[i].text:
                continue
            file_ext = names[i].text.split("\n")[1]
            file_ext = file_ext[len(file_ext)-4 : len(file_ext)]

            # Crude hardcode translation services, at your service
            # Done before split because in their naming convention they put genders after the game (which is the split seperator)
            gender = ""
            if "hembra" in names[i].text or "macho" in names[i].text:
                if "hembra" in names[i].text:
                    gender = " f"
                if "macho" in names[i].text:
                    gender = " m"

            # Removing game, file size, extension, etc
            # This conditional is due to the websites oversight-- Most on the page are XY Static shinies
                # Except mostly the Megas, hence the exception. The rest I will do by hand
            if game == "Gen6 ORAS Static Shiny" and names[i].text.startswith("\nMega-"):
                split_name = names[i].text.split(" ROZA")[0]
            else:
                split_name = names[i].text.split(split_seperators_by_game[game])[0]
            # Removing leading newline character
            split_name = split_name.split("\n")[1]

            # TODO: Group these with form translate split function
                # Default third parameter form but if not can do region, etc
            # Handling Mega evolutions -- Excluding the Meganium paradox
            mega = ""
            if split_name.startswith("Mega") and split_name != "Meganium":
                mega = " Mega"
                split_name = split_name.split("Mega-")[1]
                if split_name.endswith("X"):
                    mega = " MegaX"
                    split_name = split_name.split(" X")[0]
                if split_name.endswith("Y"):
                    mega = " MegaY"
                    split_name = split_name.split(" Y")[0]
            # Handling Dynamax (Except Eternatus Eternamax)
            dyna = ""
            if split_name.endswith("Dinamax") and not split_name.startswith("\nEternatus"):
                dyna = " Dynamax"
                split_name = split_name.split(" Dinamax")[0]
            # Handling Gigantamax
            giganta = ""
            if split_name.endswith("Gigamax"):
                giganta = " Gigantamax"
                split_name = split_name.split(" Gigamax")[0]
            # Handling regions
            region = ""
            if split_name.endswith("de Alola"):
                region = " Alolan"
                split_name = split_name.split(" de Alola")[0]
            if split_name.endswith("de Galar"):
                region = " Galarian"
                split_name = split_name.split(" de Galar")[0]

            # Doing forms becuase accumulation over all generations, shiny, static/animated, and back sprites would easily get into the thousands
            form = ""
            # Nidoran Genders in name
            if "Nidoran" in split_name and gender != "":
                if gender == " f":
                    split_name = split_name.replace("hembra", "f")
                if gender == " m":
                    split_name = split_name.replace("macho", "m")



            # Assigning Filenames
            match = False
            for poke in pokedex:
                if poke.name == split_name:
                    match = True
                    game_str = game
                    # This is to replace certain game names to include multiple games
                        # eg Black/White sprites are the same as Black2/White2
                        # XY, ORAS, SM, and USUM all use the same 3d sprites, etc
                            # So instead of doing multiple downloads for each game, I'm combining them to share the same image
                    game_title_replace("Black-White", "BW-B2W2")
                    game_title_replace("Black2-White2", "BW-B2W2")
                    game_title_replace("Gen6 XY", "Gen6-7 XY-ORAS-SM-USUM")
                    game_title_replace("Gen6 ORAS", "Gen6-7 XY-ORAS-SM-USUM")
                    # For back sprites
                    game_title_replace("Gen6-", "Gen6-7-")
                    game_title_replace("Gen7 Sun-Moon", "Gen7 SM-USUM")
                    game_title_replace("Gen7 USUM", "Gen7 SM-USUM")

                    filename = poke.number + " " + poke.name + " " + game_str + gender + mega + dyna + giganta + form + region
                    # If the filename already exists (and it will for double sprites in DPP), add alt
                    try:
                        dummy = pokemon_img_dict[filename + file_ext]
                        # Crystal apparently has different back sprites as other gen2 games
                        if game == "Gen2-Back":
                            filename += " Crystal"
                        else:
                            # Since alt images are shown first on this website, they will have the original filename
                                # So, change the first file (alt) to alt filename, and keep the original filename for the second, actually original image
                            pokemon_img_dict[filename + " alt" + file_ext] = pokemon_img_dict.pop(filename + file_ext)
                    except:
                        dummy = "key doesn't exist yet, continue"

                    filename += file_ext
                    pokemon_img_dict[filename] = imgs[i].a.img["src"]
                    # Saves first-frame statics as png from gif for Crystal & Emerald
                        # TODO: THIS CONVERTS IT TO AN ANIMATED PNG (open in Chrome) -- WILL HAVE TO FIND ANOTHER WAY TO DO THIS
                    # if game == "Gen2 Crystal Animated" or game == "Gen2 Crystal Animated Shiny" or game == "Gen3 Emerald Animated" or game == "Gen3 Emerald Animated Shiny":
                    #     filename = filename.replace("Animated", "Static")
                    #     filename = filename.replace(".gif", ".png")
                    #     pokemon_img_dict[filename] = imgs[i].a.img["src"]
            # This is to see what pokemon aren't formatted correctly
            if match == False:
                outlier_sprites.append(names[i].text.split("\n")[1])
                pokemon_img_dict[names[i].text.split("\n")[1]] = imgs[i].a.img["src"]
                    
        # for k,v in pokemon_img_dict.items():
        #     print(k, ":", v)
        
        # If next game page exists, get its url to parse
        if game_page_soup.find("a", string="página siguiente") != None:
            time.sleep(1)
            print("Opening", game, "Next Page...")
            game_page = game_page_soup.find("a", string="página siguiente").get("href")
            game_page = requests.get("https://www.wikidex.net" + game_page, headers = {'User-Agent': "Chrome/89.0.4389.82"})
            game_page_soup = BeautifulSoup(game_page.content, 'html.parser')
        else:
            amount_of_imgs = len(pokemon_img_dict)
            current_img = 1
            pokes_since_time = 0
            print("Downloading", amount_of_imgs, "Images...")
            # If done with all images for the game, save them
            for file_name, poke_link in pokemon_img_dict.items():
                if os.path.exists("Images/Pokemon/" + file_name):
                    current_img += 1
                    continue
                print("Downloading %s/%s" % (current_img, amount_of_imgs),  file_name, "...")
                download_time = time.time()
                urllib.request.urlretrieve(poke_link, "Images/Pokemon/" + file_name)
                download_time = time.time() - download_time
                print("Downloaded %s/%s" % (current_img, amount_of_imgs), file_name)
                pokes_since_time += 1
                total_time = (time.time() - start_time)/60
                print("Download took %.1f seconds" % download_time)
                print("Downloading average: %.0f pokemon per minute" % (pokes_since_time/total_time))
                print("Downloading average: %.0f pokemon per hr" % ((pokes_since_time/total_time) * 60))
                print("Minutes elapsed: %.1f with %s pokemon downloaded" % (total_time, pokes_since_time))
                current_img += 1
                time.sleep(0.3)
            print(game, "Done")
            print("Total minutes:", (time.time() - start_time)/60, "Pokemon downloaded:", pokes_since_time)
            print("\n\n\n")
            time.sleep(3)
            break
    

print(len(outlier_sprites), "outlier pokes: ", outlier_sprites)