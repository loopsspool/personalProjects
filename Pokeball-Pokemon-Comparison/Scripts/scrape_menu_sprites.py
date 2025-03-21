import requests # To retrieve webpages
from bs4 import BeautifulSoup   # To parse webpages
import re   # For filtering what images to download
import os   # For downloading those images to my computer
from globals import *

def get_menu_sprites():
    print("Getting Menu Sprites...")

    ms_end_urls = ["Generation_VI_menu_sprites", "Generation_VIII_menu_sprites"]
    for end_url in ms_end_urls:
        ms_page = requests.get("https://archives.bulbagarden.net/wiki/Category:" + end_url, headers={'User-Agent': 'Mozilla/5.0'})
        curr_ms_page_soup = BeautifulSoup(ms_page.content, 'html.parser')
        theres_a_next_page = True
        while (theres_a_next_page):
            pokemon_imgs = curr_ms_page_soup.find_all('img')
            # Downloading certain images
            for img in pokemon_imgs:
                img_text = img.attrs['alt']
                # If image doesn't match pokemon number + menu sprite + gen formula, don't bother
                if not re.search("\d\d\dMS\d", img_text):
                    continue
                poke_num = img_text[:3]
                poke_name = pokedex[int(poke_num) - 1].name
                file_ext = img_text[len(img_text) - 4:]
                # The zfill adds leading zeros
                save_name = str(poke_num).zfill(3) + ' ' + poke_name + file_ext

                if end_url == "Generation_VI_menu_sprites" and not os.path.exists(gen6_menu_sprite_save_path + save_name):
                    print("Downloading Gen6 menu sprite for ", poke_num, " ", poke_name)
                    #filename, headers = opener.retrieve(get_largest_png(img), gen6_menu_sprite_save_path + save_name)
                if end_url == "Generation_VIII_menu_sprites" and not os.path.exists(gen8_menu_sprite_save_path + save_name):
                    print("Downloading Gen8 menu sprite for ", poke_num, " ", poke_name)
                    #filename, headers = opener.retrieve(get_largest_png(img), gen8_menu_sprite_save_path + save_name)
            
            try:
                next_page_url = curr_ms_page_soup.find('a', string='next page').get('href')
                next_page = requests.get("https://archives.bulbagarden.net/" + next_page_url)
                next_page_soup = BeautifulSoup(next_page.content, 'html.parser')
                curr_ms_page_soup = next_page_soup
                theres_a_next_page = True
                print("Reading next page of menu sprite archive links...")
            # Unless the end of the next pages is reached
            except:
                theres_a_next_page = False
                print("Reached end of menu sprite archive links.")