import datetime
from PyQt5.QtWidgets import (QDialog, QFormLayout, QLineEdit, QDialogButtonBox, QComboBox,
                             QMessageBox, QVBoxLayout, QLabel, QTableWidget,
                             QTableWidgetItem, QPushButton, QHBoxLayout, QAbstractItemView)
from PyQt5.QtCore import Qt, QTimer

import database

class BookDialog(QDialog):
    def __init__(self, parent=None, current_data=None):
        super().__init__(parent)
    
        self.setWindowTitle("Tambah Buku Baru")
        self.setMinimumWidth(450)

        layout = QFormLayout(self)
        layout.setSpacing(12)
        layout.setContentsMargins(20, 20, 20, 20)

        self.judul_input = QLineEdit()
        self.judul_input.setPlaceholderText("Contoh: Belajar Python untuk Pemula")
        self.isbn_input = QLineEdit()
        self.isbn_input.setPlaceholderText("Contoh: 978-602-03-7509-0")
        self.pengarang_input = QLineEdit()
        self.pengarang_input.setPlaceholderText("Contoh: Budi Setiawan")
        self.penerbit_input = QLineEdit()
        self.penerbit_input.setPlaceholderText("Contoh: Gramedia Pustaka Utama")
        self.tahun_input = QLineEdit()
        self.tahun_input.setPlaceholderText(f"Contoh: {datetime.datetime.now().year}")

        layout.addRow("Judul Buku:", self.judul_input)
        layout.addRow("ISBN:", self.isbn_input)
        layout.addRow("Pengarang:", self.pengarang_input)
        layout.addRow("Penerbit:", self.penerbit_input)
        layout.addRow("Tahun Terbit:", self.tahun_input)

        self.button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        self.button_box.accepted.connect(self.validate_and_accept)
        self.button_box.rejected.connect(self.reject)
        layout.addRow("", self.button_box)

        if current_data:
            self.setWindowTitle("Edit Data Buku")
            self.set_data(current_data)
        else:
            QTimer.singleShot(0, self.judul_input.setFocus)

    def get_data(self):
        return (
            self.judul_input.text().strip(),
            self.isbn_input.text().strip(),
            self.pengarang_input.text().strip(),
            self.penerbit_input.text().strip(),
            int(self.tahun_input.text().strip())
        )

    def set_data(self, book_data_tuple):
        self.judul_input.setText(book_data_tuple[0])
        self.isbn_input.setText(book_data_tuple[1])
        self.pengarang_input.setText(book_data_tuple[2])
        self.penerbit_input.setText(book_data_tuple[3])
        self.tahun_input.setText(str(book_data_tuple[4]))
        QTimer.singleShot(0, self.judul_input.setFocus)
        self.judul_input.selectAll()

    def validate_and_accept(self):
        inputs_to_validate = {
            "Judul Buku": self.judul_input,
            "ISBN": self.isbn_input,
            "Pengarang": self.pengarang_input,
            "Penerbit": self.penerbit_input,
            "Tahun Terbit": self.tahun_input
        }
        for field_name, qlineedit in inputs_to_validate.items():
            if not qlineedit.text().strip():
                QMessageBox.warning(self, "Input Tidak Lengkap", f"Kolom '{field_name}' tidak boleh kosong.")
                qlineedit.setFocus()
                return

        tahun_text = self.tahun_input.text().strip()
        current_year = datetime.datetime.now().year
        if not tahun_text.isdigit() or not (1000 <= int(tahun_text) <= current_year + 5) :
            QMessageBox.warning(self, "Input Tidak Valid", f"Tahun Terbit ('{tahun_text}') harus berupa angka tahun yang valid (misal antara 1000 dan {current_year + 5}).")
            self.tahun_input.setFocus()
            self.tahun_input.selectAll()
            return
        super().accept()

