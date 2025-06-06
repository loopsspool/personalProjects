import os
import re
import shutil
from app_globals import *




#|================================================================================================|
#|~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~[     UNIVERSAL FUNCS     ]~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~|
#|================================================================================================|

def get_all_files_in_dir_w_str(path, str):
    files = os.listdir(path)
    matching_files = []

    for file in files:
        if not os.path.isfile(os.path.join(path, file)): continue   # If "file" is a directory, continue
        if str in file:
            matching_files.append(file)

    return matching_files


def get_all_files_in_dir_w_regex(path, pattern):
    files = os.listdir(path)
    matching_files = []

    for file in files:
        if not os.path.isfile(os.path.join(path, file)): continue   # If "file" is a directory, continue
        # TODO: Implement regex here
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
    for dir in save_directories.values():
        print_files_with(dir["path"], s)




#|================================================================================================|
#|~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~[     TEXT FUNCS     ]~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~|
#|================================================================================================|

def make_poke_num_have_leading_zeros_for_all_files_in_path(path, just_print=False):
    files = os.listdir(path)

    for file in files:
        if not os.path.isfile(os.path.join(path, file)): continue   # If "file" is a directory, continue

        old_full_path = os.path.join(path, file)
        match = re.match(r"(\d+)", file)
        if match:
            poke_num = match.group(1)
            
            padded_poke_num = poke_num.zfill(4)
            new_filename = file.replace(poke_num, padded_poke_num)
            new_full_path = os.path.join(path, new_filename)

            if new_filename == file: continue   # If it already had leading zeros, no need to rename
            print(f"{file}\t changed to \t{new_filename}")
            if not just_print:
                os.rename(old_full_path, new_full_path)


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
    for dir in save_directories.values():
        replace_in_filename(dir["path"], replace, replace_with, just_print)




#|================================================================================================|
#|~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~[     MOVE FUNCS     ]~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~|
#|================================================================================================|

def move_files_with_str(cur_path, dest_path, str, just_print=False):
    files_to_move = get_all_files_in_dir_w_str(cur_path, str)
    
    for file in files_to_move:
        if not os.path.isfile(os.path.join(cur_path, file)): continue   # If "file" is a directory, continue
        old_path = os.path.join(cur_path, file)
        old_path_base = os.path.basename(cur_path)
        dest_path_base = os.path.basename(dest_path)

        print(f"{file}\t moved from \t{old_path_base} to \t{dest_path_base}")
        if not just_print:
            shutil.move(old_path, dest_path)




#|================================================================================================|
#|~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~[     DELETE FUNCS     ]~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~|
#|================================================================================================|

def delete_all_files_with_str(path, str, just_print=False):
    file_matches = get_all_files_in_dir_w_str(path, str)

    for file in file_matches:
        if just_print:
            print(file)
            continue
        else:
            full_path = os.path.join(path, file)
            print(f"Deleted {file}")
            os.remove(full_path)


def delete_all_files_from_all_dirs_with_str(str, just_print=False):
    for dir in save_directories.values():
        delete_all_files_with_str(dir["path"], str, just_print)