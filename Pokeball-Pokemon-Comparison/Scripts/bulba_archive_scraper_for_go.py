# TODO: Maybe table Pokemon Go support for an update?
    # With all the costumes it adds WAY more complexity than normal forms
        # Do-able, but I may want to ship a product first

# TODO: And Pokemon Go sprites
            # Found here https://archives.bulbagarden.net/wiki/Category:Pok%C3%A9mon_GO_models
            # Denoted as GO###form
            # Download to GO folder

# NOTE: When considering doing it maybe use:
    # https://pokemongo.fandom.com/wiki/Category:Pok%C3%A9mon_sprites?from=P
    # Or another source other than bulbapedia for a more descripive and consistent filenaming system?

import requests # To retrieve webpages
from bs4 import BeautifulSoup   # To parse webpages
import re

page = requests.get("https://archives.bulbagarden.net/wiki/Category:Pok%C3%A9mon_GO_models")
soup = BeautifulSoup(page.content, 'html.parser')

img_link = ""
caption = ""
# Finding the filenames for each image
list_div = soup.find('div', {'class': 'mw-category-generated'})
for img in list_div.find_all('li'):
    # Stripping everything after the file extension
    caption = img.text.split(".png")[0]
    # Getting rid of all the leading new line characters
    caption = caption.strip("\n")

    # Shiny denoter
    if " s" in caption:
        # TODO: Denote shininess
        caption = caption.split(" s")[0]

    # Female denoter
    if caption[len(caption) - 1] == "f":
        # TODO: Denote female variation
        caption = caption[:len(caption) - 2]

    # Mega denoter
    if caption[len(caption) - 1] == "M":
        # TODO: Denote Mega variation
        caption = caption[:len(caption) - 2]

    # Regional denoters
    if caption[len(caption) - 1] == "A":
        # TODO: Denote Alolan variation
        caption = caption[:len(caption) - 2]
    if caption[len(caption) - 1] == "G":
        # TODO: Denote Galarian variation
        caption = caption[:len(caption) - 2]

    if not re.match("GO\d\d\d", caption)

# TODO: The below is only for Pokemon GO sprites with decorations
    # So only run this if the filename doesn't follow the format
        # GO001 -- Default, GO then pokedex #
        # GO001 s -- Shiny default
# Gets all table cells (where description of GO variation is)
lines = soup.find_all('td')
for line in lines:
    # Finds specific line of text describing image
    if "Model of" in line.text:
        # Splits line based off where description is (first parenthesis)
        form = line.text.split("(")[1]
        # Commas are in shiny forms, this eliminates that
        if "," in form:
            form = form.split(',')[0]
        # Otherwise, just gets text within parenthesis
        else:
            form = form.split(')')[0]
        print(form)

def get_GO_images(pokemon, img):
    # Let's Go Pikachu/Eevee images
    # NOTE: DOWNLOADS ALL IMAGES, NO CHECK IF THEY'RE ALREADY THERE

    save_name = pokemon.number + " " + pokemon.name
    if pokemon.name == "Type: Null":
        save_name = pokemon.number + " Type Null"
    # Done this way so certain images that just have characters after the pokemon number don't match
        # Don't have to do this with the others because the hyphen denoters prevent the possibility
    pokemon_name_len = len(pokemon.name)
    get_img_from_string(img, "^\d\d\d[a-zA-Z]{" + str(pokemon_name_len) + "}.png", drawn_save_path + save_name)
    # Drawn Mega
    if pokemon.has_mega:
        if pokemon.name == "Charizard" or pokemon.name == "Mewtwo":
            get_img_from_string(img, "^\d\d\d[a-zA-Z]-Mega X.png", drawn_save_path + save_name + "-Mega_X")
            get_img_from_string(img, "^\d\d\d[a-zA-Z]-Mega Y.png", drawn_save_path + save_name + "-Mega_Y")
        else:
            get_img_from_string(img, "^\d\d\d[a-zA-Z]-Mega.png", drawn_save_path + save_name + "-Mega")
    # Gigantamax
    if pokemon.has_giganta:
        get_img_from_string(img, "^\d\d\d[a-zA-Z]-Gigantamax.png", drawn_save_path + save_name + "-Gigantamax")
    # Regional forms
    if pokemon.reg_forms != "":
        if "," in pokemon.reg_forms:
            get_img_from_string(img, "^\d\d\d[a-zA-Z]-Alola.png", drawn_save_path + save_name + "-Region-Alola")
            get_img_from_string(img, "^\d\d\d[a-zA-Z]-Galar.png", drawn_save_path + save_name + "-Region-Galar")
        else:
            get_img_from_string(img, "^\d\d\d[a-zA-Z]-" + pokemon.reg_forms + ".png", drawn_save_path + save_name + "-Region-" + pokemon.reg_forms)
    # Other forms
    if pokemon.has_misc_forms or pokemon.has_type_forms:
        search_for_drawn_forms(pokemon)