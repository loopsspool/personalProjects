from json_utils import *
from db_utils import get_missing_poke_imgs_by_table, get_missing_pokeball_imgs, has_f_form, get_form_name, get_poke_name, get_pokeball_name, get_pokeball_img_type_name
from bulba_translation_mapping import *
from app_globals import *
from image_utils import *
from scraping_utils import *
from translation_utils import *

# NOTE: If bulba strays away from a/pngs, will have to implement determine_save_path_from_file_type() -- see wikidex scraping

# Their links are only the info after this
BULBA_FILE_STARTER_URL = "https://archives.bulbagarden.net/wiki/File:"


def bulba_scrape_pokemon(start_poke_num, stop_poke_num, allow_download=False):
    bulba_scrape_config = generate_config_dict(BULBA_FILE_STARTER_URL, get_bulba_img, allow_download)

    for poke_num in range(start_poke_num, stop_poke_num + 1):
        print(f"\rScraping pokemon #{poke_num} bulba images...", end='', flush=True)

        # Game Sprites
        scrape_imgs(poke_num, "obtainable_game_filenames", bulba_game_sprite_translate, exclusions=bulba_doesnt_have_images_for, has_animation=True, save_path=SAVE_PATHS["GAME_SPRITE"], config_dict=bulba_scrape_config)
        # Drawn Imgs
        scrape_imgs(poke_num, "drawn_filenames", drawn_translate, exclusions=None, has_animation=False, save_path=SAVE_PATHS["DRAWN"], config_dict=bulba_scrape_config)
        # Home Sprites
        # NOTE: has_animation set to true (because it does, just not in bulba), if it were false and missing it would just download the still
        # As of writing (4-30-25) bulba doesn't have animated HOME sprites, but I do want to leave the option open if possible
        scrape_imgs(poke_num, "home_filenames", home_sprite_translate, exclusions=None, has_animation=True, save_path=SAVE_PATHS["HOME"], config_dict=bulba_scrape_config)
        # Home Menu
        scrape_imgs(poke_num, "home_menu_filenames", home_menu_translate, exclusions=None, has_animation=False, save_path=SAVE_PATHS["HOME_MENU"], config_dict=bulba_scrape_config)
    
    # Resetting console line after updates from above
    print('\r' + ' '*55 + '\r', end='')




#|================================================================================================|
#|~~~~~~~~~~~~~~~~~~~~~~~~~~~~~[     UNIVERSAL TRANSLATIONS     ]~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~|
#|================================================================================================|

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
                # If Unown, adjust bulba translation as needed
                if poke_num == 201 and map_type == "Game":
                    translation = adjust_translation_for_unown(my_filename, translation)
                return(translation)
    
    if map_type not in ("Drawn", "Menu"):   # Drawn/HOME Menu forms will frequently omit forms to just run my filename
        print(f"Couldn't search for image to download... No respective form in map set for \t{my_filename}")
    return(EXCLUDE_TRANSLATIONS_MAP["NIM"])




#|================================================================================================|
#|~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~[     DOWNLOADING FUNCTIONS     ]~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~|
#|================================================================================================|

def get_bulba_img(url, save_path, allow_download, has_animation=False):
    my_filename = save_path.split("\\")[-1]

    img_exists, img_page_soup = img_exists_at_url(url, nonexistant_string_denoter=r"No file by this name exists.")
    if not img_exists:
        print_couldnt_dl_msg(my_filename)
        return ()
    else:
        if allow_download:
            img_url = bulba_get_largest_png(img_page_soup)

            if has_animation:
                determine_animation_status_before_downloading(img_url, save_path)
            else:
                download_img(img_url, save_path)


def bulba_doesnt_have_images_for(my_filename):
    for exclusion in BULBA_DOESNT_HAVE_GAME_IMGS_FOR:
        if exclusion in my_filename:
            if exclusion == "-Animated":
                # Allowing Gen2-5 Animated Sprites and Pokeballs (Gen6+ and HOME will be excluded from scrape)
                if any(gen in my_filename for gen in ("Gen2", "Gen3", "Gen4", "Gen5")):
                    return False
            return True
    return False




#|================================================================================================|
#|~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~[     GAME IMAGES     ]~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~|
#|================================================================================================|

def bulba_game_sprite_translate(my_filename, poke_info):
    # poke_info == (poke_num, form_id)

    # Starting bulba filename w their format
    bulba_filename_starter = "Spr"
    back_tag = " b" if "-Back" in my_filename else ""
    bulba_game = get_translated_game(my_filename, BULBA_GAME_MAP, BULBA_ALT_GAME_MAP)
    poke_num_int = poke_info[0]
    poke_num_leading_zeros = f" {str(poke_num_int).zfill(3)}"  # Converting from 4 total digits to 3
    universal_form_tag = get_translated_universal_form(my_filename, BULBA_GAMES_UNIVERSAL_FORM_MAP)
    species_form_tag = get_bulba_translated_species_form(poke_info, my_filename, "Game")
    gigantamax_tag = "Gi" if "-Gigantamax" in my_filename else ""    # Put here because of Urshifu, form before gigantamax denoter
    gender_tag = get_gender_denoter(poke_num_int, my_filename, is_game_sprite=True)
    shiny_tag = " s" if "-Shiny" in my_filename else ""
    file_ext = ".png"

    bulba_filename = f"{bulba_filename_starter}{back_tag}{bulba_game}{poke_num_leading_zeros}{universal_form_tag}{species_form_tag}{gigantamax_tag}{gender_tag}{shiny_tag}{file_ext}"
    return(bulba_filename)


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
#|~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~[     HOME IMAGES     ]~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~|
#|================================================================================================|

