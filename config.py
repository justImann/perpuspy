import os


BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Path ke file database
DATABASE_NAME = 'library.db'
DATABASE_PATH = os.path.join(BASE_DIR, DATABASE_NAME)

ICON_DIR = os.path.join(BASE_DIR, 'assets/icons')

def get_icon_path(icon_name):
    """ Helper function to get the absolute path to an icon file. """
    path = os.path.join(ICON_DIR, icon_name)
    if not os.path.exists(path):
        print(f"Peringatan: File ikon tidak ditemukan di {path}") 
        return "" 
    return path
