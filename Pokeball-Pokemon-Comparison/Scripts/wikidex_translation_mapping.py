# ===============================================================================================================================================================================================
# ===============================================================================================================================================================================================

#   N   N    OOO   TTTTT  EEEEE
#   NN  N   O   O    T    E       ::
#   N N N   O   O    T    EEEE           This is a really old file, broken off from a longer script I wrote... Not updated yet to reflect best practice/work with other scripts
#   N  NN   O   O    T    E       ::
#   N   N    OOO     T    EEEEE 

# ===============================================================================================================================================================================================
# ===============================================================================================================================================================================================



#|================================================================================================|
#|~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~[     GAME TRANSLATIONS     ]~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~|
#|================================================================================================|

WIKIDEX_GAME_MAP = {
    "Gen1 Red_Blue": "RA",
    "Gen1 Red_Green": "V",
    "Gen1 Yellow": "A",
    "Gen2 Crystal": "cristal",
    "Gen2 Gold": "oro",
    "Gen2 Silver": "plata",
    "Gen3 Emerald": "E",
    "Gen3 FRLG": "RFVH",
    "Gen3 Ruby_Sapphire": "RZ",
    "Gen4 Diamond_Pearl": "DP",
    "Gen4 HGSS": "HGSS",
    "Gen4 Platinum": "Pt",
    "Gen5 BW_B2W2": "NB",   # TODO: Also N2B2
    "Gen6 XY_ORAS": "XY",   # TODO: Also ROZA
    "Gen7 SM_USUM": "SL",   # TODO: Also USUL
    "Gen7 LGPE": "LGPE",
    "Gen8 SwSh": "EpEc",
    "Gen8 LA": "LPA",
    "Gen8 BDSP": "DBPR",
    "Gen9 SV": "EP"
}
   



#|================================================================================================|
#|~~~~~~~~~~~~~~~~~~~~~~~~~~~[     SPECIES FORM TRANSLATIONS     ]~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~|
#|================================================================================================|

def type_():
    if "?" in split_name:
        spanish_type = " ?"
        form = " Question-Mark"
    if "acero" in split_name:
        spanish_type = " acero"
        form = " Steel"
    if "agua" in split_name:
        spanish_type = " agua"
        form = " Water"
    if "bicho" in split_name:
        spanish_type = " bicho"
        form = " Bug"
    if "dragón" in split_name:
        spanish_type = " dragón"
        form = " Dragon"
    if "eléctrico" in split_name:
        spanish_type = " eléctrico"
        form = " Electric"
    if "fantasma" in split_name:
        spanish_type = " fantasma"
        form = " Ghost"
    if "fuego" in split_name:
        spanish_type = " fuego"
        form = " Fire"
    if "hada" in split_name:
        spanish_type = " hada"
        form = " Fairy"
    if "hielo" in split_name:
        spanish_type = " hielo"
        form = " Ice"
    if "lucha" in split_name:
        spanish_type = " lucha"
        form = " Fighting"
    if "planta" in split_name:
        spanish_type = " planta"
        form = " Grass"
    if "psíquico" in split_name:
        spanish_type = " psíquico"
        form = " Pyschic"
    if "roca" in split_name:
        spanish_type = " roca"
        form = " Rock"
    if "siniestro" in split_name:
        spanish_type = " siniestro"
        form = " Dark"
    if "tierra" in split_name:
        spanish_type = " tierra"
        form = " Ground"
    if "veneno" in split_name:
        spanish_type = " veneno"
        form = " Posion"
    if "volador" in split_name:
        spanish_type = " volador"
        form = " Flying"

    # Arceus has type flag in filename, Silvally does not
    # So this splits accordingly
    if split_name == split_name.split(" tipo")[0]:
        split_name = split_name.split(spanish_type)[0]
    else:
        split_name = split_name.split(" tipo")[0]


WIKIDEX_POKE_FORM_TRANSLATION_MAP = {
    
}


#|================================================================================================|
#|~~~~~~~~~~~~~~~~~~~~~~~~~~~[     SPECIES FORM TRANSLATIONS     ]~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~|
#|================================================================================================|

