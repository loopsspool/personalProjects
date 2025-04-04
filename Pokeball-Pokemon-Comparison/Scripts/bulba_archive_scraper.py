# TODO: Are any of these needed in this file?
import requests # To retrieve webpages
from bs4 import BeautifulSoup   # To parse webpages
import re   # For filtering what images to download
import urllib   # For downloading those images to my computer
import os   # For downloading those images to my computer
from PIL import Image   # For converting URL image data to PIL Image object 
import openpyxl     # For reading excel workbook
# Must explicitly state this...
from openpyxl import load_workbook
import string # To access letters easily without having to type them myself in an array
import time

from pokedex_checker import check_pokedex_db_is_current
from drawn_images import get_drawn_images
from menu_sprites import get_menu_sprites
from scraping import get_game_img_urls, scrape_game_imgs


################################# TODO: Complete all TODOs before running... please ########################
# TODO: Add a check function for files spreadsheet to see if generation is complete. 
# If generation not complete, have an optional detailed function that will output what images are missing, so public can contribute (JSON generated by file creating checklist spreadsheet, pokemon_for_file_checklist.py)
# If generation is complete (add to JSON?), omit adding missing images from parsing gen columns in spreadsheet_funcs

# TODO: Make a universal scraping file for bulba and wikidex?
# Below funcs bundled for each that you can just call when needed

# NOTE: Always check Bulba first, they have higher quality images
# TODO: Maybe occassionally run checks on images saved in mass (say all gen 9) Wikidex most common file size (250x250? 180x180? Def small, Bulba has most gen 8 (all switch?) at 1024x1024) to see if bulba now has those in higher res
# Honestly yeah, write to pokedex JSON all small, non-animated images (bc bulba sux for animation (is this true? check), mostly coming from Wikidex)
# When scraping bulba, search for higher quality ones
# TODO: Or are bulbas just more pixels bc more whitespace, not necessarily higher res??? Check visually and see
def main():
    check_pokedex_db_is_current(force=False)
    #generate_pokedex_from_spreadsheet()
    #add_missing_images_to_poke()
    #get_game_img_urls()
    #scrape_game_imgs()
    # TODO: Many more menu sprites added, see notes inside menu_sprites file
    #get_menu_sprites()
    
if __name__ == "__main__":
    main()