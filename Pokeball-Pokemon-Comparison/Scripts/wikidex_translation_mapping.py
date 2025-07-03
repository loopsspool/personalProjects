from translation_utils import EXCLUDE_TRANSLATIONS_MAP, extract_gen_num_from_my_filename

#|================================================================================================|
#|~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~[     EXCLUSIONS     ]~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~|
#|================================================================================================|

# NOTE: Just because you don't see the sprites on the respective game list DOES NOT MEAN THEY DON'T EXIST -- check URL generated, they may just not be linked properly
    # Helpful as well: https://www.wikidex.net/wiki/WikiDex:Proyecto_Pok%C3%A9dex#P%C3%A1ginas_del_proyecto
# Technically no static Crystal or emerald front sprites & they're gifs so might not color convert to apng nicely programatically, but Bulba has all stills for these gens, so all good as long as bulba scraped first
# Tehcnically no gen8 static shiny back sprites but the animateds exist, so we can pull first frame
# Take careful look at backs since wikidex lumps them by gen, not game
WIKIDEX_DOESNT_HAVE_IMGS_FOR = {
    "no animated images below gen5 except emerald & crystal": lambda my_filename: "-Animated" in my_filename and extract_gen_num_from_my_filename(my_filename)<5 and "Gen3 Emerald" not in my_filename and "Gen2 Crystal" not in my_filename,
    "no LGPE back sprites except meltan and melmetal": lambda my_filename: "Gen7_LGPE" in my_filename and not any(poke_num in my_filename for poke_num in ("0808", "0809")),
    "no animated BDSP sprites": lambda my_filename: "Gen8 BDSP" in my_filename and "-Animated" in my_filename,
    "no back sprites for these games": lambda my_filename: "-Back" in my_filename and any(game in my_filename for game in ("Gen8_BDSP", "Gen8_LA", "Gen9_SV")),
    "no gen7 sprites except gen7 pokes, forms, and glameow": lambda my_filename: "Gen7" in my_filename and not ((722 <= int(my_filename[:5]) <=809) or "0431" in my_filename or any(form in my_filename for form in ("-Region_Alola", "-Form_Cap_", "-Form_Ash", "-Form_Complete", "-Form_10%"))),
    "no gen8 back sprites except gen8 pokes and forms": lambda my_filename: "Gen8_" in my_filename and "-Back" in my_filename and not ((810 <= int(my_filename[:5]) <=905) or any(exception in my_filename for exception in ("0109", "0133", "0808", "0809", "-Region_Galar", "-Gigantamax"))),
    "no animated LA sprites except hisuian forms": lambda my_filename: "Gen8 LA" in my_filename and "-Animated" in my_filename and "-Shiny" not in my_filename and not "-Region_Hisui" in my_filename,
    "no animated shiny LA sprites except hisuian forms, white basculin, and new species": lambda my_filename: "Gen8 LA" in my_filename and "-Animated" in my_filename and "-Shiny" in my_filename and not (899 <= int(my_filename[:5]) <=905 or any(form in my_filename for form in ("-Region_Hisui", "-Form_White_Striped")))
}




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
    "Gen5 BW_B2W2": "NB",
    "Gen6 XY_ORAS": "XY",
    "Gen7 SM_USUM": "SL",
    "Gen7 LGPE": "LGPE",
    "Gen8 SwSh": "EpEc",
    "Gen8 LA": "LPA",
    "Gen8 BDSP": "DBPR",
    "Gen9 SV": "EP"
}


WIKIDEX_ALT_GAME_MAP = {
    "BW_B2W2": "N2B2",
    "XY_ORAS": "ROZA",
    "SM_USUM": "USUL"
}




#|================================================================================================|
#|~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~[     NAME ADJUSTMENTS     ]~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~|
#|================================================================================================|

