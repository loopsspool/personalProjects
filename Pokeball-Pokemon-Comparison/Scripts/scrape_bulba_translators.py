# TODO: Read through this and break it up

def bulba_game_denoter_conversion(filename):
    if "Red-Blue" in filename:
        return (" 1b")
    if "Red-Green" in filename:
        return (" 1g")
    if "Yellow" in filename:
        return (" 1y")
    if "Crystal" in filename:
        return (" 2c")
    # This has the Gen2 requirement to protect from Golduck and Goldeen entering this conditional by default
    if "Gold" in filename and "Gen2" in filename:
        return (" 2g")
    if "Silver" in filename:
        return (" 2s")
    if "Emerald" in filename:
        return (" 3e")
    if "FireRed-LeafGreen" in filename:
        return (" 3f")
    if "Ruby-Sapphire" in filename:
        return (" 3r")
    if "Diamond-Pearl" in filename:
        return (" 4d")
    if "HGSS" in filename:
        return (" 4h")
    if "Platinum" in filename:
        return (" 4p")
    # 5b2 is converted to 5b if the filename contains 5b2
        # aka Gen5 Black2/White2 (in bulba) is converted to 5b where it will be deemed BW-B2W2 (in my files)
    if "BW-B2W2" in filename:
        return (" 5b")
    # 6o is converted to 6x if the filename contains 6o
        # aka Gen6 ORAS (in bulba) is converted to 6x where it will be deemed XY-ORAS-SM-USUM (in my files)
    if "XY-ORAS" in filename:
        return (" 6x")
    if "SM-USUM" in filename:
        return (" 7s")
    if "LGPE" in filename:
        return (" 7p")
    if "Sword-Shield" in filename:
        return (" 8s")

def check_for_form(plaintext_form, bulba_form_code, curr_bulba_form, computer_filename):
    if plaintext_form in computer_filename:
        return(bulba_form_code)
    else:
        return (curr_bulba_form)

def check_for_type(computer_filename):
    for t in types:
        poke_type = "-Form-" + t
        if poke_type in computer_filename:
            # Handling the ??? type used in gen4
            if t == "Qmark":
                return("-Unknown")
            else:
                return("-" + t)
            
