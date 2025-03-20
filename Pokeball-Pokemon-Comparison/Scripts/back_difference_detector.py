import os

# TODO: This script will take all back sprites of each game in a generation up to gen 4 to compare them and see if they're different
    # If they are different between games in a gen, add game to the end of the filename with a hyphen
    # Otherwise, just gen is fine

# open("image1.jpg","rb").read() == open("image2.jpg","rb").read()

back_path = "C:\\Users\\ejone\\OneDrive\\Desktop\\Code\\Javascript\\p5\\projects\\Pokeball Pokemon Comparison\\Images\\Pokemon\\Game Sprites\\back_imgs_to_be_filtered\\"
back_imgs = os.listdir(back_path)

# TODO: List of
    # Class for each pokemon
        # Containing arrays for gen1 - gen4 (+ shiny for each)
            # If length != amount of games in that gen
                # There is a recycled back sprite
            # Else check for equality between images

# Pokemon object
class Pokemon:
    def __init__(self, name, number, gen, has_f_var, has_mega, has_giganta, reg_forms, has_type_forms, has_misc_forms, is_in_gen8):
        self.name = name
        self.number = number
        self.gen = gen
        self.has_f_var = has_f_var
        self.has_mega = has_mega
        self.has_giganta = has_giganta
        self.reg_forms = reg_forms
        self.has_type_forms = has_type_forms
        self.has_misc_forms = has_misc_forms
        self.is_in_gen8 = is_in_gen8
        self.missing_imgs = []
        self.missing_gen1_thru_gen4_back_imgs = []

#pokedex.append(Pokemon(name, num, gen, has_f_var, has_mega, has_giganta, reg_forms, has_type_forms, has_misc_forms, is_in_gen8))

curr_gen_set = []
for img in back_imgs:
    if img == "all same" or img == "000README.txt":
        continue
    
    print(img)