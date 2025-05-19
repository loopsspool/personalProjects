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


WIKIDEX_POKE_FORM_TRANSLATION_MAP = {
    "25": {
        "-Form_Cap_Alola": "Alola",
        "-Form_Cap_Hoenn": "Hoenn",
        "-Form_Cap_Kalos": "Kalos",
        "-Form_Cap_Original": "original",
        "-Form_Cap_Sinnoh": "Sinnoh",
        "-Form_Cap_Unova": "Teselia",
        "-Form_Cap_Partner": "P",
        "-Form_Cap_World": "W",
        "-Form_Cosplay_Belle": "B",
        "-Form_Cosplay_Libre": "L",
        "-Form_Cosplay_PhD": "PhD",
        "-Form_Cosplay_Pop_Star": "Pop",
        "-Form_Cosplay_Rock_Star": "Ro"
    },
    "128": {
        "-Form_Combat": "C",
        "-Form_Blaze": "B",
        "-Form_Aqua": "A"
    },
    "172": {
        "-Form_Spiky_Eared": "N"
    },
    "201": {
        "-Form_A": "",
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
        "-Form_Qmark": "QU",
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
        "-Form_!": "EX"
    },
    "215": {
        "-Region_Hisui-f": ""
    },
    "351": {
        "-Form_Rainy": "R",
        "-Form_Snowy": "H",
        "-Form_Sunny": "S"
    },
    "382": {
        "-Form_Primal": "P"
    },
    "383": {
        "-Form_Primal": "P"
    },
    "386": {
        "-Form_Attack": "A",
        "-Form_Defense": "D",
        "-Form_Speed": "S"
    },
    "412": {
        "-Form_Plant_Cloak": "",
        "-Form_Sandy_Cloak": "G",
        "-Form_Trash_Cloak": "S"
    },
    "413": {
        "-Form_Plant_Cloak": "",
        "-Form_Sandy_Cloak": "G",
        "-Form_Trash_Cloak": "S"
    },
    "421": {
        "-Form_Overcast": "",
        "-Form_Sunshine": "S"
    },
    "422": {
        "-Form_West": "",
        "-Form_East": "E"
    },
    "423": {
        "-Form_West": "",
        "-Form_East": "E"
    },
    "479": {
        "-Form_Fan": "F",
        "-Form_Frost": "R",
        "-Form_Heat": "O",
        "-Form_Mow": "L",
        "-Form_Wash": "W"
    },
    "483": {
        "-Form_Origin": "O"
    },
    "484": {
        "-Form_Origin": "O"
    },
    "487": {
        "-Form_Altered": "",
        "-Form_Origin": "O"
    },
    "492": {
        "-Form_Land": "",
        "-Form_Sky": "S"
    },
    "493": {
        "-Form_Normal": "",
        "-Form_Fighting": "-Fighting",
        "-Form_Flying": "-Flying",
        "-Form_Poison": "-Poison",
        "-Form_Ground": "-Ground",
        "-Form_Rock": "-Rock",
        "-Form_Bug": "-Bug",
        "-Form_Ghost": "-Ghost",
        "-Form_Steel": "-Steel",
        "-Form_Fire": "-Fire",
        "-Form_Water": "-Water",
        "-Form_Grass": "-Grass",
        "-Form_Electric": "-Electric",
        "-Form_Psychic": "-Psychic",
        "-Form_Ice": "-Ice",
        "-Form_Dragon": "-Dragon",
        "-Form_Dark": "-Dark",
        "-Form_Fairy": "-Fairy",
        "-Form_Qmark": "-Unknown"
    },
    "550": {
        "-Form_Red_Striped": "",
        "-Form_Blue_Striped": "B",
        "-Form_White_Striped": "W"
    },
    "555": {
        "-Form_Standard": "",
        "-Form_Zen": "Z"
    },
    "585": {
        "-Form_Spring": "",
        "-Form_Autumn": "A",
        "-Form_Summer": "S",
        "-Form_Winter": "W"
    },
    "586": {
        "-Form_Spring": "",
        "-Form_Autumn": "A",
        "-Form_Summer": "S",
        "-Form_Winter": "W"
    },
    "641": {
        "-Form_Incarnate": "",
        "-Form_Therian": "T"
    },
    "642": {
        "-Form_Incarnate": "",
        "-Form_Therian": "T"
    },
    "645": {
        "-Form_Incarnate": "",
        "-Form_Therian": "T"
    },
    "646": {
        "-Form_Black": "DO_BY_HAND",
        "-Form_Black_Overdrive": "DO_BY_HAND",
        "-Form_White": "DO_BY_HAND",
        "-Form_White_Overdrive": "DO_BY_HAND"
    },
    "647": {
        "-Form_Ordinary": "",
        "-Form_Resolute": "R"
    },
    "648": {
        "-Form_Aria": "",
        "-Form_Pirouette": "P"
    },
    "649": {
        "-Form_Douse_Drive": "B",
        "-Form_Burn_Drive": "R",
        "-Form_Chill_Drive": "W",
        "-Form_Shock_Drive": "Y"
    },
    "658": {
        "-Form_Ash": "A"
    },
    "666": {
        "-Form_Meadow": "",
        "-Form_Archipelago": "Arc",
        "-Form_Continental": "Con",
        "-Form_Elegant": "Ele",
        "-Form_Garden": "Gar",
        "-Form_High_Plains": "Hig",
        "-Form_Icy_Snow": "Icy",
        "-Form_Jungle": "Jun",
        "-Form_Marine": "Mar",
        "-Form_Modern": "Mod",
        "-Form_Monsoon": "Mon",
        "-Form_Ocean": "Oce",
        "-Form_Polar": "Pol",
        "-Form_River": "Riv",
        "-Form_Sandstorm": "San",
        "-Form_Savanna": "Sav",
        "-Form_Sun": "Sun",
        "-Form_Tundra": "Tun",
        "-Form_Poke_Ball": "Pok",
        "-Form_Fancy": "Fan"
    },
    "669": {
        "-Form_Red_Flower": "",
        "-Form_Blue_Flower": "B",
        "-Form_Orange_Flower": "O",
        "-Form_White_Flower": "W",
        "-Form_Yellow_Flower": "Y"
    },
    "670": {
        "-Form_Red_Flower": "",
        "-Form_Blue_Flower": "B",
        "-Form_Orange_Flower": "O",
        "-Form_White_Flower": "W",
        "-Form_Yellow_Flower": "Y",
        "-Form_Eternal_Flower": "E"
    },
    "671": {
        "-Form_Red_Flower": "",
        "-Form_Blue_Flower": "B",
        "-Form_Orange_Flower": "O",
        "-Form_White_Flower": "W",
        "-Form_Yellow_Flower": "Y"
    },
    "676": {
        "-Form_Dandy_Trim": "Da",
        "-Form_Debutante_Trim": "De",
        "-Form_Diamond_Trim": "Di",
        "-Form_Heart_Trim": "He",
        "-Form_Kabuki_Trim": "Ka",
        "-Form_La_Reine_Trim": "La",
        "-Form_Matron_Trim": "Ma",
        "-Form_Pharaoh_Trim": "Ph",
        "-Form_Star_Trim": "St"
    },
    "681": {
        "-Form_Shield": "",
        "-Form_Blade": "B"
    },
    "710": {
        "-Form_Average_Size": "",
        "-Form_Small_Size": "Sm",
        "-Form_Large_Size": "La",
        "-Form_Super_Size": "Su"
    },
    "711": {
        "-Form_Average_Size": "",
        "-Form_Small_Size": "Sm",
        "-Form_Large_Size": "La",
        "-Form_Super_Size": "Su"
    },
    "716": {
        "-Form_Active": "",
        "-Form_Neutral": "N"
    },
    "718": {
        "-Form_50%": "",
        "-Form_Complete": "C",
        "-Form_10%": "T"
    },
    "720": {
        "-Form_Confined": "",
        "-Form_Unbound": "U"
    },
    "741": {
        "-Form_Baile": "",
        "-Form_Pa'u": "Pa",
        "-Form_Pom_Pom": "Po",
        "-Form_Sensu": "Se"
    },
    "745": {
        "-Form_Midday": "",
        "-Form_Dusk": "D",
        "-Form_Midnight": "Mn"
    },
    "746": {
        "-Form_Solo": "",
        "-Form_School": "Sc"
    },
    "773": {
        "-Form_Normal": "",
        "-Form_Fighting": "-Fighting",
        "-Form_Flying": "-Flying",
        "-Form_Poison": "-Poison",
        "-Form_Ground": "-Ground",
        "-Form_Rock": "-Rock",
        "-Form_Bug": "-Bug",
        "-Form_Ghost": "-Ghost",
        "-Form_Steel": "-Steel",
        "-Form_Fire": "-Fire",
        "-Form_Water": "-Water",
        "-Form_Grass": "-Grass",
        "-Form_Electric": "-Electric",
        "-Form_Psychic": "-Psychic",
        "-Form_Ice": "-Ice",
        "-Form_Dragon": "-Dragon",
        "-Form_Dark": "-Dark",
        "-Form_Fairy": "-Fairy",
        "-Form_Qmark": "-Unknown"
    },
    "774": {
        "-Form_Meteor": "",
        "-Form_Blue_Core": "B",
        "-Form_Green_Core": "G",
        "-Form_Indigo_Core": "I",
        "-Form_Orange_Core": "O",
        "-Form_Red_Core": "R",
        "-Form_Violet_Core": "V",
        "-Form_Yellow_Core": "Y",
        "-Form_Core": "R"
    },
    "778": {
        "-Form_Disguised": "",
        "-Form_Busted": "B"
    },
    "791": {
        "-Form_Radiant_Sun": "R"
    },
    "792": {
        "-Form_Full_Moon": "F"
    },
    "800": {
        "-Form_Dawn_Wings": "DW",
        "-Form_Dusk_Mane": "DM",
        "-Form_Ultra": "U"
    },
    "801": {
        "-Form_Original_Color": "O"
    },
    "845": {
        "-Form_Gorging": "Go",
        "-Form_Gulping": "Gu"
    },
    "849": {
        "-Form_Amped": "",
        "-Form_Low_Key": "L"
    },
    "854": {
        "-Form_Phony": " b",
        "-Form_Antique": "A b"
    },
    "855": {
        "-Form_Phony": " b",
        "-Form_Antique": "A b"
    },
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
    "875": {
        "-Form_Ice_Face": "",
        "-Form_Noice_Face": "N"
    },
    "877": {
        "-Form_Full_Belly": "",
        "-Form_Hangry": "H"
    },
    "888": {
        "-Form_Hero_of_Many_Battles": "",
        "-Form_Crowned_Sword": "C"
    },
    "889": {
        "-Form_Hero_of_Many_Battles": "",
        "-Form_Crowned_Shield": "C"
    },
    "890": {
        "-Form_Eternamax": "E"
    },
    "892": {
        "-Form_Single_Strike": "",
        "-Form_Rapid_Strike": "R"
    },
    "893": {
        "-Form_Dada": "D"
    },
    "898": {
        "-Form_Ice_Rider": "I",
        "-Form_Shadow_Rider": "R"
    },
    "901": {
        "-Form_Bloodmoon": "B"
    },
    "905": {
        "-Form_Incarnate": "",
        "-Form_Therian": "T"
    },
    "925": {
        "-Form_Family_of_Three": "T",
        "-Form_Family_of_Four": ""
    },
    "931": {
        "-Form_Blue_Plumage": "B",
        "-Form_Green_Plumage": "",
        "-Form_White_Plumage": "W",
        "-Form_Yellow_Plumage": "Y"
    },
    "964": {
        "-Form_Zero": "",
        "-Form_Hero": "H"
    },
    "978": {
        "-Form_Curly": "",
        "-Form_Droopy": "D",
        "-Form_Stretchy": "S"
    },
    "982": {
        "-Form_Two_Segment": "",
        "-Form_Three_Segment": "-DOES_NOT_EXIST"
    },
    "999": {
        "-Form_Chest": "",
        "-Form_Roaming": "R"
    },
    "1012": {
        "-Form_Artisan": "A b",
        "-Form_Counterfeit": " b"
    },
    "1013": {
        "-Form_Masterpiece": "M b",
        "-Form_Unremarkable": " b"
    },
    "1017": {
        "-Form_Cornerstone_Mask": "C",
        "-Form_Hearthflame_Mask": "H",
        "-Form_Teal_Mask": "",
        "-Form_Wellspring_Mask": "W"
    },
    "1024": {
        "-Form_Normal": "",
        "-Form_Terastal": "T",
        "-Form_Stellar": "S"
    }
}