# Pikachu Cosplay & Caps
("Pikachu", "aristócrata", "Cosplay-Aristocrat")
("Pikachu", "enmascarada", "Cosplay-libre")
("Pikachu", "erudita", "Cosplay-Phd")
("Pikachu", "roquera", "Cosplay-Rock Star")
("Pikachu", "superstar", "Cosplay-Pop Star")

("Pikachu", "Alola", "Cap-Alola")
("Pikachu", "Hoenn", "Cap-Hoenn")
("Pikachu", "Kalos", "Cap-Kalos")
("Pikachu", "original", "Cap-Original")
("Pikachu", "Sinnoh", "Cap-Sinnoh")
("Pikachu", "Teselia", "Cap-Unova")
("Pikachu", "compañero", "Cap-Partner")
("Pikachu", "trotamundos", "Cap-World")

# Spiky-eared Pichu
("Pichu", "picoreja", "Spiky-eared")

# Castform Weathers
("Castform", "lluvia", "Rainy")
("Castform", "nieve", "Snowy")
("Castform", "sol", "Sunny")

# Primal Kyogre & Groudon
("Kyogre", "primigenio", "Primal")
("Groudon", "primigenio", "Primal")

# Deoxys
("Deoxys", "ataque", "Attack")
("Deoxys", "defensa", "Defense")
("Deoxys", "velocidad", "Speed")

# Burmy & Wormadam Cloaks
("Burmy", "planta", "Plant Cloak")
("Burmy", "arena", "Sandy Cloak")
("Burmy", "basura", "Trash cloak")
("Wormadam", "planta", "Plant Cloak")
("Wormadam", "arena", "Sandy Cloak")
("Wormadam", "basura", "Trash cloak")

# Cherrim
("Cherrim", "encapotado", "Overcast")
("Cherrim", "soleado", "Sunshine")

# Shellos & Gastrodon East/West
("Shellos", "oeste", "West")
("Shellos", "este", "East")
("Gastrodon", "oeste", "West")
("Gastrodon", "este", "East")

# Rotom Appliances
("Rotom", "calor", "Heat")
("Rotom", "lavado", "Wash")
("Rotom", "frío", "Frost")
("Rotom", "ventilador", "Fan")
("Rotom", "corte", "Mow")

# Giratina
("Giratina", "modificada", "Altered")
("Giratina", "origen", "Origin")

# Shaymin
("Shaymin", "tierra", "Land")
("Shaymin", "cielo", "Sky")

# Basculin Stripes
("Basculin", "raya azul", "Blue-Striped")
("Basculin", "raya roja", "Red-Striped")

# Darmanitan Modes
("Darmanitan", "daruma", "Zen")

# Deerling & Sawsbuck Seasons
("Deerling", "primavera", "Spring")
("Deerling", "verano", "Summer")
("Deerling", "otoño", "Autumn")
("Deerling", "invierno", "Winter")
("Sawsbuck", "primavera", "Spring")
("Sawsbuck", "verano", "Summer")
("Sawsbuck", "otoño", "Autumn")
("Sawsbuck", "invierno", "Winter")

# Forces of nature forms
("Tornadus", "avatar", "Incarnate")
("Tornadus", "tótem", "Therian")
("Thundurus", "avatar", "Incarnate")
("Thundurus", "tótem", "Therian")
("Landorus", "avatar", "Incarnate")
("Landorus", "tótem", "Therian")

# Kyurem Fusions
("Kyurem", "negro activo", "Black Overdrive")
("Kyurem", "negro inactivo", "Black")
("Kyurem", "negro", "Black")
("Kyurem", "blanco activo", "White Overdrive")
("Kyurem", "blanco inactivo", "White")
("Kyurem", "blanco", "White")

# Keldeo
("Keldeo", "brío", "Resolute")
("Keldeo", "", "Ordinary")

# Meloetta
("Meloetta", "lírica", "Aria")
("Meloetta", "danza", "Pirouette")

# Genesect
("Genesect", "fulgoROM", "Shock Drive")
("Genesect", "piroROM", "Burn Drive")
("Genesect", "crioROM", "Chill Drive")
("Genesect", "hidroROM", "Douse Drive")

