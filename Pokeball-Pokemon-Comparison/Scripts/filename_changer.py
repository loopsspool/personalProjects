import os
import re

# TODO: No form tags in drawn images

game_sprite_path = "C:\\Users\\ethan\\OneDrive\\Desktop\\Code\\Pokeball-Pokemon-Comparison\\Images\\Pokemon\\Game Sprites\\"
back_sprites_to_filter_path = "C:\\Users\\ethan\\OneDrive\\Desktop\\Code\\Pokeball-Pokemon-Comparison\\Images\\Pokemon\\Game Sprites\\back_imgs_to_be_filtered"
animated_pngs_pre_gif_conversion = "C:\\Users\\ethan\\OneDrive\\Desktop\\Code\\Pokeball-Pokemon-Comparison\\Images\\Pokemon\\Game Sprites\\animated_pngs_for_gifs\\pngs\\Converted to gif"
#files = os.listdir(game_sprite_path)
file_ext = ""

# For testing/slight correction in file names
#for f in files:
    #if not "-Region-Alola" in f and "Gen7" in f:
        #print(f)
        # old = f
        # ext = old[len(old)-4:]
        # new = old.replace(ext, "-SM-USUM" + ext)
        # print(new)
        #os.rename(game_sprite_path + f, game_sprite_path + new)
    # full_path = os.path.join("C:\\Users\\ethan\\OneDrive\\Desktop\\Code\\Pokeball-Pokemon-Comparison\\Images\\Pokemon\\Game Sprites\\back_imgs_to_be_filtered", f)
    # if os.path.isfile(full_path):
    #     new_full_path = os.path.join(game_sprite_path, "0"+f)
    #     print(new_full_path)
    #     os.rename(full_path, new_full_path)

def add_leading_zero(path):
    files = os.listdir(path)
    for f in files:
        full_path = os.path.join(path, f)
        if os.path.isfile(full_path):
            new_full_path = os.path.join(path, "0"+f)
            print(new_full_path)
            os.rename(full_path, new_full_path)

def replace_in_filename(path, replace, replace_with):
    files = os.listdir(path)
    for f in files:
        full_path = os.path.join(path, f)
        if os.path.isfile(full_path):
            if replace in f:
                new_f = f.replace(replace, replace_with)
                new_full_path = os.path.join(path, new_f)
                print(new_f)
                os.rename(full_path, new_full_path)

# Shiny tag first
# Then form (AND add -Form-____ tag to misc/type forms)
    # So they aren't sorted below shinies
# Then back
# Then by animated
# Then by alt
# file_i = 0
# for f in files:
#     shiny = False
#     female = False
#     mega = False
#     mega_x = False
#     mega_y = False
#     gigantamax = False
#     region = ""
#     form = ""
#     back = False
#     crystal_back = False
#     animated = False
#     alt = False

#     old_filename = f
#     file_ext = f[len(f)-4 : len(f)]
    
#     if "Shiny" in f:
#         shiny = True
#         old_filename = old_filename.replace(" Shiny", "")
    
#     if f.endswith("f.png") or f.endswith("f alt.png") or f.endswith("f.gif")or f.endswith("f alt.gif"):
#         female = True
#         old_filename = old_filename.replace(" f", "")
   
#     if "Mega" in f and not "Meganium" in f:
#         mega = True
#         if "MegaX" in f or "MegaY" in f:
#             if re.search(" MegaX", old_filename):
#                 old_filename = old_filename.replace(" MegaX", "")
#                 mega_x = True
#             if re.search(" MegaY", old_filename):
#                 old_filename = old_filename.replace(" MegaY", "")
#                 mega_y = True
#         else:
#             old_filename = old_filename.replace(" Mega", "")
    
#     if "Gigantamax" in f:
#         gigantamax = True
#         old_filename = old_filename.replace(" Gigantamax", "")
    
#     if "Alolan" in f:
#         region = "-Region-Alola"
#         old_filename = old_filename.replace(" Alolan", "")
#     if "Galarian" in f:
#         region = "-Region-Galar"
#         old_filename = old_filename.replace(" Galarian", "")
    
