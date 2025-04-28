import requests # To retrieve webpages
from bs4 import BeautifulSoup   # To parse webpages
import urllib   # For downloading those images to my computer
import re   # For filtering what images to download
import os

from json_utils import *
from db_utils import get_missing_poke_imgs_by_table, has_f_form
from bulba_mapping_data import *
# from app_globals import *
from image_tools import *
# from bulba_translators import potentially_adapt_game_in_filename

# TODO: Maybe keep track of images on a page that are downloaded and if another matches a pattern have an alt for it? (see primal kyogre gen6ORAS and gen7SM)
# TODO: Maybe best to run to update db and spreadsheet after this finishes
    # If I do it inline, it'll be hard to populate substitutes
    # I guess I could write a function to do so, think about it
    # *** If crashes, db wont be updated and this'll download them again
        # AT VERY LEAST have update function for db get called before running this

# NOTE: ALL DOWNLOADS MUST BE DONE IN THE FASHION BELOW
    # Otherwise bulba has a check on if the site is being web scraped and it will block the download
# This is to mask the fact I'm webscraping
    # To use, call
    # filename, headers = opener.retrieve(get_largest_png(img), gen8_menu_sprite_save_path + save_name)
opener = urllib.request.URLopener()
opener.addheader('User-Agent', 'Mozilla/5.0')

PARENT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
POKE_URL_JSON_PATH = os.path.join(PARENT_DIR, "game_sprite_urls_by_poke.json")
# Their links are only the info after this
BULBA_ARCHIVES_STARTER_URL = "https://archives.bulbagarden.net"
BULBA_FILE_STARTER_URL = "https://archives.bulbagarden.net/wiki/File:"
GAME_SPRITE_PATH = "C:\\Users\\ethan\\OneDrive\\Desktop\\Code\\Pokeball-Pokemon-Comparison\\Images\\Pokemon\\Game Sprites\\"
# https://archives.bulbagarden.net/wiki/Category:Pok%C3%A9mon_artwork

    
def get_next_page_soup(curr_page_soup):
    try:
        next_page_url = curr_page_soup.find('a', string='next page').get('href')
        next_page = requests.get(BULBA_ARCHIVES_STARTER_URL + next_page_url)
        next_page_soup = BeautifulSoup(next_page.content, 'html.parser')
        return next_page_soup
    except:
        return None


def scrape(allow_download=False):
    scrape_game_imgs(allow_download)
    #scrape_drawn_imgs(allow_download)


def scrape_game_imgs(allow_download=False):
    missing_imgs_dict = get_missing_poke_imgs_by_table("obtainable_game_filenames")
    translated_missing_imgs = translate_all_filenames_to_bulba_url(missing_imgs_dict, bulba_game_sprite_translate)

    for poke_num, files in translated_missing_imgs.items():
        print(f"{poke_num}\t{files}")
        for file in files:
            # filename == (my_file_naming_convention, bulba_url)
            bulba_game_sprite_filename_url = verify_translation_for_bulba_inconsistency(poke_num, file[0], file[1])
            my_filename = file[0] + ".png"
            save_path = os.path.join(GAME_SPRITE_PATH, my_filename)
            #get_game_img(bulba_game_sprite_filename_url, save_path, allow_download)

    # for poke_num, missing_imgs in missing_imgs_dict.items():
    #     if len(missing_imgs)==0: continue
    #     for missing_img in missing_imgs:
    #         # Right now this filters out SV & BDSP Sprites since bulba doesnt have them
    #         if bulba_doesnt_have_game_images_for(missing_img):
    #             continue
    #         bulba_game_sprite_filename = bulba_game_sprite_translate(missing_img)
    #         bulba_game_sprite_filename_url = convert_bulba_filename_to_url(bulba_game_sprite_filename)
    #         bulba_game_sprite_filename_url = verify_translation_for_bulba_inconsistency(poke_num, bulba_game_sprite_filename_url, missing_img)
    #         my_filename = missing_img + ".png"
    #         save_path = os.path.join(GAME_SPRITE_PATH, my_filename)
    #         get_game_img(bulba_game_sprite_filename_url, save_path, allow_download)


def translate_all_filenames_to_bulba_url(filename_dict, translate_func):
    for poke_num, files in filename_dict.items():
        if len(files)==0: continue
        bulba_urls = []
        for my_filename in files:
            # Right now this filters out SV & BDSP Sprites since bulba doesnt have them
            if bulba_doesnt_have_game_images_for(my_filename):
                continue
            bulba_game_sprite_filename = translate_func(my_filename)
            bulba_game_sprite_filename_url = convert_bulba_filename_to_url(bulba_game_sprite_filename)
            bulba_urls.append((my_filename, bulba_game_sprite_filename_url))
        filename_dict[poke_num] = bulba_urls
    return filename_dict


def convert_bulba_filename_to_url(filename):
    return (BULBA_FILE_STARTER_URL + filename.replace(" ", "_"))


def get_game_img(url, save_path, allow_download):
    img_exists, img_page_soup = bulba_img_exists(url)
    if not img_exists:
        return ()
    else:
        # Printing filename
        print(f"\r{save_path.split("\\")[-1]}", end='', flush=True)
        # Resetting console line after updates from above
        print('\r' + ' '*75 + '\r', end='')

        img_url = get_largest_png(img_page_soup)
        img_is_animated = is_animated(img_url)

        if "-Animated" in save_path:
            if img_is_animated:
                if allow_download:
                    download_img(img_url, save_path)
        else: # Looking for still
            if not img_is_animated:
                if allow_download:
                    download_img(img_url, save_path)
            else: # Looking for still, but image is animated
                if allow_download:
                    # TODO: Test this
                    save_first_frame(img_url, save_path)


