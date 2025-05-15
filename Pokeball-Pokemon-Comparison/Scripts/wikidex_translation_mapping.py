#|================================================================================================|
#|~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~[     GAME TRANSLATIONS     ]~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~|
#|================================================================================================|

# TODO: Convert to dicts
def game_translate(s):
    if s == "Rojo y Azul":
        return("Red-Blue")
    if s == "Verde":
        return("Red-Green")
    if s == "Amarillo":
        return("Yellow")
    if s == "Oro":
        return("Gold")
    if s == "Plata":
        return("Silver")
    # Because crystal sprites are default animated from this site
        # Will save first frame later for statics
    if s == "Cristal":
        return("Crystal Animated")
    if s == "Rubí y Zafiro":
        return("Ruby-Sapphire")
    # Because emerald sprites are default animated from this site
        # Will save first frame later for statics    
    if s == "Esmeralda":
        return("Emerald Animated")
    if s == "Rojo Fuego y Verde Hoja":
        return("FireRed-LeafGreen")
    # Because DPP & HGSS sprites are default static on this site
        # Will retrieve animated sprites from bulbagarden archives
    if s == "Diamante y Perla":
        return("Diamond-Pearl Static")
    if s == "Platino":
        return("Platinum Static")
    if s == "Oro HeartGold y Plata SoulSilver":
        return("HGSS Static")
    if s == "Negro y Blanco":
        return("Black-White")
    if s == "Negro y Blanco 2":
        return("Black2-White2")
    if s == "X y Pokémon Y":
        return("XY")
    if s == "Rubí Omega y Pokémon Zafiro Alfa":
        return("ORAS")
    if s == "Sol y Pokémon Luna":
        return("Sun-Moon")
    if s == "Ultrasol y Pokémon Ultraluna":
        return("USUM")
    if s == "Let's Go, Pikachu! y Pokémon Let's Go, Eevee!":
        return("Let's Go")
    if s == "Espada y Pokémon Escudo":
        return("Sword-Shield")
    



#|================================================================================================|
#|~~~~~~~~~~~~~~~~~~~~~~~~~~~[     UNIVERSAL FORM TRANSLATIONS     ]~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~|
#|================================================================================================|

# TODO: Universal forms (including f/m)
# if split_name.startswith("Mega") and split_name != "Meganium":
#     mega = " Mega"
#     split_name = split_name.split("Mega-")[1]
#     if split_name.endswith("X"):
#         mega = " MegaX"
#         split_name = split_name.split(" X")[0]
#     if split_name.endswith("Y"):
#         mega = " MegaY"
#         split_name = split_name.split(" Y")[0]
# # Handling Dynamax (Except Eternatus Eternamax)
# dyna = ""
# if split_name.endswith("Dinamax") and not split_name.startswith("\nEternatus"):
#     dyna = " Dynamax"
#     split_name = split_name.split(" Dinamax")[0]
# # Handling Gigantamax
# giganta = ""
# if split_name.endswith("Gigamax"):
#     giganta = " Gigantamax"
#     split_name = split_name.split(" Gigamax")[0]
# # Handling regions
# region = ""
# if split_name.endswith("de Alola"):
#     region = " Alolan"
#     split_name = split_name.split(" de Alola")[0]
# if split_name.endswith("de Galar"):
#     region = " Galarian"
#     split_name = split_name.split(" de Galar")[0]

# # Doing forms becuase accumulation over all generations, shiny, static/animated, and back sprites would easily get into the thousands
# form = ""
# # Nidoran Genders in name
# if "Nidoran" in split_name and gender != "":
#     if gender == " f":
#         split_name = split_name.replace("hembra", "f")
#     if gender == " m":
#         split_name = split_name.replace("macho", "m")




#|================================================================================================|
#|~~~~~~~~~~~~~~~~~~~~~~~~~~~[     SPECIES FORM TRANSLATIONS     ]~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~|
#|================================================================================================|

def type_form_translate_split():
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




#|================================================================================================|
#|~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~[     SPRITE TRANSLATIONS     ]~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~|
#|================================================================================================|