# TODO: Gen 9 Pokemon with 2 words as their name
POKE_NAME_ADJ_NEEDED = [
    # (condition, return name)

    ##### Species
    (lambda poke_name, form_name: poke_name == "Nidoran f", lambda poke_name, form_name: "Nidoran hembra"),
    (lambda poke_name, form_name: poke_name == "Nidoran m", lambda poke_name, form_name: "Nidoran macho"),
    (lambda poke_name, form_name: poke_name == "Flabebe", lambda poke_name, form_name: "Flabébé"),
    (lambda poke_name, form_name: poke_name == "Type Null", lambda poke_name, form_name: "Código Cero"),
    (lambda poke_name, form_name: poke_name == "Necrozma" and form_name == "-Form_Ultra", lambda poke_name, form_name: "Ultra-Necrozma"),
    (lambda poke_name, form_name: poke_name == "Great Tusk", lambda poke_name, form_name: "Colmilargo"),
    (lambda poke_name, form_name: poke_name == "Scream Tail", lambda poke_name, form_name: "Colagrito"),
    (lambda poke_name, form_name: poke_name == "Brute Bonnet", lambda poke_name, form_name: "Furioseta"),
    (lambda poke_name, form_name: poke_name == "Flutter Mane", lambda poke_name, form_name: "Melenaleteo"),
    (lambda poke_name, form_name: poke_name == "Slither Wing", lambda poke_name, form_name: "Reptalada"),
    (lambda poke_name, form_name: poke_name == "Sandy Shocks", lambda poke_name, form_name: "Pelarena"),
    (lambda poke_name, form_name: poke_name == "Iron Treads", lambda poke_name, form_name: "Ferrodada"),
    (lambda poke_name, form_name: poke_name == "Iron Bundle", lambda poke_name, form_name: "Ferrosaco"),
    (lambda poke_name, form_name: poke_name == "Iron Hands", lambda poke_name, form_name: "Ferropalmas"),
    (lambda poke_name, form_name: poke_name == "Iron Jugulis", lambda poke_name, form_name: "Ferrocuello"),
    (lambda poke_name, form_name: poke_name == "Iron Moth", lambda poke_name, form_name: "Ferropolilla"),
    (lambda poke_name, form_name: poke_name == "Iron Thorns", lambda poke_name, form_name: "Ferropúas"),
    (lambda poke_name, form_name: poke_name == "Roaring Moon", lambda poke_name, form_name: "Bramaluna"),
    (lambda poke_name, form_name: poke_name == "Iron Valiant", lambda poke_name, form_name: "Ferropaladín"),
    (lambda poke_name, form_name: poke_name == "Walking Wake", lambda poke_name, form_name: "Ondulagua"),
    (lambda poke_name, form_name: poke_name == "Iron Leaves", lambda poke_name, form_name: "Ferroverdor"),
    (lambda poke_name, form_name: poke_name == "Gouging Fire", lambda poke_name, form_name: "Flamariete"),
    (lambda poke_name, form_name: poke_name == "Raging Bolt", lambda poke_name, form_name: "Electrofuria"),
    (lambda poke_name, form_name: poke_name == "Iron Boulder", lambda poke_name, form_name: "Ferromole"),
    (lambda poke_name, form_name: poke_name == "Iron Crown", lambda poke_name, form_name: "Ferrotesta"),

    ##### Universal Forms (Needed here bc they add a denoter before the actual pokemon name)
    (lambda poke_name, form_name: "-Mega_X" in form_name, lambda poke_name, form_name: f"Mega-{poke_name} X"),
    (lambda poke_name, form_name: "-Mega_Y" in form_name, lambda poke_name, form_name: f"Mega-{poke_name} Y"),
    (lambda poke_name, form_name: "-Mega" in form_name, lambda poke_name, form_name: f"Mega-{poke_name}"),
    (lambda poke_name, form_name: "-Region_" in form_name, lambda poke_name, form_name: f"{poke_name} de {form_name.split("-")[1].replace("Region_", "")}")     # Split seperates -f from Female Hisuian Sneasel, replacing Region_ allows me to just get the region name to add that to the pokemon name
]




#|================================================================================================|
#|~~~~~~~~~~~~~~~~~~~~~~~~~~~[     SPECIES FORM TRANSLATIONS     ]~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~|
#|================================================================================================|

WIKIDEX_TYPE_FORM_MAP = {
    "-Form_Normal": "",  # Normal form considered default: so does not have a letter denoter
    "-Form_Fighting": "lucha", 
    "-Form_Flying": "volador", 
    "-Form_Poison": "veneno", 
    "-Form_Ground": "tierra", 
    "-Form_Rock": "roca", 
    "-Form_Bug": "bicho", 
    "-Form_Ghost": "fantasma", 
    "-Form_Steel": "acero", 
    "-Form_Fire": "fuego", 
    "-Form_Water": "agua", 
    "-Form_Grass": "planta", 
    "-Form_Electric": "eléctrico", 
    "-Form_Psychic": "psíquico", 
    "-Form_Ice": "hielo", 
    "-Form_Dragon": "dragón", 
    "-Form_Dark": "siniestro", 
    "-Form_Fairy": "hada", 
    "-Form_Qmark": "?"
}