# Ash Greninja
("Greninja", "Ash", "Ash")

# Vivillon Patterns
("Vivillon", "continental", "Continental")
("Vivillon", "desierto", "Sandstorm")
("Vivillon", "estepa", "High Plains")
("Vivillon", "fantasía", "Fancy")
("Vivillon", "floral", "Meadow")
("Vivillon", "isleño", "Archipelago")
("Vivillon", "jungla", "Jungle")
("Vivillon", "marino", "Marine")
("Vivillon", "moderno", "Modern")
("Vivillon", "monzón", "Monsoon")
("Vivillon", "oasis", "River")
("Vivillon", "océano", "Ocean")
("Vivillon", "oriental", "Elegant")
("Vivillon", "pantano", "Savanna")
("Vivillon", "Poké Ball", "Poké Ball")
("Vivillon", "polar", "Icy Snow")
("Vivillon", "solar", "Sun")
("Vivillon", "taiga", "Polar")
("Vivillon", "tundra", "Tundra")
("Vivillon", "vergel", "Garden")


# Flabebe, Floette, and Florges colors
("Flabébé", "amarilla", "Yellow Flower")
("Flabébé", "azul", "Blue Flower")
("Flabébé", "blanca", "White Flower")
("Flabébé", "naranja", "Orange Flower")
("Flabébé", "roja", "Red Flower")
("Floette", "amarilla", "Yellow Flower")
("Floette", "azul", "Blue Flower")
("Floette", "blanca", "White Flower")
("Floette", "naranja", "Orange Flower")
("Floette", "roja", "Red Flower")
("Floette", "eterna", "Eternal Flower")
("Florges", "amarilla", "Yellow Flower")
("Florges", "azul", "Blue Flower")
("Florges", "blanca", "White Flower")
("Florges", "naranja", "Orange Flower")
("Florges", "roja", "Red Flower")

# Furfrou Trims
("Furfrou", "aristocrático", "La Reine Trim")
("Furfrou", "caballero", "Dandy Trim")
("Furfrou", "corazón", "Heart Trim")
("Furfrou", "dama", "Matron Trim")
("Furfrou", "estrella", "Star Trim")
("Furfrou", "faraónico", "Pharaoh Trim")
("Furfrou", "kabuki", "Kabuki")
("Furfrou", "rombo", "Diamond Trim")
("Furfrou", "señorita", "Debutante Trim")

# Aegislash
("Aegislash", "escudo", "Shield")
("Aegislash", "filo", "Blade")

# Pumpkaboo and Gourgeist Sizes
("Pumpkaboo", "pequeño", "Small Size")
("Pumpkaboo", "", "Average Size")
("Pumpkaboo", "grande", "Large Size")
("Pumpkaboo", "extragrande", "Super Size")
("Gourgeist", "pequeño", "Small Size")
("Gourgeist", "", "Average Size")
("Gourgeist", "grande", "Large Size")
("Gourgeist", "extragrande", "Super Size")

# Xerneas
("Xerneas", "relajada", "Neutral")
("Xerneas", "", "Active")

# Zygarde
("Zygarde", "al 10%", "10%")
("Zygarde", "completo", "Complete")
("Zygarde", "", "50%")

# Hoopa
("Hoopa", "", "Confined")
("Hoopa", "desatado", "Unbound")

# Oricorio
("Oricorio", "animado", "Pom-Pom Style")
("Oricorio", "apasionado", "Baile Style")
("Oricorio", "plácido", "Pa'u Style")
("Oricorio", "refinado", "Sensu Style")

# Lycanroc
("Lycanroc", "diurno", "Midday")
("Lycanroc", "nocturno", "Midnight")
("Lycanroc", "crepuscular", "Dusk")

# Wishiwashi
("Wishiwashi", "individual", "Solo")
("Wishiwashi", "banco", "School")

# Minior
("Minior", "meteorito", "Meteor")
("Minior", "amarillo", "Yellow Core")
("Minior", "añil", "Indigo Core")
("Minior", "azul", "Blue Core")
("Minior", "naranja", "Orange Core")
("Minior", "rojo", "Red Core")
("Minior", "verde", "Green Core")
("Minior", "violeta", "Violet Core")
# Shiny cores all the same color?
("Minior", "núcleo", "Core")

