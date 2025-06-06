import sqlite3
from PyQt5.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
                            QLabel, QTableWidget, QTableWidgetItem, QLineEdit, QPushButton,
                            QMessageBox, QComboBox, QInputDialog, QStatusBar, QAbstractItemView,
                            QHeaderView) 
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QSize
import config
import database
import styles
from dialogs import BookDialog, HistoryDialog, MembersDialog, BorrowDialog

class LibraryApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Sistem Manajemen Perpustakaan")
        self.setGeometry(100, 100, 1080, 700)
        
        self.setWindowIcon(QIcon(config.get_icon_path("library.svg")))

        self.conn = None
        self.cursor = None
        self.init_db_connection()
        self.init_ui()
        self.load_books()
        self.update_button_states()

    
    def init_db_connection(self):
        try:
            self.conn, self.cursor = database.connect_db()
            database.init_db(self.cursor, self.conn)
        except sqlite3.Error as e:
            QMessageBox.critical(self, "Error Koneksi Database", f"Tidak dapat terhubung atau menginisialisasi database: {e}\nAplikasi akan ditutup.")
            self.conn = None 
            self.cursor = None

    def init_ui(self):
        self.setStyleSheet(styles.STYLESHEET)
        
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(25, 15, 25, 15)
        main_layout.setSpacing(15)

        title = QLabel("Manajemen Data Buku Perpustakaan")
        title.setObjectName("TitleLabel")
        title.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(title)

        search_container_widget = QWidget()
        search_layout = QHBoxLayout(search_container_widget)
        search_layout.setContentsMargins(5, 5, 5, 5) 
        search_layout.setSpacing(10) 

        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Ketik kata kunci pencarian...")
        self.search_input.textChanged.connect(self.filter_books_display)

        self.search_field = QComboBox()
        self.search_field.addItems(["Judul", "ISBN", "Pengarang", "Penerbit"])
        self.search_field.currentIndexChanged.connect(self.filter_books_display)
        
        
        
        
        
        search_layout.addWidget(QLabel("Cari berdasarkan:"))
        search_layout.addWidget(self.search_field, 1)
        search_layout.addWidget(self.search_input, 3)
        main_layout.addWidget(search_container_widget)

        self.books_table = QTableWidget()
        self.books_table.setColumnCount(8) 
        self.books_table.setHorizontalHeaderLabels(
            ["ID", "Judul Buku", "ISBN", "Pengarang", "Penerbit", "Tahun", "Status", "Actions"]
        )
        self.books_table.verticalHeader().setDefaultSectionSize(38) 
        self.books_table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.books_table.setAlternatingRowColors(True)
        self.books_table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.books_table.verticalHeader().setVisible(False)
        self.books_table.itemSelectionChanged.connect(self.update_button_states)
        main_layout.addWidget(self.books_table, 1)


        icon_size = QSize(16, 16) 

        action_buttons_layout = QHBoxLayout()
        action_buttons_layout.setSpacing(10)
        self.add_btn = QPushButton(" Tambah") 
        self.add_btn.setIcon(QIcon(config.get_icon_path("add.svg")))
        self.add_btn.setIconSize(icon_size)
        self.add_btn.setToolTip("Tambah buku baru ke perpustakaan")
        self.add_btn.clicked.connect(self.show_add_dialog)

        self.edit_btn = QPushButton(" Edit (Terpilih)")
        self.edit_btn.setIcon(QIcon(config.get_icon_path("edit.svg")))
        self.edit_btn.setIconSize(icon_size)
        self.edit_btn.setToolTip("Edit data buku yang dipilih dari tabel")
        self.edit_btn.clicked.connect(self.show_edit_dialog)

        self.delete_btn = QPushButton(" Hapus (Terpilih)")
        self.delete_btn.setIcon(QIcon(config.get_icon_path("delete.svg")))
        self.delete_btn.setIconSize(icon_size)
        self.delete_btn.setToolTip("Hapus buku yang dipilih dari tabel")
        self.delete_btn.clicked.connect(self.delete_book)

        action_buttons_layout.addWidget(self.add_btn)
        action_buttons_layout.addStretch()

        transaction_buttons_layout = QHBoxLayout()
        transaction_buttons_layout.setSpacing(10)
        self.borrow_btn = QPushButton(" Pinjam")
        self.borrow_btn.setToolTip("Pinjam buku yang dipilih")
        self.borrow_btn.clicked.connect(self.borrow_book)

        self.return_btn = QPushButton(" Kembalikan")
        self.return_btn.setToolTip("Kembalikan buku yang dipilih")
        self.return_btn.clicked.connect(self.return_book)

        self.history_btn = QPushButton(" Riwayat")
        self.history_btn.setIcon(QIcon(config.get_icon_path("history.svg")))
        self.history_btn.setIconSize(icon_size)
        self.history_btn.setToolTip("Lihat riwayat peminjaman dan pengembalian buku")
        self.history_btn.clicked.connect(self.show_history_dialog)

        transaction_buttons_layout.addStretch()
        transaction_buttons_layout.addWidget(self.borrow_btn)
        transaction_buttons_layout.addWidget(self.return_btn)
        transaction_buttons_layout.addWidget(self.history_btn)

        management_buttons_layout = QHBoxLayout()
        self.members_btn = QPushButton("Kelola Anggota")
        self.members_btn.clicked.connect(self.show_members_dialog)
        management_buttons_layout.addWidget(self.members_btn)
        management_buttons_layout.addStretch()

        buttons_master_layout = QHBoxLayout()
        buttons_master_layout.addLayout(action_buttons_layout)
        buttons_master_layout.addLayout(management_buttons_layout) 
        buttons_master_layout.addLayout(transaction_buttons_layout)
        main_layout.addLayout(buttons_master_layout)

        buttons_master_layout = QHBoxLayout()
        buttons_master_layout.addLayout(action_buttons_layout)
        buttons_master_layout.addLayout(transaction_buttons_layout)
        main_layout.addLayout(buttons_master_layout)

        self.statusBar = QStatusBar()
        self.setStatusBar(self.statusBar)
        self.show_status_message("Selamat datang di Sistem Manajemen Perpustakaan!", 5000)

    def _add_book_action_buttons(self, row_idx, book_id):
        widget = QWidget()
        layout = QHBoxLayout(widget)
        layout.setContentsMargins(5, 0, 5, 0)
        layout.setSpacing(5)

        icon_size_table = QSize(14, 14) 

        edit_btn = QPushButton() 
        edit_btn.setIcon(QIcon(config.get_icon_path("edit.svg")))
        edit_btn.setIconSize(icon_size_table)
        edit_btn.setToolTip(f"Edit buku ID: {book_id}")
        edit_btn.setFixedSize(30,30) 
        edit_btn.clicked.connect(lambda checked, b_id=book_id: self.handle_edit_book_from_table(b_id))
        
        delete_btn = QPushButton() 
        delete_btn.setIcon(QIcon(config.get_icon_path("delete.svg")))
        delete_btn.setIconSize(icon_size_table)
        delete_btn.setToolTip(f"Hapus buku ID: {book_id}")
        delete_btn.setFixedSize(30,30) 
        delete_btn.clicked.connect(lambda checked, b_id=book_id: self.handle_delete_book_from_table(b_id))

        layout.addWidget(edit_btn)
        layout.addWidget(delete_btn)
        layout.addStretch()
        widget.setLayout(layout)
        self.books_table.setCellWidget(row_idx, 7, widget)

    
    def _populate_table_with_books(self, books_data):
        self.books_table.setRowCount(0)
        self.books_table.resizeColumnsToContents()
        self.books_table.setColumnWidth(1, 250) 

        for row_idx, book in enumerate(books_data):
            self.books_table.insertRow(row_idx)
            for col_idx, value in enumerate(book): 
                item = QTableWidgetItem(str(value))
                if col_idx == 0 or col_idx == 5:
                    item.setTextAlignment(Qt.AlignCenter)
                else:
                    item.setTextAlignment(Qt.AlignLeft | Qt.AlignVCenter)
                self.books_table.setItem(row_idx, col_idx, item)
            
            book_id = book[0]
            self._add_book_action_buttons(row_idx, book_id)

        self.books_table.resizeColumnsToContents()
        self.books_table.setColumnWidth(1, 250) 
        self.books_table.setColumnWidth(7, 90) 
        self.books_table.horizontalHeader().setSectionResizeMode(1, QHeaderView.Stretch)
        for i in range(self.books_table.columnCount()):
            if i != 1:
                 self.books_table.horizontalHeader().setSectionResizeMode(i, QHeaderView.ResizeToContents)
        self.books_table.horizontalHeader().setStretchLastSection(False)
        self.update_button_states()

    def handle_edit_book_from_table(self, book_id):
        if not self.conn or not self.cursor:
            QMessageBox.warning(self, "Koneksi Error", "Koneksi database tidak tersedia.")
            return
        try:
            book_data_from_db = database.get_book_details_by_id(self.cursor, book_id)
            if book_data_from_db:
                dialog = BookDialog(self, current_data=book_data_from_db)
                if dialog.exec_():
                    updated_data = dialog.get_data()
                    old_title = book_data_from_db[0]
                    self.update_book(str(book_id), updated_data, old_title) 
            else:
                QMessageBox.critical(self, "Error", f"Data buku dengan ID {book_id} tidak ditemukan.")
                self.load_books() 
        except sqlite3.Error as e:
            QMessageBox.critical(self, "Error Database", f"Gagal mengambil data buku untuk diedit: {e}")
        except Exception as ex:
             QMessageBox.critical(self, "Error Tak Terduga", f"Terjadi kesalahan: {ex}")

    def handle_delete_book_from_table(self, book_id):
        if not self.conn or not self.cursor:
            QMessageBox.warning(self, "Koneksi Error", "Koneksi database tidak tersedia.")
            return
        try:
            self.cursor.execute("SELECT judul, status FROM books WHERE id=?", (book_id,))
            book_info = self.cursor.fetchone()
            if not book_info:
                QMessageBox.critical(self, "Error", f"Buku dengan ID {book_id} tidak ditemukan.")
                self.load_books()
                return
            
            book_title, status = book_info
            reply = QMessageBox.question(
                self, 'Konfirmasi Hapus',
                f"Apakah Anda yakin ingin menghapus buku '{book_title}' (ID: {book_id})?\n"
                "Riwayat terkait buku ini juga akan dihapus.",
                QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

            if reply == QMessageBox.Yes:
                if status == "Dipinjam":
                    QMessageBox.warning(self, "Tidak Dapat Menghapus", 
                                        f"Buku '{book_title}' sedang dipinjam dan tidak dapat dihapus. "
                                        "Kembalikan buku terlebih dahulu.")
                    return
                success, error = database.delete_book_by_id(self.cursor, self.conn, book_id)
                if error:
                    QMessageBox.critical(self, "Error Database", f"Gagal menghapus buku: {error}")
                elif success:
                    self.load_books()
                    self.show_status_message(f"Buku '{book_title}' dan riwayat terkait berhasil dihapus!", 4000)
        except sqlite3.Error as e:
            QMessageBox.critical(self, "Error Database", f"Gagal menghapus buku: {e}")
        except Exception as ex:
             QMessageBox.critical(self, "Error Tak Terduga", f"Terjadi kesalahan: {ex}")
    
    def load_books(self):
        if not self.cursor:
            self.show_status_message("Koneksi database tidak tersedia.", 5000)
            return
        try:
            books = database.load_all_books(self.cursor)
            self._populate_table_with_books(books) 
            if books:
                self.show_status_message(f"{len(books)} buku berhasil dimuat.", 3000)
            else:
                self.show_status_message("Belum ada data buku di perpustakaan.", 3000)
        except sqlite3.Error as e:
            QMessageBox.critical(self, "Error Database", f"Gagal memuat buku: {e}")
            self.show_status_message("Error memuat data buku!", 5000)

    def filter_books_display(self): 
        if not self.cursor:
            self.show_status_message("Koneksi database tidak tersedia untuk filter.", 5000)
            return
        search_text = self.search_input.text().strip()
        search_column_name = self.search_field.currentText()
        field_map = {
            "Judul": "judul", "ISBN": "isbn",
            "Pengarang": "pengarang", "Penerbit": "penerbit"
        }
        db_column = field_map.get(search_column_name, "judul")
        if not search_text:
            self.load_books()
            return
        try:
            books = database.filter_books_by_term(self.cursor, search_text, db_column)
            self._populate_table_with_books(books) 
            self.show_status_message(f"Ditemukan {len(books)} buku untuk '{search_text}'.", 3000)
        except sqlite3.Error as e:
            QMessageBox.critical(self, "Error Pencarian", f"Gagal mencari buku: {e}")
            self.show_status_message("Error saat mencari buku!", 5000)

    def show_add_dialog(self):
        if not self.conn:
            QMessageBox.warning(self, "Koneksi Error", "Koneksi database tidak tersedia.")
            return
        dialog = BookDialog(self) 
        if dialog.exec_():
            book_data = dialog.get_data()
            self.add_book(book_data)

    def add_book(self, book_data):
        if not self.cursor or not self.conn: return
        new_book_id, error = database.add_new_book(self.cursor, self.conn, book_data)
        if error:
            if isinstance(error, sqlite3.IntegrityError):
                QMessageBox.warning(self, "Gagal Menambahkan", f"ISBN '{book_data[1]}' sudah terdaftar. Mohon gunakan ISBN lain.")
            else:
                QMessageBox.critical(self, "Error Database", f"Gagal menambahkan buku: {error}")
        else:
            self.load_books()
            for row in range(self.books_table.rowCount()):
                if self.books_table.item(row, 0).text() == str(new_book_id):
                    self.books_table.selectRow(row)
                    break
            self.show_status_message(f"Buku '{book_data[0]}' berhasil ditambahkan!", 4000)
    
    def show_edit_dialog(self): 
        if not self.conn:
            QMessageBox.warning(self, "Koneksi Error", "Koneksi database tidak tersedia.")
            return
        selected_rows = self.books_table.selectionModel().selectedRows()
        if not selected_rows:
            QMessageBox.information(self, "Info", "Silakan pilih buku yang akan diedit dari tabel.")
            return
        selected_row_index = selected_rows[0].row()
        try:
            book_id_item = self.books_table.item(selected_row_index, 0) 
            if not book_id_item:
                QMessageBox.warning(self, "Info", "Tidak dapat mengambil ID buku dari baris terpilih.")
                return
            book_id_str = book_id_item.text()
            self.handle_edit_book_from_table(int(book_id_str)) 
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Tidak dapat memproses edit dari seleksi: {e}")

    def update_book(self, book_id_str, book_data, old_title): 
        if not self.cursor or not self.conn: return
        try:
            book_id = int(book_id_str)
        except ValueError:
            QMessageBox.critical(self, "Error Internal", "ID Buku tidak valid untuk pembaruan.")
            return
        success, error = database.update_existing_book(self.cursor, self.conn, book_id, book_data)
        if error:
            if isinstance(error, sqlite3.IntegrityError):
                 QMessageBox.warning(self, "Gagal Memperbarui", f"ISBN '{book_data[1]}' sudah terdaftar untuk buku lain.")
            else:
                QMessageBox.critical(self, "Error Database", f"Gagal memperbarui buku: {error}")
        elif success:
            self.load_books()
            for row in range(self.books_table.rowCount()):
                if self.books_table.item(row, 0).text() == str(book_id): 
                    self.books_table.selectRow(row)
                    break
            self.show_status_message(f"Data buku '{old_title}' berhasil diperbarui menjadi '{book_data[0]}'!", 4000)

    def delete_book(self): 
        if not self.conn:
            QMessageBox.warning(self, "Koneksi Error", "Koneksi database tidak tersedia.")
            return
        selected_rows = self.books_table.selectionModel().selectedRows()
        if not selected_rows:
            QMessageBox.information(self, "Info", "Silakan pilih buku yang akan dihapus dari tabel.")
            return
        selected_row_index = selected_rows[0].row()
        try:
            book_id_item = self.books_table.item(selected_row_index, 0) 
            if not book_id_item:
                QMessageBox.warning(self, "Info", "Tidak dapat mengambil ID buku dari baris terpilih.")
                return
            book_id_str = book_id_item.text()
            self.handle_delete_book_from_table(int(book_id_str)) 
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Tidak dapat memproses hapus dari seleksi: {e}")
    
    def update_button_states(self):
        selected_rows = self.books_table.selectionModel().selectedRows()
        has_selection = bool(selected_rows)
        self.edit_btn.setEnabled(has_selection)
        self.delete_btn.setEnabled(has_selection)
        if has_selection:
            selected_row_index = selected_rows[0].row()
            if selected_row_index < self.books_table.rowCount(): 
                status_item = self.books_table.item(selected_row_index, 6) 
                if status_item:
                    status = status_item.text().strip()
                    self.borrow_btn.setEnabled(status == "Tersedia")
                    self.return_btn.setEnabled(status == "Dipinjam")
                else: 
                    self.borrow_btn.setEnabled(False)
                    self.return_btn.setEnabled(False)
            else: 
                self.borrow_btn.setEnabled(False)
                self.return_btn.setEnabled(False)
        else:
            self.borrow_btn.setEnabled(False)
            self.return_btn.setEnabled(False)

    def show_status_message(self, message, timeout=3000):
        self.statusBar.showMessage(message, timeout)

    def _get_selected_book_info(self):
        selected_rows = self.books_table.selectionModel().selectedRows()
        if not selected_rows:
            return None, None, None
        selected_row_index = selected_rows[0].row()
        try:
            if selected_row_index < self.books_table.rowCount() and \
               self.books_table.item(selected_row_index, 0) and \
               self.books_table.item(selected_row_index, 1) and \
               self.books_table.item(selected_row_index, 6):
                book_id = self.books_table.item(selected_row_index, 0).text()
                book_title = self.books_table.item(selected_row_index, 1).text()
                status = self.books_table.item(selected_row_index, 6).text().strip()
                return book_id, book_title, status
            else:
                return None, None, None
        except AttributeError: 
            return None, None, None
            
    def borrow_book(self):
        if not self.conn:
            QMessageBox.warning(self, "Koneksi Error", "Koneksi database tidak tersedia.")
            return

        book_id, book_title, status = self._get_selected_book_info()
        if not book_id:
            QMessageBox.information(self, "Info Peminjaman", "Silakan pilih buku yang akan dipinjam.")
            return
        if status != "Tersedia":
            QMessageBox.warning(self, "Status Tidak Valid", f"Buku '{book_title}' tidak tersedia untuk dipinjam.")
            return

        
        members = database.get_all_members(self.cursor)
        if not members:
            QMessageBox.warning(self, "Tidak Ada Anggota", "Belum ada anggota yang terdaftar. Silakan tambahkan anggota terlebih dahulu.")
            return

        
        dialog = BorrowDialog(book_title, members, self)
        if dialog.exec_():
            member_id = dialog.get_selected_member_id()
            member_name = dialog.get_selected_member_name()

            
            success, error = database.borrow_book_action(self.cursor, self.conn, book_id, member_id, member_name)
            if success:
                self.load_books()
                self.show_status_message(f"Buku '{book_title}' berhasil dipinjam oleh {member_name}.", 4000)
            else:
                QMessageBox.critical(self, "Error Database", f"Gagal memproses peminjaman: {error}")

    def return_book(self):
        if not self.conn:
            QMessageBox.warning(self, "Koneksi Error", "Koneksi database tidak tersedia.")
            return
        book_id, book_title, status = self._get_selected_book_info()
        if not book_id: 
            return
        if status != "Dipinjam": 
            return

        pengembali, ok = QInputDialog.getText(self, "Identitas Pengembali", f"Masukkan nama pengembali untuk buku '{book_title}':")
        if not ok or not pengembali.strip():
            self.show_status_message("Pengembalian buku dibatalkan.", 3000)
            return

        success, error = database.return_book_action(self.cursor, self.conn, book_id, pengembali.strip())
        if success:
            self.load_books()
            self.show_status_message(f"Buku '{book_title}' berhasil dikembalikan oleh {pengembali.strip()}.", 4000)
        else:
            QMessageBox.critical(self, "Error Database", f"Gagal memproses pengembalian buku: {error}")

    def show_history_dialog(self):
        if not self.conn or not self.cursor:
            QMessageBox.warning(self, "Koneksi Error", "Koneksi database tidak tersedia untuk menampilkan riwayat.")
            return
        dialog = HistoryDialog(self, db_conn=self.conn, db_cursor=self.cursor) 
        dialog.exec_()

    def show_members_dialog(self):
        if not self.conn or not self.cursor:
            QMessageBox.warning(self, "Koneksi Error", "Koneksi database tidak tersedia.")
            return
        dialog = MembersDialog(self, db_conn=self.conn, db_cursor=self.cursor)
        dialog.exec_()


    def closeEvent(self, event):
        if self.conn:
            self.conn.close()
        event.accept()

