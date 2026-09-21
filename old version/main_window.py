# main_window.py  --  پنجره اصلی و منوی برنامه
from PyQt5.QtWidgets import (QMainWindow, QWidget, QLabel, QPushButton,
                             QVBoxLayout, QHBoxLayout, QStackedWidget,
                             QFrame, QMessageBox)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont


class PlaceholderPage(QWidget):
    """صفحه موقت — تا زمانی که بخش مربوطه ساخته شود"""
    def __init__(self, title, note=""):
        super().__init__()
        lay = QVBoxLayout(self)
        lbl = QLabel(title)
        lbl.setAlignment(Qt.AlignCenter)
        lbl.setFont(QFont("Tahoma", 16, QFont.Bold))
        lbl.setStyleSheet("color:#8a97a5;")
        lay.addStretch()
        lay.addWidget(lbl)
        if note:
            n = QLabel(note)
            n.setAlignment(Qt.AlignCenter)
            n.setWordWrap(True)
            n.setStyleSheet("color:#b0bcc8;")
            lay.addWidget(n)
        lay.addStretch()


class MainWindow(QMainWindow):
    def __init__(self, full_name="کاربر"):
        super().__init__()
        self.full_name = full_name
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("سیستم مدیریت کتابخانه")
        self.resize(1050, 640)

        # ---------- نوار کنار (منو) ----------
        sidebar = QFrame()
        sidebar.setFixedWidth(210)
        sidebar.setStyleSheet("QFrame { background:#1a3b5c; }")

        s_lay = QVBoxLayout(sidebar)
        s_lay.setContentsMargins(12, 18, 12, 18)
        s_lay.setSpacing(8)

        logo = QLabel("📚  کتابخانه")
        logo.setAlignment(Qt.AlignCenter)
        logo.setFont(QFont("Tahoma", 14, QFont.Bold))
        logo.setStyleSheet("color:white; padding-bottom:12px;")
        s_lay.addWidget(logo)

        self.buttons = []
        menu_items = [
            ("🏠  داشبورد", 0),
            ("📖  کتاب‌ها", 1),
            ("👤  اعضا", 2),
            ("🔄  امانت و بازگشت", 3),
            ("📊  گزارش‌ها", 4),
        ]
        for text, idx in menu_items:
            b = QPushButton(text)
            b.setMinimumHeight(42)
            b.setCursor(Qt.PointingHandCursor)
            b.setStyleSheet(self._menu_style(False))
            b.clicked.connect(lambda _, i=idx: self.switch_page(i))
            s_lay.addWidget(b)
            self.buttons.append(b)

        s_lay.addStretch()

        btn_logout = QPushButton("🚪  خروج از حساب")
        btn_logout.setMinimumHeight(38)
        btn_logout.setStyleSheet(
            "background:#c0392b; color:white; border:none;"
            "border-radius:6px; font-weight:bold;")
        btn_logout.clicked.connect(self.logout)
        s_lay.addWidget(btn_logout)

        # ---------- محتوای صفحات ----------
        self.pages = QStackedWidget()
        self.pages.addWidget(self._dashboard())                      # 0
        self.pages.addWidget(self._load("books",   "BooksPage",   "مدیریت کتاب‌ها"))    # 1
        self.pages.addWidget(self._load("members", "MembersPage", "مدیریت اعضا"))      # 2
        self.pages.addWidget(self._load("loans",   "LoansPage",   "امانت و بازگشت"))   # 3
        self.pages.addWidget(self._load("reports", "ReportsPage", "گزارش‌ها"))         # 4

        container = QWidget()
        c_lay = QHBoxLayout(container)
        c_lay.setContentsMargins(0, 0, 0, 0)
        c_lay.setSpacing(0)
        c_lay.addWidget(sidebar)
        c_lay.addWidget(self.pages, 1)

        self.setCentralWidget(container)
        self.statusBar().showMessage(f"کاربر جاری:  {self.full_name}")
        self.switch_page(0)

    # -----------------------------------------------------------
    def _menu_style(self, active):
        if active:
            return ("QPushButton { background:#2c7be5; color:white;"
                    "border:none; border-radius:6px; text-align:right;"
                    "padding:8px 14px; font-weight:bold; }")
        return ("QPushButton { background:transparent; color:#c9d6e3;"
                "border:none; border-radius:6px; text-align:right;"
                "padding:8px 14px; }"
                "QPushButton:hover { background:#25527d; color:white; }")

    def _load(self, module_name, class_name, title):
        """تلاش برای بارگذاری صفحه — اگر فایلش هنوز ساخته نشده، صفحه موقت"""
        try:
            module = __import__(module_name)
            return getattr(module, class_name)()
        except Exception:
            return PlaceholderPage(title, "این بخش در مرحله بعد اضافه می‌شود.")

    def _dashboard(self):
        page = QWidget()
        lay = QVBoxLayout(page)
        lay.setContentsMargins(26, 26, 26, 26)

        hello = QLabel(f"خوش آمدید، {self.full_name}")
        hello.setFont(QFont("Tahoma", 17, QFont.Bold))
        hello.setStyleSheet("color:#1a3b5c;")
        lay.addWidget(hello)

        self.cards_row = QHBoxLayout()
        self.cards_row.setSpacing(14)
        lay.addSpacing(18)
        lay.addLayout(self.cards_row)
        lay.addStretch()

        self.refresh_dashboard()
        return page

    def refresh_dashboard(self):
        """خواندن آمار از دیتابیس و ساخت کارت‌ها"""
        while self.cards_row.count():
            item = self.cards_row.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

        try:
            import db
            total_books   = db.fetch_one("SELECT COUNT(*) c FROM Books")["c"]
            total_members = db.fetch_one("SELECT COUNT(*) c FROM Members")["c"]
            active_loans  = db.fetch_one(
                "SELECT COUNT(*) c FROM Loans WHERE ReturnDate IS NULL")["c"]
            overdue = db.fetch_one(
                "SELECT COUNT(*) c FROM Loans "
                "WHERE ReturnDate IS NULL AND date(DueDate) < date('now')")["c"]
        except Exception:
            total_books = total_members = active_loans = overdue = 0

        stats = [
            ("تعداد کتاب‌ها",    total_books,   "#2c7be5"),
            ("تعداد اعضا",       total_members, "#00a97f"),
            ("امانت‌های فعال",   active_loans,  "#e8a33d"),
            ("سررسید گذشته",     overdue,       "#c0392b"),
        ]
        for label, value, color in stats:
            self.cards_row.addWidget(self._stat_card(label, value, color))
        self.cards_row.addStretch()

    def _stat_card(self, label, value, color):
        card = QFrame()
        card.setFixedSize(190, 110)
        card.setStyleSheet(
            f"QFrame {{ background:white; border:1px solid #e3e8ee;"
            f"border-radius:10px; border-top:4px solid {color}; }}")
        lay = QVBoxLayout(card)
        v = QLabel(str(value))
        v.setAlignment(Qt.AlignCenter)
        v.setFont(QFont("Tahoma", 22, QFont.Bold))
        v.setStyleSheet(f"color:{color};")
        t = QLabel(label)
        t.setAlignment(Qt.AlignCenter)
        t.setStyleSheet("color:#6b7b8b;")
        lay.addWidget(v)
        lay.addWidget(t)
        return card

    # -----------------------------------------------------------
    def switch_page(self, index):
        self.pages.setCurrentIndex(index)
        for i, b in enumerate(self.buttons):
            b.setStyleSheet(self._menu_style(i == index))
        if index == 0:
            self.refresh_dashboard()

    def logout(self):
        ok = QMessageBox.question(
            self, "خروج", "از حساب کاربری خارج می‌شوید؟",
            QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if ok == QMessageBox.Yes:
            from login import LoginWindow
            self.login = LoginWindow()
            self.login.show()
            self.close()