#     if "Back" in f:
#         back = True
#         if " Crystal" in f:
#             crystal_back = True
#             old_filename.replace(" Crystal", "")
#         old_filename = old_filename.replace("-Back", "")
    
#     if "Animated" in f:
#         animated = True
#         old_filename = old_filename.replace(" Animated", "")
   
#     if " alt" in f:
#         alt = True
#         old_filename = old_filename.replace(" alt", "")

#     # Getting form
#     for poke in pokedex:
#         if poke.number == f[0:3]:
#             if poke.has_misc_forms or poke.has_type_forms:
#                 form = old_filename.replace(file_ext, "")
#                 # Splitting filename by gen
#                     # Unfortunately, Genesects name starts with Gen lol
#                 if poke.name != "Genesect":
#                     form = form.split("Gen")[1]
#                 else:
#                     # Handling Genesects case
#                     form = form.split("Gen")[2]

#                 # Then by game
#                     # If the file is a back sprite, there's only one space after the gen split
#                         # This is due to back sprites being shared by generation
#                 split_num = -1
#                 if back == True:
#                     split_num = 1
#                 else:
#                     split_num = 2
#                 form = form.split(" ", split_num)
#                 # Getting only the last element (which should be form)
#                 form = form[len(form) - 1]
#                 # This is for a slight correction for Crystal Back Unowns
#                 if " Crystal" in form:
#                     form = form.replace(" Crystal", "")
#                     old_filename = old_filename.replace(" Crystal", "")
#                 # If form is only gen number or game (ie regular forms), skip
#                 if re.search("\d$", form) or re.search("Red-Blue", form) or re.search("Red-Green", form) or re.search("Yellow", form) or re.search("Crystal", form) or re.search("Gold", form) or re.search("Silver", form) or re.search("Emerald", form) or re.search("FireRed-LeafGreen", form) or re.search("Ruby-Sapphire", form) or re.search("Diamond-Pearl", form) or re.search("HGSS", form) or re.search("Platinum", form) or re.search("XY-ORAS-SM-USUM", form) or re.search("SM-USUM", form) or re.search("Sword-Shield", form):
#                     # This is to reset form so it doesn't add the gen number or game to the file tags lol
#                     form = ""
#                     continue

#                 # Creates a template for the new file name
#                 # Splitting by form in unown removes letters (Form G removes the G from Gen)
#                     # So instead I'm truncated them (larger numbers to include file extension)
#                 if old_filename.startswith("201"):
#                     if form == "Qmark":
#                         old_filename = old_filename[0 : len(old_filename)-10]
#                     else:
#                         old_filename = old_filename[0 : len(old_filename)-6]
#                 else:
#                     old_filename = old_filename.replace(" " + form, "")
#                 # Replacing spaces with underscores for proper file sorting
#                 form = form.replace(" ", "_")
#                 form = "-Form-" + form


#     new_filename_tags = ""
#     if shiny:
#         new_filename_tags += "-Shiny"
#     if female:
#         new_filename_tags += "-f"
#     if mega:
#         new_filename_tags += "-Mega"
#     if mega_x:
#         new_filename_tags += "_X"
#     if mega_y:
#         new_filename_tags += "_Y"
#     if gigantamax:
#         new_filename_tags += "-Gigantamax"
#     if region != "":
#         new_filename_tags += region
#     if form != "":
#         new_filename_tags += form
#     if back:
#         if crystal_back:
#             old_filename = old_filename.replace(" Crystal", "")
#             new_filename_tags += "-Back-Crystal"
#         else:
#             new_filename_tags += "-Back"
#     if animated:
#         new_filename_tags += "-Animated"
#     if alt:
#         new_filename_tags += "-Alt"
    
#     new_filename = old_filename.replace(file_ext, "")
#     new_filename += new_filename_tags + file_ext

    # print(f)
    # print(new_filename)

    # if f.startswith("646"):
    #     test = open("C:\\Users\\ejone\\OneDrive\\Desktop\\Code\\Javascript\\p5\\projects\\Pokeball Pokemon Comparison\\Images\\Pokemon\\Drawn\\" + new_filename, "x")

    # file_i += 1
    # if file_i == 500:
    #     break
                #print(poke.number, poke.name, ":", form)