# NOTE: If ever decide to use Wikidex for menu sprites, drawn, etc. this will have to be nested like bulbas
WIKIDEX_POKE_FORM_TRANSLATION_MAP = {
    # Pikachu
    25: {
        "-Form_Cap_Alola": "Alola",
        "-Form_Cap_Hoenn": "Hoenn",
        "-Form_Cap_Kalos": "Kalos",
        "-Form_Cap_Original": "original",
        "-Form_Cap_Sinnoh": "Sinnoh",
        "-Form_Cap_Unova": "Teselia",
        "-Form_Cap_Partner": "compañero",
        "-Form_Cap_World": "trotamundos",

        "-Form_Cosplay": "coqueta",
        "-Form_Cosplay_Belle": "aristócrata",
        "-Form_Cosplay_Libre": "enmascarada",
        "-Form_Cosplay_PhD": "erudita",
        "-Form_Cosplay_Pop_Star": "superstar",
        "-Form_Cosplay_Rock_Star": "roquera"
    },

    # Tauros
    128: {
        "-Form_Combat": "combatiente",
        "-Form_Blaze": "ardiente",
        "-Form_Aqua": "acuática"
    },

    # Pichu
    172: {
        "-Form_Spiky_Eared": "picoreja"
    },

    201: {
        "-Form_A": "A",
        "-Form_B": "B",
        "-Form_C": "C",
        "-Form_D": "D",
        "-Form_E": "E",
        "-Form_F": "F",
        "-Form_G": "G",
        "-Form_H": "H",
        "-Form_I": "I",
        "-Form_J": "J",
        "-Form_K": "K",
        "-Form_L": "L",
        "-Form_M": "M",
        "-Form_N": "N",
        "-Form_O": "O",
        "-Form_P": "P",
        "-Form_Qmark": "%3F",
        "-Form_Q": "Q",
        "-Form_R": "R",
        "-Form_S": "S",
        "-Form_T": "T",
        "-Form_U": "U",
        "-Form_V": "V",
        "-Form_W": "W",
        "-Form_X": "X",
        "-Form_Y": "Y",
        "-Form_Z": "Z",
        "-Form_!": "!"
    },

    # Sneasel
    215: {
        "-Region_Hisui-f": ""   # Handled w universal & female forms in wikidex scraping, blank so it doesn't get flagged as missing key
    },

    # Castform
    351: {
        "-Form_Rainy": "lluvia",
        "-Form_Snowy": "nieve",
        "-Form_Sunny": "sol"
    },

    # Kyogre & Groudon
    382: {
        "-Form_Primal": "primigenio"
    },
    383: {
        "-Form_Primal": "primigenio"
    },

    # Deoxys
    386: {
        "-Form_Attack": "ataque",
        "-Form_Defense": "defensa",
        "-Form_Speed": "velocidad"
    },

    # Burmy & Wormadam
    412: {
        "-Form_Plant_Cloak": "planta",
        "-Form_Sandy_Cloak": "arena",
        "-Form_Trash_Cloak": "basura"
    },
    413: {
        "-Form_Plant_Cloak": "planta",
        "-Form_Sandy_Cloak": "arena",
        "-Form_Trash_Cloak": "basura"
    },

    # Cherrim
    421: {
        "-Form_Overcast": "encapotado",
        "-Form_Sunshine": "soleado"
    },

    # Shellos & Gastrodon
    422: {
        "-Form_West": "oeste",
        "-Form_East": "este"
    },
    423: {
        "-Form_West": "oeste",
        "-Form_East": "este"
    },

    # Rotom
    479: {
        "-Form_Fan": "ventilador",
        "-Form_Frost": "frío",
        "-Form_Heat": "calor",
        "-Form_Mow": "corte",
        "-Form_Wash": "lavado"
    },

    # Dialga & Palkia
    483: {
        "-Form_Origin": "origen"
    },
    484: {
        "-Form_Origin": "origen"
    },

    # Giratina
    487: {
        "-Form_Altered": "modificada",
        "-Form_Origin": "origen"
    },

    # Shaymin
    492: {
        "-Form_Land": "tierra",
        "-Form_Sky": "cielo"
    },

    # Arceus
    493: WIKIDEX_TYPE_FORM_MAP,

    #  Basculin
    550: {
        "-Form_Red_Striped": "roja",
        "-Form_Blue_Striped": "azul",
        "-Form_White_Striped": "blanca"
    },

    # Darmanitan
    555: {
        "-Form_Standard": "",
        "-Form_Zen": "daruma"
    },

    # Deerling & Sawsbuck
    585: {
        "-Form_Spring": "primavera",
        "-Form_Autumn": "otoño",
        "-Form_Summer": "verano",
        "-Form_Winter": "invierno"
    },
    586: {
        "-Form_Spring": "primavera",
        "-Form_Autumn": "otoño",
        "-Form_Summer": "verano",
        "-Form_Winter": "invierno"
    },

    # Forces of nature
    641: {
        "-Form_Incarnate": "avatar",
        "-Form_Therian": "tótem"
    },
    642: {
        "-Form_Incarnate": "avatar",
        "-Form_Therian": "tótem"
    },
    645: {
        "-Form_Incarnate": "avatar",
        "-Form_Therian": "tótem"
    },

    # Kyurem
    646: {
        "-Form_Black": EXCLUDE_TRANSLATIONS_MAP["DBH"],
        "-Form_Black_Overdrive": EXCLUDE_TRANSLATIONS_MAP["DBH"],
        "-Form_White": EXCLUDE_TRANSLATIONS_MAP["DBH"],
        "-Form_White_Overdrive": EXCLUDE_TRANSLATIONS_MAP["DBH"]
    },

    # Keldeo
    647: {
        "-Form_Ordinary": "",
        "-Form_Resolute": "brío"
    },

    # Meloetta
    648: {
        "-Form_Aria": "lírica",
        "-Form_Pirouette": "danza"
    },

    # Genesect
    649: {
        "-Form_Douse_Drive": "hidroROM",
        "-Form_Burn_Drive": "piroROM",
        "-Form_Chill_Drive": "crioROM",
        "-Form_Shock_Drive": "fulgoROM"
    },

    # Greninja
    658: {
        "-Form_Ash": "Ash"
    },

    # Vivillon
    666: {
        "-Form_Meadow": "floral",
        "-Form_Archipelago": "isleño",
        "-Form_Continental": "continental",
        "-Form_Elegant": "oriental",
        "-Form_Garden": "vergel",
        "-Form_High_Plains": "estepa",
        "-Form_Icy_Snow": "polar",
        "-Form_Jungle": "jungla",
        "-Form_Marine": "marino",
        "-Form_Modern": "moderno",
        "-Form_Monsoon": "monzón",
        "-Form_Ocean": "océano",
        "-Form_Polar": "taiga",
        "-Form_River": "oasis",
        "-Form_Sandstorm": "desierto",
        "-Form_Savanna": "pantano",
        "-Form_Sun": "solar",
        "-Form_Tundra": "tundra",
        "-Form_Poke_Ball": "Poké Ball",
        "-Form_Fancy": "fantasía"
    },

    # Flabebe, Floette, and Florges
    669: {
        "-Form_Red_Flower": "roja",
        "-Form_Blue_Flower": "azul",
        "-Form_Orange_Flower": "naranja",
        "-Form_White_Flower": "blanca",
        "-Form_Yellow_Flower": "amarilla"
    },
    670: {
        "-Form_Red_Flower": "roja",
        "-Form_Blue_Flower": "azul",
        "-Form_Orange_Flower": "naranja",
        "-Form_White_Flower": "blanca",
        "-Form_Yellow_Flower": "amarilla",
        "-Form_Eternal_Flower": "eterna"
    },
    671: {
        "-Form_Red_Flower": "roja",
        "-Form_Blue_Flower": "azul",
        "-Form_Orange_Flower": "naranja",
        "-Form_White_Flower": "blanca",
        "-Form_Yellow_Flower": "amarilla"
    },

    # Furfrou
    676: {
        "-Form_Dandy_Trim": "caballero",
        "-Form_Debutante_Trim": "señorita",
        "-Form_Diamond_Trim": "rombo",
        "-Form_Heart_Trim": "corazón",
        "-Form_Kabuki_Trim": "kabuki",
        "-Form_La_Reine_Trim": "aristocrático",
        "-Form_Matron_Trim": "dama",
        "-Form_Pharaoh_Trim": "faraónico",
        "-Form_Star_Trim": "estrella"
    },

    # Aegislash
    681: {
        "-Form_Shield": "escudo",
        "-Form_Blade": "filo"
    },

    # Pumpkaboo and Gourgeist
    710: {
        "-Form_Average_Size": "",
        "-Form_Small_Size": "pequeño",
        "-Form_Large_Size": "grande",
        "-Form_Super_Size": "extragrande"
    },
    711: {
        "-Form_Average_Size": "",
        "-Form_Small_Size": "pequeño",
        "-Form_Large_Size": "grande",
        "-Form_Super_Size": "extragrande"
    },

    # Xerneas
    716: {
        "-Form_Active": "",
        "-Form_Neutral": "relajada"
    },

    # Zygarde
    718: {
        "-Form_50%": "",
        "-Form_Complete": "completo",
        "-Form_10%": "al 10%"
    },

    # Hoopa
    720: {
        "-Form_Confined": "",
        "-Form_Unbound": "desatado"
    },

    # Oricorio
    741: {
        "-Form_Baile": "apasionado",
        "-Form_Pa'u": "plácido",
        "-Form_Pom_Pom": "animado",
        "-Form_Sensu": "refinado"
    },

    # Lycanroc
    745: {
        "-Form_Midday": "diurno",
        "-Form_Dusk": "crepuscular",
        "-Form_Midnight": "nocturno"
    },

    # Wishiwashi
    746: {
        "-Form_Solo": "individual",
        "-Form_School": "banco"
    },

    # Silvally
    773: WIKIDEX_TYPE_FORM_MAP,

    # Minior
    774: {
        "-Form_Meteor": "meteorito",
        "-Form_Blue_Core": "azul",
        "-Form_Green_Core": "verde",
        "-Form_Indigo_Core": "añil",
        "-Form_Orange_Core": "naranja",
        "-Form_Red_Core": "rojo",
        "-Form_Violet_Core": "violeta",
        "-Form_Yellow_Core": "amarillo",
        "-Form_Core": "núcleo"
    },

    # Mimikyu
    778: {
        "-Form_Disguised": "",
        "-Form_Busted": "descubierto"
    },

    # Solgaleo
    791: {
        "-Form_Radiant_Sun": EXCLUDE_TRANSLATIONS_MAP["DNE"]
    },

    # Lunala
    792: {
        "-Form_Full_Moon": EXCLUDE_TRANSLATIONS_MAP["DNE"]
    },

    # Necrozma
    800: {
        "-Form_Dawn_Wings": "alas del alba",
        "-Form_Dusk_Mane": "melena crepuscular",
        "-Form_Ultra": ""   # NOTE: Taken care of in adjust_poke_name and POKE_NAME_ADJ_NEEDED
    },

    # Magearna
    801: {
        "-Form_Original_Color": "vetusta"
    },

    # Cramorant
    845: {
        "-Form_Gorging": "engulletodo",
        "-Form_Gulping": "tragatodo"
    },

    # Toxtricity
    849: {
        "-Form_Amped": "aguda",
        "-Form_Low_Key": "grave"
    },

    # Sinistea & Polteageist
    # Only used by HOME for the show stamp sprites. All other images (since identical) are default form
    854: {
        "-Form_Phony": "falsificada",
        "-Form_Antique": "genuina"
    },
    855: {
        "-Form_Phony": "falsificada",
        "-Form_Antique": "genuina"
    },

    # Alcremie
    869: {
        "-Form_Caramel_Swirl_Berry_Sweet": "mezcla caramelo fruto",
        "-Form_Caramel_Swirl_Clover_Sweet": "mezcla caramelo trébol",
        "-Form_Caramel_Swirl_Flower_Sweet": "mezcla caramelo flor",
        "-Form_Caramel_Swirl_Love_Sweet": "mezcla caramelo corazón",
        "-Form_Caramel_Swirl_Ribbon_Sweet": "mezcla caramelo lazo",
        "-Form_Caramel_Swirl_Star_Sweet": "mezcla caramelo estrella",
        "-Form_Caramel_Swirl_Strawberry_Sweet": "mezcla caramelo",
        "-Form_Lemon_Cream_Berry_Sweet": "crema de limón fruto",
        "-Form_Lemon_Cream_Clover_Sweet": "crema de limón trébol",
        "-Form_Lemon_Cream_Flower_Sweet": "crema de limón flor",
        "-Form_Lemon_Cream_Love_Sweet": "crema de limón corazón",
        "-Form_Lemon_Cream_Ribbon_Sweet": "crema de limón lazo",
        "-Form_Lemon_Cream_Star_Sweet": "crema de limón estrella",
        "-Form_Lemon_Cream_Strawberry_Sweet": "crema de limón",
        "-Form_Matcha_Cream_Berry_Sweet": "crema de té fruto",
        "-Form_Matcha_Cream_Clover_Sweet": "crema de té trébol",
        "-Form_Matcha_Cream_Flower_Sweet": "crema de té flor",
        "-Form_Matcha_Cream_Love_Sweet": "crema de té corazón",
        "-Form_Matcha_Cream_Ribbon_Sweet": "crema de té lazo",
        "-Form_Matcha_Cream_Star_Sweet": "crema de té estrella",
        "-Form_Matcha_Cream_Strawberry_Sweet": "crema de té",
        "-Form_Mint_Cream_Berry_Sweet": "crema de menta fruto",
        "-Form_Mint_Cream_Clover_Sweet": "crema de menta trébol",
        "-Form_Mint_Cream_Flower_Sweet": "crema de menta flor",
        "-Form_Mint_Cream_Love_Sweet": "crema de menta corazón",
        "-Form_Mint_Cream_Ribbon_Sweet": "crema de menta lazo",
        "-Form_Mint_Cream_Star_Sweet": "crema de menta estrella",
        "-Form_Mint_Cream_Strawberry_Sweet": "crema de menta",
        "-Form_Rainbow_Swirl_Berry_Sweet": "tres sabores fruto",
        "-Form_Rainbow_Swirl_Clover_Sweet": "tres sabores trébol",
        "-Form_Rainbow_Swirl_Flower_Sweet": "tres sabores flor",
        "-Form_Rainbow_Swirl_Love_Sweet": "tres sabores corazón",
        "-Form_Rainbow_Swirl_Ribbon_Sweet": "tres sabores lazo",
        "-Form_Rainbow_Swirl_Star_Sweet": "tres sabores estrella",
        "-Form_Rainbow_Swirl_Strawberry_Sweet": "tres sabores",
        "-Form_Ruby_Cream_Berry_Sweet": "crema rosa fruto",
        "-Form_Ruby_Cream_Clover_Sweet": "crema rosa trébol",
        "-Form_Ruby_Cream_Flower_Sweet": "crema rosa flor",
        "-Form_Ruby_Cream_Love_Sweet": "crema rosa corazón",
        "-Form_Ruby_Cream_Ribbon_Sweet": "crema rosa lazo",
        "-Form_Ruby_Cream_Star_Sweet": "crema rosa estrella",
        "-Form_Ruby_Cream_Strawberry_Sweet": "crema rosa",
        "-Form_Ruby_Swirl_Berry_Sweet": "mezcla rosa fruto",
        "-Form_Ruby_Swirl_Clover_Sweet": "mezcla rosa trébol",
        "-Form_Ruby_Swirl_Flower_Sweet": "mezcla rosa flor",
        "-Form_Ruby_Swirl_Love_Sweet": "mezcla rosa corazón",
        "-Form_Ruby_Swirl_Ribbon_Sweet": "mezcla rosa lazo",
        "-Form_Ruby_Swirl_Star_Sweet": "mezcla rosa estrella",
        "-Form_Ruby_Swirl_Strawberry_Sweet": "mezcla rosa",
        "-Form_Salted_Cream_Berry_Sweet": "crema salada fruto",
        "-Form_Salted_Cream_Clover_Sweet": "crema salada trébol",
        "-Form_Salted_Cream_Flower_Sweet": "crema salada flor",
        "-Form_Salted_Cream_Love_Sweet": "crema salada corazón",
        "-Form_Salted_Cream_Ribbon_Sweet": "crema salada lazo",
        "-Form_Salted_Cream_Star_Sweet": "crema salada estrella",
        "-Form_Salted_Cream_Strawberry_Sweet": "crema salada",
        "-Form_Vanilla_Cream_Berry_Sweet": "crema de vainilla fruto",
        "-Form_Vanilla_Cream_Clover_Sweet": "crema de vainilla trébol",
        "-Form_Vanilla_Cream_Flower_Sweet": "crema de vainilla flor",
        "-Form_Vanilla_Cream_Love_Sweet": "crema de vainilla corazón",
        "-Form_Vanilla_Cream_Ribbon_Sweet": "crema de vainilla lazo",
        "-Form_Vanilla_Cream_Star_Sweet": "crema de vainilla estrella",
        "-Form_Vanilla_Cream_Strawberry_Sweet": "",     # NOTE: Sometimes also just "crema de vainilla"... TODO: See whats missing after scrape
        "-Form_Berry_Sweet": "fruto",
        "-Form_Clover_Sweet": "trébol",
        "-Form_Flower_Sweet": "flor",
        "-Form_Love_Sweet": "corazón",
        "-Form_Ribbon_Sweet": "lazo",
        "-Form_Star_Sweet": "estrella",
        "-Form_Strawberry_Sweet": ""
    },

    # Eiscue
    875: {
        "-Form_Ice_Face": "",
        "-Form_Noice_Face": "cara deshielo"
    },

    # Morpeko
    877: {
        "-Form_Full_Belly": "",
        "-Form_Hangry": "voraz"
    },

    # Zacian & Zamazenta
    888: {
        "-Form_Hero_of_Many_Battles": "",
        "-Form_Crowned_Sword": "espada suprema"
    },
    889: {
        "-Form_Hero_of_Many_Battles": "",
        "-Form_Crowned_Shield": "escudo supremo"
    },

    # Eternatus
    890: {
        "-Form_Eternamax": "Dinamax infinito"
    },

    # Urshifu
    892: {
        "-Form_Single_Strike": "brusco",
        "-Form_Rapid_Strike": "fluido"
    },

    # Zarude
    893: {
        "-Form_Dada": "papá"
    },

    # Calyrex
    898: {
        "-Form_Ice_Rider": "jinete glacial",
        "-Form_Shadow_Rider": "jinete espectral"
    },

    # Ursaluna
    901: {
        "-Form_Bloodmoon": "luna carmesí"
    },

    # Enamorus
    905: {
        "-Form_Incarnate": "avatar",
        "-Form_Therian": "tótem"
    },

    # Maushold
    925: {
        "-Form_Family_of_Three": "familia de tres",
        "-Form_Family_of_Four": "familia de cuatro"
    },

    # Squawkabilly
    931: {
        "-Form_Blue_Plumage": "azul",
        "-Form_Green_Plumage": "verde",
        "-Form_White_Plumage": "blanco",
        "-Form_Yellow_Plumage": "amarillo"
    },

    # Palafin
    964: {
        "-Form_Zero": "Ingenua",
        "-Form_Hero": "heroica"
    },

    # Tatsugiri
    978: {
        "-Form_Curly": "curvada",
        "-Form_Droopy": "lánguida",
        "-Form_Stretchy": "recta"
    },

    # Dudunsparce
    982: {
        "-Form_Two_Segment": "binodular",
        "-Form_Three_Segment": "trinodular"
    },

    # Gimmighoul
    999: {
        "-Form_Chest": "cofre",
        "-Form_Roaming": "andante"
    },

    # Poltchageist & Sinistcha
    1012: {
        "-Form_Artisan": "opulenta",
        "-Form_Counterfeit": "fraudulenta"
    },
    1013: {
        "-Form_Masterpiece": "exquisita",
        "-Form_Unremarkable": "mediocre"
    },

    # Ogerpon
    1017: {
        "-Form_Cornerstone_Mask": "máscara cimiento",
        "-Form_Hearthflame_Mask": "máscara horno",
        "-Form_Teal_Mask": "máscara turquesa",
        "-Form_Wellspring_Mask": "máscara fuente"
    },

    # Terapagos
    1024: {
        "-Form_Normal": "normal",
        "-Form_Terastal": "Teracristal",
        "-Form_Stellar": "astral"
    }
}




