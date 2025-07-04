from pokewiki_translation_mapping import *
from db_utils import get_poke_name, get_form_name, get_pokeball_name, get_pokeball_img_type_name, get_all_form_names_for_poke
from app_globals import *
from scraping_utils import *
from image_utils import pokewiki_get_largest_img
from translation_utils import *




# WEB DATA
#sprite_page = requests.get("https://www.pokewiki.de/Kategorie:Pok%C3%A9monsprite")
POKEWIKI_STARTER_URL = "https://www.pokewiki.de/Datei:"


def pokewiki_scrape_pokemon(poke_num, allow_download=False):
    pokewiki_scrape_config = generate_config_dict(POKEWIKI_STARTER_URL, pokewiki_get_img, allow_download)
    headers["Referer"] = "https://www.pokewiki.de/"
    # headers["Accept"] = "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7"

    scrape_imgs(poke_num, "obtainable_game_filenames", pokewiki_translate, exclusions=pokewiki_doesnt_have_images_for, has_animation=True, save_path=save_directories["Game Sprites"]["path"], config_dict=pokewiki_scrape_config)
    scrape_imgs(poke_num, "obtainable_home_filenames", pokewiki_translate, exclusions=pokewiki_doesnt_have_images_for, has_animation=True, save_path=save_directories["HOME"]["path"], config_dict=pokewiki_scrape_config)
    scrape_imgs(poke_num, "bank_filenames", pokewiki_translate, exclusions=None, has_animation=False, save_path=save_directories["BANK"]["path"], config_dict=pokewiki_scrape_config)




#|================================================================================================|
#|~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~[     DOWNLOADING FUNCTIONS     ]~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~|
#|================================================================================================|

def pokewiki_get_img(url, save_path, allow_download, has_animation=False):
    my_filename = save_path.split("\\")[-1]
    img_page_soup = img_exists_at_url(url)
    
    if not img_page_soup:
        print_couldnt_dl_msg(my_filename)
        return ()
    else:
        if allow_download:
            img_url = pokewiki_get_largest_img(img_page_soup)
            determine_animation_status_before_downloading(img_url, save_path)
    

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
    for universal_form, translation in UNIVERSAL_FORMS_EXCLUDING_REGIONALS.items():
        if universal_form == form_name:
            return True, translation
    
    is_regional_form, translation = determine_regional_form_translation(poke_num, form_name)
    if is_regional_form:
        return True, translation

    return False, None


def determine_regional_form_translation(poke_num, form_name):
    # Regional forms in pokewiki are marked the same as species forms -- a, b, c, d, etc.
    # This checks if a form is ONLY a regional form (so Hisuian Female Sneasel doesnt go into this, nor galarian zen/standard darmanitan, etc)
    # And if the only forms that pokemon has are regional forms and ones that have their own non-form denoter (females, megas, etc)
    # If so, return the appropriate chronological denoter for that regional form (whichever region released first, will be sooner in alphabet)
    # This saves me from writing every regional form for every applicable poke in the translation dict
    if form_name in REGIONAL_FORMS:
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
            
    return False, None




#|================================================================================================|
#|~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~[     GAME & HOME IMAGES     ]~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~|
#|================================================================================================|

def pokewiki_translate(my_filename, poke_info):
    # poke_info == (poke_num, form_id)
    poke_num_int = poke_info[0]
    poke_num_leading_zeros = str(poke_num_int).zfill(3)   # Pokewiki only uses leading zeros up to 3
    form_name = get_form_name(poke_info[1])
    
    translated_form = get_pokewiki_translated_form(poke_info, my_filename)
    form_tag = translated_form if translated_form != "" else ""
    female_tag = determine_female_tag(poke_num_int, form_name)
    back_tag = " Rückseite" if "-Back" in my_filename else ""
    shiny_tag = " Schillernd" if "-Shiny" in my_filename else ""
    platform = determine_platform_tag(my_filename)
    file_ext = ".png" if "-Animated" not in my_filename else ".gif"

    pokewiki_filename = f"Pokémonsprite {poke_num_leading_zeros}{form_tag}{female_tag}{back_tag}{shiny_tag}{platform}{file_ext}"
    return (pokewiki_filename)


def determine_female_tag(poke_num, form_name):
    # For some reason in pokewiki, if poke was introduced gen4 or before, its noted as female. Gen5+ its noted as <poke_num>a (like another form)...
    if "-f" in form_name:
        if poke_num < 494: return (" Weiblich")
        else: return ("a")
    else: 
        return ("")


def determine_platform_tag(my_filename):
    if " HOME" in my_filename: return (" HOME")
    elif " BANK" in my_filename: return (" Bank")
    else: return(get_translated_game(my_filename, POKEWIKI_GAME_MAP, POKEWIKI_ALT_GAME_MAP))