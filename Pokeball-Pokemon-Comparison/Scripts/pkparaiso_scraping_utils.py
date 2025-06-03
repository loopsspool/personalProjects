import requests
from bs4 import BeautifulSoup

from app_globals import save_directories
from scraping_utils import *

# NOTE: For all other relevant sources, pkparaiso has a downloadable zip... Except these (Gen8 SwSh Animated Back Sprites (Both Shiny and regular))
SCRAPING_PAGE = "https://www.pkparaiso.com/espada_escudo/sprites_pokemon_espalda.php"
PKPARAISO_STARTER_URL = "https://www.pkparaiso.com"




# TODO: .......... It appears I have most of these already? Scrape page anyways and translate to see if I'm missing any (do a db search via game id, sprite id, poke id, etc)
def pkparaiso_scrape_swsh_ani_back_sprites(allow_download=False):
    # NOTE: Passing in empty string as starter url so pkparaiso_translate can return full url as "filename translation"
    pkparaiso_scrape_config = generate_config_dict("", pkparaiso_get_img, allow_download)

    # -1 for poke_num since this is only scaping one page of predetermined game, sprite types, and pokes. Meant to be run once in full.
    scrape_imgs(-1, "obtainable_game_filenames", pkparaiso_translate, exclusions=None, has_animation=True, save_path=save_directories["Game Sprites"]["path"], config_dict=pkparaiso_scrape_config)




#|================================================================================================|
#|~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~[     DOWNLOADING FUNCTIONS     ]~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~|
#|================================================================================================|

def pkparaiso_get_img(url, save_path, allow_download, has_animation=False):
    my_filename = save_path.split("\\")[-1]

    img_page_soup = img_exists_at_url(url)
    if not img_page_soup:
        print_couldnt_dl_msg(my_filename)
        return ()
    else:
        if allow_download:
            # TODO: Will just be grabbing link from item on page
            #img_url = bulba_get_largest_png(img_page_soup)

            # TODO: Put this into a func in scraping_utils and change it in bulba & wikidex scraping_utils
            if has_animation:
                determine_animation_status_before_downloading(img_url, save_path)
            else:
                download_img(img_url, save_path)




#|================================================================================================|
#|~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~[     TRANSLATIONS     ]~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~|
#|================================================================================================|

# TODO: Implement the below
# First looks through pkparaiso translate dict for passed poke_name
# If not in dict, return None -- causing file to be skipped for download
# Then check my_filename is a Gen8 SwSh Back (both shiny/animated optional since contains shinies and stills can be from first frame of gif), if not return None
# Have a global dict mapping poke_name : url
    # Make func for this -- scrapes page, gets caption and url to gif
    # Call at top of file (so accessable by this) if __file__ == main or pkparaiso_scraping_utils (lookup how to do)
# If poke on page (in translate dict) and my_filename is gen8 SwSh back, return url for poke_name (fine to do since made starter url empty string)

def pkparaiso_translate(my_filename, poke_info):
    pass
