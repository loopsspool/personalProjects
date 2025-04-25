import requests # To retrieve webpages
from bs4 import BeautifulSoup   # To parse webpages
import urllib   # For downloading those images to my computer
import re   # For filtering what images to download
import os

from json_utils import *
from db_utils import get_missing_game_imgs_by_poke
from bulba_mapping_data import *
# from app_globals import *
# from image_tools import *
# from bulba_translators import potentially_adapt_game_in_filename

# TODO: Maybe keep track of images on a page that are downloaded and if another matches a pattern have an alt for it? (see primal kyogre gen6ORAS and gen7SM)


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
# https://archives.bulbagarden.net/wiki/Category:Pok%C3%A9mon_artwork


# def get_poke_game_img_urls(force=False):
#     if force or not os.path.exists(POKE_URL_JSON_PATH):
#         pokemon_starter_page = requests.get("")
#         pokemon_starter_page_soup = BeautifulSoup(pokemon_starter_page.content, 'html.parser')
#         curr_page_soup = pokemon_starter_page_soup
#         poke_img_urls = {}

#         while curr_page_soup:
#             print("Reading page of pokemon game archive links...")
#             poke_img_urls.update(get_all_urls_on_page(curr_page_soup))
#             curr_page_soup = get_next_page_soup(curr_page_soup)

#         print("Saving to json...")
#         save_json(poke_img_urls, POKE_URL_JSON_PATH)
        
        
# # TODO: Rewrite to get specific image url
# def get_all_urls_on_page(curr_page_soup):
#     page_urls = {}
#     for list_div in curr_page_soup.find_all('div', {'class': 'mw-category-group'}):
#         for poke in list_div.find_all('li'):
#             # Skipping specific artwork I don't want
#             if poke.a.get('href') == "/wiki/Category:Ken_Sugimori_Pok%C3%A9mon_artwork" or poke.a.get('href') == "/wiki/Category:Official_Pok%C3%A9mon_artwork":
#                 continue
#             poke_name = cleanse_text(poke.a.text)
#             poke_url = BULBA_ARCHIVES_STARTER_URL + poke.a.get('href')
#             page_urls[poke_name] = poke_url
#     return page_urls


# def cleanse_text(txt):
#     # These are predetermined naming structures defined in the pokemon info spreadsheet
#     if "\u2640" in txt: return txt.replace("\u2640", " f")  # For 29, Nidoran f
#     if "\u2642" in txt: return txt.replace("\u2642", " m")  # For 32, Nidoran m
#     if "\u00e9" in txt: return txt.replace("\u00e9", "e")   # For 669, Flabebe
#     return txt

    
def get_next_page_soup(curr_page_soup):
    try:
        next_page_url = curr_page_soup.find('a', string='next page').get('href')
        next_page = requests.get(BULBA_ARCHIVES_STARTER_URL + next_page_url)
        next_page_soup = BeautifulSoup(next_page.content, 'html.parser')
        return next_page_soup
    except:
        return None


def scrape(force=False):
    # get_poke_game_img_urls(force)
    # print("Reading JSON...")
    # poke_urls = load_json(POKE_URL_JSON_PATH)
    missing_imgs_dict = get_missing_game_imgs_by_poke()
    
    # TODO: This shouldnt be needed anymore to access image directly, change to looping thru poke
    for poke_num, missing_imgs in missing_imgs_dict.items():
        if len(missing_imgs)==0: continue
        for missing_img in missing_imgs:
            bulba_game_sprite_filename = bulba_game_sprite_translate(missing_img)
            print(bulba_game_sprite_filename)


    # TODO: If wanting to use this, will need to factor in filtering of Game, GO, Home, Menu, etc  
    # Translate to bulba filenames (Don't forget to translate game denoters for back underscore)
    # try to go to image page and download
    # Game Sprites
    # Drawn
    # Home
    # Home menu sprites ONLY
    # Any others?
    # NOTE: Maybe best to run to update db and spreadsheet after this finishes
        # If I do it inline, it'll be hard to populate substitutes
        # I guess I could write a function to do so, think about it
        # *** If crashes, db wont be updated and this'll download them again
            # AT VERY LEAST have update function for db get called before running this

scrape()


