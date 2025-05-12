import os

from app_globals import DB_PATH
from db_utils import populate_db, update_file_existence, get_last_poke_num
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


def main():
    # NOTE: If program crashes a lot like last one, write this to a txt file. Each new pokemon would rewrite the line of the file where it picked up
    poke_num_start_scraping_from = 1
    poke_to_go_after_start_num = 1

    valid_start_poke_num, valid_stop_poke_num = validate_context(poke_num_start_scraping_from, poke_to_go_after_start_num)
    # TODO: Update file_exists field in db before scraping
    bulba_scrape(valid_start_poke_num, valid_stop_poke_num)     # NOTE: Always check Bulba first, they have higher quality images
    #create_file_checklist_spreadsheet()




#|================================================================================================|
#|~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~[     HELPERS     ]~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~|
#|================================================================================================|

def validate_context(start_num, num_after_start, force_update=False):
    if not os.path.exists(DB_PATH) or force_update or db_isnt_current():
        populate_db(force_update)   # Will always rewrite filename tables, so also checks if any files were downloaded. Only skips existing form game obtainabailitty records bc its slow, new records will still be added (even on old pokes)
    else:
        update_file_existence()     # Checks to see if any images were downloaded

    return verify_start_stop_scraping_poke_nums(start_num, num_after_start)


# Force, if true, will update the db even if the db has the same last pokemon as the poke_info spreadsheet
def db_isnt_current():
    print("Confirming database is up to date...")

    if info_sheet_has_more_pokes_than_db():
        print("Pokemon Information sheet more current than database, preparing to update database...")
        return True
    else:
        print("Pokedex database is current, moving on...")
        return False


def info_sheet_has_more_pokes_than_db():
    # highest poke num in db checked against highest num in poke info sheet
    if get_last_poke_num() != int(cell_value(POKEMON_INFO_SHEET, POKE_INFO_LAST_ROW, POKE_INFO_NUM_COL)): 
        return True
    return False
    

def verify_start_stop_scraping_poke_nums(start, num_after):
    last_db_poke_num = get_last_poke_num()

    if start < 1: start=1
    if start > last_db_poke_num: start = last_db_poke_num
    if num_after < 1: num_after=0
    if start + num_after > last_db_poke_num: num_after = last_db_poke_num - start
    stop = start + num_after

    return start, stop




if __name__ == "__main__":
    main()