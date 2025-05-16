import urllib   # For downloading those images to my computer
import os

from db_utils import get_missing_poke_imgs_by_table, get_missing_pokeball_imgs

# NOTE: ALL DOWNLOADS MUST BE DONE IN THE FASHION BELOW
    # Otherwise bulba has a check on if the site is being web scraped and it will block the download
# This is to mask the fact I'm webscraping
    # To use, call
    # filename, headers = opener.retrieve(get_largest_png(img), path + save_name)
opener = urllib.request.URLopener()
opener.addheader('User-Agent', 'Mozilla/5.0')

def download_img(url, save_path):
    filename, headers = opener.retrieve(url, save_path)


def scrape_imgs(poke_num, filename_table, starter_url, translate_func, download_func, exclusions, has_animation, allow_download, save_path):
    missing_imgs_dict = get_missing_poke_imgs_by_table(poke_num, filename_table) if filename_table != "pokeball_filenames" else get_missing_pokeball_imgs()
    translated_missing_imgs = translate_all_my_filenames_to_url(missing_imgs_dict, translate_func, exclusions)

    for poke_info, files in translated_missing_imgs.items():
        for file in files:
            # poke_info == (poke_num, form_id) or (pokeball_id, img_type_id) if pokeball img
            # file == (my_file_naming_convention, translated_url)
            my_filename = file[0] + ".png"
            save_path = os.path.join(save_path, my_filename)
            if allow_download:  # Putting this here in addition to the actual download func, so func doesnt try to open pages to check for existence
                download_func(file[1], save_path, allow_download, has_animation)


def translate_all_my_filenames_to_url(filename_dict, translate_func, exclude, starter_url):
    for poke_info, files in filename_dict.items():
        print(f"\rTranslating #{poke_info[0]} filenames to urls...", end='', flush=True)
        urls = []
        for my_filename in files:
            # Right now this filters out SV & BDSP Sprites, and animateds > Gen5 since bulba doesnt have them
            if exclude != None and exclude(my_filename):
                continue
            translated_filename = translate_func(my_filename, poke_info)
            translated_filename_url = convert_translated_filename_to_url(starter_url, translated_filename)
            urls.append((my_filename, translated_filename_url))
        filename_dict[poke_info] = urls
    # Resetting console line after updates from above
    print('\r' + ' '*55 + '\r', end='')
    return filename_dict


def convert_translated_filename_to_url(starter_url, translated_filename):
    return (starter_url + translated_filename.replace(" ", "_"))