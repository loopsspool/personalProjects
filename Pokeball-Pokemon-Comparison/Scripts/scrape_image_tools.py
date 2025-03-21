from PIL import Image   # For converting URL image data to PIL Image object 
import requests # To retrieve webpages
from bs4 import BeautifulSoup   # To parse webpages
import os   # For downloading those images to my computer
from globals import starter_url
import re   # For filtering what images to download

def check_if_animated(link):
    # NOTE: Works on animated pngs
    # Converting URL image to PIL Image Object
    img = Image.open(requests.get(link, stream = True).raw)
    # Checking if it is an animated image
    return(img.is_animated)


def get_largest_png(thumb):
    # Go into page of image
    img_page = requests.get(starter_url + thumb.a.get("href"))
    img_page_soup = BeautifulSoup(img_page.content, 'html.parser')
    # Find the biggest image location
    biggest_link = img_page_soup.find("div", "fullImageLink")
    # Return its link
    return (biggest_link.a.get("href"))

def get_img_from_string(thumb, s, save_path):
    img_text = thumb.img['alt']
    file_ext = img_text[len(img_text) - 4:]
    save_name = save_path + file_ext
    if re.search(s, img_text) != None and not os.path.exists(save_name):
        save_img = get_largest_png(thumb)
        print(img_text)
        #print(save_img)
        #print(s, " --- ", save_name)
        #filename, headers = opener.retrieve(save_img, save_name)