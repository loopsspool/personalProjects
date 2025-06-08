from pokewiki_translation_mapping import *
from db_utils import get_poke_name, get_form_name, get_pokeball_name, get_pokeball_img_type_name
from app_globals import *
from scraping_utils import *
from image_utils import pokewiki_get_largest_img
from translation_utils import *


# WEB DATA
#sprite_page = requests.get("https://www.pokewiki.de/Kategorie:Pok%C3%A9monsprite")
POKEWIKI_STARTER_URL = "https://www.pokewiki.de/Datei:"


def pokewiki_scrape_pokemon(poke_num, allow_download=False):
    pokewiki_scrape_config = generate_config_dict(POKEWIKI_STARTER_URL, pokewiki_get_img, allow_download)

    scrape_imgs(poke_num, "obtainable_game_filenames", pokewiki_translate, exclusions=pokewiki_doesnt_have_images_for, has_animation=True, save_path=save_directories["Game Sprites"]["path"], config_dict=pokewiki_scrape_config)
    scrape_imgs(poke_num, "obtainable_home_filenames", pokewiki_translate, exclusions=None, has_animation=True, save_path=save_directories["HOME"]["path"], config_dict=pokewiki_scrape_config)




#|================================================================================================|
#|~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~[     DOWNLOADING FUNCTIONS     ]~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~|
#|================================================================================================|

def pokewiki_get_img(url, save_path, allow_download, has_animation=False):
    my_filename = save_path.split("\\")[-1]
    img_page_soup = img_exists_at_url(url)
    
    if allow_download:
        # TODO: Implement pokewiki get largest
        # file w only 1 size: https://www.pokewiki.de/Datei:Pok%C3%A9monsprite_1016_Schillernd_HOME.png
        # file w different sizes: https://www.pokewiki.de/Datei:Pok%C3%A9monsprite_1016_Schillernd_KAPU.gif
        img_url = pokewiki_get_largest_img(img_page_soup)

        # TODO: Put this into a func in scraping_utils and change it in bulba & wikidex scraping_utils
        if has_animation:
            determine_animation_status_before_downloading(img_url, save_path)
        else:
            download_img(img_url, save_path)
    

def pokewiki_doesnt_have_images_for(my_filename):
    for exclude in POKEWIKI_DOESNT_HAVE_IMGS_FOR.values():
        if exclude(my_filename):
            return True
    return False




#|================================================================================================|
#|~~~~~~~~~~~~~~~~~~~~~~~~~~~~~[     UNIVERSAL TRANSLATIONS     ]~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~|
#|================================================================================================|

# NOTE: This can be made a universal func that all single dimension (Not different HOME, Game, Menu, etc keys in  translation dict) translation dict call from in translation_utils.py, just keeping it here so its easier to refer back to to understand whats happening
def get_pokewiki_translated_species_form(poke_info, my_filename):
    poke_num = poke_info[0]
    form_id = poke_info[1]
    form_name = get_form_name(form_id)

    # No widespread universal forms combined with species forms, the few exceptions have their own form id/name associated with it
    if form_name in UNIVERSAL_FORMS:
        return("")

    if poke_num in POKEWIKI_POKE_FORM_TRANSLATION_MAP:
        for form, translation in POKEWIKI_POKE_FORM_TRANSLATION_MAP[poke_num].items():
            if form in form_name:
                return(translation)
    
    print(f"Couldn't search for image to download... No respective form in map set for \t{my_filename}")
    return(EXCLUDE_TRANSLATIONS_MAP["NIM"])




#|================================================================================================|
#|~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~[     GAME & HOME IMAGES     ]~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~|
#|================================================================================================|

def pokewiki_translate(my_filename, poke_info):
    # poke_info == (poke_num, form_id)
    poke_num_int = poke_info[0]
    poke_num_leading_zeros = f" {str(poke_num_int).zfill(3)}"   # Pokewiki only uses leading zeros up to 3
    form_name = get_form_name(poke_info[1])
    
    # TODO: Will need to rethink universal forms for pokewiki... Default always "", next form (say galarian) "a", next form (say alolan) "b", "c", etc. -- Dynamic denoters not static
    translated_form = get_pokewiki_translated_species_form(poke_info, my_filename)
    form_tag = f" {translated_form}" if translated_form != "" else ""
    gigantamax_tag = determine_gigantamax_tag(poke_num_int, form_name)
    female_tag = " Weiblich" if "-f" in form_name else ""
    back_tag = " Rückseite" if "-Back" in my_filename else ""
    shiny_tag = " Schillernd" if "-Shiny" in my_filename else ""
    platform = get_translated_game(my_filename, POKEWIKI_GAME_MAP) if "HOME" not in my_filename else " HOME"
    file_ext = ".png" if "-Animated" not in my_filename else ".gif"

    pokewiki_filename = f"Pokémonsprite {poke_num_leading_zeros}{form_tag}{gigantamax_tag}{female_tag}{back_tag}{shiny_tag}{platform}{file_ext}"
    return (pokewiki_filename)


def determine_gigantamax_tag(poke_num, form_name):
    gmax_denoter = ""
    if "-Gigantamax" in form_name:
        if poke_num == 892 and "-Form_Rapid_Strike" in form_name:   # Urshifu has different form gigantamaxes
            gmax_denoter = "g2"
        else:
            gmax_denoter = "g1"

    return gmax_denoter