def sprite_link_dict_entry(gen, link, animated = False):
    back = False
    shiny = False

    # Get game if link isn't to back sprites (since those are generationally recycled)
    if not link.text == "E" and not link.text == "EV":
        game = get_game(link)
    # Getting shiny, back parameters
    if link.text == "V":
        shiny = True
    if link.text == "E":
        back = True
    if link.text == "EV":
        back = True
        shiny = True


split_seperators_by_game = {
    "Gen1 Red-Green": " V",
    "Gen1 Red-Blue": " RA",
    "Gen1 Yellow": " A",
    "Gen1-Back": " espalda",
    "Gen2 Gold": " oro",
    "Gen2 Gold Shiny": " oro",
    "Gen2 Silver": " plata",
    "Gen2 Silver Shiny": " plata",
    "Gen2 Crystal Animated": " cristal",
    "Gen2 Crystal Animated Shiny": " cristal",
    "Gen2-Back": " espalda",
    "Gen2-Back Shiny": " espalda",
    "Gen3 Ruby-Sapphire": " RZ",
    "Gen3 Ruby-Sapphire Shiny": " RZ",
    "Gen3 Emerald Animated": " E",
    "Gen3 Emerald Animated Shiny": " E",
    "Gen3 FireRed-LeafGreen": "RFVH",
    "Gen3 FireRed-LeafGreen Shiny": "RFVH",
    "Gen3-Back": " espalda",
    "Gen3-Back Shiny": " espalda",
    "Gen4 Diamond-Pearl Static": " DP",
    "Gen4 Diamond-Pearl Static Shiny": " DP",
    "Gen4 Platinum Static": " Pt",
    "Gen4 Platinum Static Shiny": " Pt",
    "Gen4 HGSS Static": " HGSS",
    "Gen4 HGSS Static Shiny": " HGSS",
    "Gen4-Back": " espalda",
    "Gen4-Back Shiny": " espalda",
    "Gen5 Black-White Static": " NB",
    "Gen5 Black-White Static Shiny": " NB",
    "Gen5 Black2-White2 Static": " N2B2",
    "Gen5 Black2-White2 Static Shiny": " N2B2",
    "Gen5-Back Static": " espalda",
    "Gen5-Back Static Shiny": " espalda",
    "Gen5 Black-White Animated": " NB",
    "Gen5 Black-White Animated Shiny": " NB",
    "Gen5 Black2-White2 Animated": " N2B2",
    "Gen5 Black2-White2 Animated Shiny": " N2B2",
    "Gen5-Back Animated": " espalda",
    "Gen5-Back Animated Shiny": " espalda",
    "Gen6 XY Static": " XY",
    "Gen6 XY Static Shiny": " XY",
    "Gen6 ORAS Static": " ROZA",
    "Gen6 ORAS Static Shiny": " XY",
    "Gen6-Back Static": " espalda",
    "Gen6-Back Static Shiny": " espalda",
    "Gen6 XY Animated": " XY",
    "Gen6 XY Animated Shiny": " XY",
    "Gen6 ORAS Animated": " ROZA",
    "Gen6 ORAS Animated Shiny": " ROZA",
    "Gen6-Back Animated": " espalda",
    "Gen6-Back Animated Shiny": " espalda",
    "Gen7 Sun-Moon Static": " SL",
    "Gen7 Sun-Moon Static Shiny": " SL",
    "Gen7 USUM Static": " USUL",
    "Gen7 USUM Static Shiny": " USUL",
    "Gen7-Back Static": " espalda",
    "Gen7-Back Static Shiny": " espalda",
    "Gen7 Sun-Moon Animated": " SL",
    "Gen7 Sun-Moon Animated Shiny": " SL",
    "Gen7 USUM Animated": " USUL",
    "Gen7 USUM Animated Shiny": " USUL",
    "Gen7-Back Animated": " espalda",
    "Gen7-Back Animated Shiny": " espalda",
    "Gen8 Sword-Shield Static": " EpEc",
    "Gen8 Sword-Shield Static Shiny": " EpEc",
    "Gen8-Back Static": " espalda",
    "Gen8 Sword-Shield Animated": " EpEc",
    "Gen8 Sword-Shield Animated Shiny": " EpEc",
    "Gen8-Back Animated": " espalda",
    "Gen8-Back Animated Shiny": " espalda"
}

# Pikachu Cosplay & Caps
# Not sure if this is the default cosplay image or what? But it's basically a normal Pikachu
if "Pikachu coqueta" in split_name:
    continue
