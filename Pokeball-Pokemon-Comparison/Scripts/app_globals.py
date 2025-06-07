import os
import importlib




#|================================================================================================|
#|~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~[     IMPORT WORKAROUND     ]~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~|
#|================================================================================================|

# To cache dynamically imported funcs so it only imports once
# Necessary to avoid circular import
_module_cache = {}
def lazy_import(module_name):
    if module_name not in _module_cache:
        _module_cache[module_name] = importlib.import_module(module_name)
    return _module_cache[module_name]




#|================================================================================================|
#|~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~[     GENERAL UTILITY     ]~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~|
#|================================================================================================|

def get_file_ext(file):
    return f".{file.split(".")[-1]}"


# TODO: Apply this where manually replacing
def replace_e(str):
    return str.replace("e", "\u00e9")




#|================================================================================================|
#|~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~[     SAVE DIRECTORIES     ]~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~|
#|================================================================================================|

PARENT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

# Database
DB_NAME = "pokedex.db"
DB_PATH = os.path.join(PARENT_DIR, DB_NAME)


# Files will be initialized at main run via path value
save_directories = {
    # Final save paths
    "Game Sprites" : {
        "path": os.path.join(PARENT_DIR, "Images\\Pokemon\\Game Sprites\\"),
        "files": set()
    },
    "HOME" : {
        "path": os.path.join(PARENT_DIR, "Images\\Pokemon\\HOME Sprites\\"),
        "files": set()
    },
    "HOME Downloaded Repositories" : {
        "path": os.path.join(PARENT_DIR, "Images\\Pokemon\\HOME Sprites\\downloaded_repositories\\"),
        "files": set()
    },
    "HOME Menu" : {
        "path": os.path.join(PARENT_DIR, "Images\\Pokemon\\Menu Sprites\\HOME\\"),
        "files": set()
    },
    "Drawn" : {
        "path": os.path.join(PARENT_DIR, "Images\\Pokemon\\Drawn\\"),
        "files": set()
    },
    "Pokeball" : {
        "path": os.path.join(PARENT_DIR, "Images\\Pokeballs\\"),
        "files": set()
    },

    # Staging/testing paths
    "Game Sprite Downloaded Repositories" : {
        "path": os.path.join(PARENT_DIR, "Images\\Pokemon\\Game Sprites\\downloaded_repositories\\"),
        "files": set()
    },
    "gif" : {
        "path": os.path.join(PARENT_DIR, "Images\\Pokemon\\Game Sprites\\gif\\"),
        "files": set()
    },
    "webm" : {
        "path": os.path.join(PARENT_DIR, "Images\\Pokemon\\Game Sprites\\webm\\"),
        "files": set()
    },
    "Need Transparency" : {
        "path": os.path.join(PARENT_DIR, "Images\\Pokemon\\Game Sprites\\need_transparency\\"),    # Used for saving stills from webm
        "files": set()
    },
    "Test" : {
        "path": os.path.join(PARENT_DIR, "Images\\Pokemon\\Test\\"),
        "files": set()
    },
    "Staging" : {
        "path": os.path.join(PARENT_DIR, "Images\\Pokemon\\Game Sprites\\staging\\"),
        "files": set()
    }
}


def init_save_dir_files():
    for dir, dir_info in save_directories.items():
        dir_info["files"] = set(os.listdir(dir_info["path"]))

        # TODO: Can delete once transparency is figured out
        # Joining need transparent imgs to saved game images so if a still is pulled from a webm it counts as existing and doesn't get re-downloaded
        if dir == "Need Transparency":  # Joining at Need Transparency so I dont have to copy file path
            save_directories["Game Sprites"]["files"] = save_directories["Game Sprites"]["files"] | dir_info["files"]


# Just for readability sake
def update_save_dir_existing_files():
    init_save_dir_files()