#|================================================================================================|
#|~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~[     GO TRANSLATIONS     ]~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~|
#|================================================================================================|

GO_COSTUME_TRANSLATIONS_MAP = {
    "-Costume_Halloween": "Halloween",
    "-Costume_Party_Hat_Red": "con gorro de fiesta rojo",
    "-Costume_Pikachu_Visor": "con gorro de Pikachu",
    "-Costume_Clone": "clon",
    "-Costume_Sunglasses": "con gafas de sol",
    "-Costume_Fashionable": "con disfraz de la Semana de la Moda",
    "-Costume_Party_Hat_Green": "con gorro de fiesta azul",
    "-Costume_Akari_Kerchief": "con pañuelo de Kira",
    "-Costume_Beanie": "Navidad 2019",
    "-Costume_Brendan_Hat": "con gorro de Brendan-Bruno",
    "-Costume_Cake": "con disfraz de tarta",
    "-Costume_Captain": "con gorra de Capi",
    "-Costume_Charizard_Hat": "con gorro de Charizard",
    "-Costume_Cherry_Blossoms": "con flores de cerezo",
    "-Costume_Dapper_Blue_Accents": "con traje elegante azul y gafas",
    "-Costume_Dapper_Red_Accents": "con traje elegante rojo y gafas",
    "-Costume_Dapper_Yellow_Accents": "con traje elegante amarillo y gafas",
    "-Costume_Dawn_Hat": "con el gorro de Maya",
    "-Costume_Detective": "detective",
    "-Costume_Explorer": "explorador",
    "-Costume_Festive_Hat": "con sombrero festivo",
    "-Costume_Flower_Crown": "con una corona de flores",
    "-Costume_Flower_Hat": "Primavera",
    "-Costume_Flying_1": "Volador 2022",
    "-Costume_Flying_2": "Vuelo con globos especiales",
    "-Costume_Flying_3": "Vuelo con globos morados",
    "-Costume_Flying_4": "Vuelo con globos multicolor",
    "-Costume_Flying_5th_Anniversary": "5 aniversario",
    "-Costume_Flying_6": "Vuelo con globos naranja",
    "-Costume_Flying_7": "Vuelo con globos verdes",
    "-Costume_Formal_Blue_Accents": "con traje elegante azul y monóculo",
    "-Costume_Formal_Red_Accents": "con traje elegante rojo y monóculo",
    "-Costume_Formal_Yellow_Accents": "con traje elegante amarillo y monóculo",
    "-Costume_Gem_Crown_Amethyst": "con corona de amatista",
    "-Costume_Gem_Crown_Aquamarine": "con corona de aguamarina",
    "-Costume_Gem_Crown_Malachite": "con corona de malaquita",
    "-Costume_Gem_Crown_Pyrite": "con corona de pirita",
    "-Costume_Gem_Crown_Quartz": "con corona de cuarzo",
    "-Costume_Gracidea_flower": "Gracídea",
    "-Costume_HF_Custom_Cap": "gorra negra",
    "-Costume_Halloween_Mischief": "con un disfraz de Travesuras de Halloween",
    "-Costume_Hilbert_Hat": "con gorra de Lucho",   
    "-Costume_Hilda_Hat": "con gorra de Liza",
    "-Costume_Holiday": "con estilo invernal",  # Golduck, psyduck con atuendo festivo for Pikachu/Raichu, con traje de fiesta for spheal/stantler
    "-Costume_Kariyushi_Shirt": "con una camisa kariyushi de Okinawa",
    "-Costume_Kurta": "con Kurta",
    "-Costume_Lucario_Hat": "con gorro de Lucario",
    "-Costume_Lucas_Hat": "con la boina de León",
    "-Costume_May_Bow": "con lazo de May-Aura",
    "-Costume_Meloetta_Hat": "GO Fest",
    "-Costume_Mimikyu": "Halloween",
    "-Costume_Moon_Crown": "con corona de luna",
    "-Costume_Nate_Visor": "con visera de Rizzo",
    "-Costume_New_Years_Hat": "con gorrito de Año Nuevo",
    "-Costume_Party_Hat": "con gorro de fiesta morado",
    "-Costume_Party_Top_Hat": "con chistera de fiesta",
    "-Costume_Rayquaza_Hat": "con gorro de Rayquaza",
    "-Costume_Rei_Cap": "con gorra de Luka",
    "-Costume_Rosa_Visor": "con visera de Nanci",
    "-Costume_Safari_Hat": "safari",
    "-Costume_Saree": "vestido de Sari",
    "-Costume_Shaymin_Scarf": "con bufanda inspirada en Shaymin",
    "-Costume_Straw_Hat": "pirata",
    "-Costume_Summer_Style": "Verano",
    "-Costume_Sun_Crown": "con corona de sol",
    "-Costume_T_Shirt_Blue": "con camisa azul de cítricos",
    "-Costume_T_Shirt_Gold": "con una camisa Batik",
    "-Costume_T_Shirt_Green": "con una camiseta verde (Flor)",
    "-Costume_T_Shirt_Purple": "con una camiseta morada (Flor)",
    "-Costume_TCG_Hat": "con gorra de JCC Pokémon",
    "-Costume_Tricks_and_Treats": "con disfraz de Halloween",
    "-Costume_Umbreon_Hat": "con gorro de Umbreon",
    "-Costume_Winter_Carnival": "con traje de Carnaval de invierno",
    "-Costume_Witch_Hat": "con gorro de bruja",
    "-Costume_World_Championships_2022": "con disfraz del Mundial 2022",
    "-Costume_World_Championships_2023": "con disfraz del Mundial 2023",
    "-Costume_World_Championships_2024": "del Campeonato Mundial 2024",
    "-Costume_Original_Cap": "con gorra de Ash",
    "-Costume_World_Cap": "trotamundo",
    "-Costume_Crown": "con corona",
    "-Costume_Spooky_Festival": "con disfraz del Festival Tenebroso",
    "-Costume_Ribbon": "con lazo",
    "-Costume_Candela": "con un accesorio de Candela",
    "-Costume_2020_Glasses": "con gafas de 2020",
    "-Costume_2021_Glasses": "con gafas de 2021",
    "-Costume_Cempasuchil_Crown": "con corona de cempasúchil",
    "-Costume_Spark": "con un accesorio de Spark",
    "-Costume_Blanche": "con un accesorio de Blanche",
    "-Costume_Scarf": "con bufanda",
    "-Costume_Explorer_Hat": "con sombrero de explorador",
    "-Costume_Holiday_Hat": "con gorro festivo",
    "-Costume_Satchel": "con mochila",
    "-Costume_Cowboy_Hat": "vaquero",
    "-Costume_Nightcap": "con gorro de dormir",
    "-Costume_Studded_Jacket": "con chaqueta de tachuelas",
    "-Costume_Armored": "acorazado",
    "-Costume_New_Years_Outfit": "con traje de Año Nuevo",
    "-Costume_Day_Scarf": "con bufanda de día",
    "-Costume_Night_Scarf": "con bufanda de noche",
    "-Costume_2022_Glasses": "con gafas de 2022",
    "-Costume_Holiday_Ribbon": "con lazo festivo",
    "-Costume_Visor": "con visera",
    "-Costume_Undersea_Holiday": "con traje de fiesta submarina",
    "-Costume_Holiday_Attire": "con atuendo festivo",
    "-Costume_Train_Conductor": "locomotora",
    "-Costume_Hat_with_Liko_Pin": "con sombrero y la horquilla de Liko",
    "-Costume_9th_Anniversary_Coin": "con una moneda del 9.º aniversario"
}


