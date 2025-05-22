import requests     # For fetching HTML
from bs4 import BeautifulSoup   # For parsing HTML
import xlrd     # For reading excel data (female, forms, etc)
import urllib.request      # For saving images
import re   # To check each name is formatted properly
import time     # To simulate a pause between each page opening
import os.path   # To skip a file if it already exists

from wikidex_translation_mapping import *
from db_utils import get_poke_name, get_form_name
from app_globals import *
from scraping_utils import *
from image_utils import get_largest_png
from translation_utils import *


# ===============================================================================================================================================================================================
# ===============================================================================================================================================================================================

#   N   N    OOO   TTTTT  EEEEE
#   NN  N   O   O    T    E       ::
#   N N N   O   O    T    EEEE           This is a really old file, broken off from a longer script I wrote... Not updated yet to reflect best practice/work with other scripts
#   N  NN   O   O    T    E       ::
#   N   N    OOO     T    EEEEE 

# ===============================================================================================================================================================================================
# ===============================================================================================================================================================================================

# NOTE: No animated sprites below gen5 except Crystal


# WEB DATA
sprite_page = requests.get("https://www.wikidex.net/wiki/Categor%C3%ADa:Sprites_de_Pok%C3%A9mon")
WIKIDEX_STARTER_URL = "https://www.wikidex.net/wiki/Archivo:"


# NOTE: If ever decide to use Wikidex for menu sprites, drawn, etc. this will have to be nested like bulbas
def wikidex_scrape_pokemon(start_poke_num, stop_poke_num, allow_download=False):
    wikidex_scrape_config = generate_config_dict(WIKIDEX_STARTER_URL, wikidex_get_img, allow_download)

    for poke_num in range(start_poke_num, stop_poke_num + 1):
        print(f"\rScraping pokemon #{poke_num} wikidex images...", end='', flush=True)

        scrape_imgs(poke_num, "obtainable_game_filenames", wikidex_translate, exclusions=wikidex_doesnt_have_images_for, has_animation=True, save_path=GAME_SPRITE_SAVE_PATH, config_dict=wikidex_scrape_config)
        scrape_imgs(poke_num, "home_filenames", wikidex_translate, exclusions=None, has_animation=True, save_path=HOME_SAVE_PATH, config_dict=wikidex_scrape_config)
        # NOTE: Technically Wikidex does have drawn images and home menu images, but bulba has every one so there's no need to scrape
        # If this changes in the future, it may be useful to browse their archives via url thru https://www.wikidex.net/index.php?title=Categor%C3%ADa:Pokemon_name

        # TODO: See what pokeballs they have in their archive
    
    # Resetting console line after updates from above
    print('\r' + ' '*55 + '\r', end='')




#|================================================================================================|
#|~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~[     DOWNLOADING FUNCTIONS     ]~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~|
#|================================================================================================|

def wikidex_get_img(url, save_path, allow_download, has_animation=False):
    my_filename = save_path.split("\\")[-1]
    img_exists, img_page_soup = img_exists_at_url(url, nonexistant_string_denoter=r"No existe ningún archivo con este nombre.")
    if not img_exists:
        # TODO: Test this, applies to Gen8 Shiny Back Statics
        img_exists, img_page_soup = does_ani_file_exist_for_still(url, my_filename) # Looks for animated img under different file ext
        if not img_exists:
            return ()
    
    # Printing filename
    print(f"\r{my_filename}", end='', flush=True)
    # Resetting console line after updates from above
    print('\r' + ' '*75 + '\r', end='')
    
    if allow_download:
        # TODO: Try and find one with a larger avail image, all so far say no higher resolution available
        # TODO: DL if "Not available at a higher resolution" otherwise print filename so I can figure out how to get highest resolution
        # Found one: https://www.wikidex.net/wiki/Archivo:Abomasnow_EP_hembra.webm
        img_url = get_largest_png(img_page_soup)

        if has_animation:
            determine_animation_status_before_downloading(img_url, save_path)
        else:
            download_img(img_url, save_path)



def does_ani_file_exist_for_still(url, my_filename):
    if "-Animated" in my_filename: return False, None
    else:   # Can only look up animated imgs for stills
        fake_ani_filename = f"-Animated {my_filename}"  # This will trick my determine_file_ext func into triggering getting an animated file ext based of gen
        ani_file_ext = determine_file_extension(fake_ani_filename)
        ani_url = url.replace(".png", ani_file_ext)
        return img_exists_at_url(ani_url, nonexistant_string_denoter=r"No existe ningún archivo con este nombre.")            




#|================================================================================================|
#|~~~~~~~~~~~~~~~~~~~~~~~~~~~~~[     UNIVERSAL TRANSLATIONS     ]~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~|
#|================================================================================================|

def get_wikidex_translated_species_form(poke_info, my_filename):
    poke_num = poke_info[0]
    form_id = poke_info[1]
    form_name = get_form_name(form_id)

    # No widespread universal forms combined with species forms, the few exceptions have their own form id/name associated with it
    if form_name in UNIVERSAL_FORMS:
        return("")

    if poke_num in WIKIDEX_POKE_FORM_TRANSLATION_MAP:
        for form, translation in WIKIDEX_POKE_FORM_TRANSLATION_MAP[poke_num].items():
            if form in form_name:
                return(translation)
    
    print(f"Couldn't search for image to download... No respective form in map set for \t{my_filename}")
    return("-FORM_NOT_IN_MAP_SET")




