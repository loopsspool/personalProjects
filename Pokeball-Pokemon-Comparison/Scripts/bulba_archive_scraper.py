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

from globals import *
from spreadsheet_funcs import generate_pokedex_from_spreadsheet, add_missing_images_to_poke
from scrape_drawn_images import get_drawn_images
from scrape_menu_sprites import get_menu_sprites
from scraping import get_game_img_urls, scrape_game_imgs


################################# TODO: Complete all TODOs before running... please ########################


# TODO: Make a universal scraping file for bulba and wikidex?
# Below funcs bundled for each that you can just call when needed

generate_pokedex_from_spreadsheet()
add_missing_images_to_poke()
get_game_img_urls()
scrape_game_imgs()
#get_menu_sprites()



        
    

    