class HistoryDialog(QDialog):
    def __init__(self, parent=None, db_conn=None, db_cursor=None):
        super().__init__(parent)
    
        self.setWindowTitle("Riwayat Peminjaman & Pengembalian Buku")
        self.setMinimumSize(800, 500)
        self.db_conn = db_conn
        self.db_cursor = db_cursor

        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)

        filter_layout = QHBoxLayout()
        self.filter_input = QLineEdit()
        self.filter_input.setPlaceholderText("Cari berdasarkan ID buku, judul, aksi, atau nama user...")
        self.filter_input.textChanged.connect(self.filter_history)
        filter_layout.addWidget(QLabel("Filter Riwayat:"))
        filter_layout.addWidget(self.filter_input, 1)
        layout.addLayout(filter_layout)

        self.table = QTableWidget()
        self.table.setColumnCount(6)
        self.table.setHorizontalHeaderLabels([
            "ID Riwayat", "ID Buku", "Judul Buku", "Aksi", 
            "Tanggal & Waktu", "Nama Pengguna", "Tindakan"
        ])
        self.table.setAlternatingRowColors(True)
        self.table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.table.verticalHeader().setVisible(False)
        self.table.horizontalHeader().setStretchLastSection(True)
        layout.addWidget(self.table, 1)

        close_button = QPushButton("Tutup")
        close_button.clicked.connect(self.accept)
        button_layout = QHBoxLayout()
        button_layout.addStretch()
        button_layout.addWidget(close_button)
        layout.addLayout(button_layout)

        self.all_history_data = []
        if self.db_cursor:
            self.load_history()
        else:
            QMessageBox.critical(self, "Error Database", "Koneksi atau cursor database tidak tersedia untuk memuat riwayat.")

    def load_history(self):
        if not self.db_cursor:
            return
        try:
            self.all_history_data = database.load_all_history(self.db_cursor)
            self.display_history_data(self.all_history_data)
            if not self.all_history_data and self.parent():
                 if hasattr(self.parent(), 'show_status_message'):
                    self.parent().show_status_message("Belum ada riwayat transaksi.", 3000)
        except Exception as e:
            QMessageBox.critical(self, "Error Database", f"Gagal memuat riwayat: {e}")

    def display_history_data(self, data_to_display):
        self.table.setRowCount(0)
        for row_idx, row_data in enumerate(data_to_display):
            self.table.insertRow(row_idx)
            for col_idx, value in enumerate(row_data):
                item = QTableWidgetItem(str(value))
                if col_idx == 0 or col_idx == 1:
                    item.setTextAlignment(Qt.AlignCenter)
                else:
                    item.setTextAlignment(Qt.AlignLeft | Qt.AlignVCenter)
                self.table.setItem(row_idx, col_idx, item)
        self.table.resizeColumnsToContents()
        self.table.horizontalHeader().setStretchLastSection(True)
        if self.table.columnCount() > 2:
             self.table.setColumnWidth(2, 200)
        self.table.setColumnWidth(4, 150)
        self.table.setColumnWidth(5, 150)

    def filter_history(self):
        filter_text = self.filter_input.text().lower().strip()
        if not filter_text:
            self.display_history_data(self.all_history_data)
            return

        filtered_data = []
        for row in self.all_history_data:
            if (filter_text in str(row[1]).lower() or
                filter_text in str(row[2]).lower() or
                filter_text in str(row[3]).lower() or
                filter_text in str(row[5]).lower()):
                filtered_data.append(row)
        self.display_history_data(filtered_data)

class AddEditMemberDialog(QDialog):
    def __init__(self, parent=None, current_data=None):
        super().__init__(parent)
        self.setWindowTitle("Tambah Anggota Baru")
        if current_data:
            self.setWindowTitle("Edit Data Anggota")
        
        self.setMinimumWidth(400)
        layout = QFormLayout(self)
        layout.setContentsMargins(20,20,20,20)

        self.nomor_input = QLineEdit()
        self.nama_input = QLineEdit()

        layout.addRow("Nomor Anggota:", self.nomor_input)
        layout.addRow("Nama Lengkap:", self.nama_input)

        if current_data:
        
            self.member_id = current_data[0]
            self.nomor_input.setText(current_data[1])
            self.nama_input.setText(current_data[2])

        self.button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        self.button_box.accepted.connect(self.accept)
        self.button_box.rejected.connect(self.reject)
        layout.addWidget(self.button_box)

    def get_data(self):
        return self.nomor_input.text().strip(), self.nama_input.text().strip()

