# For translating downloaded archives into my filenaming convention
import os
import re

from app_globals import save_directories
from dl_file_translation_mapping import *
from db_utils import get_poke_num, get_poke_name, has_f_form
from scraping_utils import get_file_ext




# NOTE: To do this, it may require some preprocessing of downloaded directories. file_utils contains functions that can complete these easily:
    # - Pokemon numbers, if in filename should have leading zeros totalling 4 digits (file_utils.make_poke_num_have_leading_zeros_for_all_files_in_path)
        # - Otherwise, pokemon name should be at beginning of filename. Name is not necessary if number is present.
        # - Also confirm all poke nums bc sometimes they will just order them starting from 1 instead of by poke num
    # - WATCH  CAREFULLY for their naming conventions, if they have <poke_num>-<poke_name>, and poke name starts with an f that may trigger a -f female tag
    # - Directories should only contain sprites from one game and one sprite type
        # - ie Gen8 Swsh Shiny Back Animated
        # - Shinies need to be in a seperate directory from regular colors, fronts seperate from back, animateds seperate from statics
        # - Moving files based off substrings can be accomplished via file_utils.
    # - Directory name needs to be in db_file_translation_mapping.DIRECTORY_TO_FILENAME_MAP
    # - If downloading from same source, need to confirm translations in db_file_translation_mapping for that creator key still apply (value exists in filename)
        # - If not edit their filename to include VALUE (a bit backwards, I know)
# TODO: Add some testing parameter so you can print only empty forms, just print old->new filenames, etc. like how I test it here




def translate_all_directories(just_print=False):
    game_sprite_dl_repository_root_path = os.path.join(save_directories["Game Sprites"]["path"], "downloaded_repositories")
    home_dl_repository_root_path = os.path.join(save_directories["HOME"]["path"], "downloaded_repositories")

    for creator, directories in DIRECTORY_TO_FILENAME_MAP.items():
        for dir in directories:
            if "HOME" in dir: dir_path = os.path.join(home_dl_repository_root_path, dir)
            else: dir_path = os.path.join(game_sprite_dl_repository_root_path, dir)

            convert_filenames_in_dir_to_my_naming_convention(dir_path, just_print)


def convert_filenames_in_dir_to_my_naming_convention(path, just_print=False):
    files = os.listdir(path)
    creator_name = get_creator_name_from_path(path)

    for file in files:
        if not os.path.isfile(os.path.join(path, file)) or get_file_ext(file) not in (".png", ".gif"): continue   # If "file" is a directory or not an image file, continue

        poke_num = get_poke_num_from_file(file)
        poke_name = get_poke_name(poke_num)

        # Get platform and tags from directory name (since I downloaded file, it should only contain one platform and sprite type)
        dir_name = os.path.basename(path)
        platform_w_tags = DIRECTORY_TO_FILENAME_MAP[creator_name][dir_name]
        platform_w_tags_split = platform_w_tags.split("-", 1)
        platform = platform_w_tags_split[0]
        tags = "" if "-" not in platform_w_tags else platform_w_tags_split[1]

        form = get_translated_form(poke_num, file, creator_name)
        shiny = "-Shiny" if "Shiny" in tags else ""
        back = "-Back" if "Back" in tags else ""
        animated = "-Animated" if "Animated" in tags else ""
        battle_animation_num = get_battle_animation_num(file) if dir_name in DIRECTORIES_CONTAINING_BATTLE_ANIMATIONS else ""
        file_ext = get_file_ext(file)

        my_filename = f"{poke_num} {poke_name} {platform}{shiny}{form}{back}{animated}{battle_animation_num}{file_ext}"

        if just_print: print(f"Form empty for:\t {file}")   # This is for debugging translations, lets me see if a translation is wrong for a form (mispelling in file or translation, different denoter, etc)
        print(f"{file}\t ---> \t{my_filename}")

        if not just_print:
            pass    # TODO: Implement renaming


def get_creator_name_from_path(path):
    dir_name = os.path.basename(path)
    for creator in DIRECTORY_TO_FILENAME_MAP:
        for directory in DIRECTORY_TO_FILENAME_MAP[creator].keys():
            if directory == dir_name:
                return creator
    # TODO: Throw error directory not in dict


def get_poke_num_from_file(file):
    # Try to get poke num from filename
    match = re.match(r"(\d+)", file)
    # Get poke num via poke name if not poke num w 4 leading zeros
    if not match or len(match.group(1)) != 4:
        file_wo_ext = file.split(get_file_ext(file))[0]
        poke_name = file_wo_ext.split("-")[0].title()   # Removes any tags, makes Title Case
        return get_poke_num(poke_name)
    else:
        return match.group(1)
    

def get_battle_animation_num(file):
    file = file.replace(get_file_ext(file), "")
    match = re.search(r'-(\d+)$', file) # Finds -<#> if it exists at end of file
    battle_ani_num = f"-{match.group(1)}" if match else ""
    return battle_ani_num
    

def get_translated_form(poke_num, file, creator_key):
    poke_num = int(poke_num)    # Dict keys are ints
    file = file.split(get_file_ext(file))[0]   # Seperating filename from file ext so f in gif ext doesnt trigger female form
    form = ""

    # Checking universal form
    for my_denoter, translation in DL_UNIVERSAL_FORM_MAP[creator_key].items():
        if translation in file:
            if my_denoter == "-f" and not has_f_form(poke_num): continue    # Female variants very suceptible to false positives since it could just be the letter "f" in the filename... This greatly mitigates those

            form += my_denoter
            break

    # Checking species form
    if poke_num in CREATOR_FORM_TRANSLATION_MAP:
        for my_denoter, translation in CREATOR_FORM_TRANSLATION_MAP[poke_num][creator_key].items():
            if translation in file:
                form += my_denoter
                break
    
    if form == "": print(file)  # TODO: Just to make sure none of my keys arent translating, can delete after
    return form


translate_all_directories()