# Converts forms into bulbapedia notation
def form_translation(pokemon, computer_filename):
    # TODO: Probably should've done this in like a dict, then just checked keys then tuple arrays... Oops
    bulba_code_form = ""
    # If pokemon has no type or misc forms, return empty string to concatonate onto bulba filename
        # This is running before any web scraping, so I don't need to intentionally slow the script down
    if not pokemon.has_misc_forms and not pokemon.has_type_forms:
        return(bulba_code_form)

    # Pikachu Cosplay & Caps
    if pokemon.name == "Pikachu":
        bulba_code_form = check_for_form("-Form-Cap-Alola", "A", bulba_code_form, computer_filename)
        bulba_code_form = check_for_form("-Form-Cap-Hoenn", "H", bulba_code_form, computer_filename)
        bulba_code_form = check_for_form("-Form-Cap-Kalos", "K", bulba_code_form, computer_filename)
        bulba_code_form = check_for_form("-Form-Cap-Original", "O", bulba_code_form, computer_filename)
        bulba_code_form = check_for_form("-Form-Cap-Sinnoh", "S", bulba_code_form, computer_filename)
        bulba_code_form = check_for_form("-Form-Cap-Unova", "U", bulba_code_form, computer_filename)
        bulba_code_form = check_for_form("-Form-Cap-Partner", "P", bulba_code_form, computer_filename)
        # NOTE: No world cap sprite
        # NOTE: No Sprites for Cosplay on bulbapedia

    # Spiky-eared Pichu
    if pokemon.name == "Pichu":
        bulba_code_form = check_for_form("-Form-Spiky_Eared", "N", bulba_code_form, computer_filename)

    # Unown Characters
    # NOTE: Some gens, character is right after pokemon number but on other gens (see gen 4...) there is a hyphen -- UGH
    if pokemon.name == "Unown":
        # Regular letters
        for letter in uppers:
            unown_form = "-Form-" + letter
            if unown_form in computer_filename:
                bulba_code_form = letter
                break
        # Exclamation and question mark
        if "-Form-!" in computer_filename:
            bulba_code_form = "EX"    
        if "-Form-Qmark" in computer_filename:
            bulba_code_form = "QU"


    # Castform Weathers
    if pokemon.name == "Castform":
        bulba_code_form = check_for_form("-Form-Rainy", "R", bulba_code_form, computer_filename)
        bulba_code_form = check_for_form("-Form-Snowy", "H", bulba_code_form, computer_filename)
        bulba_code_form = check_for_form("-Form-Sunny", "S", bulba_code_form, computer_filename)

    # Primal Kyogre & Groudon
    if pokemon.name == "Kyogre" or pokemon.name == "Groudon":
        bulba_code_form = check_for_form("-Form-Primal", "P", bulba_code_form, computer_filename)

    # Deoxys
    if pokemon.name == "Deoxys":
        bulba_code_form = check_for_form("-Form-Attack", "A", bulba_code_form, computer_filename)
        bulba_code_form = check_for_form("-Form-Defense", "D", bulba_code_form, computer_filename)
        bulba_code_form = check_for_form("-Form-Speed", "S", bulba_code_form, computer_filename)

    # Burmy & Wormadam Cloaks
    if pokemon.name == "Burmy" or pokemon.name == "Wormadam":
        # Plant Cloak considered default, so does not have a letter denoter
        bulba_code_form = check_for_form("-Form-Plant_Cloak", "", bulba_code_form, computer_filename)
        bulba_code_form = check_for_form("-Form-Sandy_Cloak", "G", bulba_code_form, computer_filename)
        bulba_code_form = check_for_form("-Form-Trash_Cloak", "S", bulba_code_form, computer_filename)

    # Cherrim
    if pokemon.name == "Cherrim":
        # Overcast form considered default, so does not have a letter denoter
        bulba_code_form = check_for_form("-Form-Overcast", "", bulba_code_form, computer_filename)
        bulba_code_form = check_for_form("-Form-Sunshine", "S", bulba_code_form, computer_filename)

    # Shellos & Gastrodon East/West
    if pokemon.name == "Shellos" or pokemon.name == "Gastrodon":
        # West form considered default, so does not have a letter denoter
        bulba_code_form = check_for_form("-Form-West", "", bulba_code_form, computer_filename)
        bulba_code_form = check_for_form("-Form-East", "E", bulba_code_form, computer_filename)

    # Rotom Appliances
    if pokemon.name == "Rotom":
        bulba_code_form = check_for_form("-Form-Fan", "F", bulba_code_form, computer_filename)
        bulba_code_form = check_for_form("-Form-Frost", "R", bulba_code_form, computer_filename)
        bulba_code_form = check_for_form("-Form-Heat", "O", bulba_code_form, computer_filename)
        bulba_code_form = check_for_form("-Form-Mow", "L", bulba_code_form, computer_filename)
        bulba_code_form = check_for_form("-Form-Wash", "W", bulba_code_form, computer_filename)

    # Giratina
    if pokemon.name == "Giratina":
        # Altered form considered default, so does not have a letter denoter
        bulba_code_form = check_for_form("-Form-Altered", "", bulba_code_form, computer_filename)
        bulba_code_form = check_for_form("-Form-Origin", "O", bulba_code_form, computer_filename)

    # Shaymin
    if pokemon.name == "Shaymin":
        # Land form considered default, so does not have a letter denoter
        bulba_code_form = check_for_form("-Form-Land", "", bulba_code_form, computer_filename)
        bulba_code_form = check_for_form("-Form-Sky", "S", bulba_code_form, computer_filename)

    # Arceus Types
    if pokemon.name == "Arceus":
        bulba_code_form = check_for_type(computer_filename)

    # Basculin Stripes
    if pokemon.name == "Basculin":
        # Red Striped form considered default, so does not have a letter denoter
        bulba_code_form = check_for_form("-Form-Red_Striped", "", bulba_code_form, computer_filename)
        bulba_code_form = check_for_form("-Form-Blue_Striped", "B", bulba_code_form, computer_filename)

    # Darmanitan Modes
    if pokemon.name == "Darmanitan":
        # Standard form considered default, so does not have a letter denoter
        bulba_code_form = check_for_form("-Form-Standard", "", bulba_code_form, computer_filename)
        bulba_code_form = check_for_form("-Form-Zen", "Z", bulba_code_form, computer_filename)

    # Deerling & Sawsbuck Seasons
    if pokemon.name == "Deerling" or pokemon.name == "Sawsbuck":
        # Spring form considered default, so does not have a letter denoter
        bulba_code_form = check_for_form("-Form-Spring", "", bulba_code_form, computer_filename)
        bulba_code_form = check_for_form("-Form-Autumn", "A", bulba_code_form, computer_filename)
        bulba_code_form = check_for_form("-Form-Summer", "S", bulba_code_form, computer_filename)
        bulba_code_form = check_for_form("-Form-Winter", "W", bulba_code_form, computer_filename)

    # Forces of nature forms
    if pokemon.name == "Tornadus" or pokemon.name == "Thundurus" or pokemon.name == "Landorus":
        # Incarnate form considered default, so does not have a letter denoter
        bulba_code_form = check_for_form("-Form-Incarnate", "", bulba_code_form, computer_filename)
        bulba_code_form = check_for_form("-Form-Therian", "T", bulba_code_form, computer_filename)

    # Kyurem Fusions
    # NOTE: Overdrives were mislabelled as defaults, so I did these by hand
    
    # Keldeo
    if pokemon.name == "Keldeo":
        # Ordinary form considered default, so does not have a letter denoter
        bulba_code_form = check_for_form("-Form-Ordinary", "", bulba_code_form, computer_filename)
        bulba_code_form = check_for_form("-Form-Resolute", "R", bulba_code_form, computer_filename)

    # Meloetta
    if pokemon.name == "Meloetta":
        bulba_code_form = check_for_form("-Form-Aria", "", bulba_code_form, computer_filename)
        bulba_code_form = check_for_form("-Form-Pirouette", "P", bulba_code_form, computer_filename)

    # Genesect
    if pokemon.name == "Genesect":
        if "-Form-Douse_Drive" in computer_filename:
            bulba_code_form = "B"
        if "-Form-Burn_Drive" in computer_filename:
            bulba_code_form = "R"
        if "-Form-Chill_Drive" in computer_filename:
            bulba_code_form = "W"
        if "-Form-Shock_Drive" in computer_filename:
            bulba_code_form = "Y"

    # Ash Greninja
    if pokemon.name == "Greninja":
        bulba_code_form = check_for_form("-Form-Ash", "A", bulba_code_form, computer_filename)

    # Vivillon Patterns
    if pokemon.name == "Vivillon":
        # Meadow form considered default, so does not have a letter denoter
        bulba_code_form = check_for_form("-Form-Meadow", "", bulba_code_form, computer_filename)
        bulba_code_form = check_for_form("-Form-Archipelago", "Arc", bulba_code_form, computer_filename)
        bulba_code_form = check_for_form("-Form-Continental", "Con", bulba_code_form, computer_filename)
        bulba_code_form = check_for_form("-Form-Elegant", "Ele", bulba_code_form, computer_filename)
        bulba_code_form = check_for_form("-Form-Garden", "Gar", bulba_code_form, computer_filename)
        bulba_code_form = check_for_form("-Form-High_Plains", "Hig", bulba_code_form, computer_filename)
        bulba_code_form = check_for_form("-Form-Icy_Snow", "Icy", bulba_code_form, computer_filename)
        bulba_code_form = check_for_form("-Form-Jungle", "Jun", bulba_code_form, computer_filename)
        bulba_code_form = check_for_form("-Form-Marine", "Mar", bulba_code_form, computer_filename)
        bulba_code_form = check_for_form("-Form-Modern", "Mod", bulba_code_form, computer_filename)
        bulba_code_form = check_for_form("-Form-Monsoon", "Mon", bulba_code_form, computer_filename)
        bulba_code_form = check_for_form("-Form-Ocean", "Oce", bulba_code_form, computer_filename)
        bulba_code_form = check_for_form("-Form-Polar", "Pol", bulba_code_form, computer_filename)
        bulba_code_form = check_for_form("-Form-River", "Riv", bulba_code_form, computer_filename)
        bulba_code_form = check_for_form("-Form-Sandstorm", "San", bulba_code_form, computer_filename)
        bulba_code_form = check_for_form("-Form-Savanna", "Sav", bulba_code_form, computer_filename)
        bulba_code_form = check_for_form("-Form-Sun", "Sun", bulba_code_form, computer_filename)
        bulba_code_form = check_for_form("-Form-Tundra", "Tun", bulba_code_form, computer_filename)
        bulba_code_form = check_for_form("-Form-Poke_Ball", "Pok", bulba_code_form, computer_filename)
        bulba_code_form = check_for_form("-Form-Fancy", "Fan", bulba_code_form, computer_filename)
    
    # Flabebe, Floette, and Florges colors
    if pokemon.name == "Flabebe" or pokemon.name == "Floette" or pokemon.name == "Florges":
        # Red Flower form considered default, so does not have a letter denoter
        bulba_code_form = check_for_form("-Form-Red_Flower", "", bulba_code_form, computer_filename)
        bulba_code_form = check_for_form("-Form-Blue_Flower", "B", bulba_code_form, computer_filename)
        bulba_code_form = check_for_form("-Form-Orange_Flower", "O", bulba_code_form, computer_filename)
        bulba_code_form = check_for_form("-Form-White_Flower", "W", bulba_code_form, computer_filename)
        bulba_code_form = check_for_form("-Form-Yellow_Flower", "Y", bulba_code_form, computer_filename)

    # Furfrou Trims
    if pokemon.name == "Furfrou":
        bulba_code_form = check_for_form("-Form-Dandy_Trim", "Da", bulba_code_form, computer_filename)
        bulba_code_form = check_for_form("-Form-Debutante_Trim", "De", bulba_code_form, computer_filename)
        bulba_code_form = check_for_form("-Form-Diamond_Trim", "Di", bulba_code_form, computer_filename)
        bulba_code_form = check_for_form("-Form-Heart_Trim", "He", bulba_code_form, computer_filename)
        bulba_code_form = check_for_form("-Form-Kabuki_Trim", "Ka", bulba_code_form, computer_filename)
        bulba_code_form = check_for_form("-Form-La_Reine_Trim", "La", bulba_code_form, computer_filename)
        bulba_code_form = check_for_form("-Form-Matron_Trim", "Ma", bulba_code_form, computer_filename)
        bulba_code_form = check_for_form("-Form-Pharaoh_Trim", "Ph", bulba_code_form, computer_filename)
        bulba_code_form = check_for_form("-Form-Star_Trim", "St", bulba_code_form, computer_filename)

    # Aegislash
    if pokemon.name == "Aegislash":
        # Shield form considered default, so does not have a letter denoter
        bulba_code_form = check_for_form("-Form-Shield", "", bulba_code_form, computer_filename)
        bulba_code_form = check_for_form("-Form-Blade", "B", bulba_code_form, computer_filename)

    # Pumpkaboo and Gourgeist Sizes
    if pokemon.name == "Pumpkaboo" or pokemon.name == "Gourgeist":
        # Average Size form considered default, so does not have a letter denoter
        bulba_code_form = check_for_form("-Form-1_Average_Size", "", bulba_code_form, computer_filename)
        bulba_code_form = check_for_form("-Form-0_Small_Size", "Sm", bulba_code_form, computer_filename)
        bulba_code_form = check_for_form("-Form-2_Large_Size", "La", bulba_code_form, computer_filename)
        bulba_code_form = check_for_form("-Form-3_Super_Size", "Su", bulba_code_form, computer_filename)

    # Xerneas
    if pokemon.name == "Xerneas":
        # Active form considered default, so does not have a letter denoter
        bulba_code_form = check_for_form("-Form-Active", "", bulba_code_form, computer_filename)
        bulba_code_form = check_for_form("-Form-Neutral", "N", bulba_code_form, computer_filename)

    # Zygarde
    if pokemon.name == "Zygarde":
        # 50% form considered default, so does not have a letter denoter
        bulba_code_form = check_for_form("-Form-50%", "", bulba_code_form, computer_filename)
        bulba_code_form = check_for_form("-Form-Complete", "C", bulba_code_form, computer_filename)
        bulba_code_form = check_for_form("-Form-10%", "T", bulba_code_form, computer_filename)

    # Hoopa
    if pokemon.name == "Hoopa":
        # Confined form considered default, so does not have a letter denoter
        bulba_code_form = check_for_form("-Form-Confined", "", bulba_code_form, computer_filename)
        bulba_code_form = check_for_form("-Form-Unbound", "U", bulba_code_form, computer_filename)

    # Oricorio
    if pokemon.name == "Oricorio":
        # Confined form considered default, so does not have a letter denoter
        bulba_code_form = check_for_form("-Form-Baile", "", bulba_code_form, computer_filename)
        bulba_code_form = check_for_form("-Form-Pa'u", "Pa", bulba_code_form, computer_filename)
        bulba_code_form = check_for_form("-Form-Pom_Pom", "Po", bulba_code_form, computer_filename)
        bulba_code_form = check_for_form("-Form-Sensu", "Se", bulba_code_form, computer_filename)

    # Lycanroc
    if pokemon.name == "Lycanroc":
        # Midday form considered default, so does not have a letter denoter
        bulba_code_form = check_for_form("-Form-Midday", "", bulba_code_form, computer_filename)
        bulba_code_form = check_for_form("-Form-Dusk", "D", bulba_code_form, computer_filename)
        bulba_code_form = check_for_form("-Form-Midnight", "Mn", bulba_code_form, computer_filename)

    # Wishiwashi
    if pokemon.name == "Wishiwashi":
        # Solo form considered default, so does not have a letter denoter
        bulba_code_form = check_for_form("-Form-Solo", "", bulba_code_form, computer_filename)
        bulba_code_form = check_for_form("-Form-School", "Sc", bulba_code_form, computer_filename)

    # Silvally Types
    if pokemon.name == "Silvally":
        bulba_code_form = check_for_type(computer_filename)

    # Minior
    # NOTE: Bulba has shiny core form denoted as red, so this will probably have to manually be changed
    if pokemon.name == "Minior":
        # Meteor form considered default, so does not have a letter denoter
        bulba_code_form = check_for_form("-Form-Meteor", "", bulba_code_form, computer_filename)
        bulba_code_form = check_for_form("-Form-Blue_Core", "B", bulba_code_form, computer_filename)
        bulba_code_form = check_for_form("-Form-Green_Core", "G", bulba_code_form, computer_filename)
        bulba_code_form = check_for_form("-Form-Indigo_Core", "I", bulba_code_form, computer_filename)
        bulba_code_form = check_for_form("-Form-Orange_Core", "O", bulba_code_form, computer_filename)
        bulba_code_form = check_for_form("-Form-Red_Core", "R", bulba_code_form, computer_filename)
        bulba_code_form = check_for_form("-Form-Violet_Core", "V", bulba_code_form, computer_filename)
        bulba_code_form = check_for_form("-Form-Yellow_Core", "Y", bulba_code_form, computer_filename)

    # Mimikyu
    if pokemon.name == "Mimikyu":
        # Disguised form considered default, so does not have a letter denoter
        bulba_code_form = check_for_form("-Form-Disguised", "", bulba_code_form, computer_filename)
        bulba_code_form = check_for_form("-Form-Busted", "B", bulba_code_form, computer_filename)

    # Solgaleo
    if pokemon.name == "Solgaleo":
        bulba_code_form = check_for_form("-Form-Full_Moon", "F", bulba_code_form, computer_filename)

    # Lunala
    if pokemon.name == "Lunala":
        bulba_code_form = check_for_form("-Form-Radiant_Sun", "R", bulba_code_form, computer_filename)

    # Necrozma
    if pokemon.name == "Necrozma":
        bulba_code_form = check_for_form("-Form-Dawn_Wings", "DW", bulba_code_form, computer_filename)
        bulba_code_form = check_for_form("-Form-Dusk_Mane", "DM", bulba_code_form, computer_filename)
        bulba_code_form = check_for_form("-Form-Ultra", "U", bulba_code_form, computer_filename)

    # Magearna
    if pokemon.name == "Magearna":
        bulba_code_form = check_for_form("-Form-Original_Color", "O", bulba_code_form, computer_filename)
    
    # Marshadow
    # NOTE: Bulba does not have Zenith form
    #if pokemon.name == "Marshadow":
    #    bulba_code_form = check_for_form("-Form-Zenith", "Z", bulba_code_form, computer_filename)
    
    # Cramorant
    if pokemon.name == "Cramorant":
        bulba_code_form = check_for_form("-Form-Gorging", "Go", bulba_code_form, computer_filename)
        bulba_code_form = check_for_form("-Form-Gulping", "Gu", bulba_code_form, computer_filename)
    
    # Toxtricity
    if pokemon.name == "Toxtricity":
        # Amped form considered default, so does not have a letter denoter
        bulba_code_form = check_for_form("-Form-Amped", "", bulba_code_form, computer_filename)
        bulba_code_form = check_for_form("-Form-Low_Key", "L", bulba_code_form, computer_filename)

    # Alcremie Creams & Sweets
    if pokemon.name == "Alcremie":
        # Gigantamax version doesn't show cream or sweets, so there's no point to go through them
        if "-Form-Gigantamax" in computer_filename:
            return("")
            
        for sweet in sweets:
            if sweet[0] in computer_filename:
                # Shiny Alcremie only shows sweet, not cream color
                if "-Shiny" in computer_filename:
                    bulba_code_form = sweet[1]
                    break
                else:
                    # If regular color, find cream
                    for cream in creams:
                        if cream[0] in computer_filename:
                            bulba_code_form = cream[1] + sweet[1]
                            break

    # Eiscue
    if pokemon.name == "Eiscue":
        # Ice Face form considered default, so does not have a letter denoter
        bulba_code_form = check_for_form("-Form-Ice_Face", "", bulba_code_form, computer_filename)
        bulba_code_form = check_for_form("-Form-Noice_Face", "N", bulba_code_form, computer_filename)
    
    # Morpeko
    if pokemon.name == "Morpeko":
        # Full Belly form considered default, so does not have a letter denoter
        bulba_code_form = check_for_form("-Form-Full_Belly", "", bulba_code_form, computer_filename)
        bulba_code_form = check_for_form("-Form-Hangry", "H", bulba_code_form, computer_filename)

    # Zacian
    if pokemon.name == "Zacian":
        # Hero form considered default, so does not have a letter denoter
        bulba_code_form = check_for_form("-Form-Hero_of_Many_Battles", "", bulba_code_form, computer_filename)
        bulba_code_form = check_for_form("-Form-Crowned_Sword", "C", bulba_code_form, computer_filename)

    # Zamazenta
    if pokemon.name == "Zamazenta":
        # Hero form considered default, so does not have a letter denoter
        bulba_code_form = check_for_form("-Form-Hero_of_Many_Battles", "", bulba_code_form, computer_filename)
        bulba_code_form = check_for_form("-Form-Crowned_Shield", "C", bulba_code_form, computer_filename)

    # Eternatus Eternamax
    if pokemon.name == "Eternatus":
        bulba_code_form = check_for_form("-Form-Eternamax", "E", bulba_code_form, computer_filename)

    # Urshifu
    # NOTE: NO game sprites for Urshifu??!

    # Zarude
    # NOTE: NO game sprites for Zarude either??!

    # Calyrex Ridings
    # NOTE: And no game sprites for Calyrex...

    return(bulba_code_form)