#|================================================================================================|
#|~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~[     GAME IMAGES     ]~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~|
#|================================================================================================|

# TODO: Early games (Emerald, Crystal? FRLG? Check animation capable games) ONLY have animated sprites in gif... So add them to WIKIDEX DOESNT HAVE dict
# TODO: See how check animated status and trying to get the still would affect things since these are gifs and those were intended for same name pngs

def wikidex_translate(my_filename, poke_info):
    # poke_info == (poke_num, form_id)
    poke_num = poke_info[0]
    poke_name = get_poke_name(poke_num)
    form_name = get_form_name(poke_info[1])
    
    adj_poke_name = adjust_poke_name(poke_name, form_name)
    translated_form = get_wikidex_translated_species_form(poke_info, my_filename)
    form_tag = f" {translated_form}" if translated_form != "" else ""
    gigantamax_tag = " Gigamax" if "-Gigantamax" in form_name else ""
    back_tag = " espalda" if "-Back" in my_filename else ""
    platform = determine_platform(my_filename, back_tag)    # Determines if wikidex translate should have HOME, Game denoter, or Gen# for back sprites
    shiny_tag = " variocolor" if "-Shiny" in my_filename else ""
    female_tag = " hembra" if "-f" in form_name else ""
    file_ext = determine_file_extension(my_filename)

    wikidex_filename = f"{adj_poke_name}{form_tag}{gigantamax_tag}{back_tag}{platform}{shiny_tag}{female_tag}{file_ext}"
    return (wikidex_filename)
    

def adjust_poke_name(poke_name, form_name):
    for poke_form_needs_adj, adjust_name in POKE_NAME_ADJ_NEEDED:
        if poke_form_needs_adj(poke_name, form_name):
            adjusted_name = adjust_name(poke_name, form_name)
            return adjusted_name
        
    # If no need to adjust the name, just return it
    return poke_name


def determine_platform(my_filename, back_tag):
    if " HOME" in my_filename: platform = " HOME"
    elif back_tag == "":    # Img is front game sprite, get game
        platform = get_translated_game(my_filename, WIKIDEX_GAME_MAP, WIKIDEX_ALT_GAME_MAP)
    else:   # Get back gen
        # NOTE: Wikidex lumps backs together by gen, so gen8 is noted as gen8 but is only SwSh, no BDSP or LA back sprites in there
        platform = f" G{extract_gen_num_from_my_filename(my_filename)}"
        if "Gen2_Crystal" in my_filename: platform += " cristal"

    return platform


def determine_file_extension(my_filename):
    gen = 0
    if "-Animated" not in my_filename: return ".png"
    # Wikidex transitioned to .webm for animated HOME/Gen9. Gen8 below is .gif
    else:
        if " HOME" in my_filename: return ".webm"
        gen = extract_gen_num_from_my_filename(my_filename)
        
        if gen < 9: return ".gif"
        else: return ".webm"
    

def wikidex_doesnt_have_images_for(my_filename):
    for exclusion in WIKIDEX_DOESNT_HAVE_IMGS_FOR:
        # No animateds below gen5 except emerald and crystal
        if exclusion == ("-Animated") and "-Animated" in my_filename:
            if extract_gen_num_from_my_filename(my_filename) < 5:
                if "Gen3 Emerald" not in my_filename and "Gen2 Crystal" not in my_filename:
                    return True
                return False
        elif all(keyword in my_filename for keyword in exclusion):
            return True
    return False

# pokemon_img_dict[filename] = imgs[i].a.img["src"]
# # Saves first-frame statics as png from gif for Crystal & Emerald
#     # TODO: THIS CONVERTS IT TO AN ANIMATED PNG (open in Chrome) -- WILL HAVE TO FIND ANOTHER WAY TO DO THIS
# # if game == "Gen2 Crystal Animated" or game == "Gen2 Crystal Animated Shiny" or game == "Gen3 Emerald Animated" or game == "Gen3 Emerald Animated Shiny":
# #     filename = filename.replace("Animated", "Static")
# #     filename = filename.replace(".gif", ".png")
# #     pokemon_img_dict[filename] = imgs[i].a.img["src"]


# print("Downloading", amount_of_imgs, "Images...")
# # If done with all images for the game, save them
# for file_name, poke_link in pokemon_img_dict.items():
# if os.path.exists("Images/Pokemon/" + file_name):
#     current_img += 1
#     continue
# print("Downloading %s/%s" % (current_img, amount_of_imgs),  file_name, "...")
# download_time = time.time()
# urllib.request.urlretrieve(poke_link, "Images/Pokemon/" + file_name)
# download_time = time.time() - download_time
# print("Downloaded %s/%s" % (current_img, amount_of_imgs), file_name)
# pokes_since_time += 1
# total_time = (time.time() - start_time)/60
# print("Download took %.1f seconds" % download_time)
# print("Downloading average: %.0f pokemon per minute" % (pokes_since_time/total_time))
# print("Downloading average: %.0f pokemon per hr" % ((pokes_since_time/total_time) * 60))
# print("Minutes elapsed: %.1f with %s pokemon downloaded" % (total_time, pokes_since_time))
# current_img += 1
# time.sleep(0.3)