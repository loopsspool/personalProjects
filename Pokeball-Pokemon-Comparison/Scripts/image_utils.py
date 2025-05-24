from PIL import Image   # For converting URL image data to PIL Image object 
import requests # To retrieve webpages
from bs4 import BeautifulSoup   # To parse webpages
import re
import os
# import cv2  # To save first frame of webm
# import numpy as np  # To parse webm
import subprocess
import tempfile     # To read webm


def is_animated(url):
    file_type = f".{url.split(".")[-1]}"

    if file_type in (".png", ".gif"):
        img = Image.open(requests.get(url, stream = True).raw)
        return(img.is_animated)
    elif file_type in (".webm"):
        return(True)
    else:
        raise RuntimeError("Unkown file type")


# TODO: Properly convert gif to png to preserve color
def save_first_frame_of_png_or_gif(url, save_path):
    img = Image.open(requests.get(url, stream = True).raw)
    first_frame = img.copy()    # Returns just first frame
    first_frame.save(save_path)


# TODO: No webm videos have transparency, will need to set a different save file for these to remove later
    # Or write function to remove them now
def save_first_frame_of_webm(url, save_path):
    # Download the video
    response = requests.get(url)
    response.raise_for_status()

    # TODO: This always asks to overwrite an existing file, fix
    # Write to a temp video file
    with tempfile.NamedTemporaryFile(suffix=".webm", delete=False) as tmp:
        tmp.write(response.content)
        tmp.flush()
        temp_video_path = tmp.name

    # Write to a temp image file
    with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as image_file:
        temp_image_path = image_file.name

    # Extract first frame using ffmpeg
    subprocess.run([
        "ffmpeg",
        "-i", temp_video_path,
        "-vf", "select=eq(n\\,0)",
        "-vframes", "1",
        "-pix_fmt", "rgba",  # keep transparency
        temp_image_path
    ], check=True)

    # Save Img
    img = Image.open(temp_image_path)
    img.save(save_path)

    os.remove(temp_video_path)
    os.remove(temp_image_path)


# TODO: Incorporate the below to save each frame of an animated png
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
    biggest_url = img_page_soup.find("div", "fullImageLink")
    # Return its url
    return (biggest_url.a.get("href"))


def wikidex_get_largest_img(img_page_soup):
    has_larger_img = img_page_soup.find("a", string=re.compile(r"Mostrar imagen en alta resolución"))
    if has_larger_img: 
        return (has_larger_img.get("href"))
    else: 
        img_div = img_page_soup.find("div", "fullMedia")
        return (img_div.a.get("href"))