form_translate_split("Pikachu", "aristócrata", "Cosplay-Aristocrat")
form_translate_split("Pikachu", "enmascarada", "Cosplay-libre")
form_translate_split("Pikachu", "erudita", "Cosplay-Phd")
form_translate_split("Pikachu", "roquera", "Cosplay-Rock Star")
form_translate_split("Pikachu", "superstar", "Cosplay-Pop Star")
form_translate_split("Pikachu", "Alola", "Cap-Alola")
form_translate_split("Pikachu", "Hoenn", "Cap-Hoenn")
form_translate_split("Pikachu", "Kalos", "Cap-Kalos")
form_translate_split("Pikachu", "original", "Cap-Original")
form_translate_split("Pikachu", "Sinnoh", "Cap-Sinnoh")
form_translate_split("Pikachu", "Teselia", "Cap-Unova")
form_translate_split("Pikachu", "compañero", "Cap-Partner")
form_translate_split("Pikachu", "trotamundos", "Cap-World")

# Spiky-eared Pichu
form_translate_split("Pichu", "picoreja", "Spiky-eared")

# Unown Characters
if "Unown" in split_name:
    # Default sprite image for unown is Unown A, so skip in favor of A
    if "Unown" == split_name:
        continue
    # Get last character (Unown form)
    form = " " + split_name[-1]
    # This splices just Unown name (since ? and ! don't have spaces but the characters do)
    split_name = split_name[0:5]
    # Can't have question marks in file names on Windows
    if form == " ?":
        form = " Q-Mark"

# Castform Weathers
form_translate_split("Castform", "lluvia", "Rainy")
form_translate_split("Castform", "nieve", "Snowy")
form_translate_split("Castform", "sol", "Sunny")

# Primal Kyogre & Groudon
form_translate_split("Kyogre", "primigenio", "Primal")
form_translate_split("Groudon", "primigenio", "Primal")

# Deoxys
form_translate_split("Deoxys", "ataque", "Attack")
form_translate_split("Deoxys", "defensa", "Defense")
form_translate_split("Deoxys", "velocidad", "Speed")
# Deoxys only available in FRLG as defense or attack form dependent on game
    # Split must work fine for leading characters, but not trailing. Hence this workaround of sorts
if names[i].text.startswith("\nDeoxys defensa"):
    form = " Defense"
    split_name = names[i].text.split(" defensa")[0]
    split_name = split_name.split("\n")[1]

# Burmy & Wormadam Cloaks
form_translate_split("Burmy", "planta", "Plant Cloak")
form_translate_split("Burmy", "arena", "Sandy Cloak")
form_translate_split("Burmy", "basura", "Trash cloak")
form_translate_split("Wormadam", "planta", "Plant Cloak")
form_translate_split("Wormadam", "arena", "Sandy Cloak")
form_translate_split("Wormadam", "basura", "Trash cloak")

# Cherrim
form_translate_split("Cherrim", "encapotado", "Overcast")
form_translate_split("Cherrim", "soleado", "Sunshine")

# Shellos & Gastrodon East/West
    # Done a lil differently since "este" (East) is contained in "oeste" (West)
if "Shellos" in split_name or "Gastrodon" in split_name:
    if "oeste" in split_name:
        form = " West"
        split_name = split_name.split(" oeste")[0]
    else:
        form = " East"
        split_name = split_name.split(" este")[0]

# Rotom Appliances
form_translate_split("Rotom", "calor", "Heat")
form_translate_split("Rotom", "lavado", "Wash")
form_translate_split("Rotom", "frío", "Frost")
form_translate_split("Rotom", "ventilador", "Fan")
form_translate_split("Rotom", "corte", "Mow")

# Giratina
form_translate_split("Giratina", "modificada", "Altered")
form_translate_split("Giratina", "origen", "Origin")

# Shaymin
form_translate_split("Shaymin", "tierra", "Land")
form_translate_split("Shaymin", "cielo", "Sky")

# Arceus Types
if "Arceus" == split_name:
    form = " Normal"
if "Arceus" in split_name and split_name != "Arceus":
    type_form_translate_split()

# Basculin Stripes
form_translate_split("Basculin", "raya azul", "Blue-Striped")
form_translate_split("Basculin", "raya roja", "Red-Striped")

