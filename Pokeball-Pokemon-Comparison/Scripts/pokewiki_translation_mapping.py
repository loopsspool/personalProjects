from translation_utils import UNIVERSAL_FORMS, EXCLUDE_TRANSLATIONS_MAP, extract_gen_num_from_my_filename


#|================================================================================================|
#|~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~[     FORM DENOTERS     ]~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~|
#|================================================================================================|

# Pokewiki uses the same denoter on all forms
# NOTE: Can go up to arbitrary amount, but will throw error if less used than shared regional forms for a poke (Meowth has Alola, Galar, so this must go to at least "b")
POKEWIKI_FORM_DENOTER = {
    "Default": "",
    "1st Variant": "a",
    "2nd Variant": "b",
    "3rd Variant": "c",
    "4th Variant": "d"
}




#|================================================================================================|
#|~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~[     EXCLUSIONS     ]~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~|
#|================================================================================================|

# NOTE: Just because you don't see the sprites on the respective game list DOES NOT MEAN THEY DON'T EXIST -- check URL generated, they may just not be linked properly
    # Helpful as well: https://www.wikidex.net/wiki/WikiDex:Proyecto_Pok%C3%A9dex#P%C3%A1ginas_del_proyecto
# Technically no static Crystal or emerald front sprites & they're gifs so might not color convert to apng nicely programatically, but Bulba has all stills for these gens, so all good as long as bulba scraped first
# Tehcnically no gen8 static shiny back sprites but the animateds exist, so we can pull first frame
# Take careful look at backs since wikidex lumps them by gen, not game
POKEWIKI_DOESNT_HAVE_IMGS_FOR = {
    # TODO: Implement, basically only scraping LGPE and above. Any exclusions? No HOME animated I don't think, no SV backsprites it seems, check

    # Example format:
    #"no animated images below gen5 except emerald & crystal": lambda my_filename: "-Animated" in my_filename and extract_gen_num_from_my_filename(my_filename)<5 and "Gen3 Emerald" not in my_filename and "Gen2 Crystal" not in my_filename,
}




#|================================================================================================|
#|~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~[     UNIVERSAL FORMS DATA     ]~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~|
#|================================================================================================|

UNIVERSAL_FORMS_EXCLUDING_REGIONALS = [form for form in UNIVERSAL_FORMS if "-Region" not in form]
UNIVERSAL_FORMS_EXCLUDING_REGIONALS.extend(["-Gigantamax-Form_Single_Strike", "-Gigantamax-Form_Rapid_Strike"])   # Since I check for equality, "-Gigantamax" wont filter these
REGIONAL_FORMS = [form for form in UNIVERSAL_FORMS if "-Region" in form]    # Chronological earliest -> latest




#|================================================================================================|
#|~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~[     GAME TRANSLATIONS     ]~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~|
#|================================================================================================|

POKEWIKI_GAME_MAP = {
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




#|================================================================================================|
#|~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~[     NAME ADJUSTMENTS     ]~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~|
#|================================================================================================|

# TODO: Shouldn't need since all filenames go off of poke num? See
POKE_NAME_ADJ_NEEDED = [
    # (condition, return name)

    ##### Species
    (lambda poke_name, form_name: poke_name == "Nidoran f", lambda poke_name, form_name: "Nidoran hembra"),
    (lambda poke_name, form_name: poke_name == "Nidoran m", lambda poke_name, form_name: "Nidoran macho"),
    (lambda poke_name, form_name: poke_name == "Flabebe", lambda poke_name, form_name: "Flabébé"),
    (lambda poke_name, form_name: poke_name == "Type Null", lambda poke_name, form_name: "Código Cero"),
    (lambda poke_name, form_name: poke_name == "Necrozma" and form_name == "-Form_Ultra", lambda poke_name, form_name: "Ultra-Necrozma"),

    ##### Universal Forms (Needed here bc they add a denoter before the actual pokemon name)
    (lambda poke_name, form_name: "-Mega_X" in form_name, lambda poke_name, form_name: f"Mega-{poke_name} X"),
    (lambda poke_name, form_name: "-Mega_Y" in form_name, lambda poke_name, form_name: f"Mega-{poke_name} Y"),
    (lambda poke_name, form_name: "-Mega" in form_name, lambda poke_name, form_name: f"Mega-{poke_name}"),
    (lambda poke_name, form_name: "-Region_" in form_name, lambda poke_name, form_name: f"{poke_name} de {form_name.split("-")[1].replace("Region_", "")}")     # Split seperates -f from Female Hisuian Sneasel, replacing Region_ allows me to just get the region name to add that to the pokemon name
]




#|================================================================================================|
#|~~~~~~~~~~~~~~~~~~~~~~~~~~~[     SPECIES FORM TRANSLATIONS     ]~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~|
#|================================================================================================|

POKEWIKI_TYPE_FORM_MAP = {
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


POKEWIKI_POKE_FORM_TRANSLATION_MAP = {
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
    493: POKEWIKI_TYPE_FORM_MAP,

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
    773: POKEWIKI_TYPE_FORM_MAP,

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