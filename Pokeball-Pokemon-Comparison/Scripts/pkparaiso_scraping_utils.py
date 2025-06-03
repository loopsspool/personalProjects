from app_globals import save_directories
from scraping_utils import *

# NOTE: For all other relevant sources, pkparaiso has a downloadable zip... Except these
SCRAPING_PAGE = "https://www.pkparaiso.com/espada_escudo/sprites_pokemon_espalda.php"
PKPARAISO_STARTER_URL = "https://www.pkparaiso.com"


def pkparaiso_scrape_swsh_ani_back_sprites(allow_download=False):
    wikidex_scrape_config = generate_config_dict(PKPARAISO_STARTER_URL, pkparaiso_get_img, allow_download)

    # -1 for poke_num since this is only scaping one page of predetermined game, sprite types, and pokes. Meant to be run once in full.
    scrape_imgs(-1, "obtainable_game_filenames", pkparaiso_translate, exclusions=None, has_animation=True, save_path=save_directories["Game Sprites"]["path"], config_dict=wikidex_scrape_config)




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

            if has_animation:
                determine_animation_status_before_downloading(img_url, save_path)
            else:
                download_img(img_url, save_path)




#|================================================================================================|
#|~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~[     TRANSLATIONS     ]~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~|
#|================================================================================================|

# As opposed to other web scrapers, instead of crafting the site filename after my filename, I will be discovering my filename from the site filename
# This is due to a relatively small pool of pokemon (thus forms), knowing the game and sprite type, and having to cycle through a single page instead of generating urls
def pkparaiso_translate(pkp_filename):
    pass
