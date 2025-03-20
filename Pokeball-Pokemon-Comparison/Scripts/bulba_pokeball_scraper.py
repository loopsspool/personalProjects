import os # To check if the file exists already
import requests # To retrieve webpages
from bs4 import BeautifulSoup   # To parse webpages
import urllib   # For downloading those images to my computer

save_path = "C:\\Users\\ejone\\OneDrive\\Desktop\\Code\\Javascript\\p5\\projects\\Pokeball Pokemon Comparison\\Images\\Pokeballs\\"
starter_url = "https://archives.bulbagarden.net"
# NOTE: ALL DOWNLOADS MUST BE DONE IN THE FASHION BELOW
    # Otherwise bulba has a check on if the site is being web scraped and it will block the download
# This is to mask the fact I'm webscraping
    # To use, call
        # filename, headers = opener.retrieve(get_largest_png(img), gen8_menu_sprite_save_path + save_name)
opener = urllib.request.URLopener()
opener.addheader('User-Agent', 'Mozilla/5.0')

def get_largest_png(thumb):
    # Go into page of image
    img_page = requests.get(starter_url + thumb.a.get("href"))
    img_page_soup = BeautifulSoup(img_page.content, 'html.parser')
    # Find the biggest image location
    biggest_link = img_page_soup.find("div", "fullImageLink")
    # Return its link
    return (biggest_link.a.get("href"))

pokeball_thumbs = []
def get_pages():
    curr_page = requests.get("https://archives.bulbagarden.net/w/index.php?title=Category:Pok%C3%A9_Balls&fileuntil=Flying+Pok%C3%A9dex+book.png#mw-category-media")
    curr_page_soup = BeautifulSoup(curr_page.content, 'html.parser')
    # Loops through pages of archives of pokemon images
    while True:
        # Grabbing each individual pokemons archived image url
        for pokeball in curr_page_soup.find_all('div', {'class': 'thumb'}):
            pokeball_thumbs.append(pokeball)

        # Moving on to the next page
        try:
            next_page_url = curr_page_soup.find('a', string='next page').get('href')
            next_page = requests.get(starter_url + next_page_url)
            next_page_soup = BeautifulSoup(next_page.content, 'html.parser')
            curr_page_soup = next_page_soup
            print("Reading next page of pokeball archive links...")
        # Unless the end of the next pages is reached
        except:
            print("Reached end of pokeball archive links.")
            break

balls = ["Poké Ball", "Great Ball", "Ultra Ball", "Master Ball", "Safari Ball", "Fast Ball", "Level Ball", "Lure Ball", "Heavy Ball", "Love Ball", "Friend Ball", "Moon Ball", "Sport Ball", "Net Ball", "Nest Ball", "Repeat Ball", "Timer Ball", "Luxury Ball", "Premier Ball", "Dive Ball", "Dusk Ball", "Heal Ball", "Quick Ball", "Cherish Ball", "Park Ball", "Dream Ball", "Beast Ball"]
# This sorts them alphabetically, speeding up in
balls = sorted(balls)

# What balls I want
# XY-ORAS, 4th gen battle, 5th gen battle (animated), gen3, LGPE, gen4 status screen, gen5 status screen, gen8
suffix = [" battle 3DS", " battle IV", " battle V", " III", " PE", " summary IV", " summary V", " VIII"]

to_be_downloaded = []
# Getting ball strings to download
for ball in balls:
    # Bag Sprites
    bag_sprite = "Bag " + ball + " Sprite.png"
    to_be_downloaded.append(bag_sprite)
    if ball == "Lure Ball" or ball == "Park Ball":
        to_be_downloaded.append(bag_sprite.replace(" Sprite", " IV Sprite"))
    
    # Dream Sprites (Pokemon Global Link)
    dream_sprite = "Dream " + ball + " Sprite.png"
    to_be_downloaded.append(dream_sprite)
    
    # Drawn Sprites
    drawn_sprite = ball.replace(" ", "")
    if "é" in drawn_sprite:
        drawn_sprite = drawn_sprite.replace("é", "e")
    drawn_sprite = "Sugimori" + drawn_sprite + ".png"
    to_be_downloaded.append(drawn_sprite)

    # Misc subtleties in bulba
    if ball == "Dream Ball":
        to_be_downloaded.append(ball + " summary.png")
    if ball == "Beast Ball":
        to_be_downloaded.append(ball + " battle SMUSUM.png")

    # Game Sprites
    for s in suffix:
        game_sprite = ball + s + ".png"
        to_be_downloaded.append(game_sprite)

# Actually downloading
get_pages()
for thumb in pokeball_thumbs:
    if thumb.img["alt"] in to_be_downloaded:
        # Making sure a file doesn't get overridden
        save_name = save_path + thumb.img["alt"]
        if not os.path.exists(save_name):
            img = get_largest_png(thumb)
            print("Downloading " + thumb.img["alt"] + "...")
            filename, headers = opener.retrieve(img, save_name)