# Darmanitan Modes
if "Darmanitan" == split_name:
    form = "Standard"
else:
    form_translate_split("Darmanitan", "daruma", "Zen")

# Deerling & Sawsbuck Seasons
form_translate_split("Deerling", "primavera", "Spring")
form_translate_split("Deerling", "verano", "Summer")
form_translate_split("Deerling", "otoño", "Autumn")
form_translate_split("Deerling", "invierno", "Winter")
form_translate_split("Sawsbuck", "primavera", "Spring")
form_translate_split("Sawsbuck", "verano", "Summer")
form_translate_split("Sawsbuck", "otoño", "Autumn")
form_translate_split("Sawsbuck", "invierno", "Winter")

# Forces of nature forms
form_translate_split("Tornadus", "avatar", "Incarnate")
form_translate_split("Tornadus", "tótem", "Therian")
form_translate_split("Thundurus", "avatar", "Incarnate")
form_translate_split("Thundurus", "tótem", "Therian")
form_translate_split("Landorus", "avatar", "Incarnate")
form_translate_split("Landorus", "tótem", "Therian")

# Kyurem Fusions
if "negro" in split_name:
    if "activo" in split_name:
        form_translate_split("Kyurem", "negro activo", "Black Overdrive")
    if "inactivo" in split_name:
        form_translate_split("Kyurem", "negro inactivo", "Black")
    if split_name == "Kyurem negro":
        form_translate_split("Kyurem", "negro", "Black")
if "blanco" in split_name:
    if "activo" in split_name:
        form_translate_split("Kyurem", "blanco activo", "White Overdrive")
    if "inactivo" in split_name:
        form_translate_split("Kyurem", "blanco inactivo", "White")
    if split_name == "Kyurem blanco":
        form_translate_split("Kyurem", "blanco", "White")

# Keldeo
if "Keldeo" in split_name and "brío" in split_name:
    form_translate_split("Keldeo", "brío", "Resolute")
else:
    if "Keldeo" == split_name:
        form = " Ordinary"

# Meloetta
form_translate_split("Meloetta", "lírica", "Aria")
form_translate_split("Meloetta", "danza", "Pirouette")

# Genesect
form_translate_split("Genesect", "fulgoROM", "Shock Drive")
form_translate_split("Genesect", "piroROM", "Burn Drive")
form_translate_split("Genesect", "crioROM", "Chill Drive")
form_translate_split("Genesect", "hidroROM", "Douse Drive")
# Website named Genesect differenlt in gen8:
form_translate_split("Genesect", "disco amarillo", "Shock Drive")
form_translate_split("Genesect", "disco rojo", "Burn Drive")
form_translate_split("Genesect", "disco blanco", "Chill Drive")
form_translate_split("Genesect", "disco azul", "Douse Drive")

# Ash Greninja
form_translate_split("Greninja", "Ash", "Ash")

# Vivillon Patterns
form_translate_split("Vivillon", "continental", "Continental")
form_translate_split("Vivillon", "desierto", "Sandstorm")
form_translate_split("Vivillon", "estepa", "High Plains")
form_translate_split("Vivillon", "fantasía", "Fancy")
form_translate_split("Vivillon", "floral", "Meadow")
form_translate_split("Vivillon", "isleño", "Archipelago")
form_translate_split("Vivillon", "jungla", "Jungle")
form_translate_split("Vivillon", "marino", "Marine")
form_translate_split("Vivillon", "moderno", "Modern")
form_translate_split("Vivillon", "monzón", "Monsoon")
form_translate_split("Vivillon", "oasis", "River")
form_translate_split("Vivillon", "océano", "Ocean")
form_translate_split("Vivillon", "oriental", "Elegant")
form_translate_split("Vivillon", "pantano", "Savanna")
form_translate_split("Vivillon", "Poké Ball", "Poké Ball")
form_translate_split("Vivillon", "polar", "Icy Snow")
form_translate_split("Vivillon", "solar", "Sun")
form_translate_split("Vivillon", "taiga", "Polar")
form_translate_split("Vivillon", "tundra", "Tundra")
form_translate_split("Vivillon", "vergel", "Garden")


