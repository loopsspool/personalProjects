from urllib.request import Request, urlopen   # For downloading those images to my computer
from urllib.parse import quote  # For translating non-english letters (with dots, lines, etc) to ASCII for Referer header
import os
import requests
from bs4 import BeautifulSoup
import re
import random
import time
from email.utils import parsedate_to_datetime
from datetime import datetime, timezone
from zoneinfo import ZoneInfo

from db_utils import get_missing_poke_imgs_by_table, get_missing_pokeball_imgs, update_file_existence
from translation_utils import EXCLUDE_TRANSLATIONS_MAP
from app_globals import *


# TODO: Add headers for wikidex and bulba
headers = {'User-Agent': 'Mozilla/5.0'}     # NOTE: For each new website add a Referer member (eg 'Referer': 'https://www.pokewiki.de/')


#|================================================================================================|
#|~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~[     DOWNLOADING UTILITIES     ]~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~|
#|================================================================================================|

# TODO: After conversion process figured out, this will need to convert animateds to webp
def download_img(url, save_path):
    img_type = get_file_ext(url)
    req = Request(url, headers=headers)

    #wait_for_server_to_load_img_if_needed(url)

    if img_type in (".png", ".gif"):
        with urlopen(req) as response, open(save_path, 'wb') as my_file:
            my_file.write(response.read())
    elif img_type == ".webm":
        ani_img = fetch_url_with_retry(url, headers).content
        with open(save_path, 'wb') as my_file:
            my_file.write(ani_img)


# NOTE: Only reason this works is because bulba uses same file extension for static/animated sprites
# Wikidex has some logic for same filename, different extensions, may be worth expanding on if ever scraping more sites
def determine_animation_status_before_downloading(img_url, save_path):
    from image_utils import is_animated, save_first_frame

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


# TODO: Rename function to be more accurate?
def img_exists_at_url(url):
    img_page = fetch_url_with_retry(url, headers)

    if img_page == None: return False     # This means a redirect or 404 was caught, and saying the page doesn't exist
    
    img_page_soup = BeautifulSoup(img_page.content, 'html.parser')
    
    return (img_page_soup)


def fetch_url_with_retry(url, headers=headers, stream_flag=False):
    MAX_RETRIES = 5
    BASE_DELAY = 5
    attempt = 0

    while attempt < MAX_RETRIES:
        try:
            response = requests.get(url, headers=headers, stream=stream_flag, allow_redirects=False)

            # Sometimes (really only with pokewiki) the image will be cutoff, I think due to caching. The below are ways to get data length so I can retry if this happens
            content_type = response.headers.get('Content-Type')
            content_length = response.headers.get("Content-Length")
            data = response.content
            
            # The below catches a redirect... Can happen for instance trying to get gen6 pokemon back sprites for gen 7, which just downloads the same image twice when I already have the games as fallbacks in my db
            # Generally, I want my URLs to go to that exact image, and if it links to another, my db should also link to another... But TODO: Check after scrape, if oddballs missing this may be why
            if 300 <= response.status_code < 400:
                return None
            
            elif response.status_code == 404:
                return None

            # Most frequent error is 503, I assume rate limiting. Content length (image cutoff) perhaps a caching issue, checking content type is the image bc sometimes pages are cut short too
            elif response.status_code in (429, 503) or ("image" in content_type and len(data) != int(content_length)):
                retry_after = response.headers.get("Retry-After")
                wait_time = parse_retry_after(retry_after) if retry_after else None
                reason = response.status_code if response.status_code in (429, 503) else "incomplete image given from server"

                if wait_time is None:
                    # Fallback to exponential backoff
                    wait_time = BASE_DELAY * (2 ** attempt)

                current_central_time = datetime.now(ZoneInfo("America/Chicago"))
                pp_current_central_time = current_central_time.strftime("%I:%M:%S %p")
                print(f"""\n\n\n
                      *********************************************************************************************
                      Retrying after {wait_time} seconds due to {reason} at {pp_current_central_time}
                      *********************************************************************************************
                      \n\n\n""")
                time.sleep(wait_time)
                attempt += 1
            
                # Success, return page
            elif response.status_code == 200: 
                return response
            
            else:
                response.raise_for_status()  # Raise other HTTP errors

        except requests.RequestException as e:
            # For connection timeouts, DNS errors, etc.
            print(f"Request failed: {e}. Retrying...")
            time.sleep(BASE_DELAY * (2 ** attempt))
            attempt += 1

    raise Exception(f"Failed to fetch {url} after {MAX_RETRIES} attempts.")


def parse_retry_after(retry_after):
    try:
        return int(retry_after)
    except ValueError:
        try:
            dt = parsedate_to_datetime(retry_after)
            now = datetime.now(timezone.utc)
            return max(0, int((dt - now).total_seconds()))
        except Exception:
            return None


def determine_save_path_from_file_type(file_ext):
    if file_ext == ".png": return save_directories["Game Sprites"]["path"]
    elif file_ext == ".gif": return save_directories["gif"]["path"]
    elif file_ext == ".webm": return save_directories["webm"]["path"]
    else: raise RuntimeError(f"Unkown file type: {file_ext}")


def print_couldnt_dl_msg(file):
    print(f"Couldn't download {file}")




#|================================================================================================|
#|~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~[     SCRAPING UTILITIES     ]~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~|
#|================================================================================================|

def scrape_imgs(poke_num, filename_table, translate_func, exclusions, has_animation, save_path, config_dict):
    missing_imgs_dict = get_missing_poke_imgs_by_table(poke_num, filename_table) if filename_table != "obtainable_pokeball_filenames" else get_missing_pokeball_imgs()
    translated_missing_imgs = translate_all_my_filenames_to_url(missing_imgs_dict, translate_func, exclusions, config_dict["Site URL"])

    missing_count = 0
    for poke_info, poke_files in translated_missing_imgs.items():
        missing_count += len(poke_files)
        for file in poke_files:
            # poke_info == (poke_num, form_id) or (pokeball_id, img_type_id) if pokeball img
            # file == (my_file_naming_convention, translated_url)
            
            my_filename = file[0]
            if "-Animated" not in my_filename: my_filename += ".png"
            else:
                # TODO: When finished figuring out conversion, this will not be accurate -- should be webp for both
                url_file_ext = get_file_ext(file[1])
                my_filename += url_file_ext

            print(f"{file[1]} \t<-->\t {my_filename}")
            file_save_path = os.path.join(save_path, my_filename)
            if config_dict["Allow Download"]:  # Putting this here in addition to the actual download func, so func doesnt try to open pages to check for existence
                # To prevent my program downloading stuff too quickly
                sleep_time = random.uniform(1, 4)
                time.sleep(sleep_time)

                config_dict["Site DL Logic Function"](file[1], file_save_path, config_dict["Allow Download"], has_animation)

    if missing_count > 0:
        update_file_existence()


def translate_all_my_filenames_to_url(filename_dict, translate_func, exclude, starter_url):
    for poke_info, files in filename_dict.items():
        print(f"\rTranslating #{poke_info[0]} filenames to urls...", end='', flush=True)
        urls = []
        for my_filename in files:
            if exclude != None and exclude(my_filename): continue

            translated_filename = translate_func(my_filename, poke_info)
            if found_excluded_term(translated_filename) or translated_filename is None: continue

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