import sqlite3
import datetime
import config 

def connect_db():
    """Mengkoneksikan ke database SQLite dan mengembalikan koneksi serta cursor."""
    conn = sqlite3.connect(config.DATABASE_PATH)
    cursor = conn.cursor()
    return conn, cursor

def init_db(cursor, conn):
    """Menginisialisasi tabel-tabel yang diperlukan jika belum ada."""
    # 1. Tabel Books
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS books (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        judul TEXT NOT NULL,
        isbn TEXT UNIQUE NOT NULL,
        pengarang TEXT NOT NULL,
        penerbit TEXT NOT NULL,
        tahun_terbit INTEGER NOT NULL,
        status TEXT NOT NULL DEFAULT 'Tersedia'
    )
    ''')

    # 2. Tabel Members
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS members (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nomor_anggota TEXT UNIQUE NOT NULL,
        nama TEXT NOT NULL,
        tanggal_daftar TEXT NOT NULL
    )
    ''')

    # 3. Tabel History (Versi yang sudah diperbaiki)
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS history (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        book_id INTEGER NOT NULL,
        member_id INTEGER,
        aksi TEXT NOT NULL,
        tanggal TEXT NOT NULL,
        nama_pengguna_aksi TEXT,
        FOREIGN KEY(book_id) REFERENCES books(id) ON DELETE CASCADE,
        FOREIGN KEY(member_id) REFERENCES members(id) ON DELETE SET NULL
    )
    ''')
    conn.commit()

def load_all_books(cursor):
    """Memuat semua buku dari database, diurutkan berdasarkan judul."""
    cursor.execute("SELECT * FROM books ORDER BY judul ASC")
    return cursor.fetchall()

def filter_books_by_term(cursor, search_text, db_column):
    """Memfilter buku berdasarkan term dan kolom yang diberikan."""
    query = f"SELECT * FROM books WHERE {db_column} LIKE ? ORDER BY judul ASC"
    cursor.execute(query, (f"%{search_text}%",))
    return cursor.fetchall()

def add_new_book(cursor, conn, book_data):
    """Menambahkan buku baru ke database."""
    try:
        cursor.execute('''
        INSERT INTO books (judul, isbn, pengarang, penerbit, tahun_terbit, status)
        VALUES (?, ?, ?, ?, ?, 'Tersedia')
        ''', book_data)
        conn.commit()
        return cursor.lastrowid, None  
    except sqlite3.IntegrityError as e:
        return None, e 
    except sqlite3.Error as e:
        return None, e 

def get_book_details_by_id(cursor, book_id):
    """Mengambil detail buku berdasarkan ID."""
    cursor.execute("SELECT judul, isbn, pengarang, penerbit, tahun_terbit FROM books WHERE id=?", (book_id,))
    return cursor.fetchone()

def update_existing_book(cursor, conn, book_id, book_data):
    """Memperbarui data buku yang ada di database."""
    try:
        cursor.execute('''
        UPDATE books
        SET judul=?, isbn=?, pengarang=?, penerbit=?, tahun_terbit=?
        WHERE id=?
        ''', (*book_data, book_id))
        conn.commit()
        return True, None 
    except sqlite3.IntegrityError as e:
        return False, e 
    except sqlite3.Error as e:
        return False, e 

def get_book_status(cursor, book_id):
    """Mendapatkan status buku berdasarkan ID."""
    cursor.execute("SELECT status FROM books WHERE id=?", (book_id,))
    return cursor.fetchone()

def delete_book_by_id(cursor, conn, book_id):
    """Menghapus buku dan riwayat terkaitnya dari database."""
    try:
        # ON DELETE CASCADE di tabel history akan menangani penghapusan riwayat secara otomatis
        # Namun untuk keamanan, kita biarkan saja.
        cursor.execute("DELETE FROM history WHERE book_id=?", (book_id,))
        cursor.execute("DELETE FROM books WHERE id=?", (book_id,))
        conn.commit()
        return True, None 
    except sqlite3.Error as e:
        return False, e 

def borrow_book_action(cursor, conn, book_id, member_id, member_name):
    """Memproses aksi peminjaman buku (dengan member_id)."""
    try:
        current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        cursor.execute("UPDATE books SET status='Dipinjam' WHERE id=?", (book_id,))
        cursor.execute(
            "INSERT INTO history (book_id, member_id, aksi, tanggal, nama_pengguna_aksi) VALUES (?, ?, 'Pinjam', ?, ?)",
            (book_id, member_id, current_time, member_name)
        )
        conn.commit()
        return True, None
    except sqlite3.Error as e:
        return False, e

def return_book_action(cursor, conn, book_id, pengembali_name):
    """Memproses aksi pengembalian buku."""
    try:
        current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        cursor.execute("UPDATE books SET status='Tersedia' WHERE id=?", (book_id,))
        cursor.execute(
            "INSERT INTO history (book_id, aksi, tanggal, nama_pengguna_aksi) VALUES (?, 'Kembali', ?, ?)",
            (book_id, current_time, pengembali_name)
        )
        conn.commit()
        return True, None
    except sqlite3.Error as e:
        return False, e

def load_all_history(cursor):
    """Memuat semua riwayat transaksi dari database, menggabungkan nama anggota."""
    cursor.execute('''
        SELECT h.id, h.book_id, b.judul, h.aksi, h.tanggal, 
               h.nama_pengguna_aksi AS nama_pengguna
        FROM history h
        JOIN books b ON h.book_id = b.id
        ORDER BY h.tanggal DESC
    ''')
    return cursor.fetchall()

def add_new_member(cursor, conn, nomor_anggota, nama):
    """Menambahkan anggota baru ke database."""
    try:
        current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        cursor.execute("INSERT INTO members (nomor_anggota, nama, tanggal_daftar) VALUES (?, ?, ?)",
                       (nomor_anggota, nama, current_time))
        conn.commit()
        return True, None
    except sqlite3.IntegrityError as e:
        return False, e 
    except sqlite3.Error as e:
        return False, e

def get_all_members(cursor):
    """Mengambil semua data anggota dari database."""
    cursor.execute("SELECT id, nomor_anggota, nama, tanggal_daftar FROM members ORDER BY nama ASC")
    return cursor.fetchall()

def update_member_details(cursor, conn, member_id, nomor_anggota, nama):
    """Memperbarui detail anggota."""
    try:
        cursor.execute("UPDATE members SET nomor_anggota = ?, nama = ? WHERE id = ?",
                       (nomor_anggota, nama, member_id))
        conn.commit()
        return True, None
    except sqlite3.IntegrityError as e:
        return False, e 
    except sqlite3.Error as e:
        return False, e

def delete_member_by_id(cursor, conn, member_id):
    """Menghapus anggota berdasarkan ID."""
    cursor.execute("""
        SELECT COUNT(*) FROM history h
        JOIN books b ON h.book_id = b.id
        WHERE h.member_id = ? AND b.status = 'Dipinjam'
    """, (member_id,))
    
    if cursor.fetchone()[0] > 0:
        return False, "Anggota ini masih memiliki buku yang sedang dipinjam."

    try:
        cursor.execute("DELETE FROM members WHERE id = ?", (member_id,))
        conn.commit()
        return True, None
    except sqlite3.Error as e:
        return False, str(e)