STYLESHEET = """
    /* === Global Styles === */
    QMainWindow {
        background-color: #f0f2f5; /* Latar belakang utama yang lembut */
    }

    QWidget { /* Font default untuk seluruh aplikasi */
        font-family: Segoe UI, Arial, sans-serif; /* Prioritaskan font yang umum */
        font-size: 13px; /* Ukuran font dasar */
    }

    /* === Main Title Label === */
    QLabel#TitleLabel {
        font-size: 28px; /* Sedikit lebih besar */
        font-weight: bold;
        color: #1c313a; /* Warna judul yang gelap dan elegan */
        margin: 20px 0 15px 0; /* Margin atas-bawah disesuaikan */
        padding-bottom: 5px; /* Padding bawah untuk sedikit ruang */
        /* border-bottom: 1px solid #d1d8e0; */ /* Opsional: garis bawah tipis */
    }

    /* === Table Styling === */
    QTableWidget {
        background-color: #ffffff;
        border: 1px solid #d1d8e0; /* Border halus */
        border-radius: 7px; /* Border radius sedikit lebih besar */
        font-size: 13px;
        selection-background-color: #455a64; /* Warna seleksi lebih gelap agar kontras */
        selection-color: #ffffff; /* Teks seleksi menjadi putih */
        alternate-background-color: #f8f9fa; /* Warna baris alternatif */
        gridline-color: #e9ecef; /* Warna garis grid halus */
        outline: none; /* Hilangkan outline fokus default tabel */
    }
    QHeaderView::section {
        background-color: #37474f; /* Warna header lebih gelap, sedikit diubah */
        color: #ffffff;
        font-weight: bold;
        font-size: 14px;
        padding: 10px 8px; /* Padding sedikit lebih tinggi */
        border: none;
        border-bottom: 1px solid #2c3a41; /* Garis bawah header lebih gelap */
    }
    QTableWidget::item {
        padding: 5px; /* Padding untuk sel tabel */
    }

    /* === Input Fields (QLineEdit, QComboBox) === */
    QLineEdit, QComboBox {
        padding: 9px 12px; /* Padding sedikit lebih nyaman */
        border: 1px solid #ced4da;
        border-radius: 6px; /* Border radius disamakan */
        font-size: 14px;
        background-color: #ffffff;
        selection-background-color: #a5b1c2;
        height: 20px; /* Tinggi eksplisit untuk konsistensi */
    }
    QLineEdit:focus, QComboBox:focus {
        border: 1.5px solid #37474f; /* Border fokus lebih tebal dan gelap */
        /* background-color: #fdfdfe; */ /* Latar belakang sedikit berubah saat fokus (opsional) */
    }
    QComboBox::drop-down {
        subcontrol-origin: padding;
        subcontrol-position: top right;
        width: 20px; /* Lebar area panah */
        border-left-width: 1px;
        border-left-color: #ced4da;
        border-left-style: solid;
        border-top-right-radius: 6px;
        border-bottom-right-radius: 6px;
        background-color: #f8f9fa; /* Latar belakang panah sedikit beda */
    }
    QComboBox::down-arrow {
        image: url(); /* Kosongkan untuk menggunakan panah default atau ganti dengan SVG/PNG */
        /* Jika ingin menggunakan karakter:
        qproperty-text: "▼"; (mungkin memerlukan penyesuaian font)
        */
        width: 10px; /* Ukuran ikon panah */
        height: 10px;
    }
    QComboBox::down-arrow:on { /* Saat dropdown terbuka */
        /* qproperty-text: "▲"; */
    }
    QComboBox QAbstractItemView { /* Styling untuk item di dropdown */
        border: 1px solid #ced4da;
        background-color: #ffffff;
        selection-background-color: #455a64;
        selection-color: #ffffff;
        padding: 4px;
    }


    /* === Buttons === */
    QPushButton {
        background-color: #455a64; /* Warna dasar tombol */
        color: #ffffff;
        border-radius: 6px; /* Border radius disamakan */
        padding: 10px 22px; /* Padding disesuaikan untuk ukuran font */
        font-size: 13px;
        font-weight: bold;
        margin: 0 4px; /* Margin antar tombol */
        border: none;
        outline: none;
        min-height: 20px; /* Tinggi minimum tombol */
    }
    QPushButton:hover {
        background-color: #546e7a; /* Warna hover lebih terang */
    }
    QPushButton:pressed {
        background-color: #37474f; /* Warna saat ditekan */
    }
    QPushButton:disabled {
        background-color: #90a4ae; /* Warna tombol nonaktif */
        color: #cfd8dc;
    }
    /* Tombol khusus (jika diperlukan styling berbeda) */
    /* QPushButton#SpecialButton { background-color: #c0392b; } */

    /* === Dialog Specific Styles === */
    QDialog {
        background-color: #f0f2f5; /* Sama dengan main window */
    }
    QDialog QLabel { /* Label umum di dialog */
        font-size: 14px;
        padding-top: 3px; /* Sedikit padding atas untuk form layout */
    }
     /* QFormLayout QLabel di dalam QDialog (lebih spesifik) */
    QDialog QFormLayout > QLabel {
        font-weight: normal; /* Atau bold jika diinginkan */
        color: #333333;
        padding-right: 10px; /* Jarak antara label dan input field */
    }
    QDialog QLineEdit, QDialog QComboBox { /* Input field di dialog */
        font-size: 14px; /* Konsisten dengan main window */
    }
    QDialogButtonBox QPushButton { /* Tombol OK/Cancel di dialog */
        padding: 8px 20px; /* Padding sedikit berbeda untuk dialog */
        font-size: 13px;
    }


    /* === Status Bar === */
    QStatusBar {
        font-size: 12px;
        color: #37474f;
        background-color: #e9ecef; /* Warna latar status bar */
        border-top: 1px solid #d1d8e0; /* Garis atas untuk pemisah */
        padding: 3px 0;
    }
    QStatusBar::item {
        border: none; /* Hilangkan border default item status bar */
    }

    /* === QMessageBox === */
    QMessageBox {
        background-color: #f0f2f5;
    }
    QMessageBox QLabel {
        font-size: 14px;
        color: #333333;
    }
    QMessageBox QPushButton {
        padding: 8px 18px;
    }

    /* === ScrollBar Styling === */
    QScrollBar:vertical {
        border: 1px solid #d1d8e0;
        background: #f0f2f5;
        width: 14px; /* Lebar scrollbar */
        margin: 14px 0 14px 0; /* Margin atas-bawah untuk tombol panah */
    }
    QScrollBar::handle:vertical {
        background: #b0bec5; /* Warna handle */
        min-height: 25px; /* Tinggi minimum handle */
        border-radius: 6px;
    }
    QScrollBar::handle:vertical:hover {
        background: #90a4ae;
    }
    QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
        border: 1px solid #d1d8e0;
        background: #e0e0e0;
        height: 14px; /* Tinggi tombol panah */
        subcontrol-position: top;
        subcontrol-origin: margin;
        border-radius: 3px;
    }
    QScrollBar::sub-line:vertical {
        subcontrol-position: bottom;
    }
    QScrollBar::up-arrow:vertical, QScrollBar::down-arrow:vertical {
        /* Anda bisa menggunakan image untuk panah kustom */
        width: 8px;
        height: 8px;
        background: #607d8b; /* Warna panah */
    }
    QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {
        background: none; /* Area track di belakang handle */
    }

    QScrollBar:horizontal {
        border: 1px solid #d1d8e0;
        background: #f0f2f5;
        height: 14px;
        margin: 0 14px 0 14px;
    }
    QScrollBar::handle:horizontal {
        background: #b0bec5;
        min-width: 25px;
        border-radius: 6px;
    }
    QScrollBar::handle:horizontal:hover {
        background: #90a4ae;
    }
    QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal {
        border: 1px solid #d1d8e0;
        background: #e0e0e0;
        width: 14px;
        subcontrol-position: left; /* left untuk sub-line, right untuk add-line */
        subcontrol-origin: margin;
        border-radius: 3px;
    }
    QScrollBar::sub-line:horizontal {
        subcontrol-position: right;
    }
    QScrollBar::left-arrow:horizontal, QScrollBar::right-arrow:horizontal {
        width: 8px;
        height: 8px;
        background: #607d8b;
    }
    QScrollBar::add-page:horizontal, QScrollBar::sub-page:horizontal {
        background: none;
    }
"""