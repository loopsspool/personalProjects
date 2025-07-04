from wikidex_translation_mapping import *
from db_utils import get_poke_name, get_form_name, get_costume_name
from app_globals import *
from scraping_utils import *
from image_utils import wikidex_get_largest_img
from translation_utils import *


# WEB DATA
#sprite_page = requests.get("https://www.wikidex.net/wiki/Categor%C3%ADa:Sprites_de_Pok%C3%A9mon")
WIKIDEX_STARTER_URL = "https://www.wikidex.net/wiki/Archivo:"


def wikidex_scrape_pokemon(poke_num, allow_download=False):
    wikidex_scrape_config = generate_config_dict(WIKIDEX_STARTER_URL, wikidex_get_img, allow_download)

    # Game filenames now from Pokewiki
    # HOME CAN come from here, but prefer Root on X
    #scrape_imgs(poke_num, "obtainable_game_filenames", wikidex_game_translate, exclusions=wikidex_doesnt_have_images_for, has_animation=True, save_path=save_directories["Game Sprites"]["path"], config_dict=wikidex_scrape_config)
    #scrape_imgs(poke_num, "obtainable_home_filenames", wikidex_game_translate, exclusions=None, has_animation=True, save_path=save_directories["HOME"]["path"], config_dict=wikidex_scrape_config)
    scrape_imgs(poke_num, "obtainable_go_filenames", wikidex_go_translate, exclusions=None, has_animation=False, save_path=save_directories["GO"]["path"], config_dict=wikidex_scrape_config)




#|================================================================================================|
#|~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~[     DOWNLOADING FUNCTIONS     ]~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~|
#|================================================================================================|

def wikidex_get_img(url, save_path, allow_download, has_animation=False):
    my_filename = save_path.split("\\")[-1]
    img_page_soup, my_filename_w_wikidex_file_ext = search_image_under_all_file_extensions(url, my_filename)

    if not img_page_soup:
        print_couldnt_dl_msg(my_filename)
        return
    else:
        # TODO: Once everything is webp this wont be necessary as my filename will always be a webp
        save_path = save_path.replace(my_filename, my_filename_w_wikidex_file_ext)
    
    if allow_download:
        img_url = wikidex_get_largest_img(img_page_soup)

        # TODO: After implementing webm -> webp conversion, can implement this if want to save gif/webm
        # Can't do now bc db wont recognize it as existing in these filepaths so will continuously try to download images    
        #save_path = os.path.join(determine_save_path_from_file_type(img_url_file_ext), my_filename)

        determine_animation_status_before_downloading(img_url, save_path)


def search_image_under_all_file_extensions(url, my_filename):
    file_exts_wikidex_uses = [".png", ".gif"]  # Ordered in terms of preference (png for stills, gif for transparency, webm bc its there) -- NO LONGER SCRAPING WEBM

    # Rotating through file extensions to find an existing image
    for file_ext in file_exts_wikidex_uses:
        if "-Animated" in my_filename and file_ext == ".png": continue  # pngs for stills only
        if " HOME" in my_filename and file_ext != ".webm": continue     # HOME sprites always webm (w/o transparency) -- No longer scraping
        # Replacing file extension
        if file_ext not in url: url = url.replace(get_file_ext(url), file_ext)
        # Seeing if the URL exists
        img_page_soup = img_exists_at_url(url)
        # If so, return relevant data, otherwise try next file extension
        if img_page_soup: 
            my_filename_proper_ext = my_filename.replace(get_file_ext(my_filename), file_ext)
            return img_page_soup, my_filename_proper_ext

    # Img doesnt exist under any file extensions
    return None, None
    

def wikidex_doesnt_have_images_for(my_filename):
    for exclude in WIKIDEX_DOESNT_HAVE_IMGS_FOR.values():
        if exclude(my_filename):
            return True
    return False




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
    
    # This adjusts some form names that differ in GO (namely empty for games, but in GO they have a denoter)
    if " GO" in my_filename:
        if poke_num in GO_FORM_TRANSLATION_EXCEPTIONS:
            if form_name in GO_FORM_TRANSLATION_EXCEPTIONS[poke_num]:
                return GO_FORM_TRANSLATION_EXCEPTIONS[poke_num][form_name]

    if poke_num in WIKIDEX_POKE_FORM_TRANSLATION_MAP:
        for form, translation in WIKIDEX_POKE_FORM_TRANSLATION_MAP[poke_num].items():
            if form in form_name:
                return(translation)
    
    print(f"Couldn't search for image to download... No respective form in map set for \t{my_filename}")
    return(EXCLUDE_TRANSLATIONS_MAP["NIM"])


def get_wikidex_translated_costume(poke_info, costume_name, my_filename):
    poke_num = poke_info[0]

    if costume_name == "None": return ""
    # These pokes have the same costume name as others, but its denoted differently in wikidex
    if poke_num in GO_COSTUME_TRANSLATION_EXCEPTIONS:
        if costume_name in GO_COSTUME_TRANSLATION_EXCEPTIONS[poke_num]:
            return GO_COSTUME_TRANSLATION_EXCEPTIONS[poke_num][costume_name]
        
    if costume_name in GO_COSTUME_TRANSLATIONS_MAP:
        return GO_COSTUME_TRANSLATIONS_MAP[costume_name]
    
    print(f"Couldn't search for image to download... No respective form in map set for \t{my_filename}")
    return(EXCLUDE_TRANSLATIONS_MAP["NIM"])





#|================================================================================================|
#|~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~[     GAME IMAGES     ]~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~|
#|================================================================================================|

def wikidex_game_translate(my_filename, poke_info):
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
    if file_ext == ".webm": return None     # No longer scraping webm

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
    if "-Animated" not in my_filename: return ".png"
    # Wikidex transitioned to .webm for animated HOME/Gen9. Gen8 below is .gif
    # HOME always webm, Gen9 has a lot of gifs, so will try that first. If it doesn't exist it will search for a webm in wikidex_get_img
    else:
        if " HOME" in my_filename: return ".webm"
        else: return ".gif"




#|================================================================================================|
#|~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~[     GO IMAGES     ]~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~|
#|================================================================================================|

def wikidex_go_translate(my_filename, poke_info):
    # poke_info == (poke_num, form_id, costume_id)
    poke_num = poke_info[0]
    poke_name = get_poke_name(poke_num)
    form_name = get_form_name(poke_info[1])
    costume_name = get_costume_name(poke_info[2])

    translated_costume = get_wikidex_translated_costume(poke_info, costume_name, my_filename)
    translated_form = get_wikidex_translated_species_form(poke_info, my_filename)
    adj_poke_name = adjust_poke_name(poke_name, form_name)
    if poke_name == "Spinda": adj_poke_name += " 9"  # Spinda has predetermined forms in GO, I'm just selecting one here for use

    costume_tag = f" {translated_costume}" if translated_costume != "" else ""
    form_tag = f" {translated_form}" if translated_form != "" else ""
    gigantamax_tag = " Gigamax" if "-Gigantamax" in form_name else ""
    female_tag = " hembra" if "-f" in form_name else ""
    shiny_tag = " variocolor" if "-Shiny" in my_filename else ""

    wikidex_filename = f"{adj_poke_name}{form_tag}{gigantamax_tag}{costume_tag} GO{female_tag}{shiny_tag}.png"
    return (wikidex_filename)