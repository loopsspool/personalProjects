import requests # To retrieve webpages
from bs4 import BeautifulSoup   # To parse webpages
import urllib   # For downloading those images to my computer
import re   # For filtering what images to download
import os

from json_utils import *
from db_utils import get_missing_poke_imgs_by_table, has_f_form, get_form_id, get_form_name, get_poke_name
from bulba_translation_mapping import *
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
# TODO: Import these from app_globals
GAME_SPRITE_PATH = "C:\\Users\\ethan\\OneDrive\\Desktop\\Code\\Pokeball-Pokemon-Comparison\\Images\\Pokemon\\Game Sprites\\"
DRAWN_SAVE_PATH = "C:\\Users\\ethan\\OneDrive\\Desktop\\Code\\Pokeball-Pokemon-Comparison\\Images\\Pokemon\\Drawn\\"
HOME_SAVE_PATH = "C:\\Users\\ethan\\OneDrive\\Desktop\\Code\\Pokeball-Pokemon-Comparison\\Images\\Pokemon\\HOME Sprites\\"
HOME_MENU_SAVE_PATH = "C:\\Users\\ethan\\OneDrive\\Desktop\\Code\\Pokeball-Pokemon-Comparison\\Images\\Pokemon\\Menu Sprites\\HOME\\"
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
    #scrape_game_imgs(allow_download)
    #scrape_drawn_imgs(allow_download)
    #scrape_home_sprite_imgs(allow_download)
    scrape_home_menu_imgs(allow_download)


def scrape_game_imgs(allow_download=False):
    missing_imgs_dict = get_missing_poke_imgs_by_table("obtainable_game_filenames")
    translated_missing_imgs = translate_all_filenames_to_bulba_url(missing_imgs_dict, bulba_game_sprite_translate)

    for poke_info, files in translated_missing_imgs.items():
        for file in files:
            # poke_info == (poke_num, form_id)
            # file == (my_file_naming_convention, bulba_url)
            bulba_game_sprite_filename_url = verify_translation_for_bulba_inconsistency(poke_info[0], file[0], file[1])
            my_filename = file[0] + ".png"
            save_path = os.path.join(GAME_SPRITE_PATH, my_filename)
            if allow_download:  # Putting this here in addition to the actual func, so dont try to open bulba pages to check for existence
                get_bulba_img(bulba_game_sprite_filename_url, save_path, allow_download, has_animation=True)


def translate_all_filenames_to_bulba_url(filename_dict, translate_func):
    for poke_info, files in filename_dict.items():
        if len(files)==0: continue
        print(f"\rTranslating #{poke_info[0]} game sprite filenames to bulba urls...", end='', flush=True)
        bulba_urls = []
        for my_filename in files:
            # Right now this filters out SV & BDSP Sprites since bulba doesnt have them
            if bulba_doesnt_have_game_images_for(my_filename):
                continue
            bulba_game_sprite_filename = translate_func(my_filename, poke_info)
            bulba_game_sprite_filename_url = convert_bulba_filename_to_url(bulba_game_sprite_filename)
            bulba_urls.append((my_filename, bulba_game_sprite_filename_url))
        filename_dict[poke_info] = bulba_urls
    # Resetting console line after updates from above
    print('\r' + ' '*55 + '\r', end='')
    return filename_dict


def convert_bulba_filename_to_url(bulba_filename):
    return (BULBA_FILE_STARTER_URL + bulba_filename.replace(" ", "_"))


def get_bulba_img(url, save_path, allow_download, has_animation=False):
    img_exists, img_page_soup = bulba_img_exists(url)
    if not img_exists:
        return ()
    else:
        # Printing filename
        print(f"\r{save_path.split("\\")[-1]}", end='', flush=True)
        # Resetting console line after updates from above
        print('\r' + ' '*75 + '\r', end='')
        
        if allow_download:
            img_url = get_largest_png(img_page_soup)

            if has_animation:
                determine_animation_status_before_downloading(img_url, save_path)
            else:
                download_img(img_url, save_path)


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
            # TODO: Test this
            save_first_frame(img_url, save_path)


