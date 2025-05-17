import requests     # For fetching HTML
from bs4 import BeautifulSoup   # For parsing HTML
import xlrd     # For reading excel data (female, forms, etc)
import urllib.request      # For saving images
import re   # To check each name is formatted properly
import time     # To simulate a pause between each page opening
import os.path   # To skip a file if it already exists

from db_utils import get_missing_poke_imgs_by_table
from app_globals import *
from scraping_utils import *


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
# NOTE: No animated sprites below gen5


# WEB DATA
sprite_page = requests.get("https://www.wikidex.net/wiki/Categor%C3%ADa:Sprites_de_Pok%C3%A9mon")
WIKIDEX_STARTER_URL = "https://www.wikidex.net/wiki/Archivo:"


def wikidex_scrape_pokemon(start_poke_num, stop_poke_num, allow_download=False):
    wikidex_scrape_config = generate_config_dict(WIKIDEX_STARTER_URL, wikidex_get_img, allow_download)

    for poke_num in range(start_poke_num, stop_poke_num + 1):
        print(f"\rScraping pokemon #{poke_num} wikidex images...", end='', flush=True)

        scrape_imgs(poke_num, "obtainable_game_imgs", game_translate, exclusions=None, has_animation=True, save_path=GAME_SPRITE_SAVE_PATH, config_dict=wikidex_scrape_config)
        scrape_imgs(poke_num, "home_filenames", home_translate, exclusions=None, has_animation=True, save_path=HOME_SAVE_PATH, config_dict=wikidex_scrape_config)
        # NOTE: Technically Wikidex does have drawn images and home menu images, but bulba has every one so there's no need to scrape
        # If this changes in the future, it may be useful to browse their archives via url thru https://www.wikidex.net/index.php?title=Categor%C3%ADa:Pokemon_name

        # TODO: See what pokeballs they have in their archive
    
    # Resetting console line after updates from above
    print('\r' + ' '*55 + '\r', end='')


#|================================================================================================|
#|~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~[     GAME IMAGES     ]~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~|
#|================================================================================================|

def game_translate():
    pass


def wikidex_get_img():
    pass

def home_translate():
    pass

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


filename = poke.number + " " + poke.name + " " + game_str + gender + mega + dyna + giganta + form + region

# Crystal apparently has different back sprites as other gen2 games
if game == "Gen2-Back":
    filename += " Crystal"

pokemon_img_dict[filename] = imgs[i].a.img["src"]
# Saves first-frame statics as png from gif for Crystal & Emerald
    # TODO: THIS CONVERTS IT TO AN ANIMATED PNG (open in Chrome) -- WILL HAVE TO FIND ANOTHER WAY TO DO THIS
# if game == "Gen2 Crystal Animated" or game == "Gen2 Crystal Animated Shiny" or game == "Gen3 Emerald Animated" or game == "Gen3 Emerald Animated Shiny":
#     filename = filename.replace("Animated", "Static")
#     filename = filename.replace(".gif", ".png")
#     pokemon_img_dict[filename] = imgs[i].a.img["src"]


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