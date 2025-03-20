import string # To access letters easily without having to type them myself in an array

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

pokedex = []

uppers = list(string.ascii_uppercase)
types = ["Normal", "Fighting", "Flying", "Poison", "Ground", "Rock", "Bug", "Ghost", "Steel", "Fire", "Water", "Grass", "Electric", "Psychic", "Ice", "Dragon", "Dark", "Fairy", "Qmark"]
# Vanilla Cream is default, so no letter denoter
creams = [("Caramel_Swirl", "CaS"), ("Lemon_Cream", "LeC"), ("Matcha_Cream", "MaC"), ("Mint_Cream", "MiC"), ("Rainbow_Swirl", "RaS"), ("Ruby_Cream", "RaC"), ("Ruby_Swirl", "RuS"), ("Salted_Cream", "SaC"), ("Vanilla_Cream", "")]
# Strawberry Sweet is default, so no letter denoter
sweets = [("Berry_Sweet", "B"), ("Clover_Sweet", "C"), ("Flower_Sweet", "F"), ("Love_Sweet", "L"), ("Ribbon_Sweet", "R"), ("Star_Sweet", "S"), ("Strawberry_Sweet", "")]

save_path_starter = "C:\\Users\\ejone\\OneDrive\\Desktop\\Code\\Javascript\\p5\\projects\\Pokeball Pokemon Comparison\\Images\\Pokemon"
game_save_path = save_path_starter + "\\Game Sprites\\"
gen6_menu_sprite_save_path = save_path_starter + "\\Menu Sprites\\Gen6\\"
gen8_menu_sprite_save_path = save_path_starter + "\\Menu Sprites\\Gen8\\"
drawn_save_path = save_path_starter + "\\Drawn\\"