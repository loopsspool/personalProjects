from PIL import Image   # For converting URL image data to PIL Image object 
import requests # To retrieve webpages
from bs4 import BeautifulSoup   # To parse webpages


def is_animated(link):
    # NOTE: Works on animated pngs
    # Converting URL image to PIL Image Object
    img = Image.open(requests.get(link, stream = True).raw)
    # Checking if it is an animated image
    return(img.is_animated)


def save_first_frame(link, save_path):
    img = Image.open(requests.get(link, stream = True).raw)
    first_frame = img.copy()    # Returns just first frame
    first_frame.save(save_path)


def get_largest_png(img_page_soup):
    # Find the biggest image location
    biggest_link = img_page_soup.find("div", "fullImageLink")
    # Return its link
    return (biggest_link.a.get("href"))