def download_img(url, save_path):
    filename, headers = opener.retrieve(url, save_path)


def bulba_img_exists(url):
    img_page = requests.get(url)
    img_page_soup = BeautifulSoup(img_page.content, 'html.parser')
    img_exists = not img_page_soup.find("p", string=re.compile(r"No file by this name exists."))    # Negating a found non-existant statement on page
    return (img_exists, img_page_soup)


def bulba_doesnt_have_game_images_for(my_filename):
    for exclusion in BULBA_DOESNT_HAVE_GAME_IMGS_FOR:
        if exclusion in my_filename:
            return True
    return False


# NOTE: If pokemon has LOTS of forms, this func will probably be too slow. If searching less than say, 30 images probably fine. If more, hardcode probably
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
        # Resetting console line after updates from above
        print('\r' + ' '*55 + '\r', end='')
        return (url[:insert_index] + "-NOT_FOUND" + url[insert_index:])     # This prevents the default bulba image being downloaded for that form


def bulba_game_sprite_translate(my_filename, poke_info):
    # Starting bulba filename w their format
    bulba_filename = "Spr"
    if "-Back" in my_filename: bulba_filename += " b"
    bulba_game = get_bulba_translated_game(my_filename)    # Not just adding it so I can evaluate it later
    bulba_filename += bulba_game
    poke_num_int = poke_info[0]
    poke_num_leading_zeros = str(poke_num_int).zfill(3)  # Converting from 4 total digits to 3
    bulba_filename += f" {poke_num_leading_zeros}"
    bulba_filename += get_bulba_translated_universal_form(my_filename, BULBA_GAMES_UNIVERSAL_FORM_MAP)
    bulba_filename += get_bulba_translated_species_form(poke_info, my_filename, "Game")
    if "-Gigantamax" in my_filename: bulba_filename += "Gi"    # Put here because of Urshifu, form before gigantamax denoter
    bulba_filename += get_gender_denoter(poke_num_int, my_filename, is_game_sprite=True)
    if "-Shiny" in my_filename: bulba_filename += " s"
    bulba_filename += ".png"
    return(bulba_filename)


def get_bulba_translated_game(my_filename):
    for game, translation in BULBA_GAME_MAP.items():
        if "-Back" in my_filename:
            game = game.replace(" ", "_")
        if game in my_filename:
            return(f" {translation}")
        

# Mega and regional forms, not gigantamax (bc urshifu, see dict in file for more)
def get_bulba_translated_universal_form(my_filename, mapping):
    for u_form, translation in mapping.items():
        if u_form in my_filename: return(translation)
    return ("")


def get_bulba_translated_species_form(poke_info, my_filename, map_type):
    poke_num = poke_info[0]
    form_id = poke_info[1]
    form_name = get_form_name(form_id)

    # Keep above universal form check, otherwise may return empty string
    # Doing these by hand because they aren't clearly marked in bulba
    # TODO: Check these arent considered back sprites in bulba, see wikidex for true back sprite if so
        # If nowhere to be found, check in HOME
    if "-Show_Stamp" in my_filename:
        return("-DO_BY_HAND")

    # No widespread universal forms combined with species forms, the few exceptions have their own form id/name associated with it
    if form_name in UNIVERSAL_FORMS:
        return("")

    if poke_num in BULBA_TRANSLATION_MAP:
        for form, translation in BULBA_TRANSLATION_MAP[poke_num][map_type].items():
            # TODO: Changed this from checking my_filename to form_name, make sure it didnt break anything
                # I think I'll have to remove all hyphens from Drawn & Menu dicts bc -West isnt in -Form_West
            if form in form_name:
                # If Unown, adjust bulba translation as needed, see NOTE above function if need more info
                if poke_num == 201 and map_type == "Game":
                    translation = adjust_translation_for_unown(my_filename, translation)
                return(translation)
    
    if map_type not in ("Drawn", "Menu"):   # Drawn/HOME Menu forms will frequently omit forms to just run my filename
        print(f"Couldn't search for image to download... No respective form in map set for \t{my_filename}")
    return("-FORM_NOT_IN_MAP_SET")