# Flabebe, Floette, and Florges colors
# Unused form in XY
if "Floette" in split_name and "eterna" in split_name:
    continue
form_translate_split("Flabébé", "amarilla", "Yellow Flower")
form_translate_split("Flabébé", "azul", "Blue Flower")
form_translate_split("Flabébé", "blanca", "White Flower")
form_translate_split("Flabébé", "naranja", "Orange Flower")
form_translate_split("Flabébé", "roja", "Red Flower")
form_translate_split("Floette", "amarilla", "Yellow Flower")
form_translate_split("Floette", "azul", "Blue Flower")
form_translate_split("Floette", "blanca", "White Flower")
form_translate_split("Floette", "naranja", "Orange Flower")
form_translate_split("Floette", "roja", "Red Flower")
form_translate_split("Florges", "amarilla", "Yellow Flower")
form_translate_split("Florges", "azul", "Blue Flower")
form_translate_split("Florges", "blanca", "White Flower")
form_translate_split("Florges", "naranja", "Orange Flower")
form_translate_split("Florges", "roja", "Red Flower")

# Furfrou Trims
form_translate_split("Furfrou", "aristocrático", "La Reine Trim")
form_translate_split("Furfrou", "caballero", "Dandy Trim")
form_translate_split("Furfrou", "corazón", "Heart Trim")
form_translate_split("Furfrou", "dama", "Matron Trim")
form_translate_split("Furfrou", "estrella", "Star Trim")
form_translate_split("Furfrou", "faraónico", "Pharaoh Trim")
form_translate_split("Furfrou", "kabuki", "Kabuki")
form_translate_split("Furfrou", "rombo", "Diamond Trim")
form_translate_split("Furfrou", "señorita", "Debutante Trim")

# Aegislash
form_translate_split("Aegislash", "escudo", "Shield")
form_translate_split("Aegislash", "filo", "Blade")

# Pumpkaboo and Gourgeist Sizes
if "Pumpkaboo" == split_name or "Gourgeist" == split_name:
    # Average sizes have no indication in filename on this website
    form = " 1Average Size"
else:
    form_translate_split("Pumpkaboo", "pequeño", "0Small Size")
    form_translate_split("Pumpkaboo", "grande", "2Large Size")
    form_translate_split("Pumpkaboo", "extragrande", "3Super Size")
    form_translate_split("Gourgeist", "pequeño", "0Small Size")
    form_translate_split("Gourgeist", "grande", "2Large Size")
    form_translate_split("Gourgeist", "extragrande", "3Super Size")

# Xerneas
if "Xerneas" == split_name:
    form = " Active"
else:
    form_translate_split("Xerneas", "relajada", "Neutral")

# Zygarde
# Cells & Nuclei aren't really sprites, so continue
if split_name == "Zygarde célula" or split_name == "Zygarde núcleo":
    continue
if "Zygarde" == split_name:
    form = " 50%"
else:
    form_translate_split("Zygarde", "al 10%", "10%")
    form_translate_split("Zygarde", "completo", "Complete")

# Hoopa
if "Hoopa" == split_name:
    form = " Confined"
else:
    form_translate_split("Hoopa", "desatado", "Unbound")

# Oricorio
form_translate_split("Oricorio", "animado", "Pom-Pom Style")
form_translate_split("Oricorio", "apasionado", "Baile Style")
form_translate_split("Oricorio", "plácido", "Pa'u Style")
form_translate_split("Oricorio", "refinado", "Sensu Style")

# Lycanroc
form_translate_split("Lycanroc", "diurno", "Midday")
form_translate_split("Lycanroc", "nocturno", "Midnight")
form_translate_split("Lycanroc", "crepuscular", "Dusk")

# Wishiwashi
form_translate_split("Wishiwashi", "individual", "Solo")
form_translate_split("Wishiwashi", "banco", "School")

# Silvally Types
if "Silvally" == split_name:
    form = " Normal"
if "Silvally" in split_name and split_name != "Silvally":
    type_form_translate_split()

# Minior
form_translate_split("Minior", "meteorito", "Meteor")
form_translate_split("Minior", "amarillo", "Yellow Core")
form_translate_split("Minior", "añil", "Indigo Core")
form_translate_split("Minior", "azul", "Blue Core")
form_translate_split("Minior", "naranja", "Orange Core")
form_translate_split("Minior", "rojo", "Red Core")
form_translate_split("Minior", "verde", "Green Core")
form_translate_split("Minior", "violeta", "Violet Core")
# Shiny cores all the same color?
form_translate_split("Minior", "núcleo", "Core")

