import requests     # For fetching HTML
from bs4 import BeautifulSoup   # For parsing HTML
import xlrd     # For reading excel data (female, forms, etc)
import urllib.request      # For saving images
import re   # To check each name is formatted properly
import time     # To simulate a pause between each page opening
import os.path   # To skip a file if it already exists

# SPREADSHEET DATA
pokemon_info = xlrd.open_workbook('C:\\Users\\ejone\\OneDrive\\Desktop\\Code\\Javascript\\p5\\projects\\Pokeball Pokemon Comparison\\Pokemon Info.xls')
sheet = pokemon_info.sheet_by_index(0)

def cell_value(row, col):
    return (sheet.cell_value(row, col))

def isnt_empty(row, col):
    return (str(cell_value(row, col)) != "")

def is_empty(row, col):
    return (cell_value(row, col) == empty_cell.value)

# Returns column number from column name
def get_col_number(col_name):
    for col in range(sheet.ncols):
        if (cell_value(1, col) == col_name):
            return col


# WEB DATA
sprite_page = requests.get("https://www.wikidex.net/wiki/Categor%C3%ADa:Sprites_de_Pok%C3%A9mon")
sprite_page_soup = BeautifulSoup(sprite_page.content, 'html.parser')

game_sprites_link_table = sprite_page_soup.find("table")
games_by_gen = []

# Crude translations due to the page being in spanish lol
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

def get_game(a):
    # From titles, not text, so shiny pokemon (who's text is V) can still get the game
    title = a["title"].split("Pokémon ", 1)[1]
    title = game_translate(title)
    return(title)

def game_title_replace(old, new):
    global game
    global game_str

    if old in game:
        game_str = game_str.replace(old, new)

def form_translate_split(pokemon, spanish_form, translated_form):
    global form
    global split_name

    if pokemon in split_name and pokemon != split_name:
        if spanish_form in split_name:
            form = " " + translated_form
            split_name = split_name.split(" " + spanish_form)[0]



def type_form_translate_split():
    global form
    global split_name
    spanish_type = ""

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

sprites_link_dict = {}
# Template for file naming, also easy access to each game sprites link
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

    keyname = ""
    # No animated sprites below gen 5 on this website
        # Except for Crystal, which the tag was added in game_translate
    if gen < 5:
        if back == False and shiny == False:
            keyname = "Gen" + str(gen) + " " + game
        if back == False and shiny == True:
            keyname = "Gen" + str(gen) + " " + game + " Shiny"
        if back == True and shiny == False:
            keyname = "Gen" + str(gen) + "-Back"
        if back == True and shiny == True:
            keyname = "Gen" + str(gen) + "-Back Shiny"
    else:
        if animated == True:
            if back == False and shiny == False:
                keyname = "Gen" + str(gen) + " " + game + " Animated"
            if back == False and shiny == True:
                keyname = "Gen" + str(gen) + " " + game + " Animated" + " Shiny"
            if back == True and shiny == False:
                keyname = "Gen" + str(gen) + "-Back" + " Animated"
            if back == True and shiny == True:
                keyname = "Gen" + str(gen) + "-Back Animated Shiny"
        if animated == False:
            if back == False and shiny == False:
                keyname = "Gen" + str(gen) + " " + game + " Static"
            if back == False and shiny == True:
                keyname = "Gen" + str(gen) + " " + game + " Static" + " Shiny"
            if back == True and shiny == False:
                keyname = "Gen" + str(gen) + "-Back" + " Static"
            if back == True and shiny == True:
                keyname = "Gen" + str(gen) + "-Back Static Shiny"

    # Excludes Let's Go because there's not enough sprites to justify it's inclusion
    # And Gen8 Shiny Back sprites because the page isn't uploaded yet
    if not "Let's Go" in keyname and not keyname == "Gen8-Back Static Shiny":
        sprites_link_dict[keyname] = "https://www.wikidex.net" + link.get("href")