# NOTE: I hate to hardcode it this way, but attempting 2-3 page opens just to find the right name (via verify_bulba_inconsistency func)
# AND THEN ANOTHER to download FOR EACH game AND sprite type was way too taxing for bulba resources and my time
# This may break in the future if someone (ie me) ever fixes their naming convention on bulba
# But in the meantime this is like 1000x faster than doing it programatically 
def adjust_translation_for_unown(my_filename, translation):
    # Gen4 has hyphens, A is always blank
    if "Gen4" in my_filename and "-Form_A" not in my_filename:
        # Regular color back doesn't have the hyphen, but the shiny backs do (ARRRAAAAGHHH)
        if "-Back" in my_filename and "-Shiny" not in my_filename:
            return translation
        adj_translation = "-" + translation
        return adj_translation
    # If condition isnt met, just return the letter
    return translation


# TODO: Adjust the likes of cap pikachu
# is_game_sprite necessary since both game sprites and home sprites are run through this, game sprites have m denoter where applicable, home sprites never do
def get_gender_denoter(poke_num, my_filename, is_game_sprite):
    has_f_var = has_f_form(poke_num)
    if "-f" in my_filename:
        return(" f")
    elif "-f" not in my_filename and has_f_var and is_game_sprite and include_male_denoter(my_filename):
        return(" m")
    else:
        return("")
    

def include_male_denoter(my_filename):
    # Checking file is gen4 or above (when f variations started)
    for gen_exclusion in MALE_DENOTER_EXCLUSION_GENS:
        if gen_exclusion in my_filename:
            return False
    # No universal forms w gender differences, except excpetions (Hisuian Sneasel f)
    if universal_form_in_filename(my_filename) and not f_exception_poke_in_filename(my_filename):
        return False
    return True


def universal_form_in_filename(my_filename):
    for u_form in BULBA_GAMES_UNIVERSAL_FORM_MAP:
        if u_form in my_filename:
            return True
        
    # Gigantamax pulled out of UNIVERRSAL_FORM_MAP for Urshifu
    if "-Gigantamax" in my_filename: return True
    
    return False


def f_exception_poke_in_filename(my_filename):
    for poke_num in FEMALE_DENOTER_UNIVERSAL_FORM_EXCEPTION_POKEMON:
        if poke_num in my_filename:
            return True
    return False


def scraping_if_no_extra_steps_needed(filename_table, translate_func, has_animation, allow_download, save_path):
    missing_imgs_dict = get_missing_poke_imgs_by_table(filename_table)
    translated_missing_imgs = translate_all_filenames_to_bulba_url(missing_imgs_dict, translate_func)

    for poke_info, files in translated_missing_imgs.items():
        for file in files:
            # poke_info == (poke_num, form_id)
            # file == (my_file_naming_convention, bulba_url)
            print(file)
            save_path = os.path.join(save_path, file[0])
            if allow_download:  # Putting this here in addition to the actual func, so func doesnt try to open bulba pages to check for existence
                get_bulba_img(file[1], save_path, allow_download, has_animation)


def scrape_home_sprite_imgs(allow_download=False):
    # NOTE: has_animation set to true (because it does, just not in bulba), if it were false and missing it would just download the still
    # As of writing (4-30-25) bulba doesn't have animated HOME sprites, but I do want to leave the option open if possible
    scraping_if_no_extra_steps_needed("home_filenames", home_sprite_translate, True, allow_download, HOME_SAVE_PATH)


def home_sprite_translate(my_filename, poke_info):
    poke_num = poke_info[0]
    poke_num_leading_zeros = str(poke_num).zfill(4)
    home_sprite_filename = f"HOME{poke_num_leading_zeros}"
    home_sprite_filename += get_bulba_translated_universal_form(my_filename, BULBA_GAMES_UNIVERSAL_FORM_MAP)
    home_sprite_filename += get_bulba_translated_species_form(poke_info, my_filename, "Game")
    if "-Gigantamax" in my_filename: home_sprite_filename += "Gi"    # Put here because of Urshifu, form before gigantamax denoter
    home_sprite_filename += get_gender_denoter(poke_num, my_filename, is_game_sprite=False)
    if "-Shiny" in my_filename: home_sprite_filename += " s"
    home_sprite_filename += ".png"
    return(home_sprite_filename)