no_bulba_forms = []
# Pikachu World Cap
no_bulba_forms.append("-Form-Cap-World")
# Cosplay Pikachu
no_bulba_forms.append("-Form-Cosplay")
# Overdrive Reshiram, Zekrom, and Kyurem
no_bulba_forms.append("Overdrive")
# Marshadow Zenith
no_bulba_forms.append("-Form-Zenith")
# Urshifu Forms
no_bulba_forms.extend(["-Form-Rapid_Strike", "-Form-Single_Strike"])
# Dada Zarude
no_bulba_forms.append("-Form-Dada")
# Calyrex Riders
no_bulba_forms.extend(["-Form-Shadow_Rider", "-Form-Ice_Rider"])
def bulba_doesnt_have_this_form(filename):
    for form in no_bulba_forms:
        if form in filename:
            return True

    return False
    

exception_strings = []
# Mega
exception_strings.append("M")
# Gigantamax
exception_strings.append("Gi")
# Regions
exception_strings.extend(["A", "G"])
# Pikachu caps
# NOTE: To be honest this shouldn't even be needed since the first check is for a -f in the filename, which the cap variants don't have
    # But what the hell, err on the side of caution
exception_strings.extend(["025A", "025H", "025K", "025O", "025S", "025U", "025P"])

# Checks if there's a string in the bulba filename (usually from a form)
    # That excepts the need of a male denoter (m) 
        # This is then passed to where this denoter is added, recognizing if it should be or not