def home_sprite_translate(my_filename, poke_info):
    poke_num = poke_info[0]
    poke_num_leading_zeros = str(poke_num).zfill(4)
    home_sprite_filename = f"HOME{poke_num_leading_zeros}"
    home_sprite_filename += get_translated_universal_form(my_filename, BULBA_GAMES_UNIVERSAL_FORM_MAP)
    home_sprite_filename += get_bulba_translated_species_form(poke_info, my_filename, "Game")
    if "-Gigantamax" in my_filename: home_sprite_filename += "Gi"    # Put here because of Urshifu, form before gigantamax denoter
    home_sprite_filename += get_gender_denoter(poke_num, my_filename, is_game_sprite=False)
    if "-Shiny" in my_filename: home_sprite_filename += " s"
    home_sprite_filename += ".png"
    return(home_sprite_filename)




#|================================================================================================|
#|~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~[     HOME MENU IMAGES     ]~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~|
#|================================================================================================|

def home_menu_translate(my_filename, poke_info):
    poke_num = poke_info[0]
    poke_num_leading_zeros = str(poke_num).zfill(4)
    home_menu_filename = f"Menu HOME {poke_num_leading_zeros}"
    # Urshifu order doesn't matter because no gigantamax home menu sprites
    # TODO: But also doesn't have form menu sprites either? See if thats the case for others after download
        # Also check if they're in Wikidex
    home_menu_filename += get_translated_universal_form(my_filename, DRAWN_IMAGES_UNIVERSAL_FORMS_MAP)
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
    if form_translation == EXCLUDE_TRANSLATIONS_MAP["NIM"]:    # If form was omitted for species form bulba translation mapping
        species_form = get_form_name(poke_info[1]).replace("Form_", "")
        return(species_form)
    else:
        return(form_translation)




#|================================================================================================|
#|~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~[     DRAWN IMAGES     ]~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~|
#|================================================================================================|

def drawn_translate(my_filename, poke_info):
    poke_num = poke_info[0]
    poke_num_leading_zeros = str(poke_num).zfill(4)
    poke_name = get_poke_name(poke_num)
    if poke_num == 669: poke_name = poke_name.replace("e", "\u00e9")    # Adjusting for flabebe proper name
    bulba_drawn_filename = f"{poke_num_leading_zeros}{poke_name}"
    if poke_num == 29: bulba_drawn_filename = bulba_drawn_filename.replace(" f", "")
    if poke_num == 32: bulba_drawn_filename = bulba_drawn_filename.replace(" m", "")
    bulba_drawn_filename += get_translated_universal_form(my_filename, DRAWN_IMAGES_UNIVERSAL_FORMS_MAP)
    bulba_drawn_filename += get_bulba_translated_species_form(poke_info, my_filename, "Drawn")
    bulba_drawn_filename += ".png"

    # If this showed up in the filename, its either an intentional omission of the form in my mapping file because my file translation is an exact match for bulbas
    # or its a new pokemon not added to the mapping file yet, which will either work without further action or remind me I need to add its form to map
    if EXCLUDE_TRANSLATIONS_MAP["NIM"] in bulba_drawn_filename:    # If form was omitted for species form bulba translation mapping
        bulba_drawn_filename = my_filename.replace(" ", "", 1)  # Try scraping for my filename (without space between poke num and name)
    # Bulba Dream files only go up to 3 leading zeros, not 4... This adjusts for that
    if " Dream" in bulba_drawn_filename and bulba_drawn_filename[0] == "0":
        bulba_drawn_filename = bulba_drawn_filename.replace("0","",1) 
    return bulba_drawn_filename




#|================================================================================================|
#|~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~[     POKEBALL IMAGES     ]~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~|
#|================================================================================================|

def bulba_scrape_pokeballs(allow_download=False):
    bulba_scrape_config = generate_config_dict(BULBA_FILE_STARTER_URL, get_bulba_img, allow_download)

    # Setting animated to True for gen5_Battle-Animated, -1 for poke_num which just gets ignored for this table name anyways
    scrape_imgs(-1, "pokeball_filenames", pokeball_translate, exclusions=None, has_animation=True, save_path=SAVE_PATHS["POKEBALL"], config_dict=bulba_scrape_config)


def pokeball_translate(my_filename, pokeball_info):
    bulba_filename = ""
    pokeball_name = get_pokeball_name(pokeball_info[0])
    img_type_name = get_pokeball_img_type_name(pokeball_info[1])

    if pokeball_name == "Poke Ball" and img_type_name != "Drawn": pokeball_name = pokeball_name.replace("e", "\u00e9")
    # NOTE: Hisuian pokeballs do not get any bulba denotion for bag sprites (so poke ball and hisuian poke ball are formatted the same), just that they are the only ones to exist in LA & HOME bag sprites...
    if "-Hisui" in pokeball_name and any(types in img_type_name for types in ("Bag", "LA")): pokeball_name = pokeball_name.replace("-Hisui", "")
    
    if "Bag" in img_type_name:
        bag_platform = get_bulba_translated_pokeball_info(img_type_name)
        bulba_filename = f"Bag {pokeball_name}{bag_platform} Sprite.png"
    elif img_type_name == "PGL":
        bulba_filename = f"Dream {pokeball_name} Sprite.png"
    elif img_type_name == "Drawn":
        no_space_ball_name = pokeball_name.replace(" ", "")
        bulba_filename = f"Sugimori{no_space_ball_name}.png"
    elif "-Hisui" in pokeball_name and "HOME" in img_type_name:
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
        return (EXCLUDE_TRANSLATIONS_MAP["NIM"])