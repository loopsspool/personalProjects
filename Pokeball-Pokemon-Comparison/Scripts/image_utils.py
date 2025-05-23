from PIL import Image   # For converting URL image data to PIL Image object 
import requests # To retrieve webpages
from bs4 import BeautifulSoup   # To parse webpages
import re


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


# TODO: Incorporate the below to save each frame of an animated img
# img = Image.open(os.path.join(POKEBALL_SAVE_PATH, file))
#         frame=0
#         try:
#             while True:
#                 img.seek(frame)
#                 name = new_f_static.replace("Battle", f"Battle-Static_{frame}")
#                 img.save(os.path.join(POKEBALL_SAVE_PATH, name))
#                 frame+=1
#         except EOFError:
#             pass


def bulba_get_largest_png(img_page_soup):
    # Find the biggest image location
    biggest_link = img_page_soup.find("div", "fullImageLink")
    # Return its link
    return (biggest_link.a.get("href"))


def wikidex_get_largest_img(img_page_soup):
    has_larger_img = img_page_soup.find("a", string=re.compile(r"Mostrar imagen en alta resolución"))
    if has_larger_img: 
        return (has_larger_img.get("href"))
    else: 
        img_div = img_page_soup.find("div", "fullMedia")
        return (img_div.a.get("href"))