def bulba_game_sprite_translate(filename):
    # Starting bulba filename w their format
    bulba_filename = "Spr "
    is_back_sprite = False
    # Adding bulbapedia format of back, gen, and game
    for game, bulba_v_game in BULBA_GAME_MAP.items():
        if "-Back" in filename:
            is_back_sprite = True
            game = game.replace(" ", "_")
        if game in filename:
            if is_back_sprite: bulba_filename += "b "
            bulba_filename += bulba_v_game + " "
    # Adding poke num (TODO: always 3 digits total with leading zeros unless 4 digits used? check)
    poke_num = str(int(filename[:4])).zfill(3)  # Converting from 4 total digits to 3
    bulba_filename += poke_num
    # Then Mega
    # Then Regions
    # Then Forms
    # Then Giganta (After forms for Urshifu)
    # TODO: if has f form, denote f or m for sprite (if after gen4)... may need to join some tables in SQL
        # Add space before
        # After Regions for Hisuian Sneasel
    # Then shiny

    # Dont forget to factor in the underscore in gen/game if its a back sprite
    # Include searching for -f and shiny here, must be last after reference_date
    # If has a female counterpart, MAY have " m"


# Drawn images
# TODO: 
# Add exclusions (Arceus, Silvally, probably Alcremie) -- and what to do (dream forms, nothing?)
# Check all forms, see if exceptions



# TODO: Uncomment download function
def ani_check_and_download(img, filename):
    dl_destination = ""
    if "-Back" in filename and ("Gen1" in filename or "Gen2" in filename or "Gen3" in filename or "Gen4" in filename):
        dl_destination = gen1_thru_4_backs_save_path

    # TODO: Put the opener retrieve inside of a lock loop... that's why you get errors most often
        # Trying to access the image too much in a short window (see stackoverflow)
    file_ext = img.img['alt'][-4:]
    save_name = filename + file_ext
    if "-Animated" in save_name:
        # TODO: Original filetype is preferred for color retention
        dl_destination = game_save_path + "animated_pngs_for_gifs\\pngs\\"
        if not os.path.exists(dl_destination + save_name):
            # NOTE: Keep this AFTER exist check, makes it run way quicker for skipping images
            img = get_largest_png(img)
            if is_animated(img):
                #download_img(img, filename, save_name, dl_destination)
                # Returning downloaded boolean
                return True
            else:
                print(save_name, " was not animated... Skipped")
                return False
        else:
            print(save_name, " already exists")
            return False
    else:
        # Don't override the gen1 thru 4 save path if that's present
        if not dl_destination == gen1_thru_4_backs_save_path:
            dl_destination = game_save_path + "initial_downloads_for_border_removal\\"
        if not os.path.exists(dl_destination + save_name):
            # NOTE: Keep this AFTER exist check, makes it run way quicker for skipping images
            img = get_largest_png(img)
            # Making sure its NOT animated
            if not is_animated(img):
                #download_img(img, filename, save_name, dl_destination)
                # Returning downloaded boolean
                return True
            # If it is animated, save it anyways to take first frame for missing still
            else:
                if not os.path.exists(dl_destination + "TO_BE_CONVERTED_TO_STILL_" + save_name):
                    # If it is animated, still download it with an obvious denoter to convert it to a static
                    # TODO: Make sure concat the string is valid
                    #download_img(img, filename, save_name, dl_destination + "TO_BE_CONVERTED_TO_STILL_")
                    # Returning downloaded boolean
                    return True
                else:
                    print(save_name, " already exists")
                    return False
        else:
            print(save_name, " already exists")
            return False
        
def download_img(img, filename, save_name, dl_destination):
    print("Downloading ", save_name)
    filename, headers = opener.retrieve(img, dl_destination + save_name)
    print(save_name, img)
        
