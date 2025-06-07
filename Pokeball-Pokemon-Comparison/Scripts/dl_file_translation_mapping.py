from translation_utils import EXCLUDE_TRANSLATIONS_MAP

#|================================================================================================|
#|~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~[     DIRECTORY TRANSLATIONS     ]~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~|
#|================================================================================================|

DIRECTORY_TO_FILENAME_MAP = {
    "pkparaiso": {
        "Gen 6 XY w Battle Animations": "Gen6 XY_ORAS-Animated",
        "Gen 8 SwSh Animated - SAME QUALITY CHECK MISSING": "Gen8 SwSh-Animated",
        "Gen 8 SwSh Shiny Animated - SAME QUALITY CHECK MISSING": "Gen8 SwSh-Shiny-Animated"
    },
    "root": {
        "Gen 8 LGPE Front Stills - HIGHER QUALITY": "Gen7 LGPE",
        "Gen 8 LGPE Shiny Front Stills - HIGHER QUALITY": "Gen7 LGPE-Shiny",
        "Gen 9 Poke Front Stills - HIGHER QUALITY": "Gen9 SV",
        "Gen 9 Poke Shiny Front Stills - HIGHER QUALITY": "Gen9 SV-Shiny",
        "Gen 9 SV Shiny Animated - SOME HIGHER QUALITY": "Gen9 SV-Shiny-Animated",
        "HOME": "HOME",
        "HOME Shiny": "HOME-Shiny"
    },
    "adamsb": {
        "Gen 9 SV Animated - SAME QUALITY CHECK MISSING": "Gen9 SV-Animated",
        "Gen 9 SV Shiny Animated - SAME QUALITY CHECK MISSING": "Gen9 SV-Shiny-Animated"
    }
}


DIRECTORIES_CONTAINING_BATTLE_ANIMATIONS = ["Gen 6 XY w Battle Animations", "Gen 8 SwSh Animated - SAME QUALITY CHECK MISSING"]




#|================================================================================================|
#|~~~~~~~~~~~~~~~~~~~~~~~~~~~[     UNIVERSAL FORM TRANSLATIONS     ]~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~|
#|================================================================================================|

DL_UNIVERSAL_FORM_MAP = {
    "root": {
        "-f": "(Female)",
        # NOTE: I did have to modify these since root split them as Mega <poke name> X
        "-Mega_X": "Mega X",
        "-Mega_Y": "Mega Y",
        "-Mega": "Mega ",   # This after X&Y so when looping through Mega wont trigger a form meant to be X or Y
        "-Region_Alola": "(Alola",
        "-Region_Galar": "(Galar",
        "-Region_Hisui": "(Hisuian",
        "-Region_Paldea": "Paldea"  # Covers both Tauros and Wooper, which are formatted differently
    },
    "pkparaiso": {
        "-f": "-f",
        "-Gigantamax": "-gigantamax",
        "-Mega_X": "-megax",
        "-Mega_Y": "-megay",
        "-Mega": "-mega",   # This after X&Y so when looping through Mega wont trigger a form meant to be X or Y
        "-Region_Alola": "-alola",
        "-Region_Galar": "-galar",
        "-Region_Hisui": "-hisuian",
        "-Region_Paldea": "-paldea"
    },
    "adamsb": {     # Only gen9 stills
        "-f": "f",
        "-Region_Paldea": "-p"
    }
}




#|================================================================================================|
#|~~~~~~~~~~~~~~~~~~~~~~~~~~~[     SPECIES FORM TRANSLATIONS     ]~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~|
#|================================================================================================|

CREATOR_TYPE_FORM_MAP = {
    "root": {
        "-Form_Normal": "Normal",
        "-Form_Fighting": "Fighting", 
        "-Form_Flying": "Flying", 
        "-Form_Poison": "Poison", 
        "-Form_Ground": "Ground", 
        "-Form_Rock": "Rock", 
        "-Form_Bug": "Bug", 
        "-Form_Ghost": "Ghost", 
        "-Form_Steel": "Steel", 
        "-Form_Fire": "Fire", 
        "-Form_Water": "Water", 
        "-Form_Grass": "Grass", 
        "-Form_Electric": "Electric", 
        "-Form_Psychic": "Psychic", 
        "-Form_Ice": "Ice", 
        "-Form_Dragon": "Dragon", 
        "-Form_Dark": "Dark", 
        "-Form_Fairy": "Fairy", 
    },
    "pkparaiso": {
        "-Form_Normal": "-normal",
        "-Form_Fighting": "-fighting", 
        "-Form_Flying": "-flying", 
        "-Form_Poison": "-poison", 
        "-Form_Ground": "-ground", 
        "-Form_Rock": "-rock", 
        "-Form_Bug": "-bug", 
        "-Form_Ghost": "-ghost", 
        "-Form_Steel": "-steel", 
        "-Form_Fire": "-fire", 
        "-Form_Water": "-water", 
        "-Form_Grass": "-grass", 
        "-Form_Electric": "-electric", 
        "-Form_Psychic": "-psychic", 
        "-Form_Ice": "-ice", 
        "-Form_Dragon": "-dragon", 
        "-Form_Dark": "-dark", 
        "-Form_Fairy": "-fairy", 
    }
}


