def get_translated_game(my_filename, map_dict):
    for game, translation in map_dict.items():
        if "-Back" in my_filename:
            game = game.replace(" ", "_")
        if game in my_filename:
            return(f" {translation}")
        

def get_translated_universal_form(my_filename, mapping):
    for u_form, translation in mapping.items():
        if u_form in my_filename: return(translation)
    return ("")
        

# This is to filter out these forms when translating species forms
# The exceptions that have a universal AND species form (See 555 Galarian Darmanitan Zen form) have their own unique form id generated in db_utils > FORM_EXCEPTION_POKEMON
UNIVERSAL_FORMS = {
    "Default", 
    "-f", 
    "-Mega", 
    "-Mega_X", 
    "-Mega_Y", 
    "-Gigantamax", 
    "-Region_Alola", 
    "-Region_Galar", 
    "-Region_Hisui", 
    "-Region_Paldea"
}