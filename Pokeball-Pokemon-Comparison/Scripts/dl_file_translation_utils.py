# For translating downloaded archives into my filenaming convention
import os
import re

from dl_file_translation_mapping import *
from db_utils import get_poke_num, get_poke_name




# NOTE: To do this, it may require some preprocessing of downloaded directories. file_utils contains functions that can complete these easily:
    # - Pokemon numbers, if in filename should have leading zeros totalling 4 digits (file_utils.make_poke_num_have_leading_zeros_for_all_files_in_path)
        # - Otherwise, pokemon name should be at beginning of filename. Name is not necessary if number is present.
    # - Directories should only contain sprites from one game and one sprite type
        # - ie Gen8 Swsh Shiny Back Animated
        # - Shinies need to be in a seperate directory from regular colors, fronts seperate from back, animateds seperate from statics
        # - Moving files based off substrings can be accomplished via file_utils. TODO: Implement moving function from substring
def convert_filename_to_my_naming_convention(path, creator_name):
    files = os.listdir(path)

    for file in files:
        if not os.path.isfile(os.path.join(path, file)): continue   # If "file" is a directory, continue

        # Try to get poke num
        match = re.match(r"(\d+)", file)

        # Get poke num via poke name if not poke num w 4 leading zeros
        if not match or len(match.group(1)) != 4:
            file_wo_ext = file.strip(".")[0]
            poke_name = file_wo_ext.strip("-")[0]   # Removes any tags
            poke_num = get_poke_num(poke_name)
        else:
            poke_num = match.group(1)

        # Get poke_name
        poke_name = get_poke_name(poke_num)

        # Get platform and tags from directory name (since I downloaded file, it should only contain one platform and sprite type)
        dir_name = os.path.basename(path)
        platform_w_tags = DIRECTORY_TO_FILENAME_MAP[dir_name]
        platform_w_tags_split = platform_w_tags.split("-", 1)
        platform = platform_w_tags_split[0]
        tags = platform_w_tags_split[1]