CREATOR_FORM_TRANSLATION_MAP = {
    # Pikachu
    25: {
        "root": {
            "-Form_Cap_Alola": "(Alola Cap)",
            "-Form_Cap_Hoenn": "(Hoenn Cap)",
            "-Form_Cap_Kalos": "(Kalos Cap)",
            "-Form_Cap_Original": "(Original Cap)",
            "-Form_Cap_Sinnoh": "(Sinnoh Cap)",
            "-Form_Cap_Unova": "(Unova Cap)",
            "-Form_Cap_Partner": "(Partner Cap)",
            "-Form_Cap_World": "(World Cap)"
            # No cosplays past gen 6
        },
        "pkparaiso": {
            "-Form_Cap_Alola": "-alolacap",
            "-Form_Cap_Hoenn": "-hoenncap",
            "-Form_Cap_Kalos": "-kaloscap",
            "-Form_Cap_Original": "-originalcap",
            "-Form_Cap_Partner": "-partnercap",
            "-Form_Cap_Sinnoh": "-sinnohcap",
            "-Form_Cap_Unova": "-unovacap",
            "-Form_Cap_World": "-worldcap"
            # No cosplays even in my XY folder of theirs
        }
    },

    # Tauros (Region Paldea added from universal check)
    128: {
        "root": {
            "-Form_Combat": "Fighting",
            "-Form_Blaze": "Fire",
            "-Form_Aqua": "Water"
        },
        "pkparaiso": {
            "-Form_Combat": "-combat",
            "-Form_Blaze": "-blaze",
            "-Form_Aqua": "-aqua"
        },
        "adamsb": {
            "-Form_Blaze": "-1",
            "-Form_Aqua": "-2",
            "-Form_Combat": ""
        }
    },

    # No Spiky Eared Pichu past gen 4/HOME

    # Unown
    201: {
        "root": {
            "-Form_A": " A",
            "-Form_B": " B",
            "-Form_C": " C",
            "-Form_D": " D",
            "-Form_E": " E",
            "-Form_F": " F",
            "-Form_G": " G",
            "-Form_H": " H",
            "-Form_I": " I",
            "-Form_J": " J",
            "-Form_K": " K",
            "-Form_L": " L",
            "-Form_M": " M",
            "-Form_N": " N",
            "-Form_O": " O",
            "-Form_P": " P",
            "-Form_Qmark": "(Question)",    # QU before Q because Q form would trigger first and misname file
            "-Form_Q": " Q",
            "-Form_R": " R",
            "-Form_S": " S",
            "-Form_T": " T",
            "-Form_U": " U",
            "-Form_V": " V",
            "-Form_W": " W",
            "-Form_X": " X",
            "-Form_Y": " Y",
            "-Form_Z": " Z",
            "-Form_!": "(Exclamation)"
        },
        "pkparaiso": {
            "-Form_A": "-alpha",  # I did have to write this in myself
            "-Form_B": "-bravo",
            "-Form_C": "-charlie",
            "-Form_D": "-delta",
            "-Form_E": "-echo",
            "-Form_F": "-foxtrot",
            "-Form_G": "-golf",
            "-Form_H": "-hotel",
            "-Form_I": "-india",
            "-Form_J": "-juliet",
            "-Form_K": "-kilo",
            "-Form_L": "-lima",
            "-Form_M": "-mike",
            "-Form_N": "-november",
            "-Form_O": "-oscar",
            "-Form_P": "-papa",
            "-Form_Qmark": "-interrogation",
            "-Form_Q": "-quebec",
            "-Form_R": "-romeo",
            "-Form_S": "-sierra",
            "-Form_T": "-tango",
            "-Form_U": "-uniform",
            "-Form_V": "-victor",
            "-Form_W": "-whiskey",
            "-Form_X": "-xray",
            "-Form_Y": "-yankee",
            "-Form_Z": "-zulu",
            "-Form_!": "-exclamation"
        }
    },

    # Sneasel (f added from universal check)
    215: {
        "root": {"-Region_Hisui": "Hisui"},
        "pkparaiso": {"-Region_Hisui": "-hisui"}
    },

    # Castform
    351: {
        "root": {
            "-Form_Rainy": "Rainy",
            "-Form_Snowy": "Snowy",
            "-Form_Sunny": "Sunny"
        },
        "pkparaiso": {
            "-Form_Rainy": "-rainy",
            "-Form_Snowy": "-snowy",
            "-Form_Sunny": "-sunny"
        }
    },

    # Kyogre & Groudon
    382: {
        "root": {"-Form_Primal": "Primal"},
        "pkparaiso": {"-Form_Primal": "-primal"}
    },
    383: {
        "root": {"-Form_Primal": "Primal"},
        "pkparaiso": {"-Form_Primal": "-primal"}
    },

    #Deoxys
    386: {
        "root": {
            "-Form_Attack": "Attack",
            "-Form_Defense": "Defense",
            "-Form_Speed": "Speed"
        },
        "pkparaiso": {
            "-Form_Attack": "-attack",
            "-Form_Defense": "-defense",
            "-Form_Speed": "-speed"
        }
    },

    # Burmy & Wormadam
    412: {
        "root": {
            "-Form_Plant_Cloak": "Plant",
            "-Form_Sandy_Cloak": "Sandy",
            "-Form_Trash_Cloak": "Trash"
        },
        "pkparaiso": {
            "-Form_Sandy_Cloak": "-sandy",
            "-Form_Trash_Cloak": "-trash",
            "-Form_Plant_Cloak": ""
        }
    },
    413: {
        "root": {
            "-Form_Plant_Cloak": "Plant",
            "-Form_Sandy_Cloak": "Sandy",
            "-Form_Trash_Cloak": "Trash"
        },
        "pkparaiso": {
            "-Form_Sandy_Cloak": "-sandy",
            "-Form_Trash_Cloak": "-trash",
            "-Form_Plant_Cloak": ""
        }
    },

    #Cherrim
    421: {
        "root": {
            "-Form_Overcast": "Overcast",
            "-Form_Sunshine": "Sunshine"
        },
        "pkparaiso": {
            "-Form_Sunshine": "-sunshine",
            "-Form_Overcast": ""
        }
    },
    
    # Shellos & Gastrodon
    422: {
        "root": {
            "-Form_West": "West",
            "-Form_East": "East"
        },
        "pkparaiso": {
            "-Form_East": "-east",
            "-Form_West": ""
        }
    },
    423: {
        "root": {
            "-Form_West": "West",
            "-Form_East": "East"
        },
        "pkparaiso": {
            "-Form_East": "-east",
            "-Form_West": ""
        }
    },
    
    # Rotom
    479: {
        "root": {
            "-Form_Fan": "Fan",
            "-Form_Frost": "Frost",
            "-Form_Heat": "Heat",
            "-Form_Mow": "Mow",
            "-Form_Wash": "Wash"
        },
        "pkparaiso": {
            "-Form_Fan": "-fan",
            "-Form_Frost": "-frost",
            "-Form_Heat": "-heat",
            "-Form_Mow": "-mow",
            "-Form_Wash": "-wash"
        }
    },
    
    # Dialga & Palkia
    483: {
        "root": {"-Form_Origin": "Origin"},
        "pkparaiso": {"-Form_Origin": "-origin"}
    },
    484: {
        "root": {"-Form_Origin": "Origin"},
        "pkparaiso": {"-Form_Origin": "-origin"}
    },
    
    # Giratina
    487: {
        "root": {
            "-Form_Altered": "Altered",
            "-Form_Origin": "Origin"
        },
        "pkparaiso": {
            "-Form_Origin": "-origin",
            "-Form_Altered": ""
        }
    },
    
    # Shaymin
    492: {
        "root": {
            "-Form_Land": "Land",
            "-Form_Sky": "Sky"
        },
        "pkparaiso": {
            "-Form_Sky": "-sky",
            "-Form_Land": "" 
        }
    },

    # Arceus
    493: {
        "root": CREATOR_TYPE_FORM_MAP["root"],
        "pkparaiso": CREATOR_TYPE_FORM_MAP["pkparaiso"],
    },

    # Basculin
    550: {
        "root": {
            "-Form_Red_Striped": "Red",
            "-Form_Blue_Striped": "Blue",
            "-Form_White_Striped": "White"
        },
        "pkparaiso": {
            "-Form_Blue_Striped": "-blue",
            "-Form_White_Striped": "-white",
            "-Form_Red_Striped": ""
        }
    },

    # Darmanitan
    555: {
        "root": {
            "-Form_Zen": "Zen",
            "-Form_Standard": ""
        },
        "pkparaiso": {
            "-Form_Zen": "-zen",
            "-Form_Standard": ""
        }
    },

    # Deerling & Sawsbuck
    585: {
        "root": {
            "-Form_Spring": "Spring",
            "-Form_Autumn": "Autumn",
            "-Form_Summer": "Summer",
            "-Form_Winter": "Winter"
        },
        "pkparaiso": {
            "-Form_Autumn": "-autumn",
            "-Form_Summer": "-summer",
            "-Form_Winter": "-winter",
            "-Form_Spring": ""
        }
    },
    586: {
        "root": {
            "-Form_Spring": "Spring",
            "-Form_Autumn": "Autumn",
            "-Form_Summer": "Summer",
            "-Form_Winter": "Winter"
        },
        "pkparaiso": {
            "-Form_Autumn": "-autumn",
            "-Form_Summer": "-summer",
            "-Form_Winter": "-winter",
            "-Form_Spring": ""
        }
    },

    # Forces of Nature
    641: {
        "root": {
            "-Form_Incarnate": "Incarnate",
            "-Form_Therian": "Therian"
        },
        "pkparaiso": {
            "-Form_Therian": "-therian",
            "-Form_Incarnate": ""
        }
    },
    642: {
        "root": {
            "-Form_Incarnate": "Incarnate",
            "-Form_Therian": "Therian"
        },
        "pkparaiso": {
            "-Form_Therian": "-therian",
            "-Form_Incarnate": ""
        }
    },
    645: {
        "root": {
            "-Form_Incarnate": "Incarnate",
            "-Form_Therian": "Therian"
        },
        "pkparaiso": {
            "-Form_Therian": "-therian",
            "-Form_Incarnate": ""
        }
    },

    # Kyurem
    646: {
        "root": {
            "-Form_Black": "Black",
            "-Form_Black_Overdrive": EXCLUDE_TRANSLATIONS_MAP["DBH"],   #TODO
            "-Form_White": "White",
            "-Form_White_Overdrive": EXCLUDE_TRANSLATIONS_MAP["DBH"]    #TODO
        },
        "pkparaiso": {
            "-Form_Black": "-black",
            "-Form_Black_Overdrive": "-overdriveblack",
            "-Form_White": "-white",
            "-Form_White_Overdrive": "-overdrivewhite"
        },
    },

    # Keldeo
    647: {
        "root": {
            "-Form_Ordinary": "Ordinary",
            "-Form_Resolute": "Resolute"
        },
        "pkparaiso": {
            "-Form_Resolute": "-resolute",
            "-Form_Ordinary": ""
        }
    },

    # Meloetta
    648: {
        "root": {
            "-Form_Aria": "Aria",
            "-Form_Pirouette": "Pirouette"
        },
        "pkparaiso": {
            "-Form_Pirouette": "-pirouette",
            "-Form_Aria": ""
        }
    },

    # Genesect
    649: {
        "root": {
            "-Form_Douse_Drive": "Douse",
            "-Form_Burn_Drive": "Burn",
            "-Form_Chill_Drive": "Chill",
            "-Form_Shock_Drive": "Shock"
        },
        "pkparaiso": {
            "-Form_Douse_Drive": "-douse",
            "-Form_Burn_Drive": "-burn",
            "-Form_Chill_Drive": "-chill",
            "-Form_Shock_Drive": "-shock"
        }
    },

    # Greninja
    658: {
        "root": {"-Form_Ash": "Ash"},
        "pkparaiso": {"-Form_Ash": "-ash"}
    },

    # Vivillon
    666: {
        "root": {
            "-Form_Archipelago": "Archipelago",
            "-Form_Continental": "Continental",
            "-Form_Elegant": "Elegant",
            "-Form_Fancy": "Fancy",
            "-Form_Garden": "Garden",
            "-Form_High_Plains": "High Plains",
            "-Form_Icy_Snow": "Icy Snow",
            "-Form_Jungle": "Jungle",
            "-Form_Marine": "Marine",
            "-Form_Meadow": "Meadow",
            "-Form_Modern": "Modern",
            "-Form_Monsoon": "Monsoon",
            "-Form_Ocean": "Ocean",
            "-Form_Poke_Ball": "Pokeball",
            "-Form_Polar": "Polar",
            "-Form_River": "River",
            "-Form_Sandstorm": "Sandstorm",
            "-Form_Savanna": "Savanna",
            "-Form_Sun": "Sun",
            "-Form_Tundra": "Tundra"
        },
        "pkparaiso": {
            "-Form_Archipelago": "-archipelago",
            "-Form_Continental": "-continental",
            "-Form_Elegant": "-elegant",
            "-Form_Fancy": "-fancy",
            "-Form_Garden": "-garden",
            "-Form_High_Plains": "-highplains",
            "-Form_Icy_Snow": "-icysnow",
            "-Form_Jungle": "-jungle",
            "-Form_Marine": "-marine",
            "-Form_Meadow": "-meadow",
            "-Form_Modern": "-modern",
            "-Form_Monsoon": "-monsoon",
            "-Form_Ocean": "-ocean",
            "-Form_Poke_Ball": "-pokeball",
            "-Form_Polar": "-polar",
            "-Form_River": "-river",
            "-Form_Sandstorm": "-sandstorm",
            "-Form_Savanna": "-savanna",
            "-Form_Sun": "-sun",
            "-Form_Tundra": "-tundra"
        }
    },

    # Flabebe, Floette, and Florges
    669: {
        "root": {
            "-Form_Red_Flower": "Red",
            "-Form_Blue_Flower": "Blue",
            "-Form_Orange_Flower": "Orange",
            "-Form_White_Flower": "White",
            "-Form_Yellow_Flower": "Yellow"
        },
        "pkparaiso": {
            "-Form_Blue_Flower": "-blue",
            "-Form_Orange_Flower": "-orange",
            "-Form_White_Flower": "-white",
            "-Form_Yellow_Flower": "-yellow",
            "-Form_Red_Flower": ""
        }
    },
    670: {
        "root": {
            "-Form_Red_Flower": "Red",
            "-Form_Blue_Flower": "Blue",
            "-Form_Orange_Flower": "Orange",
            "-Form_White_Flower": "White",
            "-Form_Yellow_Flower": "Yellow",
            "-Form_Eternal_Flower": "Eternal"
        },
        "pkparaiso": {
            "-Form_Eternal_Flower": "-eternal",
            "-Form_Blue_Flower": "-blue",
            "-Form_Orange_Flower": "-orange",
            "-Form_White_Flower": "-white",
            "-Form_Yellow_Flower": "-yellow",
            "-Form_Red_Flower": ""
        }
    },
    671: {
        "root": {
            "-Form_Red_Flower": "Red",
            "-Form_Blue_Flower": "Blue",
            "-Form_Orange_Flower": "Orange",
            "-Form_White_Flower": "White",
            "-Form_Yellow_Flower": "Yellow"
        },
        "pkparaiso": {
            "-Form_Blue_Flower": "-blue",
            "-Form_Orange_Flower": "-orange",
            "-Form_White_Flower": "-white",
            "-Form_Yellow_Flower": "-yellow",
            "-Form_Red_Flower": ""
        },
    },

    # Furfrou
    676: {
        "root": {
            "-Form_Dandy_Trim": "Dandy",
            "-Form_Debutante_Trim": "Debutante",
            "-Form_Diamond_Trim": "Diamond",
            "-Form_Heart_Trim": "Heart",
            "-Form_Kabuki_Trim": "Kabuki",
            "-Form_La_Reine_Trim": "La Reine",
            "-Form_Matron_Trim": "Matron",
            "-Form_Pharaoh_Trim": "Pharaoh",
            "-Form_Star_Trim": "Star"
        },
        "pkparaiso": {
            "-Form_Dandy_Trim": "-dandy",
            "-Form_Debutante_Trim": "-debutante",
            "-Form_Diamond_Trim": "-diamond",
            "-Form_Heart_Trim": "-heart",
            "-Form_Kabuki_Trim": "-kabuki",
            "-Form_La_Reine_Trim": "-lareine",
            "-Form_Matron_Trim": "-matron",
            "-Form_Pharaoh_Trim": "-pharaoh",
            "-Form_Star_Trim": "-star"
        }
    },

    # Aegislash
    681: {
        "root": {
            "-Form_Shield": "Shield",
            "-Form_Blade": "Blade"
        },
        "pkparaiso": {
            "-Form_Blade": "-blade",
            "-Form_Shield": ""
        }
    },

    # Pumpkaboo & Gourgeist
    710: {
        "root": {
            # TODO: Make the 1 average? Convert my webms?
            # Doesn't have these... I do in webm
            "-Form_Average_Size": EXCLUDE_TRANSLATIONS_MAP["DNE"],
            "-Form_Small_Size": EXCLUDE_TRANSLATIONS_MAP["DNE"],
            "-Form_Large_Size": EXCLUDE_TRANSLATIONS_MAP["DNE"],
            "-Form_Super_Size": EXCLUDE_TRANSLATIONS_MAP["DNE"]
        },
        "pkparaiso": {
            "-Form_Small_Size": "-small",
            "-Form_Large_Size": "-large",
            "-Form_Super_Size": "-super",
            "-Form_Average_Size": ""
        }
    },
    711: {
        "root": {
            # TODO: Make the 1 average? Convert my webms?
            # Doesn't have these... I do in webm
            "-Form_Average_Size": EXCLUDE_TRANSLATIONS_MAP["DNE"],
            "-Form_Small_Size": EXCLUDE_TRANSLATIONS_MAP["DNE"],
            "-Form_Large_Size": EXCLUDE_TRANSLATIONS_MAP["DNE"],
            "-Form_Super_Size": EXCLUDE_TRANSLATIONS_MAP["DNE"]
        },
        "pkparaiso": {
            "-Form_Small_Size": "-small",
            "-Form_Large_Size": "-large",
            "-Form_Super_Size": "-super",
            "-Form_Average_Size": ""
        }
    },

    # Xerneas
    716: {
        "root": {
            "-Form_Active": "Active",
            "-Form_Neutral": EXCLUDE_TRANSLATIONS_MAP["DNE"]    # TODO: See if it exists in Gen9 SV, if not do I have webm
        },
        "pkparaiso": {
            "-Form_Active": "-active",
            "-Form_Neutral": ""
        }
    },

    # Zygarde
    718: {
        "root": {
            "-Form_50%": "50",
            "-Form_Complete": "Complete",
            "-Form_10%": "10"
        },
        "pkparaiso": {
            "-Form_Complete": "-complete",
            "-Form_10%": "-10percent",
            "-Form_50%": ""
        }
    },

    # Hoopa
    720: {
        "root": {
            "-Form_Confined": "Confined",
            "-Form_Unbound": "Unbound"
        },
        "pkparaiso": {
            "-Form_Confined": "-confined",
            "-Form_Unbound": "-unbound"
        }
    },

    # Oricorio
    741: {
        "root": {
            "-Form_Baile": "Baile",
            "-Form_Pa'u": "Pa_u",
            "-Form_Pom_Pom": "Pom-Pom",
            "-Form_Sensu": "Sensu"
        },
        "pkparaiso": {
            "-Form_Baile": "-baile",
            "-Form_Pa'u": "-pau",
            "-Form_Pom_Pom": "-pompom",
            "-Form_Sensu": "-sensu"
        }
    },

    # Lycanroc
    745: {
        "root": {
            "-Form_Midday": "Midday",
            "-Form_Dusk": "Dusk",
            "-Form_Midnight": "Midnight"
        },
        "pkparaiso": {
            "-Form_Midday": "-midday",
            "-Form_Dusk": "-dusk",
            "-Form_Midnight": "-midnight"
        },
    },

    # Wishiwashi
    746: {
        "root": {
            "-Form_Solo": "Solo",
            "-Form_School": "School"
        },
        "pkparaiso": {
            "-Form_School": "-school",
            "-Form_Solo": ""
        }
    },

    # Silvally
    773: {
        "root": CREATOR_TYPE_FORM_MAP["root"],
        "pkparaiso": CREATOR_TYPE_FORM_MAP["pkparaiso"]
    },

    # Minior
    774: {
        "root": {
            "-Form_Meteor": "Meteor",
            "-Form_Blue_Core": "Blue",
            "-Form_Green_Core": "Green",
            "-Form_Indigo_Core": "Indigo",
            "-Form_Orange_Core": "Orange",
            "-Form_Red_Core": "Red",
            "-Form_Violet_Core": "Violet",
            "-Form_Yellow_Core": "Yellow",
            "-Form_Core": ""   # This is the shiny sprite TODO
        },
        "pkparaiso": {
            "-Form_Blue_Core": "-blue",
            "-Form_Green_Core": "-green",
            "-Form_Indigo_Core": "-indigo",
            "-Form_Orange_Core": "-orange",
            "-Form_Red_Core": "-red",
            "-Form_Violet_Core": "-violet",
            "-Form_Yellow_Core": "-yellow",
            "-Form_Core": "-shiny",
            "-Form_Meteor": ""
        }
    },

    # Mimikyu
    778: {
        "root": {
            "-Form_Disguised": "Disguised",
            "-Form_Busted": "Busted"
        },
        "pkparaiso": {
            "-Form_Busted": "-busted",
            "-Form_Disguised": ""
        }
    },

    # Solgaleo
    # TODO: Dont exist in HOME, Gen9 tho?
    791: {
        "root": {"-Form_Radiant_Sun": EXCLUDE_TRANSLATIONS_MAP["DNE"]},
        "pkparaiso": {"-Form_Radiant_Sun": "-radiantsun"},
    },

    # Lunala
    #  TODO: Dont exist in HOME, Gen9 tho?
    792: {
        "root": {"-Form_Full_Moon": EXCLUDE_TRANSLATIONS_MAP["DNE"]},
        "pkparaiso": {"-Form_Full_Moon": "-fullmoonphase"},
    },

    # Necrozma
    800: {
        "root": {
            "-Form_Dawn_Wings": "Dawn Wings",
            "-Form_Dusk_Mane": "Dusk Mane",
            "-Form_Ultra": "Ultra"
        },
        "pkparaiso": {
            "-Form_Dawn_Wings": "-dawnwings",
            "-Form_Dusk_Mane": "-duskmane",
            "-Form_Ultra": "-ultra"
        }
    },

    # Magearna
    801: {
        "root": {"-Form_Original_Color": "Original Color"},
        "pkparaiso": {"-Form_Original_Color": "-originalcolor"},
    },

    # Cramorant
    845: {
        "root": {
            "-Form_Gorging": "Gorging",
            "-Form_Gulping": "Gulping"
        },
        "pkparaiso": {
            "-Form_Gorging": "-gorging",
            "-Form_Gulping": "-gulping"
        }
    },

    # Toxtricity
    849: {
        "root": {
            "-Form_Amped": "Amped",
            "-Form_Low_Key": "Low Key"
        },
        "pkparaiso": {
            "-Form_Low_Key": "-lowkey",
            "-Form_Amped": "-amped"
        }
    },

    # Sinistea & Polteageist not applicable since their forms only matter to show stamps, which are static only

    # Alcremie
    869: {
        "root": {
            "-Form_Caramel_Swirl_Berry_Sweet": "(Caramel Swirl) (Berry Sweet)",
            "-Form_Caramel_Swirl_Clover_Sweet": "(Caramel Swirl) (Clover Sweet)",
            "-Form_Caramel_Swirl_Flower_Sweet": "(Caramel Swirl) (Flower Sweet)",
            "-Form_Caramel_Swirl_Love_Sweet": "(Caramel Swirl) (Love Sweet)",
            "-Form_Caramel_Swirl_Ribbon_Sweet": "(Caramel Swirl) (Ribbon Sweet)",
            "-Form_Caramel_Swirl_Star_Sweet": "(Caramel Swirl) (Star Sweet)",
            "-Form_Caramel_Swirl_Strawberry_Sweet": "(Caramel Swirl) (Strawberry Sweet)",
            "-Form_Lemon_Cream_Berry_Sweet": "(Lemon Cream) (Berry Sweet)",
            "-Form_Lemon_Cream_Clover_Sweet": "(Lemon Cream) (Clover Sweet)",
            "-Form_Lemon_Cream_Flower_Sweet": "(Lemon Cream) (Flower Sweet)",
            "-Form_Lemon_Cream_Love_Sweet": "(Lemon Cream) (Love Sweet)",
            "-Form_Lemon_Cream_Ribbon_Sweet": "(Lemon Cream) (Ribbon Sweet)",
            "-Form_Lemon_Cream_Star_Sweet": "(Lemon Cream) (Star Sweet)",
            "-Form_Lemon_Cream_Strawberry_Sweet": "(Lemon Cream) (Strawberry Sweet)",
            "-Form_Matcha_Cream_Berry_Sweet": "(Matcha Cream) (Berry Sweet)",
            "-Form_Matcha_Cream_Clover_Sweet": "(Matcha Cream) (Clover Sweet)",
            "-Form_Matcha_Cream_Flower_Sweet": "(Matcha Cream) (Flower Sweet)",
            "-Form_Matcha_Cream_Love_Sweet": "(Matcha Cream) (Love Sweet)",
            "-Form_Matcha_Cream_Ribbon_Sweet": "(Matcha Cream) (Ribbon Sweet)",
            "-Form_Matcha_Cream_Star_Sweet": "(Matcha Cream) (Star Sweet)",
            "-Form_Matcha_Cream_Strawberry_Sweet": "(Matcha Cream) (Strawberry Sweet)",
            "-Form_Mint_Cream_Berry_Sweet": "(Mint Cream) (Berry Sweet)",
            "-Form_Mint_Cream_Clover_Sweet": "(Mint Cream) (Clover Sweet)",
            "-Form_Mint_Cream_Flower_Sweet": "(Mint Cream) (Flower Sweet)",
            "-Form_Mint_Cream_Love_Sweet": "(Mint Cream) (Love Sweet)",
            "-Form_Mint_Cream_Ribbon_Sweet": "(Mint Cream) (Ribbon Sweet)",
            "-Form_Mint_Cream_Star_Sweet": "(Mint Cream) (Star Sweet)",
            "-Form_Mint_Cream_Strawberry_Sweet": "(Mint Cream) (Strawberry Sweet)",
            "-Form_Rainbow_Swirl_Berry_Sweet": "(Rainbow Swirl) (Berry Sweet)",
            "-Form_Rainbow_Swirl_Clover_Sweet": "(Rainbow Swirl) (Clover Sweet)",
            "-Form_Rainbow_Swirl_Flower_Sweet": "(Rainbow Swirl) (Flower Sweet)",
            "-Form_Rainbow_Swirl_Love_Sweet": "(Rainbow Swirl) (Love Sweet)",
            "-Form_Rainbow_Swirl_Ribbon_Sweet": "(Rainbow Swirl) (Ribbon Sweet)",
            "-Form_Rainbow_Swirl_Star_Sweet": "(Rainbow Swirl) (Star Sweet)",
            "-Form_Rainbow_Swirl_Strawberry_Sweet": "(Rainbow Swirl) (Strawberry Sweet)",
            "-Form_Ruby_Cream_Berry_Sweet": "(Ruby Cream) (Berry Sweet)",
            "-Form_Ruby_Cream_Clover_Sweet": "(Ruby Cream) (Clover Sweet)",
            "-Form_Ruby_Cream_Flower_Sweet": "(Ruby Cream) (Flower Sweet)",
            "-Form_Ruby_Cream_Love_Sweet": "(Ruby Cream) (Love Sweet)",
            "-Form_Ruby_Cream_Ribbon_Sweet": "(Ruby Cream) (Ribbon Sweet)",
            "-Form_Ruby_Cream_Star_Sweet": "(Ruby Cream) (Star Sweet)",
            "-Form_Ruby_Cream_Strawberry_Sweet": "(Ruby Cream) (Strawberry Sweet)",
            "-Form_Ruby_Swirl_Berry_Sweet": "(Ruby Swirl) (Berry Sweet)",
            "-Form_Ruby_Swirl_Clover_Sweet": "(Ruby Swirl) (Clover Sweet)",
            "-Form_Ruby_Swirl_Flower_Sweet": "(Ruby Swirl) (Flower Sweet)",
            "-Form_Ruby_Swirl_Love_Sweet": "(Ruby Swirl) (Love Sweet)",
            "-Form_Ruby_Swirl_Ribbon_Sweet": "(Ruby Swirl) (Ribbon Sweet)",
            "-Form_Ruby_Swirl_Star_Sweet": "(Ruby Swirl) (Star Sweet)",
            "-Form_Ruby_Swirl_Strawberry_Sweet": "(Ruby Swirl) (Strawberry Sweet)",
            "-Form_Salted_Cream_Berry_Sweet": "(Salted Cream) (Berry Sweet)",
            "-Form_Salted_Cream_Clover_Sweet": "(Salted Cream) (Clover Sweet)",
            "-Form_Salted_Cream_Flower_Sweet": "(Salted Cream) (Flower Sweet)",
            "-Form_Salted_Cream_Love_Sweet": "(Salted Cream) (Love Sweet)",
            "-Form_Salted_Cream_Ribbon_Sweet": "(Salted Cream) (Ribbon Sweet)",
            "-Form_Salted_Cream_Star_Sweet": "(Salted Cream) (Star Sweet)",
            "-Form_Salted_Cream_Strawberry_Sweet": "(Salted Cream) (Strawberry Sweet)",
            "-Form_Vanilla_Cream_Berry_Sweet": "(Vanilla Cream) (Berry Sweet)",
            "-Form_Vanilla_Cream_Clover_Sweet": "(Vanilla Cream) (Clover Sweet)",
            "-Form_Vanilla_Cream_Flower_Sweet": "(Vanilla Cream) (Flower Sweet)",
            "-Form_Vanilla_Cream_Love_Sweet": "(Vanilla Cream) (Love Sweet)",
            "-Form_Vanilla_Cream_Ribbon_Sweet": "(Vanilla Cream) (Ribbon Sweet)",
            "-Form_Vanilla_Cream_Star_Sweet": "(Vanilla Cream) (Star Sweet)",
            "-Form_Vanilla_Cream_Strawberry_Sweet": "(Vanilla Cream) (Strawberry Sweet)",
            # Shinies (which have only berry differences)
            "-Form_Berry_Sweet": "(Vanilla Cream) (Berry Sweet)",
            "-Form_Clover_Sweet": "(Vanilla Cream) (Clover Sweet)",
            "-Form_Flower_Sweet": "(Vanilla Cream) (Flower Sweet)",
            "-Form_Love_Sweet": "(Vanilla Cream) (Love Sweet)",
            "-Form_Ribbon_Sweet": "(Vanilla Cream) (Ribbon Sweet)",
            "-Form_Star_Sweet": "(Vanilla Cream) (Star Sweet)",
            "-Form_Strawberry_Sweet": "(Vanilla Cream) (Strawberry Sweet)"
        },
        "pkparaiso": {
            "-Form_Caramel_Swirl_Berry_Sweet": "caramel-swirl-berry",
            "-Form_Caramel_Swirl_Clover_Sweet": "caramel-swirl-clover",
            "-Form_Caramel_Swirl_Flower_Sweet": "caramel-swirl-flower",
            "-Form_Caramel_Swirl_Love_Sweet": "caramel-swirl-love",
            "-Form_Caramel_Swirl_Ribbon_Sweet": "caramel-swirl-ribbon",
            "-Form_Caramel_Swirl_Star_Sweet": "caramel-swirl-star",
            "-Form_Caramel_Swirl_Strawberry_Sweet": "caramel-swirl-strawberry",
            "-Form_Lemon_Cream_Berry_Sweet": "lemon-cream-berry",
            "-Form_Lemon_Cream_Clover_Sweet": "lemon-cream-clover",
            "-Form_Lemon_Cream_Flower_Sweet": "lemon-cream-flower",
            "-Form_Lemon_Cream_Love_Sweet": "lemon-cream-love",
            "-Form_Lemon_Cream_Ribbon_Sweet": "lemon-cream-ribbon",
            "-Form_Lemon_Cream_Star_Sweet": "lemon-cream-star",
            "-Form_Lemon_Cream_Strawberry_Sweet": "lemon-cream-strawberry",
            "-Form_Matcha_Cream_Berry_Sweet": "matcha-cream-berry",
            "-Form_Matcha_Cream_Clover_Sweet": "matcha-cream-clover",
            "-Form_Matcha_Cream_Flower_Sweet": "matcha-cream-flower",
            "-Form_Matcha_Cream_Love_Sweet": "matcha-cream-love",
            "-Form_Matcha_Cream_Ribbon_Sweet": "matcha-cream-ribbon",
            "-Form_Matcha_Cream_Star_Sweet": "matcha-cream-star",
            "-Form_Matcha_Cream_Strawberry_Sweet": "matcha-cream-strawberry",
            "-Form_Mint_Cream_Berry_Sweet": "mint-cream-berry",
            "-Form_Mint_Cream_Clover_Sweet": "mint-cream-clover",
            "-Form_Mint_Cream_Flower_Sweet": "mint-cream-flower",
            "-Form_Mint_Cream_Love_Sweet": "mint-cream-love",
            "-Form_Mint_Cream_Ribbon_Sweet": "mint-cream-ribbon",
            "-Form_Mint_Cream_Star_Sweet": "mint-cream-star",
            "-Form_Mint_Cream_Strawberry_Sweet": "mint-cream-strawberry",
            "-Form_Rainbow_Swirl_Berry_Sweet": "rainbow-swirl-berry",
            "-Form_Rainbow_Swirl_Clover_Sweet": "rainbow-swirl-clover",
            "-Form_Rainbow_Swirl_Flower_Sweet": "rainbow-swirl-flower",
            "-Form_Rainbow_Swirl_Love_Sweet": "rainbow-swirl-love",
            "-Form_Rainbow_Swirl_Ribbon_Sweet": "rainbow-swirl-ribbon",
            "-Form_Rainbow_Swirl_Star_Sweet": "rainbow-swirl-star",
            "-Form_Rainbow_Swirl_Strawberry_Sweet": "rainbow-swirl-strawberry",
            "-Form_Ruby_Cream_Berry_Sweet": "ruby-cream-berry",
            "-Form_Ruby_Cream_Clover_Sweet": "ruby-cream-clover",
            "-Form_Ruby_Cream_Flower_Sweet": "ruby-cream-flower",
            "-Form_Ruby_Cream_Love_Sweet": "ruby-cream-love",
            "-Form_Ruby_Cream_Ribbon_Sweet": "ruby-cream-ribbon",
            "-Form_Ruby_Cream_Star_Sweet": "ruby-cream-star",
            "-Form_Ruby_Cream_Strawberry_Sweet": "ruby-cream-strawberry",
            "-Form_Ruby_Swirl_Berry_Sweet": "ruby-swirl-berry",
            "-Form_Ruby_Swirl_Clover_Sweet": "ruby-swirl-clover",
            "-Form_Ruby_Swirl_Flower_Sweet": "ruby-swirl-flower",
            "-Form_Ruby_Swirl_Love_Sweet": "ruby-swirl-love",
            "-Form_Ruby_Swirl_Ribbon_Sweet": "ruby-swirl-ribbon",
            "-Form_Ruby_Swirl_Star_Sweet": "ruby-swirl-star",
            "-Form_Ruby_Swirl_Strawberry_Sweet": "ruby-swirl-strawberry",
            "-Form_Salted_Cream_Berry_Sweet": "salted-cream-berry",
            "-Form_Salted_Cream_Clover_Sweet": "salted-cream-clover",
            "-Form_Salted_Cream_Flower_Sweet": "salted-cream-flower",
            "-Form_Salted_Cream_Love_Sweet": "salted-cream-love",
            "-Form_Salted_Cream_Ribbon_Sweet": "salted-cream-ribbon",
            "-Form_Salted_Cream_Star_Sweet": "salted-cream-star",
            "-Form_Salted_Cream_Strawberry_Sweet": "salted-cream-strawberry",
            "-Form_Vanilla_Cream_Berry_Sweet": "vanilla-cream-berry",
            "-Form_Vanilla_Cream_Clover_Sweet": "vanilla-cream-clover",
            "-Form_Vanilla_Cream_Flower_Sweet": "vanilla-cream-flower",
            "-Form_Vanilla_Cream_Love_Sweet": "vanilla-cream-love",
            "-Form_Vanilla_Cream_Ribbon_Sweet": "vanilla-cream-ribbon",
            "-Form_Vanilla_Cream_Star_Sweet": "vanilla-cream-star",
            "-Form_Vanilla_Cream_Strawberry_Sweet": "vanilla-cream-strawberry",
            # They list all their shinies with all creams/swirls
            "-Form_Berry_Sweet": "vanilla-cream-berry",
            "-Form_Clover_Sweet": "vanilla-cream-clover",
            "-Form_Flower_Sweet": "vanilla-cream-flower",
            "-Form_Love_Sweet": "vanilla-cream-love",
            "-Form_Ribbon_Sweet": "vanilla-cream-ribbon",
            "-Form_Star_Sweet": "vanilla-cream-star",
            "-Form_Strawberry_Sweet": "vanilla-cream-strawberry"
        }
    },

    # Eiscue
    875: {
        "root": {
            "-Form_Ice_Face": "Ice",
            "-Form_Noice_Face": "Noice"
        },
        "pkparaiso": {
            "-Form_Noice_Face": "-noice",
            "-Form_Ice_Face": ""
        }
    },

    # Morpeko
    877: {
        "root": {
            "-Form_Full_Belly": "Full Belly",
            "-Form_Hangry": "Hangry"
        },
        "pkparaiso": {
            "-Form_Hangry": "-hangry",
            "-Form_Full_Belly": ""
        }
    },

    # Zacian & Zamazenta
    888: {
        "root": {
            "-Form_Hero_of_Many_Battles": "Hero of Many Battles",
            "-Form_Crowned_Sword": "Crowned"
        },
        "pkparaiso": {
            "-Form_Crowned_Sword": "-crowned",
            "-Form_Hero_of_Many_Battles": ""
        }
    },
    889: {
        "root": {
            "-Form_Hero_of_Many_Battles": "Hero of Many Battles",
            "-Form_Crowned_Shield": "Crowned"
        },
        "pkparaiso": {
            "-Form_Crowned_Sword": "-crowned",
            "-Form_Hero_of_Many_Battles": ""
        }
    },

    # Eternatus
    890: {
        "root": {
            "-Form_Eternamax": EXCLUDE_TRANSLATIONS_MAP["DNE"]
        },
        "pkparaiso": {
            "-Form_Eternamax": "-eternamax"
        }
    },
    
    # Urshifu
    892: {
        "root": {
            "-Form_Single_Strike": "Single Strike",
            "-Form_Rapid_Strike": "Rapid Strike"
        },
        "pkparaiso": {
            "-Form_Single_Strike": "-singlestrike",
            "-Form_Rapid_Strike": "-rapidstrike"
        }
    },

    # Zarude
    893: {
        "root": {"-Form_Dada": "Dada"},
        "pkpariaso": {"-Form_Dada": "-dada"},
    },

    # Calyrex
    898: {
        "root": {
            "-Form_Ice_Rider": "Ice",
            "-Form_Shadow_Rider": "Shadow"
        },
        "pkparaiso": {
            "-Form_Ice_Rider": "-ice",
            "-Form_Shadow_Rider": "-shadow"
        }
    },

    # Ursaluna
    901: {
        "root": {
            "-Form_Bloodmoon": "Blood Moon"
        }
    },

    # Enamorus
    905: {
        "root": {
            "-Form_Incarnate": "Incarnate",
            "-Form_Therian": "Therian"
        }
    },

    # Maushold
    925: {
        "root": {
            "-Form_Family_of_Three": "Three",
            "-Form_Family_of_Four": "Four"
        },
        "adamsb": {
            "-Form_Family_of_Three": "-1",
            "-Form_Family_of_Four": ""
        }
    },

    # Squawkabilly
    931: {
        "root": {
            "-Form_Blue_Plumage": "Blue",
            "-Form_Green_Plumage": "Green",
            "-Form_White_Plumage": "White",
            "-Form_Yellow_Plumage": "Yellow"
        },
        "adamsb": {
            "-Form_Blue_Plumage": "-1", 
            "-Form_White_Plumage": "-3", 
            "-Form_Yellow_Plumage": "-2",
            "-Form_Green_Plumage": "",
        }
    },

    # Palafin
    964: {
        "root": {
            "-Form_Zero": "Zero",
            "-Form_Hero": "Hero"
        },
        "adamsb": {
            "-Form_Hero": "-1",
            "-Form_Zero": ""
        }
    },
    
    # Tatsugiri
    978: {
        "root": {
            "-Form_Curly": "Curly",
            "-Form_Droopy": "Droopy",
            "-Form_Stretchy": "Stretchy"
        },
        "adamsb": {
            "-Form_Droopy": "-1",
            "-Form_Stretchy": "-2",
            "-Form_Curly": ""
        }
    },

    # Dudunsparce
    982: {
        "root": {
            "-Form_Two_Segment": "Two",
            "-Form_Three_Segment": "Three"
        },
        "adamsb": {
            "-Form_Three_Segment": "-1",
            "-Form_Two_Segment": ""
        },
    },

    # Gimmighoul
    999: {
        "root": {
            "-Form_Roaming": "Roaming",
            "-Form_Chest": ""
        },
        "adamsb": {
            "-Form_Roaming": "-1",
            "-Form_Chest": ""
        }
    },

    # Poltchageist & Sinistcha not applicable since only forms used for stamps, which aren't animated

    # Ogerpon
    1017: {
        "root": {
            "-Form_Cornerstone_Mask": "Cobblestone",
            "-Form_Hearthflame_Mask": "Hearthflame",
            "-Form_Teal_Mask": "Teal",
            "-Form_Wellspring_Mask": "Wellspring"
        }
    },

    # Terapagos
    1024: {
        "root": {
            "-Form_Normal": "Normal",
            "-Form_Terastal": "Terastal",
            "-Form_Stellar": "Stellar"  # TODO: Check Gen9, not in HOME
        }
    }
}