# Mimikyu
if "Mimikyu" == split_name:
    form = " Disguised"
else:
    form_translate_split("Mimikyu", "descubierto", "Busted")

# Necrozma
form_translate_split("Necrozma", "alas del alba", "Dawn Wings")
form_translate_split("Necrozma", "melena crepuscular", "Dusk Mane")
if "Ultra-Necrozma" == split_name:
    form = " Ultra"
    split_name = split_name.split("Ultra-")[1]

# Magearna
form_translate_split("Magearna", "vetusta", "Original Color")

# Cramorant
form_translate_split("Cramorant", "engulletodo", "Gorging")
form_translate_split("Cramorant", "tragatodo", "Gulping")

# Toxtricity
form_translate_split("Toxtricity", "aguda", "Amped")
form_translate_split("Toxtricity", "grave", "Low-Key")

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
        form_translate_split("Alcremie", "crema de limón", "Lemon Cream-" + form)
    if "crema de menta" in split_name:
        form_translate_split("Alcremie", "crema de menta", "Mint Cream-" + form)
    # Site left out most of the corazón, so I left it out too since theres no te anywhere else
    if "crema de té" in split_name:
        form_translate_split("Alcremie", "crema de té", "Matcha Cream-" + form)
    if "crema de vainilla" in split_name:
        form_translate_split("Alcremie", "crema de vainilla", "Vanilla Cream-" + form)
    if "crema rosa" in split_name:
        form_translate_split("Alcremie", "crema rosa", "Ruby Cream-" + form)
    if "crema salada" in split_name:
        form_translate_split("Alcremie", "crema salada", "Salted Cream-" + form)
    if "mezcla caramelo" in split_name:
        form_translate_split("Alcremie", "mezcla caramelo", "Caramel Swirl-" + form)
    if "mezcla rosa" in split_name:
        form_translate_split("Alcremie", "mezcla rosa", "Ruby Swirl-" + form)
    if "tres sabores" in split_name:
        form_translate_split("Alcremie", "tres sabores", "Rainbow Swirl-" + form)

    # On website there is no notation if it is Strawberry sweet form, so adding that here
    if form.endswith("-"):
        form += "Strawberry Sweet"
# Since shiny Alcremies all have the same base color, split name by sweet
if game.endswith("Shiny"):
    form_translate_split("Alcremie", "corazón", "Love Sweet")
    form_translate_split("Alcremie", "estrella", "Star Sweet")
    form_translate_split("Alcremie", "flor", "Flower Sweet")
    form_translate_split("Alcremie", "fruto", "Berry Sweet")
    form_translate_split("Alcremie", "lazo", "Ribbon Sweet")
    form_translate_split("Alcremie", "trébol", "Clover Sweet")


# Eiscue
if "Eiscue" == split_name:
    form = "Ice Face"
else:
    form_translate_split("Eiscue", "cara deshielo", "Noice Face")

# Morpeko
if "Morpeko" == split_name:
    form = "Full Belly"
else:
    form_translate_split("Morpeko", "voraz", "Hangry")

# Zacian and Zamazenta
if "Zacian" == split_name:
    form = "Hero of Many Battles"
else:
    form_translate_split("Zacian", "espada suprema", "Crowned Sword")
if "Zamazenta" == split_name:
    form = "Hero of Many Battles"
else:
    form_translate_split("Zamazenta", "escudo supremo", "Crowned Shield")

# Eternatus Eternamax
form_translate_split("Eternatus", "Dinamax infinito", "Eternamax")

# Urshifu
form_translate_split("Urshifu", "brusco", "Single Strike")
form_translate_split("Urshifu", "fluido", "Rapid Strike")

# Zarude
form_translate_split("Zarude", "papá", "Dada")

# Calyrex Ridings
form_translate_split("Calyrex", "jinete espectral", "Shadow Rider")
form_translate_split("Calyrex", "jinete glacial", "Ice Rider")

# Type: Null name is completely translated
if split_name == "Código Cero":
    split_name = "Type Null"