GO_COSTUME_TRANSLATION_EXCEPTIONS = {
    # Pikachu
    25: {
        "-Costume_Beanie": "con gorro de copo de nieve",
        "-Costume_Holiday": "con atuendo festivo"
    },
    # Raichu
    26: { "-Costume_Holiday": "con atuendo festivo" },

    # Stantler
    234: { "-Costume_Holiday": "con traje de fiesta" },

    # Spheal
    363: { "-Costume_Holiday": "con traje de fiesta" },

    # Greninja line
    656: { "-Costume_Halloween": "con disfraz de Halloween" },
    657: { "-Costume_Halloween": "con disfraz de Halloween" },
    658: { "-Costume_Halloween": "con disfraz de Halloween" },
    
    # Decidiueye line
    722: { "-Costume_Halloween": "con disfraz de Halloween" },
    723: { "-Costume_Halloween": "con disfraz de Halloween" },
    724: { "-Costume_Halloween": "con disfraz de Halloween" }    
}


# NOTE: If I ever combine all translation dicts, nest these into wikidex[GO]
GO_FORM_TRANSLATION_EXCEPTIONS = {
    # Pikachu
    25: {
        #TODO: Add caps
        "-Form_Cap_Alola": EXCLUDE_TRANSLATIONS_MAP["DNE"],
        "-Form_Cap_Hoenn": EXCLUDE_TRANSLATIONS_MAP["DNE"],
        "-Form_Cap_Kalos": EXCLUDE_TRANSLATIONS_MAP["DNE"],
        "-Form_Cap_Original": "con gorra de Ash",
        "-Form_Cap_Sinnoh": EXCLUDE_TRANSLATIONS_MAP["DNE"],
        "-Form_Cap_Unova": EXCLUDE_TRANSLATIONS_MAP["DNE"],
        "-Form_Cap_Partner": EXCLUDE_TRANSLATIONS_MAP["DNE"],
        "-Form_Cap_World": "trotamundo",

        "-Form_Cosplay": EXCLUDE_TRANSLATIONS_MAP["DNE"],
        "-Form_Cosplay_Belle": EXCLUDE_TRANSLATIONS_MAP["DNE"],
        "-Form_Cosplay_Libre": "Libre",
        "-Form_Cosplay_PhD": "Erudita",
        "-Form_Cosplay_Pop_Star": "Estrella del Pop",
        "-Form_Cosplay_Rock_Star": "Estrella del Rock"
    },

    # Cherrim
    421: {
        "-Form_Overcast": "encapotada",
        "-Form_Sunshine": "soleada"
    },

    # Keldeo
    647: { "-Form_Ordinary": "habitual" },

    # Xerneas
    716: { "-Form_Active": "activa" },

    # Zygarde
    718: { "-Form_50%": "al 50%" },

    # Hoopa
    720: { "-Form_Confined": "contenido" },

    # Mimikyu
    778: { "-Form_Disguised": EXCLUDE_TRANSLATIONS_MAP["DNE"] },

    # Eiscue
    875: { "-Form_Ice_Face": EXCLUDE_TRANSLATIONS_MAP["DNE"] },

    # Morpeko
    877: { "-Form_Full_Belly": "saciada" },

    # Zacian & Zamazenta
    888: { "-Form_Hero_of_Many_Battles": "guerrero avezado" },
    889: { "-Form_Hero_of_Many_Battles": "guerrero avezado" }
}