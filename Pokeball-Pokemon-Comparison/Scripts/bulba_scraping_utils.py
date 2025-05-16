import requests # To retrieve webpages
from bs4 import BeautifulSoup   # To parse webpages
import re   # For filtering what images to download
import os

from json_utils import *
from db_utils import get_missing_poke_imgs_by_table, get_missing_pokeball_imgs, has_f_form, get_form_name, get_poke_name, get_pokeball_name, get_pokeball_img_type_name
from bulba_translation_mapping import *
from app_globals import *
from image_tools import *
from scraping_utils import *


# Their links are only the info after this
BULBA_FILE_STARTER_URL = "https://archives.bulbagarden.net/wiki/File:"


def bulba_scrape_pokemon(start_poke_num, stop_poke_num, allow_download=False):
    for poke_num in range(start_poke_num, stop_poke_num + 1):
        print(f"\rScraping pokemon #{poke_num} bulba images...", end='', flush=True)

        scrape_game_imgs(poke_num, allow_download)
        scrape_drawn_imgs(poke_num, allow_download)
        scrape_home_sprite_imgs(poke_num, allow_download)
        scrape_home_menu_imgs(poke_num, allow_download)
    
    # Resetting console line after updates from above
    print('\r' + ' '*55 + '\r', end='')




#|================================================================================================|
#|~~~~~~~~~~~~~~~~~~~~~~~~~~~~~[     UNIVERSAL TRANSLATIONS     ]~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~|
#|================================================================================================|

def translate_all_filenames_to_bulba_url(filename_dict, translate_func):
    for poke_info, files in filename_dict.items():
        if len(files)==0: continue
        print(f"\rTranslating #{poke_info[0]} filenames to bulba urls...", end='', flush=True)
        bulba_urls = []
        for my_filename in files:
            # Right now this filters out SV & BDSP Sprites, and animateds > Gen5 since bulba doesnt have them
            if bulba_doesnt_have_images_for(my_filename):
                continue
            bulba_filename = translate_func(my_filename, poke_info)
            bulba_filename_url = convert_bulba_filename_to_url(bulba_filename)
            bulba_urls.append((my_filename, bulba_filename_url))
        filename_dict[poke_info] = bulba_urls
    # Resetting console line after updates from above
    print('\r' + ' '*55 + '\r', end='')
    return filename_dict


def convert_bulba_filename_to_url(bulba_filename):
    return (BULBA_FILE_STARTER_URL + bulba_filename.replace(" ", "_"))


# Mega and regional forms, not gigantamax (bc urshifu, see dict in file for more)
def get_bulba_translated_universal_form(my_filename, mapping):
    for u_form, translation in mapping.items():
        if u_form in my_filename: return(translation)
    return ("")


def get_bulba_translated_species_form(poke_info, my_filename, map_type):
    poke_num = poke_info[0]
    form_id = poke_info[1]
    form_name = get_form_name(form_id)

    # No widespread universal forms combined with species forms, the few exceptions have their own form id/name associated with it
    if form_name in UNIVERSAL_FORMS:
        return("")

    if poke_num in BULBA_POKE_FORM_TRANSLATION_MAP:
        for form, translation in BULBA_POKE_FORM_TRANSLATION_MAP[poke_num][map_type].items():
            if form in form_name:
                # If Unown, adjust bulba translation as needed, see NOTE above function if need more info
                if poke_num == 201 and map_type == "Game":
                    translation = adjust_translation_for_unown(my_filename, translation)
                return(translation)
    
    if map_type not in ("Drawn", "Menu"):   # Drawn/HOME Menu forms will frequently omit forms to just run my filename
        print(f"Couldn't search for image to download... No respective form in map set for \t{my_filename}")
    return("-FORM_NOT_IN_MAP_SET")




#|================================================================================================|
#|~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~[     DOWNLOADING FUNCTIONS     ]~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~|
#|================================================================================================|

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
            save_first_frame(img_url, save_path)


def bulba_img_exists(url):
    img_page = requests.get(url)
    img_page_soup = BeautifulSoup(img_page.content, 'html.parser')
    img_exists = not img_page_soup.find("p", string=re.compile(r"No file by this name exists."))    # Negating a found non-existant statement on page
    return (img_exists, img_page_soup)


def bulba_doesnt_have_images_for(my_filename):
    for exclusion in BULBA_DOESNT_HAVE_GAME_IMGS_FOR:
        if exclusion in my_filename:
            if exclusion == "-Animated":
                # Allowing Gen2-5 Animated Sprites and Pokeballs (HOME will be excluded)
                if any(gen in my_filename for gen in ("Gen2", "Gen3", "Gen4", "Gen5")):
                    return False
            return True
    return False




#|================================================================================================|
#|~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~[     GAME IMAGES     ]~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~|
#|================================================================================================|

def scrape_game_imgs(poke_num, allow_download=False):
    missing_imgs_dict = get_missing_poke_imgs_by_table(poke_num, "obtainable_game_filenames")
    translated_missing_imgs = translate_all_filenames_to_bulba_url(missing_imgs_dict, bulba_game_sprite_translate)

    for poke_info, files in translated_missing_imgs.items():
        for file in files:
            # poke_info == (poke_num, form_id)
            # file == (my_file_naming_convention, bulba_url)
            bulba_game_sprite_filename_url = verify_translation_for_bulba_inconsistency(poke_info[0], file[0], file[1])
            my_filename = file[0] + ".png"
            save_path = os.path.join(GAME_SPRITE_SAVE_PATH, my_filename)
            if allow_download:  # Putting this here in addition to the actual func, so dont try to open bulba pages to check for existence
                get_bulba_img(bulba_game_sprite_filename_url, save_path, allow_download, has_animation=True)


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
    # No f version cosplay/cap pikachu
    if "0025" in my_filename and any(form in my_filename for form in ("-Form_Cap", "-Form_Cosplay")):
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




