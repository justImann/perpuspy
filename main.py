import sys
from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QFont
from app_window import LibraryApp
import sqlite3

if __name__ == "__main__":
    app = QApplication(sys.argv)

    default_font = QFont("Segoe UI", 10)
    app.setFont(default_font)
    
    try:
        window = LibraryApp()
        if window.conn is None: 
            print("Gagal menginisialisasi koneksi database. Aplikasi akan keluar.")
            sys.exit(1) 

        window.show()
        sys.exit(app.exec_())

    except sqlite3.Error as e: 
        print(f"Terjadi error fatal pada database saat inisialisasi: {e}")
        
        sys.exit(1)

    except Exception as e: 
        print(f"Terjadi error tidak terduga saat memulai aplikasi: {e}")

        sys.exit(1)