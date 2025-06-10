from pokewiki_translation_mapping import *
from db_utils import get_poke_name, get_form_name, get_pokeball_name, get_pokeball_img_type_name, get_all_form_names_for_poke
from app_globals import *
from scraping_utils import *
#from image_utils import pokewiki_get_largest_img
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

def get_pokewiki_translated_form(poke_info, my_filename):
    poke_num = poke_info[0]
    form_id = poke_info[1]
    form_name = get_form_name(form_id)
    
    has_universal_form, universal_form_translation = get_pokewiki_universal_form(poke_num, form_name)
    # No widespread universal forms combined with species forms, the few exceptions have their own form id/name associated with it
    if has_universal_form: return universal_form_translation

    # --------  SPECIES FORMS  --------
    if poke_num in POKEWIKI_POKE_FORM_TRANSLATION_MAP:
        for form, translation in POKEWIKI_POKE_FORM_TRANSLATION_MAP[poke_num].items():
            if form in form_name:
                return(translation)
    
    print(f"Couldn't search for image to download... No respective form in map set for \t{my_filename}")
    return(EXCLUDE_TRANSLATIONS_MAP["NIM"])


def get_pokewiki_universal_form(poke_num, form_name):
    # Checking equality so any pokes that have a universal paired with another form (ie Hisuian Female Sneasel) will continue so can be denoted for the other form
    if any(universal_form == form_name for universal_form in UNIVERSAL_FORMS_EXCLUDING_REGIONALS):
        return True, ""
    
    # Regional forms in pokewiki are marked the same as species forms -- a, b, c, d, etc.
    # This checks if a form is ONLY a regional form (so Hisuian Female Sneasel doesnt go into this, nor galarian zen/standard darmanitan, etc)
    # And if the only forms that pokemon has are regional forms and ones that have their own non-form denoter (females, megas, etc)
    # If so, return the appropriate chronological denoter for that regional form (whichever region released first, will be sooner in alphabet)
    # This saves me from writing every regional form for every applicable poke in the translation dict
    elif form_name in REGIONAL_FORMS:
        all_forms_for_poke = get_all_form_names_for_poke(poke_num)
        regional_forms_for_poke = [form for form in all_forms_for_poke if "-Region" in form]
        # Checking against UNIVERSAL_FORMS to make sure only forms are Default, Regionals, and ones that have their own non-form denoter and dont affect regionals (mega, female, etc)
        # For example, if burmy had regional forms for his cloaks, we couldn't do this as we wouldn't know which cloak for which region would be labelled a,b,c and so we'd have to include it in our species form dict instead 
        if all(form in UNIVERSAL_FORMS for form in all_forms_for_poke):
            if len(regional_forms_for_poke) == 1: 
                return True, POKEWIKI_FORM_DENOTER["1st Variant"]
            else:
                # For pokes with only regional forms, the pokewiki form denoters (a, b, c, d) necessarily must be chronological
                # This, because say SM released an alolan form, at the release of the game, they would label the sprite with a, since at that time its its only form
                # But if SwSh releases a galarian form for that same poke, it now must be labelled as b since it is the second form
                # The below basically maps chronological order of regional variants applicable to the pokemon to order of pokewiki label denotions (a, b, c, etc)
                chronological_regional_forms_for_poke = sorted(regional_forms_for_poke, key=REGIONAL_FORMS.index)   # Sorts regional forms of poke chronologically by all regional forms
                chronological_regional_form_index = chronological_regional_forms_for_poke.index(form_name)  # Gets chronological index of specific regional form (form_name)
                chronological_regional_form_translated = list(POKEWIKI_FORM_DENOTER.values())[chronological_regional_form_index + 1]   # Getting form denoter, +1 to account for Default form 
                return True, chronological_regional_form_translated
    else:
        return False, None




#|================================================================================================|
#|~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~[     GAME & HOME IMAGES     ]~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~|
#|================================================================================================|

def pokewiki_translate(my_filename, poke_info):
    # poke_info == (poke_num, form_id)
    poke_num_int = poke_info[0]
    poke_num_leading_zeros = f" {str(poke_num_int).zfill(3)}"   # Pokewiki only uses leading zeros up to 3
    form_name = get_form_name(poke_info[1])
    
    # TODO: Will need to rethink universal forms for pokewiki... Default always "", next form (say galarian) "a", next form (say alolan) "b", "c", etc. -- Dynamic denoters not static
    translated_form = get_pokewiki_translated_form(poke_info, my_filename)
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