# TODO: Add all new gen 8 (LA) and gen 9 (SV) games

# Determines if a pokemon can only be obtained in SM-USUM (so exclude XY-ORAS in filename)
def sm_usum_exclusivity_test(poke_num, tags):
    if poke_num >= 722:
        return True
    if "-Region-Alola" in tags:
        return True
    # For Cap Pikachu
    if "-Form-Cap" in tags:
        return True
    # For Ash Greninja
    if "-Form-Ash" in tags:
        return True
    # For Zygarde
    if "-Form-10%" in tags or "-Form-Complete" in tags:
        return True

def combine_gen_and_game(game, poke_num, tags):
    if game == "Red-Blue" or game == "Red-Green" or game == "Yellow":
        return ("Gen1 " + game)
    if game == "Crystal" or game == "Gold" or game == "Silver":
        return ("Gen2 " + game)
    if game == "Emerald" or game == "FireRed-LeafGreen" or game == "Ruby-Sapphire":
        return ("Gen3 " + game)
    if game == "Diamond-Pearl" or game == "HGSS" or game == "Platinum":
        return ("Gen4 " + game)
    if game == "BW-B2W2":
        return ("Gen5 " + game)
    # Since XY-ORAS and SM-USUM shared sprites
    if game == "XY-ORAS" or game == "SM-USUM":
        is_sm_usum_exclusive = sm_usum_exclusivity_test(poke_num, tags)
        if is_sm_usum_exclusive:
            return ("Gen7 " + game)
        else:
            return ("Gen6-7 XY-ORAS-SM-USUM")
    if game == "LGPE":
        return ("Gen7 " + game)
    if game == "Sword-Shield":
        return ("Gen8 " + game)

# Get back gen from game
    # Handles more sophistocated cases -- Regions, forms, etc
def get_back_gen(game, poke_num, tags):
    if game == "Red-Blue" or game == "Red-Green" or game == "Yellow":
        return ("Gen1")
    if game == "Crystal" or game == "Gold" or game == "Silver":
        return ("Gen2")
    if game == "Emerald" or game == "FireRed-LeafGreen" or game == "Ruby-Sapphire":
        return ("Gen3")
    if game == "Diamond-Pearl" or game == "HGSS" or game == "Platinum":
        return ("Gen4")
    if game == "BW-B2W2":
        return ("Gen5")
    # Since XY-ORAS and SM-USUM shared sprites
    if game == "XY-ORAS" or game == "SM-USUM":
        is_sm_usum_exclusive = sm_usum_exclusivity_test(poke_num, tags)
        if is_sm_usum_exclusive:
            return ("Gen7")
        else:
            return ("Gen6-7")
    if game == "LGPE":
        return ("Gen7")
    if game == "Sword-Shield":
        return ("Gen8")

# Determines what gen to start reading games from
    # Returns gen - 1 for what it's respective index is in the gen array
    # Only goes up to 4 because that's where the potential back discrepancies go up to
def get_back_gen_index_starter(poke_num):
    if poke_num <= 151:
        return (0)
    if poke_num >= 152 and poke_num <= 251:
        return (1)
    if poke_num >= 252 and poke_num <= 386:
        return (2)
    if poke_num >= 387 and poke_num <= 493:
        return (3)