#|================================================================================================|
#|~~~~~~~~~~~~~~~~~~~~~~~~~~~~[     SCRAPING FOR NON-GAME IMAGES     ]~~~~~~~~~~~~~~~~~~~~~~~~~~~~|
#|================================================================================================|

def scraping_if_no_extra_steps_needed(poke_num, filename_table, translate_func, has_animation, allow_download, save_path):
    missing_imgs_dict = get_missing_poke_imgs_by_table(poke_num, filename_table) if filename_table != "pokeball_filenames" else get_missing_pokeball_imgs()
    translated_missing_imgs = translate_all_filenames_to_bulba_url(missing_imgs_dict, translate_func)

    for poke_info, files in translated_missing_imgs.items():
        for file in files:
            # poke_info == (poke_num, form_id) or (pokeball_id, img_type_id) if pokeball img
            # file == (my_file_naming_convention, bulba_url)
            save_path = os.path.join(save_path, file[0])
            if allow_download:  # Putting this here in addition to the actual func, so func doesnt try to open bulba pages to check for existence
                get_bulba_img(file[1], save_path, allow_download, has_animation)




#|================================================================================================|
#|~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~[     HOME IMAGES     ]~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~|
#|================================================================================================|

def scrape_home_sprite_imgs(poke_num, allow_download=False):
    # NOTE: has_animation set to true (because it does, just not in bulba), if it were false and missing it would just download the still
    # As of writing (4-30-25) bulba doesn't have animated HOME sprites, but I do want to leave the option open if possible
    scraping_if_no_extra_steps_needed(poke_num, "home_filenames", home_sprite_translate, True, allow_download, HOME_SAVE_PATH)


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




#|================================================================================================|
#|~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~[     HOME MENU IMAGES     ]~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~|
#|================================================================================================|

def scrape_home_menu_imgs(poke_num, allow_download=False):
    scraping_if_no_extra_steps_needed(poke_num, "home_menu_filenames", home_menu_translate, False, allow_download, HOME_MENU_SAVE_PATH)


def home_menu_translate(my_filename, poke_info):
    poke_num = poke_info[0]
    poke_num_leading_zeros = str(poke_num).zfill(4)
    home_menu_filename = f"Menu HOME {poke_num_leading_zeros}"
    # Urshifu order doesn't matter because no gigantamax home menu sprites
    # TODO: But also doesn't have form menu sprites either? See if thats the case for others after download
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




#|================================================================================================|
#|~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~[     DRAWN IMAGES     ]~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~|
#|================================================================================================|

def scrape_drawn_imgs(poke_num, allow_download=False):
    scraping_if_no_extra_steps_needed(poke_num, "drawn_filenames", drawn_translate, False, allow_download, DRAWN_SAVE_PATH)


def drawn_translate(my_filename, poke_info):
    poke_num = poke_info[0]
    poke_num_leading_zeros = str(poke_num).zfill(4)
    poke_name = get_poke_name(poke_num)
    if poke_num == 669: poke_name = poke_name.replace("e", "\u00e9")    # Adjusting for flabebe proper name
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




#|================================================================================================|
#|~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~[     POKEBALL IMAGES     ]~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~|
#|================================================================================================|

def bulba_scrape_pokeballs(allow_download=False):
    # Setting animated to True for gen5_Battle-Animated, -1 for poke_num which just gets ignored for this table name anyways
    scraping_if_no_extra_steps_needed(-1, "pokeball_filenames", pokeball_translate, True, allow_download, POKEBALL_SAVE_PATH)


def pokeball_translate(my_filename, pokeball_info):
    bulba_filename = ""
    pokeball_name = get_pokeball_name(pokeball_info[0])
    img_type_name = get_pokeball_img_type_name(pokeball_info[1])

    if pokeball_name == "Poke Ball" and img_type_name != "Drawn": pokeball_name = pokeball_name.replace("e", "\u00e9")
    # NOTE: Hisuian pokeballs do not get any bulba denotion for bag sprites (so poke ball and hisuian poke ball are formatted the same), just that they are the only ones to exist in LA & HOME bag sprites...
    if "-Hisui" in pokeball_name and any(types in img_type_name for types in ("-Bag", "LA_Summary")): pokeball_name = pokeball_name.replace("-Hisui", "")
    
    if "Bag" in img_type_name:
        bag_platform = get_bulba_translated_pokeball_info(img_type_name)
        bulba_filename = f"Bag {pokeball_name}{bag_platform} Sprite.png"
    elif img_type_name == "PGL":
        bulba_filename = f"Dream {pokeball_name} Sprite.png"
    elif img_type_name == "Drawn":
        no_space_ball_name = pokeball_name.replace(" ", "")
        bulba_filename = f"Sugimori{no_space_ball_name}.png"
    elif "-Hisui" in pokeball_name and img_type_name == "HOME":
        pokeball_name = pokeball_name.replace("-Hisui", "")
        bulba_filename = f"Hisuian {pokeball_name} HOME.png"
    else:
        translation = get_bulba_translated_pokeball_info(img_type_name)
        # Gen3 ultra ball different between games, adding on FRLGE or RS depending on which I'm looking for 
        if pokeball_name == "Ultra Ball" and img_type_name == "Gen3": translation += f"-{my_filename.split("-")[-1]}"
        bulba_filename = f"{pokeball_name} {translation}.png"
    
    return bulba_filename


def get_bulba_translated_pokeball_info(info):
    try:
        return BULBA_POKEBALL_TRANSLATION_MAP[info]
    except KeyError:
        return ("-NOT_IN_MAP_SET")