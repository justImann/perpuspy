import sqlite3
import datetime
import random
import config 


DUMMY_BOOKS = [
    ("Laskar Pelangi", "Andrea Hirata", "Bentang Pustaka", 2005),
    ("Bumi Manusia", "Pramoedya Ananta Toer", "Hasta Mitra", 1980),
    ("Negeri 5 Menara", "Ahmad Fuadi", "Gramedia Pustaka Utama", 2009),
    ("Filosofi Teras", "Henry Manampiring", "Kompas", 2018),
    ("Sapiens: Riwayat Singkat Umat Manusia", "Yuval Noah Harari", "KPG", 2011),
    ("Cantik Itu Luka", "Eka Kurniawan", "Gramedia Pustaka Utama", 2002),
    ("Pulang", "Tere Liye", "Republika", 2015),
    ("Laut Bercerita", "Leila S. Chudori", "KPG", 2017),
    ("Atomic Habits", "James Clear", "Gramedia Pustaka Utama", 2018),
    ("Sebuah Seni untuk Bersikap Bodo Amat", "Mark Manson", "Grasindo", 2016),
]

DUMMY_MEMBERS = [
    ("A001", "Budi Santoso"),
    ("A002", "Citra Lestari"),
    ("A003", "Ahmad Fauzi"),
    ("A004", "Dewi Anggraini"),
    ("A005", "Eko Prasetyo"),
]

def seed_database():
    """Fungsi utama untuk mengisi database dengan data dummy."""
    try:
        conn = sqlite3.connect(config.DATABASE_PATH)
        cursor = conn.cursor()
        print("Koneksi database berhasil.")

        
        print("Menghapus data lama...")
        cursor.execute("DELETE FROM history")
        cursor.execute("DELETE FROM members")
        cursor.execute("DELETE FROM books")
        
        cursor.execute("DELETE FROM sqlite_sequence WHERE name IN ('history', 'members', 'books')")
        print("Data lama berhasil dihapus.")

        
        print(f"Menambahkan {len(DUMMY_BOOKS)} data buku...")
        for book in DUMMY_BOOKS:
            judul, pengarang, penerbit, tahun = book
            
            isbn = f"978-602-{random.randint(1000, 9999)}-{random.randint(10, 99)}-{random.randint(0,9)}"
            cursor.execute(
                "INSERT INTO books (judul, isbn, pengarang, penerbit, tahun_terbit, status) VALUES (?, ?, ?, ?, ?, 'Tersedia')",
                (judul, isbn, pengarang, penerbit, tahun)
            )
        print("Data buku berhasil ditambahkan.")

        
        print(f"Menambahkan {len(DUMMY_MEMBERS)} data anggota...")
        now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        for member in DUMMY_MEMBERS:
            nomor, nama = member
            cursor.execute("INSERT INTO members (nomor_anggota, nama, tanggal_daftar) VALUES (?, ?, ?)", (nomor, nama, now))
        print("Data anggota berhasil ditambahkan.")

        
        print("Membuat data riwayat peminjaman...")
        
        
        cursor.execute("SELECT id FROM books")
        book_ids = [row[0] for row in cursor.fetchall()]
        
        cursor.execute("SELECT id, nama FROM members")
        members = cursor.fetchall() 
        
        
        num_borrowed_books = len(book_ids) // 2
        borrowed_book_ids = random.sample(book_ids, num_borrowed_books)
        
        for book_id in borrowed_book_ids:
            
            member_id, member_name = random.choice(members)
            
            
            borrow_date = datetime.datetime.now() - datetime.timedelta(days=random.randint(1, 30))
            borrow_date_str = borrow_date.strftime("%Y-%m-%d %H:%M:%S")
            
            
            cursor.execute("UPDATE books SET status = 'Dipinjam' WHERE id = ?", (book_id,))
            
            
            cursor.execute(
                "INSERT INTO history (book_id, member_id, aksi, tanggal, nama_pengguna_aksi) VALUES (?, ?, 'Pinjam', ?, ?)",
                (book_id, member_id, borrow_date_str, member_name)
            )

        print(f"{num_borrowed_books} buku telah ditandai sebagai 'Dipinjam' dan riwayatnya telah dibuat.")

        
        conn.commit()
        print("\nProses seeding data dummy berhasil!")

    except sqlite3.Error as e:
        print(f"Terjadi error pada database: {e}")
    finally:
        if conn:
            conn.close()
            print("Koneksi database ditutup.")

if __name__ == "__main__":
    
    print("--------------------------------------------------")
    print("PERINGATAN: Script ini akan MENGHAPUS SEMUA data")
    print("yang ada di database dan menggantinya dengan data dummy.")
    print("--------------------------------------------------")
    
    
    confirm = input("Apakah Anda yakin ingin melanjutkan? (y/n): ")
    
    if confirm.lower() == 'y':
        seed_database()
    else:
        print("Proses dibatalkan.")