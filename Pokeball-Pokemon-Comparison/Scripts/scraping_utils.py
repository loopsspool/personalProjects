import urllib   # For downloading those images to my computer
import os
import requests
from bs4 import BeautifulSoup
import re

from db_utils import get_missing_poke_imgs_by_table, get_missing_pokeball_imgs
from image_utils import save_first_frame, is_animated
from translation_utils import EXCLUDE_TRANSLATIONS_MAP
from app_globals import *




#|================================================================================================|
#|~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~[     DOWNLOADING UTILITIES     ]~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~|
#|================================================================================================|

# TODO: Add scraping countermeasures: 1-3 sec wait between downloads, rotate IPs w proxy pools, session spoofing?
# TODO: Keep track of files that didn't exist and make sure it doesn't try to get run again (animateds, back sprites in Wikidex, etc)

# NOTE: ALL DOWNLOADS MUST BE DONE IN THE FASHION BELOW -- Otherwise bulba has a check on if the site is being web scraped and it will block the download
opener = urllib.request.URLopener()
opener.addheader('User-Agent', 'Mozilla/5.0')

def download_img(url, save_path):
    img_type = get_file_ext(url)

    if img_type in (".png", ".gif"):
        filename, headers = opener.retrieve(url, save_path)
    elif img_type == ".webm":
        ani_img = requests.get(url).content
        with open(save_path, 'wb') as my_file:
            my_file.write(ani_img)


# NOTE: Only reason this works is because bulba uses same file extension for static/animated sprites
# Wikidex has some logic for same filename, different extensions, may be worth expanding on if ever scraping more sites
def determine_animation_status_before_downloading(img_url, save_path):
    img_is_animated = is_animated(img_url)
    if "-Animated" in save_path:
        if img_is_animated:
            download_img(img_url, save_path)
        else:
            print(f"Could not download animated img for {save_path.split("\\")[-1]}")
    else: # Looking for still
        if not img_is_animated:
            download_img(img_url, save_path)
        else: # Looking for still, but image is animated
            save_first_frame(img_url, save_path)


def img_exists_at_url(url, nonexistant_string_denoter):
    img_page = requests.get(url, allow_redirects=False)
    # The below catches a redirect... Can happen for instance trying to get gen6 pokemon back sprites for gen 7, which just downloads the same image twice when I already have the games as fallbacks in my db
    # Generally, I want my URLs to go to that exact image, and if it links to another, my db should also link to another... But TODO: Check after scrape, if oddballs missing this may be why
    if 300 <= img_page.status_code < 400:
        return False, None
    
    img_page_soup = BeautifulSoup(img_page.content, 'html.parser')
    img_exists = not img_page_soup.find("p", string=re.compile(nonexistant_string_denoter))    # Negating a found non-existant statement on page
    return (img_exists, img_page_soup)


def determine_save_path_from_file_type(file_ext):
    if file_ext == ".png": return GAME_SPRITE_SAVE_PATH
    if file_ext == ".gif": return GIF_SAVE_PATH
    if file_ext == ".webm": return WEBM_SAVE_PATH





#|================================================================================================|
#|~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~[     SCRAPING UTILITIES     ]~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~|
#|================================================================================================|

def scrape_imgs(poke_num, filename_table, translate_func, exclusions, has_animation, save_path, config_dict):
    missing_imgs_dict = get_missing_poke_imgs_by_table(poke_num, filename_table) if filename_table != "pokeball_filenames" else get_missing_pokeball_imgs()
    translated_missing_imgs = translate_all_my_filenames_to_url(missing_imgs_dict, translate_func, exclusions, config_dict["Site URL"])

    for poke_info, files in translated_missing_imgs.items():
        for file in files:
            # poke_info == (poke_num, form_id) or (pokeball_id, img_type_id) if pokeball img
            # file == (my_file_naming_convention, translated_url)
            
            url_file_ext = get_file_ext(file[1])
            my_filename = f"{file[0]}{url_file_ext}"

            print(f"{file[1]} \t<-->\t {my_filename}")
            file_save_path = os.path.join(save_path, my_filename)
            if config_dict["Allow Download"]:  # Putting this here in addition to the actual download func, so func doesnt try to open pages to check for existence
                config_dict["Site DL Logic Function"](file[1], file_save_path, config_dict["Allow Download"], has_animation)


def translate_all_my_filenames_to_url(filename_dict, translate_func, exclude, starter_url):
    for poke_info, files in filename_dict.items():
        print(f"\rTranslating #{poke_info[0]} filenames to urls...", end='', flush=True)
        urls = []
        for my_filename in files:
            if exclude != None and exclude(my_filename): continue

            translated_filename = translate_func(my_filename, poke_info)
            if found_excluded_term(translated_filename): continue

            translated_filename_url = convert_translated_filename_to_url(starter_url, translated_filename)
            urls.append((my_filename, translated_filename_url))

        filename_dict[poke_info] = urls
    # Resetting console line after updates from above
    print('\r' + ' '*55 + '\r', end='')
    return filename_dict


def found_excluded_term(translated_filename):
    for excl_term in EXCLUDE_TRANSLATIONS_MAP.values(): # These are forms that are translated to DO_BY_HAND, DOES_NOT_EXIST, etc
        if excl_term in translated_filename: 
            return True


def convert_translated_filename_to_url(starter_url, translated_filename):
    return (starter_url + translated_filename.replace(" ", "_"))


# This logic is constant coming from a script (bulba/wikidex/other) and does not matter which image type is being passed, 
# So I can pull these parameters out of the scrape_imgs calls
def generate_config_dict(starter_url, download_func, allow_download):
    config_dict = {
        "Site URL": starter_url,
        "Site DL Logic Function": download_func,
        "Allow Download": allow_download
    }
    return config_dict