# Gets rows (games) of sprite link table
print("Adding games to dict...")
for games in game_sprites_link_table.findAll("td"):
    games_by_gen.append(games)

for i in range(len(games_by_gen)):
    current_gen = i + 1
    current_game = ""
    # No animated sprites below gen5, so just get statics
    if (current_gen < 5):
        # Grabbing links and adding them to the dict
        for link in games_by_gen[i].findAll("a"):
            sprite_link_dict_entry(current_gen, link)

    # Seperates static and animated sprite pages gen 5 and above
    else:
        for image_type in games_by_gen[i].findAll('b'):
            # Excludes game seperators
            if not image_type.text == '|':
                # Gets animated or static
                if image_type.text == "Estáticos:":
                    is_animated = False
                if image_type.text == "Animados:":
                    is_animated = True
                # Grabbing links and adding them to the dict
                for link in image_type.find_next_siblings("a"):
                    sprite_link_dict_entry(current_gen, link, is_animated)

# for k,v in sprites_link_dict.items():
#     print(k, ":", v, "\n\n")

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
# Gets pokemon info from excel sheet
class Pokemon:
    def __init__(self, name, number, gen, has_f_var, has_mega, has_giganta, reg_forms, has_type_forms, has_misc_forms):
        self.name = name
        self.number = number
        self.gen = gen
        self.has_f_var = has_f_var
        self.has_mega = has_mega
        self.has_giganta = has_giganta
        self.reg_forms = reg_forms
        self.has_type_forms = has_type_forms
        self.has_misc_forms = has_misc_forms

# Gets column numbers from spreadsheet
name_col = get_col_number("Name")
num_col = get_col_number("#")
gen_col = get_col_number("Gen")
f_col = get_col_number("Female Variation")
mega_col = get_col_number("Mega")
giganta_col = get_col_number("Gigantamax")
reg_forms_col = get_col_number("Regional Forms")
type_forms_col = get_col_number("Type Forms")
misc_forms_col = get_col_number("Misc Forms")

# Adds pokemon info from spreadsheet to object array
print("Getting pokemon info from spreadsheet...")
pokedex = []
for i in range(2, 900):
    name = cell_value(i, name_col)
    num = cell_value(i, num_col)
    gen = int(cell_value(i, gen_col))
    has_f_var = isnt_empty(i, f_col)
    has_mega = isnt_empty(i, mega_col)
    has_giganta = isnt_empty(i, giganta_col)
    reg_forms = cell_value(i, reg_forms_col)
    has_type_forms = isnt_empty(i, type_forms_col)
    has_misc_forms = isnt_empty(i, misc_forms_col)

    pokedex.append(Pokemon(name, num, gen, has_f_var, has_mega, has_giganta, reg_forms, has_type_forms, has_misc_forms))

# Prints out each pokemon's relevant info from spreadsheet
# for i in range(len(pokedex)):
#     print(vars(pokedex[i]))

