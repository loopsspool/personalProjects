import sys
import os

# To go into parent directory to import db_utils
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(parent_dir)

from db_utils import FORM_EXCLUSIONS, is_form_available, get_poke_form_records, get_game_records

def test_is_form_available():
    # TODO: Will have to create connection to db
    is_form_available()

