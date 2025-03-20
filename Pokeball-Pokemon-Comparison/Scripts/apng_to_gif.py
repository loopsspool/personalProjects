import os
import apnggif

apng_path = "C:\\Users\\ejone\\OneDrive\\Desktop\\Code\\Javascript\\p5\\projects\\Pokeball Pokemon Comparison\\Images\\Pokemon\\Game Sprites\\animated_pngs_for_gifs\\pngs\\"
gif_path = "C:\\Users\\ejone\\OneDrive\\Desktop\\Code\\Javascript\\p5\\projects\\Pokeball Pokemon Comparison\\Images\\Pokemon\\Game Sprites\\animated_pngs_for_gifs\\gifs\\"

apng_files = os.listdir(apng_path)
gif_files = os.listdir(gif_path)

for apng in apng_files:
    if apng == "Converted to gif":
        continue
    if apng not in gif_files:
        filename = apng[:-4]
        filename += ".gif"
        apnggif.apnggif(apng_path + apng, gif_path + filename)
        print(filename)