game_hit = False
outlier_sprites = []
for game, link in sprites_link_dict.items():
    # Running only specific games
    # Multiple after game
    # if game != "Gen8 Sword-Shield Animated Shiny":
    #     # If the game hasn't been hit yet, continue on to next game
    #     # If it HAS been hit, run the script
    #     if not game_hit:
    #         print("Skipping game...")
    #         continue
    # else:
    #     # If the game equals the one specified, run script
    #     print("Found game...")
    #     game_hit = True
    
    # Single game
    # if game != "Gen4 Diamond-Pearl Static":
    #     continue

    # Getting soup of the corresponding sprite page
    game_page = requests.get(link, headers = {'User-Agent': "Chrome/89.0.4389.82"})
    game_page_soup = BeautifulSoup(game_page.content, 'html.parser')
    print("Opening", game, "First Page...")
    start_time = time.time()

    # Inside for loop to clear for each game
    pokemon_img_dict = {}

    current_gen = re.findall("Gen\d", game)[0][-1]
    # Loops through pages of sprites collecting image links to download
    # No do-while loop in python, so running a while True loop with a break condition
        # This break condition being if there is not a next page
    while True:
        print("Reading pokemon...")
        # Gets images and captions on page
        names = game_page_soup.find_all(class_="gallerytext")
        imgs = game_page_soup.find_all(class_="gallerybox")
        for i in range(len(names)):
            # If japanese sprites, 3d ones, or game blocks skip em
            if "\(CV\)" in names[i].text or "Japón" in names[i].text or "3D" in names[i].text or "Bloque" in names[i].text:
                continue
            file_ext = names[i].text.split("\n")[1]
            file_ext = file_ext[len(file_ext)-4 : len(file_ext)]

            # Crude hardcode translation services, at your service
            # Done before split because in their naming convention they put genders after the game (which is the split seperator)
            gender = ""
            if "hembra" in names[i].text or "macho" in names[i].text:
                if "hembra" in names[i].text:
                    gender = " f"
                if "macho" in names[i].text:
                    gender = " m"

            # Removing game, file size, extension, etc
            # This conditional is due to the websites oversight-- Most on the page are XY Static shinies
                # Except mostly the Megas, hence the exception. The rest I will do by hand
            if game == "Gen6 ORAS Static Shiny" and names[i].text.startswith("\nMega-"):
                split_name = names[i].text.split(" ROZA")[0]
            else:
                split_name = names[i].text.split(split_seperators_by_game[game])[0]
            # Removing leading newline character
            split_name = split_name.split("\n")[1]

            # TODO: Group these with form translate split function
                # Default third parameter form but if not can do region, etc
            # Handling Mega evolutions -- Excluding the Meganium paradox
            mega = ""
            if split_name.startswith("Mega") and split_name != "Meganium":
                mega = " Mega"
                split_name = split_name.split("Mega-")[1]
                if split_name.endswith("X"):
                    mega = " MegaX"
                    split_name = split_name.split(" X")[0]
                if split_name.endswith("Y"):
                    mega = " MegaY"
                    split_name = split_name.split(" Y")[0]
            # Handling Dynamax (Except Eternatus Eternamax)
            dyna = ""
            if split_name.endswith("Dinamax") and not split_name.startswith("\nEternatus"):
                dyna = " Dynamax"
                split_name = split_name.split(" Dinamax")[0]
            # Handling Gigantamax
            giganta = ""
            if split_name.endswith("Gigamax"):
                giganta = " Gigantamax"
                split_name = split_name.split(" Gigamax")[0]
            # Handling regions
            region = ""
            if split_name.endswith("de Alola"):
                region = " Alolan"
                split_name = split_name.split(" de Alola")[0]
            if split_name.endswith("de Galar"):
                region = " Galarian"
                split_name = split_name.split(" de Galar")[0]

            # Doing forms becuase accumulation over all generations, shiny, static/animated, and back sprites would easily get into the thousands
            form = ""
            # Nidoran Genders in name
            if "Nidoran" in split_name and gender != "":
                if gender == " f":
                    split_name = split_name.replace("hembra", "f")
                if gender == " m":
                    split_name = split_name.replace("macho", "m")

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

            # Assigning Filenames
            match = False
            for poke in pokedex:
                if poke.name == split_name:
                    match = True
                    game_str = game
                    # This is to replace certain game names to include multiple games
                        # eg Black/White sprites are the same as Black2/White2
                        # XY, ORAS, SM, and USUM all use the same 3d sprites, etc
                            # So instead of doing multiple downloads for each game, I'm combining them to share the same image
                    game_title_replace("Black-White", "BW-B2W2")
                    game_title_replace("Black2-White2", "BW-B2W2")
                    game_title_replace("Gen6 XY", "Gen6-7 XY-ORAS-SM-USUM")
                    game_title_replace("Gen6 ORAS", "Gen6-7 XY-ORAS-SM-USUM")
                    # For back sprites
                    game_title_replace("Gen6-", "Gen6-7-")
                    game_title_replace("Gen7 Sun-Moon", "Gen7 SM-USUM")
                    game_title_replace("Gen7 USUM", "Gen7 SM-USUM")

                    filename = poke.number + " " + poke.name + " " + game_str + gender + mega + dyna + giganta + form + region
                    # If the filename already exists (and it will for double sprites in DPP), add alt
                    try:
                        dummy = pokemon_img_dict[filename + file_ext]
                        # Crystal apparently has different back sprites as other gen2 games
                        if game == "Gen2-Back":
                            filename += " Crystal"
                        else:
                            # Since alt images are shown first on this website, they will have the original filename
                                # So, change the first file (alt) to alt filename, and keep the original filename for the second, actually original image
                            pokemon_img_dict[filename + " alt" + file_ext] = pokemon_img_dict.pop(filename + file_ext)
                    except:
                        dummy = "key doesn't exist yet, continue"

                    filename += file_ext
                    pokemon_img_dict[filename] = imgs[i].a.img["src"]
                    # Saves first-frame statics as png from gif for Crystal & Emerald
                        # TODO: THIS CONVERTS IT TO AN ANIMATED PNG (open in Chrome) -- WILL HAVE TO FIND ANOTHER WAY TO DO THIS
                    # if game == "Gen2 Crystal Animated" or game == "Gen2 Crystal Animated Shiny" or game == "Gen3 Emerald Animated" or game == "Gen3 Emerald Animated Shiny":
                    #     filename = filename.replace("Animated", "Static")
                    #     filename = filename.replace(".gif", ".png")
                    #     pokemon_img_dict[filename] = imgs[i].a.img["src"]
            # This is to see what pokemon aren't formatted correctly
            if match == False:
                outlier_sprites.append(names[i].text.split("\n")[1])
                pokemon_img_dict[names[i].text.split("\n")[1]] = imgs[i].a.img["src"]
                    
        # for k,v in pokemon_img_dict.items():
        #     print(k, ":", v)
        
        # If next game page exists, get its url to parse
        if game_page_soup.find("a", string="página siguiente") != None:
            time.sleep(1)
            print("Opening", game, "Next Page...")
            game_page = game_page_soup.find("a", string="página siguiente").get("href")
            game_page = requests.get("https://www.wikidex.net" + game_page, headers = {'User-Agent': "Chrome/89.0.4389.82"})
            game_page_soup = BeautifulSoup(game_page.content, 'html.parser')
        else:
            amount_of_imgs = len(pokemon_img_dict)
            current_img = 1
            pokes_since_time = 0
            print("Downloading", amount_of_imgs, "Images...")
            # If done with all images for the game, save them
            for file_name, poke_link in pokemon_img_dict.items():
                if os.path.exists("Images/Pokemon/" + file_name):
                    current_img += 1
                    continue
                print("Downloading %s/%s" % (current_img, amount_of_imgs),  file_name, "...")
                download_time = time.time()
                urllib.request.urlretrieve(poke_link, "Images/Pokemon/" + file_name)
                download_time = time.time() - download_time
                print("Downloaded %s/%s" % (current_img, amount_of_imgs), file_name)
                pokes_since_time += 1
                total_time = (time.time() - start_time)/60
                print("Download took %.1f seconds" % download_time)
                print("Downloading average: %.0f pokemon per minute" % (pokes_since_time/total_time))
                print("Downloading average: %.0f pokemon per hr" % ((pokes_since_time/total_time) * 60))
                print("Minutes elapsed: %.1f with %s pokemon downloaded" % (total_time, pokes_since_time))
                current_img += 1
                time.sleep(0.3)
            print(game, "Done")
            print("Total minutes:", (time.time() - start_time)/60, "Pokemon downloaded:", pokes_since_time)
            print("\n\n\n")
            time.sleep(3)
            break
    

print(len(outlier_sprites), "outlier pokes: ", outlier_sprites)