def has_male_denoter_exception(bulba_filename):
    for ex_str in exception_strings:
        if ex_str in bulba_filename:
            return True
    return False

# Converts my filename structure to bulbapedias
def determine_bulba_name(computer_filename, pokemon):
    # All files start with Spr
    bulba_name = "Spr"
    # Back denotions first
    is_gen1_back = False
    if "-Back" in computer_filename:
        bulba_name += " b"
        if " Gen1" in computer_filename:
            is_gen1_back = True
            bulba_name += " g1"
    # Then Game denoters
    if not is_gen1_back:
        bulba_name += bulba_game_denoter_conversion(computer_filename)
    # Then pokedex number
    bulba_name += " " + computer_filename[:3]
    
    # Then Mega
        # Not gender specific, so can go before gender check
    if "-Mega" in computer_filename:
        bulba_name += "M"

    # Then Region
        # Not gender specific, so can go before gender check
    if "-Region-Alola" in computer_filename:
        bulba_name += "A"
    if "-Region-Galar" in computer_filename:
        bulba_name += "G"

    # Then Forms
        # MUST COME AFTER REGION
            # See Darmanitan (555)
    bulba_name += form_translation(pokemon, computer_filename)

    # Then Gigantamax
        # MUST COME AFTER FORMS (see Urshifu 892)
            # But not gender specific, so can go before gender check
    if "-Gigantamax" in computer_filename:
        bulba_name += "Gi"

    # Then gender
    # But ONLY for gen4 or after, prior to gen4 (when female forms were released) bulba name appears as normal
        # Normally this wouldn't be necessary since in excel file-check I have female versions prior
    if " Gen4" in computer_filename or " Gen5" in computer_filename or " Gen6" in computer_filename or " Gen7" in computer_filename or " Gen8" in computer_filename:
        if "-f" in computer_filename:
            bulba_name += " f"
        else:
            # Bulbapedia puts m denoters into filenames for male version
                # So if the female denoter is missing in my filename, but the species has a gender difference
                    # Check for this and exceptions and add the male denoter if needed
            has_m_exception = has_male_denoter_exception(bulba_name)
            if pokemon.has_f_var and not has_m_exception:
                bulba_name += " m"

    # Then shiny
    if "Shiny" in computer_filename:
        bulba_name += " s"

    return (bulba_name)