def download_img(url, save_path):
    filename, headers = opener.retrieve(url, save_path)


def bulba_img_exists(url):
    img_page = requests.get(url)
    img_page_soup = BeautifulSoup(img_page.content, 'html.parser')
    img_exists = not img_page_soup.find("p", string=re.compile(r"No file by this name exists."))    # Negating a found non-existant statement on page
    return (img_exists, img_page_soup)


def bulba_doesnt_have_game_images_for(filename):
    for exclusion in BULBA_DOESNT_HAVE_GAME_IMGS_FOR:
        if exclusion in filename:
            return True
    return False


# TODO: This is taking way too much time and using way too many bulba resources for a single gen inconsistency, find way to adapt for gen
# NOTE: poke num limited to 3 digits here since time of writing inconsistency was for game sprites
def verify_translation_for_bulba_inconsistency(poke_num, my_filename, url):
    if poke_num in BULBA_GAME_INCONSISTENCIES:
        poke_num_str = str(poke_num).zfill(3)
        insert_index = re.search(poke_num_str, url).end()
        for form, translation_list in BULBA_GAME_INCONSISTENCIES[poke_num].items():
            if form in my_filename:
                print(f"\rSearching for proper bulba filename for {my_filename}...", end='', flush=True)
                for translation in translation_list:
                    new_url = url[:insert_index] + translation + url[insert_index:]
                    exists, page_soup = bulba_img_exists(new_url)
                    if exists:
                        return (new_url)
        return (url[:insert_index] + "-NOT_FOUND" + url[insert_index:])     # This prevents the default bulba image being downloaded for that form


def bulba_game_sprite_translate(filename):
    # Starting bulba filename w their format
    bulba_filename = "Spr"
    if "-Back" in filename: bulba_filename += " b"
    bulba_game = get_bulba_translated_game(filename)    # Not just adding it so I can evaluate it later
    bulba_filename += bulba_game
    poke_num_int = int(filename[:4])
    poke_num_leading_zeros = str(poke_num_int).zfill(3)  # Converting from 4 total digits to 3
    bulba_filename += f" {poke_num_leading_zeros}"
    bulba_filename += get_bulba_translated_universal_form(filename)
    bulba_filename += get_bulba_translated_specific_form(poke_num_int, filename, BULBA_FORM_MAP)
    if "-Gigantamax" in filename: bulba_filename += "Gi"    # Put here because of Urshifu, form before gigantamax denoter
    bulba_filename += get_gender_denoter(poke_num_int, filename)
    if "-Shiny" in filename: bulba_filename += " s"
    bulba_filename += ".png"
    return(bulba_filename)


def get_bulba_translated_game(filename):
    for game, translation in BULBA_GAME_MAP.items():
        if "-Back" in filename:
            game = game.replace(" ", "_")
        if game in filename:
            return(f" {translation}")
        

# Mega and regional forms, not gigantamax (bc urshifu, see dict in file for more)
def get_bulba_translated_universal_form(filename):
    for u_form, translation in BULBA_UNIVERSAL_FORM_MAP.items():
        if u_form in filename: return(translation)
    return ("")


def get_bulba_translated_specific_form(poke_num, filename, mapping):
    if poke_num in mapping:
        for form, translation in mapping[poke_num].items():
            if form in filename:
                # If 201 and 4 in filename, add hyphen
                return(translation)
        if "-Form" in filename:     # This allows a default image to be downloaded for a default pokemon (will skip and go to empty string)
            return("FORM_NOT_IN_MAP_SET")    # This prevents a default image being downloaded for a pokemon with a form
    return("")


def get_gender_denoter(poke_num, filename):
    has_f_var = has_f_form(poke_num)
    if "-f" in filename:
        return(" f")
    elif "-f" not in filename and has_f_var and include_male_denoter(filename):
        return(" m")
    else:
        return("")
    

def include_male_denoter(filename):
    # Checking file is gen4 or above (when f variations started)
    for gen_exclusion in MALE_DENOTER_EXCLUSION_GENS:
        if gen_exclusion in filename:
            return False
    # No universal forms w gender differences, except excpetions (Hisuian Sneasel f)
    if universal_form_in_filename(filename) and not f_exception_poke_in_filename(filename):
        return False
    return True


def universal_form_in_filename(filename):
    for u_form in BULBA_UNIVERSAL_FORM_MAP:
        if u_form in filename:
            return True
        
    # Gigantamax pulled out of UNIVERRSAL_FORM_MAP for Urshifu
    if "-Gigantamax" in filename: return True
    
    return False


def f_exception_poke_in_filename(filename):
    for poke_num in FEMALE_DENOTER_UNIVERSAL_FORM_EXCEPTION_POKEMON:
        if poke_num in filename:
            return True
    return False


def scrape_drawn_imgs(allow_download=False):
    missing_imgs_dict = get_missing_poke_imgs_by_table("drawn_filenames")

    for poke_num, missing_imgs in missing_imgs_dict.items():
        if len(missing_imgs)==0: continue
        for missing_img in missing_imgs:
            bulba_filename = get_bulba_translated_specific_form(poke_num, missing_img, DRAWN_IMAGES_MAP)
            print(bulba_filename)

# Drawn
# Home
# Home menu sprites ONLY

# Drawn images
# TODO: 
# Remove space between poke num & name
# Check all forms, see if exceptions