def scrape_home_menu_imgs(allow_download=False):
    scraping_if_no_extra_steps_needed("home_menu_filenames", home_menu_translate, False, allow_download, HOME_MENU_SAVE_PATH)


def home_menu_translate(my_filename, poke_info):
    poke_num = poke_info[0]
    poke_num_leading_zeros = str(poke_num).zfill(4)
    home_menu_filename = f"Menu HOME {poke_num_leading_zeros}"
    # Urshifu order doesn't matter because no gigantamax home menu sprites
    # TODO: But also doesn't have form menu sprites either? See if thats the case for others
    home_menu_filename += get_bulba_translated_universal_form(my_filename, DRAWN_IMAGES_UNIVERSAL_FORMS_MAP)
    home_menu_filename += get_home_menu_translated_species_form(poke_info, my_filename)
    home_menu_filename += ".png"
    return home_menu_filename
    
def get_home_menu_translated_species_form(poke_info, my_filename):
    poke_num = poke_info[0]
    form_id = poke_info[1]
    form_name = get_form_name(form_id)

    # Species forms will usually translate from the drawn images species form translation dict, but sometimes that has weird cases/needs to use dream images
    # If that's the case (poke num in this exclusion set), translate from home menu translation dict
    try:    # If Menu denoters exist, use those. If not, use Drawn. If no drawn, use just the form name
        form_translation = get_bulba_translated_species_form(poke_info, my_filename, "Menu")
    except KeyError:
        try:
            form_translation = get_bulba_translated_species_form(poke_info, my_filename, "Drawn")
        except KeyError:
            species_form = get_form_name(poke_info[1]).replace("Form_", "")
            return(species_form)

    # If this showed up in the filename, its either an intentional omission of the form in my mapping file because my form name convention is an exact match for bulbas
    # or its a new pokemon not added to the mapping file yet, which will either work without further action or remind me I need to add its form to map
    if form_translation == "-FORM_NOT_IN_MAP_SET":    # If form was omitted for species form bulba translation mapping
        species_form = get_form_name(poke_info[1]).replace("Form_", "")
        return(species_form)
    else:
        return(form_translation)


def scrape_drawn_imgs(allow_download=False):
    scraping_if_no_extra_steps_needed("drawn_filenames", drawn_translate, False, allow_download, DRAWN_SAVE_PATH)


def drawn_translate(my_filename, poke_info):
    poke_num = poke_info[0]
    poke_num_leading_zeros = str(poke_num).zfill(4)
    poke_name = get_poke_name(poke_num)
    if poke_num == 669: poke_name.replace("e", "\u00e9")    # Adjusting for flabebe proper name
    bulba_drawn_filename = f"{poke_num_leading_zeros}{poke_name}"
    if poke_num == 29: bulba_drawn_filename = bulba_drawn_filename.replace(" f", "")
    if poke_num == 32: bulba_drawn_filename = bulba_drawn_filename.replace(" m", "")
    bulba_drawn_filename += get_bulba_translated_universal_form(my_filename, DRAWN_IMAGES_UNIVERSAL_FORMS_MAP)
    bulba_drawn_filename += get_bulba_translated_species_form(poke_info, my_filename, "Drawn")
    bulba_drawn_filename += ".png"

    # If this showed up in the filename, its either an intentional omission of the form in my mapping file because my file translation is an exact match for bulbas
    # or its a new pokemon not added to the mapping file yet, which will either work without further action or remind me I need to add its form to map
    if "-FORM_NOT_IN_MAP_SET" in bulba_drawn_filename:    # If form was omitted for species form bulba translation mapping
        bulba_drawn_filename = my_filename.replace(" ", "", 1)  # Try scraping for my filename (without space between poke num and name)
    # Bulba Dream files only go up to 3 leading zeros, not 4... This adjusts for that
    if " Dream" in bulba_drawn_filename and bulba_drawn_filename[0] == "0":
        bulba_drawn_filename = bulba_drawn_filename.replace("0","",1) 
    return bulba_drawn_filename