# TODO: Have this factor in poke_start and to go after
# Have to wait for JSON implementation since this parses pokemon_img_urls
def scrape_game_imgs():
    # NOTE: Before running, uncomment all filename, headers = opener.retrieve(get_largest_png(img), gen8_menu_sprite_save_path + save_name)
    imgs_downloaded = 0
    imgs_still_missing = []
    pokemon_not_reached_yet = True
    poke_acc = 0
    print("Processing game sprite images...")
    
    for i in range(len(pokemon_img_urls)):
        # Getting relevant pokemon data
        pokemon = pokedex[i]
        missing_imgs = pokemon.missing_imgs
        missing_gen1_thru_gen4_back_imgs = pokemon.missing_gen1_thru_gen4_back_imgs
        # TODO: Add that if the above are zero AND THERE ARE NO MISSING DRAWN IMAGES, continue to not go into each page
        # Or break out the drawn images from this function

        # TODO: Add small images array when added?
        print(pokemon.name, " has ", len(missing_imgs) + len(missing_gen1_thru_gen4_back_imgs), " missing images...")
        # Fixing a bulba error here that adds a hyphen between unown number and form in gen4
        # NOTE: This would probably make more sense to add to where I put the missing imgs in the array, but I'm not touching this hahaha
        if pokemon.name == "Unown":
            for img in missing_imgs:
                if "Gen4" in img[0]:
                    img = (img[0], img[1].replace(" 201", " 201-"))
            for img in missing_gen1_thru_gen4_back_imgs:
                if "Gen4" in img[0]:
                    img = (img[0], img[1].replace(" 201", " 201-"))

        for img in missing_gen1_thru_gen4_back_imgs:
            print(img)
        # Getting pokemon archived image page information
        curr_page = requests.get(BULBA_ARCHIVES_STARTER_URL + pokemon_img_urls[i])
        curr_page_soup = BeautifulSoup(curr_page.content, 'html.parser')

        theres_a_next_page = True
        theres_more_imgs = True
        while (theres_a_next_page and theres_more_imgs):
            # Thumbs here refers to thumbnails FYI
            thumbs = curr_page_soup.find_all('div', 'thumb')
            thumb_text = []
            thumb_text_wo_file_ext = []
            missing_imgs_that_exist = []

            # Getting just the caption for each of the thumbnails
            for thumb in thumbs:
                caption = thumb.img['alt']
                # Change 5b to 5b2 and 6x to 6o if needed to grab those sprites
                caption = potentially_adapt_game_in_filename(caption)
                thumb_text.append(caption)
                thumb_text_wo_file_ext.append(caption[:len(caption)-4])

            # This should never happen, but in case it does the pokemon images will not get downloaded incorrectly
            if len(thumb_text_wo_file_ext) != len(thumbs):
                print("Captions array length not equal to image array length")
                break

            # Breaking the while loop if there's no sprite images on the page
            for txt in thumb_text_wo_file_ext:
                if txt.startswith("Spr"):
                    theres_more_imgs = True
                    break
                theres_more_imgs = False
            if not theres_more_imgs:
                print("No sprite files on this page. Moving to next pokemon...")
                break

            # TODO: Will have to go in its own file to scrape, circular imports if I do it here
            # Will pull a little more requests but really shouldn't be bad with proper tracking and stashed urls via JSON
            # Getting Drawn images
            # Keep this here before the break for missing sprites so I can still get the drawn images even if there's no missing sprites
            #for i, caption in enumerate(thumb_text):
            #    if re.search("^\d\d\d[a-zA-Z]", caption) != None:
            #        get_drawn_images(pokemon, thumbs[i])

            # Breaking the while loop if the pokemon already has all it's images
            if len(missing_imgs) == 0 and len(missing_gen1_thru_gen4_back_imgs) == 0:
                theres_more_imgs = False
                print("No missing images for this pokemon. Continuing to next pokemon...")
                break

            # Getting missing images
            for missing in missing_imgs:
                if missing[1] in thumb_text_wo_file_ext:
                    thumb_index = thumb_text_wo_file_ext.index(missing[1])
                    missing_imgs_that_exist.append((thumbs[thumb_index], missing[0]))
                else:
                    if not missing in imgs_still_missing:
                        imgs_still_missing.append(missing)
            
            # Getting missing back images
            for missing_back in missing_gen1_thru_gen4_back_imgs:
                if missing_back[1] in thumb_text_wo_file_ext:
                    thumb_index = thumb_text_wo_file_ext.index(missing_back[1])
                    missing_imgs_that_exist.append((thumbs[thumb_index], missing_back[0]))
                else:
                    if missing_back not in imgs_still_missing:
                        imgs_still_missing.append(missing_back)

            # Actually downloading and tracking counts
            # A bit misleading with the "existing image" name because I have to check for animation first
            for existing_img in missing_imgs_that_exist:
                downloaded = ani_check_and_download(existing_img[0], existing_img[1])
                if downloaded:
                    imgs_downloaded += 1
                if not downloaded:
                    imgs_still_missing.append(existing_img[1])

            # Moving on to the next page
            try:
                next_page_url = curr_page_soup.find('a', string='next page').get('href')
                next_page = requests.get(BULBA_ARCHIVES_STARTER_URL + next_page_url)
                next_page_soup = BeautifulSoup(next_page.content, 'html.parser')
                curr_page_soup = next_page_soup
                theres_a_next_page = True
                print("Reading next page of ", pokemon.name, " archive links...")
            # Unless the end of the next pages is reached
            except:
                theres_a_next_page = False
                print("Reached end of ", pokemon.name, " archive links.")
                break


    for i in imgs_still_missing:
        print(i)
    print (imgs_downloaded,  " images downloaded")
    print (len(imgs_still_missing),  " images still missing (see above)")