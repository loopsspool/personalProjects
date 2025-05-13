import os
import shutil
from app_globals import *


def add_leading_zero(path):
    files = set(os.listdir(path))
    for f in files:
        full_path = os.path.join(path, f)
        if os.path.isfile(full_path):
            new_full_path = os.path.join(path, "0"+f)
            print(new_full_path)
            os.rename(full_path, new_full_path)


def replace_in_filename(path, replace, replace_with, just_print=False):
    files = set(os.listdir(path))
    for f in files:
        full_path = os.path.join(path, f)
        if os.path.isfile(full_path):
            if replace in f:
                new_f = f.replace(replace, replace_with)
                new_full_path = os.path.join(path, new_f)
                print(f"{f}\t changed to \t{new_f}")
                if not just_print:
                    os.rename(full_path, new_full_path)


def replace_filename_in_all_dirs(replace, replace_with, just_print=False):
    replace_in_filename(GAME_SPRITE_SAVE_PATH, replace, replace_with, just_print)
    replace_in_filename(DRAWN_SAVE_PATH, replace, replace_with, just_print)
    replace_in_filename(HOME_SAVE_PATH, replace, replace_with, just_print)
    replace_in_filename(HOME_MENU_SAVE_PATH, replace, replace_with, just_print)
    replace_in_filename(POKEBALL_SAVE_PATH, replace, replace_with, just_print)
    replace_in_filename(ANIMATED_PNGS_PRE_GIF_CONVERSION_PATH, replace, replace_with, just_print)
    replace_in_filename(GIFS_POST_CONVERSION_PATH, replace, replace_with, just_print)
    replace_in_filename(TEST_PATH, replace, replace_with, just_print)
    replace_in_filename(STAGING_PATH, replace, replace_with, just_print)


def print_files_with(path, s):
    files = set(os.listdir(path))
    for f in files:
        if s in f:
            print(f)


def print_files_with_from_all_dirs(s):
    print_files_with(GAME_SPRITE_SAVE_PATH, s)
    print_files_with(DRAWN_SAVE_PATH, s)
    print_files_with(HOME_SAVE_PATH, s)
    print_files_with(HOME_MENU_SAVE_PATH, s)
    print_files_with(POKEBALL_SAVE_PATH, s)
    print_files_with(ANIMATED_PNGS_PRE_GIF_CONVERSION_PATH, s)
    print_files_with(GIFS_POST_CONVERSION_PATH, s)
    print_files_with(TEST_PATH, s)
    print_files_with(STAGING_PATH, s)