from PIL import Image, ImageEnhance, ImageFilter   # For converting URL image data to PIL Image object 
import requests # To retrieve webpages
from bs4 import BeautifulSoup   # To parse webpages
import re
import os
import subprocess   # To run ffmpeg to download first frame of webm
from apng import APNG   # To convert webm to apng
import cv2  # To convert webm background to transparent
import numpy as np  # To parse webm
import tempfile     # To temporarily read webm

from scraping_utils import fetch_url_with_retry

def is_animated(url):
    file_type = f".{url.split(".")[-1]}"

    if file_type in (".png", ".gif"):
        img = Image.open(fetch_url_with_retry(url, stream_flag=True).raw)
        return(img.is_animated)
    elif file_type in (".webm"):
        return(True)
    else:
        raise RuntimeError(f"Unkown file type: {file_type}")


def save_first_frame(url, save_path):
    url_file_type = f".{url.split(".")[-1]}"
    if url_file_type in (".png", ".gif"):
        save_first_frame_of_png_or_gif(url, save_path)
    elif url_file_type in (".webm"):
        save_first_frame_of_webm(url, save_path)
    else:
        raise RuntimeError(f"Unkown url file type: {url_file_type}")


def save_first_frame_of_png_or_gif(url, save_path):
    img = Image.open(fetch_url_with_retry(url, stream_flag=True).raw)
    first_frame = img.copy()    # Returns just first frame
    first_frame.save(save_path)


# TODO: No webm videos have transparency, will need to set a different save file for these to remove later
def save_first_frame_of_webm(url, save_path):
    from app_globals import save_directories

    # Download the video
    response = fetch_url_with_retry(url)
    response.raise_for_status()

    # Write to a temp video file
    with tempfile.NamedTemporaryFile(suffix=".webm", delete=False) as tmp:
        tmp.write(response.content)
        tmp.flush()
        temp_video_path = tmp.name

    # TODO: Once transparency issue is resolved, these can instead be saved to passed save_path (game sprites/home sprites)
    filename = save_path.split("\\")[-1]
    still_save_path = os.path.join(save_directories["Need Transparency"]["path"], filename)

    # Extract first frame using ffmpeg
    try:
        subprocess.run([
            "ffmpeg",
            "-y",   # To overwrite file if it exists w/o asking
            "-i", temp_video_path,
            "-vf", "select=eq(n\\,0)",  # Only get first frame
            "-frames:v", "1",   # Only output 1 frame
            "-pix_fmt", "rgba",  # keep transparency/color
            still_save_path
        ], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    except subprocess.CalledProcessError as e:
        print("FFmpeg failed:")
        print(e.stderr.decode())  # print detailed FFmpeg error

    os.remove(temp_video_path)


# from app_globals import TEST_PATH
# save_first_frame_of_webm("https://images.wikidexcdn.net/mwuploads/wikidex/8/8c/latest/20240121112549/Grafaiai_EP.webm", os.path.join(TEST_PATH, "webm_still_test.png"))


# TODO: Put pause on this until after scraping, then incorporate it
# NOTE: Cropping out pure white from the image made the body of certain pokes also transparent if they had white
# Machine learning model necessary to create background mask based on frame-by-frame edges of the poke model
# Even this had issues, so pre-processing each frame to increase contrast, saturation, and edges
# TODO: Save frames into folder to be bg excluded by u2net
# TODO: Just download webm while scraping, save image/video processing for end since it takes a while
def split_webm_into_frames(webm_path, save_path, fps=None):
    webm_name = webm_path.split("\\")[-1].replace(".webm", "")
    cmd = [
        "ffmpeg",
        "-i", webm_path
    ]
    if fps: cmd += ["-vf", f"fps={fps}"]

    cmd += [os.path.join(save_path, f"{webm_name}--Frame_%04d.png")]

    subprocess.run(cmd, check=True)


def preprocess_for_u2net(input_filepath, output_path):
    CONTRAST_FACTOR = 2.5
    SHARPNESS_FACTOR = 3.0
    BRIGHTNESS_FACTOR = 1.5

    img = Image.open(input_filepath).convert('L')

    img = ImageEnhance.Contrast(img).enhance(CONTRAST_FACTOR)
    img = ImageEnhance.Sharpness(img).enhance(SHARPNESS_FACTOR)
    #img = ImageEnhance.Brightness(img).enhance(BRIGHTNESS_FACTOR)

    # Boost Edges
    img = img.filter(ImageFilter.FIND_EDGES)

    img.save(output_path)


# from app_globals import STAGING_PATH
# # test_vid = os.path.join(STAGING_PATH, "test_vid.webm")
# # split_webm_into_frames(test_vid, STAGING_PATH)
# test_frames = os.path.join(STAGING_PATH, "Frames")
# TODO: Change to just using 1 file for testing
# for file in os.listdir(test_frames):
#     og_path = os.path.join(test_frames, file)
#     new_path = os.path.join(test_frames, f"2{file}")
#     preprocess_for_u2net(og_path, new_path)


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
    if biggest_url is None:
        print(img_page_soup)
    # Return its url
    return (biggest_url.a.get("href"))


def wikidex_get_largest_img(img_page_soup):
    has_larger_img = img_page_soup.find("a", string=re.compile(r"Mostrar imagen en alta resolución"))
    if has_larger_img: 
        return (has_larger_img.get("href"))
    else: 
        img_div = img_page_soup.find("div", "fullMedia")
        if img_div is None:
            print(img_page_soup)
        return (img_div.a.get("href"))