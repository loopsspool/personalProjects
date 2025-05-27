import os
from app_globals import *




#|================================================================================================|
#|~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~[     UNIVERSAL FUNCS     ]~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~|
#|================================================================================================|

def get_all_files_in_dir_w_str(path, str):
    files = set(os.listdir(path))
    matching_files = []

    for file in files:
        if not os.path.isfile(os.path.join(path, file)): continue   # If "file" is a directory, continue
        if str in file:
            matching_files.append(file)

    return matching_files




#|================================================================================================|
#|~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~[     PRINT FUNCS     ]~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~|
#|================================================================================================|

def print_files_with(path, s):
    file_matches = get_all_files_in_dir_w_str(path, s)
    for f in file_matches: print(f)


def print_files_with_from_all_dirs(s):
    for path in SAVE_PATHS.values():
        print_files_with(path, s)




#|================================================================================================|
#|~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~[     TEXT FUNCS     ]~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~|
#|================================================================================================|

def add_leading_zero(path):
    files = set(os.listdir(path))
    for f in files:
        full_path = os.path.join(path, f)
        if os.path.isfile(full_path):
            new_full_path = os.path.join(path, "0"+f)
            print(new_full_path)
            os.rename(full_path, new_full_path)


def replace_in_filename(path, replace, replace_with, just_print=False):
    file_matches = get_all_files_in_dir_w_str(path, replace)

    for file in file_matches:
        full_path = os.path.join(path, file)
        new_file = file.replace(replace, replace_with)
        new_full_path = os.path.join(path, new_file)
        print(f"{file}\t changed to \t{new_file}")
        if not just_print:
            os.rename(full_path, new_full_path)


def replace_filename_in_all_dirs(replace, replace_with, just_print=False):
    for path in SAVE_PATHS.values():
        replace_in_filename(path, replace, replace_with, just_print)




#|================================================================================================|
#|~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~[     DELETE FUNCS     ]~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~|
#|================================================================================================|

def delete_all_files_with_str(path, str, just_print=False):
    file_matches = get_all_files_in_dir_w_str(path, str)