class MembersDialog(QDialog):
    def __init__(self, parent=None, db_conn=None, db_cursor=None):
        super().__init__(parent)
        self.setWindowTitle("Manajemen Anggota Perpustakaan")
        self.setMinimumSize(700, 500)
        self.db_conn = db_conn
        self.db_cursor = db_cursor
        
        main_layout = QVBoxLayout(self)
        
    
        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(["ID", "Nomor Anggota", "Nama Lengkap", "Tanggal Daftar"])
        self.table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.table.setSelectionMode(QAbstractItemView.SingleSelection)
        main_layout.addWidget(self.table)
        
    
        button_layout = QHBoxLayout()
        self.add_btn = QPushButton("Tambah Anggota")
        self.add_btn.clicked.connect(self.add_member)
        self.edit_btn = QPushButton("Edit Anggota")
        self.edit_btn.clicked.connect(self.edit_member)
        self.delete_btn = QPushButton("Hapus Anggota")
        self.delete_btn.clicked.connect(self.delete_member)
        self.close_btn = QPushButton("Tutup")
        self.close_btn.clicked.connect(self.accept)
        
        button_layout.addWidget(self.add_btn)
        button_layout.addWidget(self.edit_btn)
        button_layout.addWidget(self.delete_btn)
        button_layout.addStretch()
        button_layout.addWidget(self.close_btn)
        main_layout.addLayout(button_layout)
        
        self.load_members()

    def load_members(self):
        self.table.setRowCount(0)
        members = database.get_all_members(self.db_cursor)
        for row, member_data in enumerate(members):
            self.table.insertRow(row)
            for col, data in enumerate(member_data):
                self.table.setItem(row, col, QTableWidgetItem(str(data)))
        self.table.resizeColumnsToContents()
        
    def add_member(self):
        dialog = AddEditMemberDialog(self)
        if dialog.exec_():
            nomor, nama = dialog.get_data()
            if not nomor or not nama:
                QMessageBox.warning(self, "Input Kosong", "Nomor anggota dan nama tidak boleh kosong.")
                return
            success, error = database.add_new_member(self.db_cursor, self.db_conn, nomor, nama)
            if success:
                self.load_members()
            else:
                QMessageBox.critical(self, "Error", f"Gagal menambahkan anggota: {error}")

    def edit_member(self):
        selected_row = self.table.currentRow()
        if selected_row < 0:
            QMessageBox.warning(self, "Peringatan", "Pilih anggota yang akan diedit.")
            return
        
        member_id = self.table.item(selected_row, 0).text()
        nomor_anggota = self.table.item(selected_row, 1).text()
        nama = self.table.item(selected_row, 2).text()
        
        dialog = AddEditMemberDialog(self, current_data=(member_id, nomor_anggota, nama))
        if dialog.exec_():
            new_nomor, new_nama = dialog.get_data()
            success, error = database.update_member_details(self.db_cursor, self.db_conn, member_id, new_nomor, new_nama)
            if success:
                self.load_members()
            else:
                QMessageBox.critical(self, "Error", f"Gagal memperbarui anggota: {error}")

    def delete_member(self):
        selected_row = self.table.currentRow()
        if selected_row < 0:
            QMessageBox.warning(self, "Peringatan", "Pilih anggota yang akan dihapus.")
            return
            
        member_id = self.table.item(selected_row, 0).text()
        nama = self.table.item(selected_row, 2).text()

        reply = QMessageBox.question(self, "Konfirmasi Hapus", f"Yakin ingin menghapus anggota '{nama}'?",
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            success, error = database.delete_member_by_id(self.db_cursor, self.db_conn, member_id)
            if success:
                self.load_members()
            else:
                QMessageBox.critical(self, "Error", f"Gagal menghapus anggota: {error}")

class BorrowDialog(QDialog):
    def __init__(self, book_title, members, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Pilih Peminjam")
        layout = QVBoxLayout(self)
        
        layout.addWidget(QLabel(f"<b>Buku:</b> {book_title}"))
        layout.addWidget(QLabel("Pilih anggota yang akan meminjam:"))
        
        self.members_combo = QComboBox()
        self.members_data = members
        for member in members:
        
            self.members_combo.addItem(f"{member[2]} ({member[1]})", userData=member[0])
        layout.addWidget(self.members_combo)
        
        button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)
        layout.addWidget(button_box)

    def get_selected_member_id(self):
        return self.members_combo.currentData()

    def get_selected_member_name(self):
    
        full_text = self.members_combo.currentText()
        return full_text.split(' (')[0]
