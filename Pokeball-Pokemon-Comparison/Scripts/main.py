import os

from app_globals import DB_PATH
from db_utils import populate_db, get_last_poke_num
from spreadsheet_utils import create_file_checklist_spreadsheet, cell_value, POKEMON_INFO_SHEET, POKE_INFO_LAST_ROW, POKE_INFO_NUM_COL
from bulba_scraping_utils import bulba_scrape


################################ React Native TODOs ############################################
# TODO: Also in RN will have to visually change Qmark with ??? (Arceus) or ? (Unown)
    # Probably best to check all forms after RN implemented


################################# TODO: Complete all TODOs here and from all files before running... please ########################
# TODO: Rename existing pokeball imgs before running (can use existing mapping)
# TODO: Write script to find files that have a default sprite saved that shouldnt

# Later TODOs (after scraping)
# TODO: Add a check function for files spreadsheet to see if generation is complete. If not, output missing imgs
# TODO: Run checks on existing images to find small sizes and check bulba for larger files
    # Wikidex most common file size (250x250? 180x180? Def small, Bulba has most gen 8 (all switch?) at 1024x1024)
# TODO: Check if there's any female backs missing where male backs are present... May only have visual difference in front and sprite is recycled for back


# NOTE: If program crashes a lot like last one, write this to a txt file. Each new pokemon would rewrite the line of the file where it picked up
POKE_NUM_START_SCRAPING_FROM = 1
POKE_TO_GO_AFTER_START_NUM = 10000
def main():
    validate_context()
    populate_db()
    # TODO: Update file_exists field in db before scraping
    bulba_scrape()     # NOTE: Always check Bulba first, they have higher quality images
    create_file_checklist_spreadsheet()

    
if __name__ == "__main__":
    main()




#|================================================================================================|
#|~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~[     HELPERS     ]~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~|
#|================================================================================================|

def validate_context(force_update=False):
    # If database doesn't exist, create & populate it. Or update it if forced
    if not os.path.exists(DB_PATH) or force_update:
        populate_db()
    else:
        check_db_is_current()

    verify_start_stop_scraping_poke_nums()


# Force, if true, will update the db even if the db has the same last pokemon as the poke_info spreadsheet
def check_db_is_current():
    print("Confirming database is up to date...")

    # TODO: Add a pokemon_info spreadsheet save datetime check? Save datetime of last spreadsheet save in a file and if when this function is run again it doesnt match, update pokedex
    if info_sheet_has_more_pokes_than_db():
        print("Pokemon Information sheet more current than pokedex, preparing to update database...")
        populate_db()
    else:
        print("Pokedex database is current, moving on...")


def info_sheet_has_more_pokes_than_db():
    # highest poke num in db checked against highest num in poke info sheet
    if get_last_poke_num != cell_value(POKEMON_INFO_SHEET, POKE_INFO_LAST_ROW, POKE_INFO_NUM_COL): 
        return True
    return False
    

# TODO: Have all functions utilize the start and to go after start denoters
def verify_start_stop_scraping_poke_nums():
    global POKE_NUM_START_SCRAPING_FROM
    global POKE_TO_GO_AFTER_START_NUM
    LAST_DB_POKE_NUM = get_last_poke_num()

    if POKE_NUM_START_SCRAPING_FROM < 1: POKE_NUM_START_SCRAPING_FROM=1
    if POKE_NUM_START_SCRAPING_FROM > LAST_DB_POKE_NUM: POKE_NUM_START_SCRAPING_FROM = LAST_DB_POKE_NUM
    if POKE_TO_GO_AFTER_START_NUM < 1: POKE_TO_GO_AFTER_START_NUM=0
    if POKE_NUM_START_SCRAPING_FROM + POKE_TO_GO_AFTER_START_NUM > LAST_DB_POKE_NUM: POKE_TO_GO_AFTER_START_NUM = LAST_DB_POKE_NUM - POKE_NUM_START_SCRAPING_FROM
    # TODO: Needed? Implement Start & go after and see
    POKE_NUM_END_AT = POKE_NUM_START_SCRAPING_FROM + POKE_TO_GO_AFTER_START_NUM