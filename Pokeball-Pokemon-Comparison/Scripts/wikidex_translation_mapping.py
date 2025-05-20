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

# TODO: Confirm this is all forms w info spreadsheet
WIKIDEX_POKE_FORM_TRANSLATION_MAP = {
    # Pikachu
    "25": {
        "-Form_Cap_Alola": "Alola",
        "-Form_Cap_Hoenn": "Hoenn",
        "-Form_Cap_Kalos": "Kalos",
        "-Form_Cap_Original": "original",
        "-Form_Cap_Sinnoh": "Sinnoh",
        "-Form_Cap_Unova": "Teselia",
        "-Form_Cap_Partner": "compañero",
        "-Form_Cap_World": "trotamundos",

        "-Form_Cosplay_Belle": "aristócrata",
        "-Form_Cosplay_Libre": "enmascarada",
        "-Form_Cosplay_PhD": "erudita",
        "-Form_Cosplay_Pop_Star": "superstar",
        "-Form_Cosplay_Rock_Star": "roquera"
    },

    # Tauros
    "128": {
        "-Form_Combat": "combatiente",
        "-Form_Blaze": "ardiente",
        "-Form_Aqua": "acuática"
    },

    # Pichu
    "172": {
        "-Form_Spiky_Eared": "picoreja"
    },

    "201": {
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
        "-Form_Qmark": "?",
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
    "215": {
        "-Region_Hisui-f": ""   # Handled w universal & female forms in wikidex scraping, blank so it doesn't get flagged as missing key
    },

    # Castform
    "351": {
        "-Form_Rainy": "lluvia",
        "-Form_Snowy": "nieve",
        "-Form_Sunny": "sol"
    },

    # Kyogre & Groudon
    "382": {
        "-Form_Primal": "primigenio"
    },
    "383": {
        "-Form_Primal": "primigenio"
    },

    # Deoxys
    "386": {
        "-Form_Attack": "ataque",
        "-Form_Defense": "defensa",
        "-Form_Speed": "velocidad"
    },

    # Burmy & Wormadam
    "412": {
        "-Form_Plant_Cloak": "planta",
        "-Form_Sandy_Cloak": "arena",
        "-Form_Trash_Cloak": "basura"
    },
    "413": {
        "-Form_Plant_Cloak": "planta",
        "-Form_Sandy_Cloak": "arena",
        "-Form_Trash_Cloak": "basura"
    },

    # Cherrim
    "421": {
        "-Form_Overcast": "encapotado",
        "-Form_Sunshine": "soleado"
    },

    # Shellos & Gastrodon
    "422": {
        "-Form_West": "oeste",
        "-Form_East": "este"
    },
    "423": {
        "-Form_West": "oeste",
        "-Form_East": "este"
    },

    # Rotom
    "479": {
        "-Form_Fan": "ventilador",
        "-Form_Frost": "frío",
        "-Form_Heat": "calor",
        "-Form_Mow": "corte",
        "-Form_Wash": "lavado"
    },

    # Dialga & Palkia
    "483": {
        "-Form_Origin": "origen"
    },
    "484": {
        "-Form_Origin": "origen"
    },

    # Giratina
    "487": {
        "-Form_Altered": "modificada",
        "-Form_Origin": "origen"
    },

    # Shaymin
    "492": {
        "-Form_Land": "tierra",
        "-Form_Sky": "cielo"
    },

    # Arceus
    "493": WIKIDEX_TYPE_FORM_MAP,

    #  Basculin
    "550": {
        "-Form_Red_Striped": "roja",
        "-Form_Blue_Striped": "azul",
        "-Form_White_Striped": "blanca"
    },

    # Darmanitan
    "555": {
        "-Form_Standard": "",
        "-Form_Zen": "daruma"
    },

    # Deerling & Sawsbuck
    "585": {
        "-Form_Spring": "primavera",
        "-Form_Autumn": "otoño",
        "-Form_Summer": "verano",
        "-Form_Winter": "invierno"
    },
    "586": {
        "-Form_Spring": "primavera",
        "-Form_Autumn": "otoño",
        "-Form_Summer": "verano",
        "-Form_Winter": "invierno"
    },

    # Forces of nature
    "641": {
        "-Form_Incarnate": "avatar",
        "-Form_Therian": "tótem"
    },
    "642": {
        "-Form_Incarnate": "avatar",
        "-Form_Therian": "tótem"
    },
    "645": {
        "-Form_Incarnate": "avatar",
        "-Form_Therian": "tótem"
    },

    # Kyurem
    "646": {
        "-Form_Black": "negro inactivo",    # TODO: Sometimes just negro
        "-Form_Black_Overdrive": "negro activo",
        "-Form_White": "blanco inactivo",   # TODO: Sometimes just blanco
        "-Form_White_Overdrive": "blanco activo"
    },

    # Keldeo
    "647": {
        "-Form_Ordinary": "",
        "-Form_Resolute": "brío"
    },

    # Meloetta
    "648": {
        "-Form_Aria": "lírica",
        "-Form_Pirouette": "danza"
    },

    # Genesect
    "649": {
        "-Form_Douse_Drive": "hidroROM",
        "-Form_Burn_Drive": "piroROM",
        "-Form_Chill_Drive": "crioROM",
        "-Form_Shock_Drive": "fulgoROM"
    },

    # Greninja
    "658": {
        "-Form_Ash": "Ash"
    },

    # Vivillon
    "666": {
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
    "669": {
        "-Form_Red_Flower": "roja",
        "-Form_Blue_Flower": "azul",
        "-Form_Orange_Flower": "naranja",
        "-Form_White_Flower": "blanca",
        "-Form_Yellow_Flower": "amarilla"
    },
    "670": {
        "-Form_Red_Flower": "roja",
        "-Form_Blue_Flower": "azul",
        "-Form_Orange_Flower": "naranja",
        "-Form_White_Flower": "blanca",
        "-Form_Yellow_Flower": "amarilla",
        "-Form_Eternal_Flower": "eterna"
    },
    "671": {
        "-Form_Red_Flower": "roja",
        "-Form_Blue_Flower": "azul",
        "-Form_Orange_Flower": "naranja",
        "-Form_White_Flower": "blanca",
        "-Form_Yellow_Flower": "amarilla"
    },

    # Furfrou
    "676": {
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
    "681": {
        "-Form_Shield": "escudo",
        "-Form_Blade": "filo"
    },

    # Pumpkaboo and Gourgeist
    "710": {
        "-Form_Average_Size": "",
        "-Form_Small_Size": "pequeño",
        "-Form_Large_Size": "grande",
        "-Form_Super_Size": "extragrande"
    },
    "711": {
        "-Form_Average_Size": "",
        "-Form_Small_Size": "pequeño",
        "-Form_Large_Size": "grande",
        "-Form_Super_Size": "extragrande"
    },

    # Xerneas
    "716": {
        "-Form_Active": "",
        "-Form_Neutral": "relajada"
    },

    # Zygarde
    "718": {
        "-Form_50%": "",
        "-Form_Complete": "completo",
        "-Form_10%": "al 10%"
    },

    # Hoopa
    "720": {
        "-Form_Confined": "",
        "-Form_Unbound": "desatado"
    },

    # Oricorio
    "741": {
        "-Form_Baile": "apasionado",
        "-Form_Pa'u": "plácido",
        "-Form_Pom_Pom": "animado",
        "-Form_Sensu": "refinado"
    },

    # Lycanroc
    "745": {
        "-Form_Midday": "diurno",
        "-Form_Dusk": "crepuscular",
        "-Form_Midnight": "nocturno"
    },

    # Wishiwashi
    "746": {
        "-Form_Solo": "individual",
        "-Form_School": "banco"
    },

    # Silvally
    "773": WIKIDEX_TYPE_FORM_MAP,

    # Minior
    "774": {
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
    "778": {
        "-Form_Disguised": "",
        "-Form_Busted": "descubierto"
    },

    # Solgaleo
    "791": {
        "-Form_Radiant_Sun": "-DOES_NOT_EXIST"
    },

    # Lunala
    "792": {
        "-Form_Full_Moon": "-DOES_NOT_EXIST"
    },

    # Necrozma
    "800": {
        "-Form_Dawn_Wings": "alas del alba",
        "-Form_Dusk_Mane": "melena crepuscular",
        "-Form_Ultra": ""   # TODO: Adds Ultra- before poke_name
    },

    # Magearna
    "801": {
        "-Form_Original_Color": "vetusta"
    },

    # Cramorant
    "845": {
        "-Form_Gorging": "engulletodo",
        "-Form_Gulping": "tragatodo"
    },

    # Toxtricity
    "849": {
        "-Form_Amped": "aguda",
        "-Form_Low_Key": "grave"
    },

    # Sinistea & Polteageist
    # Only used by HOME for the show stamp sprites. All other images (since identical) are default form
    "854": {
        "-Form_Phony": "falsificada",
        "-Form_Antique": "genuina"
    },
    "855": {
        "-Form_Phony": "falsificada",
        "-Form_Antique": "genuina"
    },

    # TODO: Combine creams & sweets from file_utils.py
    # Alcremie
    "869": {
        "-Form_Caramel_Swirl_Berry_Sweet": "CaSB",
        "-Form_Caramel_Swirl_Clover_Sweet": "CaSC",
        "-Form_Caramel_Swirl_Flower_Sweet": "CaSF",
        "-Form_Caramel_Swirl_Love_Sweet": "CaSL",
        "-Form_Caramel_Swirl_Ribbon_Sweet": "CaSR",
        "-Form_Caramel_Swirl_Star_Sweet": "CaSS",
        "-Form_Caramel_Swirl_Strawberry_Sweet": "CaS",
        "-Form_Lemon_Cream_Berry_Sweet": "LeCB",
        "-Form_Lemon_Cream_Clover_Sweet": "LeCC",
        "-Form_Lemon_Cream_Flower_Sweet": "LeCF",
        "-Form_Lemon_Cream_Love_Sweet": "LeCL",
        "-Form_Lemon_Cream_Ribbon_Sweet": "LeCR",
        "-Form_Lemon_Cream_Star_Sweet": "LeCS",
        "-Form_Lemon_Cream_Strawberry_Sweet": "LeC",
        "-Form_Matcha_Cream_Berry_Sweet": "MaCB",
        "-Form_Matcha_Cream_Clover_Sweet": "MaCC",
        "-Form_Matcha_Cream_Flower_Sweet": "MaCF",
        "-Form_Matcha_Cream_Love_Sweet": "MaCL",
        "-Form_Matcha_Cream_Ribbon_Sweet": "MaCR",
        "-Form_Matcha_Cream_Star_Sweet": "MaCS",
        "-Form_Matcha_Cream_Strawberry_Sweet": "MaC",
        "-Form_Mint_Cream_Berry_Sweet": "MiCB",
        "-Form_Mint_Cream_Clover_Sweet": "MiCC",
        "-Form_Mint_Cream_Flower_Sweet": "MiCF",
        "-Form_Mint_Cream_Love_Sweet": "MiCL",
        "-Form_Mint_Cream_Ribbon_Sweet": "MiCR",
        "-Form_Mint_Cream_Star_Sweet": "MiCS",
        "-Form_Mint_Cream_Strawberry_Sweet": "MiC",
        "-Form_Rainbow_Swirl_Berry_Sweet": "RaSB",
        "-Form_Rainbow_Swirl_Clover_Sweet": "RaSC",
        "-Form_Rainbow_Swirl_Flower_Sweet": "RaSF",
        "-Form_Rainbow_Swirl_Love_Sweet": "RaSL",
        "-Form_Rainbow_Swirl_Ribbon_Sweet": "RaSR",
        "-Form_Rainbow_Swirl_Star_Sweet": "RaSS",
        "-Form_Rainbow_Swirl_Strawberry_Sweet": "RaS",
        "-Form_Ruby_Cream_Berry_Sweet": "RaCB",
        "-Form_Ruby_Cream_Clover_Sweet": "RaCC",
        "-Form_Ruby_Cream_Flower_Sweet": "RaCF",
        "-Form_Ruby_Cream_Love_Sweet": "RaCL",
        "-Form_Ruby_Cream_Ribbon_Sweet": "RaCR",
        "-Form_Ruby_Cream_Star_Sweet": "RaCS",
        "-Form_Ruby_Cream_Strawberry_Sweet": "RaC",
        "-Form_Ruby_Swirl_Berry_Sweet": "RuSB",
        "-Form_Ruby_Swirl_Clover_Sweet": "RuSC",
        "-Form_Ruby_Swirl_Flower_Sweet": "RuSF",
        "-Form_Ruby_Swirl_Love_Sweet": "RuSL",
        "-Form_Ruby_Swirl_Ribbon_Sweet": "RuSR",
        "-Form_Ruby_Swirl_Star_Sweet": "RuSS",
        "-Form_Ruby_Swirl_Strawberry_Sweet": "RuS",
        "-Form_Salted_Cream_Berry_Sweet": "SaCB",
        "-Form_Salted_Cream_Clover_Sweet": "SaCC",
        "-Form_Salted_Cream_Flower_Sweet": "SaCF",
        "-Form_Salted_Cream_Love_Sweet": "SaCL",
        "-Form_Salted_Cream_Ribbon_Sweet": "SaCR",
        "-Form_Salted_Cream_Star_Sweet": "SaCS",
        "-Form_Salted_Cream_Strawberry_Sweet": "SaC",
        "-Form_Vanilla_Cream_Berry_Sweet": "B",
        "-Form_Vanilla_Cream_Clover_Sweet": "C",
        "-Form_Vanilla_Cream_Flower_Sweet": "F",
        "-Form_Vanilla_Cream_Love_Sweet": "L",
        "-Form_Vanilla_Cream_Ribbon_Sweet": "R",
        "-Form_Vanilla_Cream_Star_Sweet": "S",
        "-Form_Vanilla_Cream_Strawberry_Sweet": "",
        "-Form_Berry_Sweet": "B",
        "-Form_Clover_Sweet": "C",
        "-Form_Flower_Sweet": "F",
        "-Form_Love_Sweet": "L",
        "-Form_Ribbon_Sweet": "R",
        "-Form_Star_Sweet": "S",
        "-Form_Strawberry_Sweet": ""
    },

    # Eiscue
    "875": {
        "-Form_Ice_Face": "",
        "-Form_Noice_Face": "cara deshielo"
    },

    # Morpeko
    "877": {
        "-Form_Full_Belly": "",
        "-Form_Hangry": "voraz"
    },

    # Zacian & Zamazenta
    "888": {
        "-Form_Hero_of_Many_Battles": "",
        "-Form_Crowned_Sword": "espada suprema"
    },
    "889": {
        "-Form_Hero_of_Many_Battles": "",
        "-Form_Crowned_Shield": "escudo supremo"
    },

    # Eternatus
    "890": {
        "-Form_Eternamax": "Dinamax infinito"
    },

    # Urshifu
    "892": {
        "-Form_Single_Strike": "brusco",
        "-Form_Rapid_Strike": "fluido"
    },

    # Zarude
    "893": {
        "-Form_Dada": "papá"
    },

    # Calyrex
    "898": {
        "-Form_Ice_Rider": "jinete glacial",
        "-Form_Shadow_Rider": "jinete espectral"
    },

    # Ursaluna
    "901": {
        "-Form_Bloodmoon": "luna carmesí"
    },

    # Enamorus
    "905": {
        "-Form_Incarnate": "avatar",
        "-Form_Therian": "tótem"
    },

    # Maushold
    "925": {
        "-Form_Family_of_Three": "familia de tres",
        "-Form_Family_of_Four": "familia de cuatro"
    },

    # Squawkabilly
    "931": {
        "-Form_Blue_Plumage": "azul",
        "-Form_Green_Plumage": "verde",
        "-Form_White_Plumage": "blanco",
        "-Form_Yellow_Plumage": "amarillo"
    },

    # Palafin
    "964": {
        "-Form_Zero": "Ingenua",
        "-Form_Hero": "heroica"
    },

    # Tatsugiri
    "978": {
        "-Form_Curly": "curvada",
        "-Form_Droopy": "lánguida",
        "-Form_Stretchy": "recta"
    },

    # Dudunsparce
    "982": {
        "-Form_Two_Segment": "binodular",
        "-Form_Three_Segment": "trinodular"
    },

    # Gimmighoul
    "999": {
        "-Form_Chest": "cofre",
        "-Form_Roaming": "andante"
    },

    # Poltchageist & Sinistcha
    "1012": {
        "-Form_Artisan": "opulenta",
        "-Form_Counterfeit": "fraudulenta"
    },
    "1013": {
        "-Form_Masterpiece": "exquisita",
        "-Form_Unremarkable": "mediocre"
    },

    # Ogerpon
    "1017": {
        "-Form_Cornerstone_Mask": "máscara cimiento",
        "-Form_Hearthflame_Mask": "máscara horno",
        "-Form_Teal_Mask": "máscara turquesa",
        "-Form_Wellspring_Mask": "máscara fuente"
    },

    # Terapagos
    "1024": {
        "-Form_Normal": "normal",
        "-Form_Terastal": "Teracristal",
        "-Form_Stellar": "astral"
    }
}