# Mimikyu
("Mimikyu", "", "Disguised")
("Mimikyu", "descubierto", "Busted")

# Necrozma
("Necrozma", "alas del alba", "Dawn Wings")
("Necrozma", "melena crepuscular", "Dusk Mane")

# Magearna
("Magearna", "vetusta", "Original Color")

# Cramorant
("Cramorant", "engulletodo", "Gorging")
("Cramorant", "tragatodo", "Gulping")

# Toxtricity
("Toxtricity", "aguda", "Amped")
("Toxtricity", "grave", "Low-Key")

# Alcremie Creams & Sweets
# Default Alcremie is Vanilla Cream-Strawberry Sweet, so continue
if "Alcremie" == split_name:
    continue
if "Alcremie" in split_name:
    # Ends with, not in because sweet names overlap with come Cream names
    if split_name.endswith("corazón") and not "crema de té corazón" in split_name:
        form = "Love Sweet"
    if split_name.endswith("estrella"):
        form = "Star Sweet"
    if split_name.endswith("flor"):
        form = "Flower Sweet"
    if split_name.endswith("fruto"):
        form = "Berry Sweet"
    if split_name.endswith("lazo"):
        form = "Ribbon Sweet"
    if split_name.endswith("trébol"):
        form = "Clover Sweet"

    if "crema de limón" in split_name:
        ("Alcremie", "crema de limón", "Lemon Cream-" + form)
    if "crema de menta" in split_name:
        ("Alcremie", "crema de menta", "Mint Cream-" + form)
    # Site left out most of the corazón, so I left it out too since theres no te anywhere else
    if "crema de té" in split_name:
        ("Alcremie", "crema de té", "Matcha Cream-" + form)
    if "crema de vainilla" in split_name:
        ("Alcremie", "crema de vainilla", "Vanilla Cream-" + form)
    if "crema rosa" in split_name:
        ("Alcremie", "crema rosa", "Ruby Cream-" + form)
    if "crema salada" in split_name:
        ("Alcremie", "crema salada", "Salted Cream-" + form)
    if "mezcla caramelo" in split_name:
        ("Alcremie", "mezcla caramelo", "Caramel Swirl-" + form)
    if "mezcla rosa" in split_name:
        ("Alcremie", "mezcla rosa", "Ruby Swirl-" + form)
    if "tres sabores" in split_name:
        ("Alcremie", "tres sabores", "Rainbow Swirl-" + form)

    # On website there is no notation if it is Strawberry sweet form, so adding that here
    if form.endswith("-"):
        form += "Strawberry Sweet"
# Since shiny Alcremies all have the same base color, split name by sweet
if game.endswith("Shiny"):
    ("Alcremie", "corazón", "Love Sweet")
    ("Alcremie", "estrella", "Star Sweet")
    ("Alcremie", "flor", "Flower Sweet")
    ("Alcremie", "fruto", "Berry Sweet")
    ("Alcremie", "lazo", "Ribbon Sweet")
    ("Alcremie", "trébol", "Clover Sweet")


# Eiscue
("Eiscue", "cara deshielo", "Noice Face")
("Eiscue", "", "Ice Face")

# Morpeko
("Morpeko", "", "Full Belly")
("Morpeko", "voraz", "Hangry")

# Zacian and Zamazenta
("Zacian", "", "Hero of Many Battles")
("Zacian", "espada suprema", "Crowned Sword")
("Zamazenta", "", "Hero of Many Battles")
("Zamazenta", "escudo supremo", "Crowned Shield")

# Eternatus Eternamax
("Eternatus", "Dinamax infinito", "Eternamax")

# Urshifu
("Urshifu", "brusco", "Single Strike")
("Urshifu", "fluido", "Rapid Strike")

# Zarude
("Zarude", "papá", "Dada")

# Calyrex Ridings
("Calyrex", "jinete espectral", "Shadow Rider")
("Calyrex", "jinete glacial", "Ice Rider")

