import os


game_sprite_path = "C:\\Users\\ethan\\OneDrive\\Desktop\\Code\\Pokeball-Pokemon-Comparison\\Images\\Pokemon\\Game Sprites\\"
back_sprites_to_filter_path = "C:\\Users\\ethan\\OneDrive\\Desktop\\Code\\Pokeball-Pokemon-Comparison\\Images\\Pokemon\\Game Sprites\\back_imgs_to_be_filtered"
animated_pngs_pre_gif_conversion = "C:\\Users\\ethan\\OneDrive\\Desktop\\Code\\Pokeball-Pokemon-Comparison\\Images\\Pokemon\\Game Sprites\\animated_pngs_for_gifs\\pngs\\Converted to gif"
test_path = "C:\\Users\\ethan\\OneDrive\\Desktop\\Code\\Pokeball-Pokemon-Comparison\\Images\\Pokemon\\Test"
staging_path = "C:\\Users\\ethan\\OneDrive\\Desktop\\Code\\Pokeball-Pokemon-Comparison\\Images\\Pokemon\\Game Sprites\\staging"
file_ext = ""


def add_leading_zero(path):
    files = os.listdir(path)
    for f in files:
        full_path = os.path.join(path, f)
        if os.path.isfile(full_path):
            new_full_path = os.path.join(path, "0"+f)
            print(new_full_path)
            os.rename(full_path, new_full_path)


def replace_in_filename(path, replace, replace_with, just_print=False):
    files = os.listdir(path)
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
    replace_in_filename(game_sprite_path, replace, replace_with, just_print)
    replace_in_filename(back_sprites_to_filter_path, replace, replace_with, just_print)
    replace_in_filename(animated_pngs_pre_gif_conversion, replace, replace_with, just_print)


def print_files_with(path, s):
    files = os.listdir(path)
    for f in files:
        if s in f:
            print(f)