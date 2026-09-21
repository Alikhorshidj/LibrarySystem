import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QMainWindow, QLabel, QLineEdit,
    QPushButton, QVBoxLayout, QHBoxLayout, QGridLayout,
    QMessageBox, QFrame
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont


# ==========================================================
# پنجره اصلی نرم‌افزار
# ==========================================================
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("سیستم مدیریت کتابخانه")
        self.resize(1050, 650)

        self.create_ui()

    def create_ui(self):
        # ---------- منوی سمت راست ----------
        sidebar = QFrame()
        sidebar.setFixedWidth(220)
        sidebar.setStyleSheet("""
            QFrame {
                background-color: #1a3b5c;
            }
        """)

        menu_layout = QVBoxLayout()
        menu_layout.setContentsMargins(15, 25, 15, 20)
        menu_layout.setSpacing(10)

        logo = QLabel("📚 کتابخانه")
        logo.setAlignment(Qt.AlignCenter)
        logo.setFont(QFont("Tahoma", 16, QFont.Bold))
        logo.setStyleSheet("color: white; padding-bottom: 20px;")
        menu_layout.addWidget(logo)

        # دکمه‌های منو
        btn_dashboard = self.create_menu_button("🏠  داشبورد")
        btn_books = self.create_menu_button("📖  مدیریت کتاب‌ها")
        btn_members = self.create_menu_button("👥  مدیریت اعضا")
        btn_loans = self.create_menu_button("🔄  امانت و بازگشت")
        btn_reports = self.create_menu_button("📊  گزارش‌ها")

        btn_dashboard.clicked.connect(self.show_dashboard_message)
        btn_books.clicked.connect(lambda: self.show_coming_soon("مدیریت کتاب‌ها"))
        btn_members.clicked.connect(lambda: self.show_coming_soon("مدیریت اعضا"))
        btn_loans.clicked.connect(lambda: self.show_coming_soon("امانت و بازگشت کتاب"))
        btn_reports.clicked.connect(lambda: self.show_coming_soon("گزارش‌ها"))

        menu_layout.addWidget(btn_dashboard)
        menu_layout.addWidget(btn_books)
        menu_layout.addWidget(btn_members)
        menu_layout.addWidget(btn_loans)
        menu_layout.addWidget(btn_reports)

        menu_layout.addStretch()

        btn_logout = QPushButton("🚪 خروج از حساب")
        btn_logout.setMinimumHeight(42)
        btn_logout.setStyleSheet("""
            QPushButton {
                background-color: #c0392b;
                color: white;
                border: none;
                border-radius: 6px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #a93226;
            }
        """)
        btn_logout.clicked.connect(self.logout)
        menu_layout.addWidget(btn_logout)

        sidebar.setLayout(menu_layout)

        # ---------- بخش محتوای اصلی ----------
        content = QWidget()
        content_layout = QVBoxLayout()
        content_layout.setContentsMargins(35, 30, 35, 30)
        content_layout.setSpacing(15)

        welcome = QLabel("خوش آمدید، مدیر سیستم 👋")
        welcome.setFont(QFont("Tahoma", 18, QFont.Bold))
        welcome.setStyleSheet("color: #1a3b5c;")
        content_layout.addWidget(welcome)

        description = QLabel("داشبورد سیستم مدیریت کتابخانه")
        description.setStyleSheet("color: #718096; font-size: 12px;")
        content_layout.addWidget(description)

        content_layout.addSpacing(15)

        # کارت‌های آماری
        cards_layout = QGridLayout()
        cards_layout.setSpacing(15)

        cards_layout.addWidget(
            self.create_stat_card("تعداد کتاب‌ها", "0", "#2c7be5"), 0, 0
        )
        cards_layout.addWidget(
            self.create_stat_card("تعداد اعضا", "0", "#00a97f"), 0, 1
        )
        cards_layout.addWidget(
            self.create_stat_card("امانت‌های فعال", "0", "#e8a33d"), 1, 0
        )
        cards_layout.addWidget(
            self.create_stat_card("کتاب‌های دیرکرد", "0", "#c0392b"), 1, 1
        )

        content_layout.addLayout(cards_layout)
        content_layout.addStretch()

        footer = QLabel("سیستم مدیریت کتابخانه | پروژه درس برنامه‌نویسی")
        footer.setAlignment(Qt.AlignCenter)
        footer.setStyleSheet("color: #9aa7b4; font-size: 10px;")
        content_layout.addWidget(footer)

        content.setLayout(content_layout)

        # قرار دادن منو و محتوا کنار هم
        main_layout = QHBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # چون برنامه فارسی است، منو سمت راست قرار می‌گیرد
        main_layout.addWidget(content, 1)
        main_layout.addWidget(sidebar)

        central_widget = QWidget()
        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)

        # ظاهر کلی برنامه
        self.setStyleSheet("""
            QMainWindow {
                background-color: #f4f7fb;
                font-family: Tahoma;
                font-size: 12px;
            }
        """)

    def create_menu_button(self, text):
        """ساخت دکمه‌های یک‌شکل برای منو"""
        button = QPushButton(text)
        button.setMinimumHeight(45)
        button.setCursor(Qt.PointingHandCursor)
        button.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                color: #d7e3ef;
                border: none;
                border-radius: 6px;
                text-align: right;
                padding-right: 12px;
                font-size: 12px;
            }
            QPushButton:hover {
                background-color: #28577f;
                color: white;
            }
        """)
        return button

    def create_stat_card(self, title, value, color):
        """ساخت کارت آماری داشبورد"""
        card = QFrame()
        card.setMinimumSize(240, 130)
        card.setStyleSheet(f"""
            QFrame {{
                background-color: white;
                border: 1px solid #e1e7ee;
                border-top: 5px solid {color};
                border-radius: 9px;
            }}
        """)

        layout = QVBoxLayout()
        layout.setContentsMargins(15, 12, 15, 12)

        value_label = QLabel(value)
        value_label.setAlignment(Qt.AlignCenter)
        value_label.setFont(QFont("Tahoma", 24, QFont.Bold))
        value_label.setStyleSheet(f"color: {color}; border: none;")

        title_label = QLabel(title)
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setStyleSheet("color: #607080; border: none; font-size: 12px;")

        layout.addWidget(value_label)
        layout.addWidget(title_label)

        card.setLayout(layout)
        return card

    def show_dashboard_message(self):
        QMessageBox.information(
            self,
            "داشبورد",
            "شما در صفحه اصلی و داشبورد سیستم هستید."
        )

    def show_coming_soon(self, section_name):
        QMessageBox.information(
            self,
            section_name,
            f"بخش «{section_name}» در مرحله بعدی ساخته می‌شود."
        )

    def logout(self):
        answer = QMessageBox.question(
            self,
            "خروج از حساب",
            "آیا می‌خواهید از حساب کاربری خارج شوید؟",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )

        if answer == QMessageBox.Yes:
            self.login_window = LoginWindow()
            self.login_window.show()
            self.close()


# ==========================================================
# فرم ورود
# ==========================================================
class LoginWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("ورود | سیستم مدیریت کتابخانه")
        self.setFixedSize(420, 350)

        title = QLabel("📚 سیستم مدیریت کتابخانه")
        title.setAlignment(Qt.AlignCenter)
        title.setFont(QFont("Tahoma", 16, QFont.Bold))
        title.setStyleSheet("color: #1a3b5c;")

        subtitle = QLabel("لطفاً نام کاربری و رمز عبور را وارد کنید")
        subtitle.setAlignment(Qt.AlignCenter)
        subtitle.setStyleSheet("color: #6c7a89; font-size: 11px;")

        username_label = QLabel("نام کاربری:")
        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("مثال: admin")
        self.username_input.setAlignment(Qt.AlignRight)

        password_label = QLabel("رمز عبور:")
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("رمز عبور را وارد کنید")
        self.password_input.setEchoMode(QLineEdit.Password)
        self.password_input.setAlignment(Qt.AlignRight)

        login_button = QPushButton("ورود به سیستم")
        login_button.setMinimumHeight(42)
        login_button.clicked.connect(self.check_login)

        self.password_input.returnPressed.connect(self.check_login)

        hint = QLabel("برای تست: نام کاربری admin | رمز عبور 1234")
        hint.setAlignment(Qt.AlignCenter)
        hint.setStyleSheet("color: #8b98a5; font-size: 10px;")

        layout = QVBoxLayout()
        layout.setContentsMargins(45, 30, 45, 30)
        layout.setSpacing(10)

        layout.addWidget(title)
        layout.addWidget(subtitle)
        layout.addSpacing(15)
        layout.addWidget(username_label)
        layout.addWidget(self.username_input)
        layout.addWidget(password_label)
        layout.addWidget(self.password_input)
        layout.addSpacing(10)
        layout.addWidget(login_button)
        layout.addSpacing(10)
        layout.addWidget(hint)

        self.setLayout(layout)

        self.setStyleSheet("""
            QWidget {
                background-color: white;
                font-family: Tahoma;
                font-size: 12px;
            }
            QLineEdit {
                border: 1px solid #b8c4d0;
                border-radius: 6px;
                padding: 8px;
            }
            QLineEdit:focus {
                border: 2px solid #2c7be5;
            }
            QPushButton {
                background-color: #2c7be5;
                color: white;
                border: none;
                border-radius: 6px;
                font-weight: bold;
                padding: 8px;
            }
            QPushButton:hover {
                background-color: #1b65c2;
            }
        """)

        self.username_input.setFocus()

    def check_login(self):
        username = self.username_input.text().strip()
        password = self.password_input.text().strip()

        if username == "" or password == "":
            QMessageBox.warning(
                self,
                "اطلاعات ناقص",
                "لطفاً نام کاربری و رمز عبور را وارد کنید."
            )
            return

        if username == "admin" and password == "1234":
            # پنجره اصلی را در متغیر نگه می‌داریم تا بسته نشود
            self.main_window = MainWindow()
            self.main_window.show()
            self.close()
        else:
            QMessageBox.critical(
                self,
                "ورود ناموفق",
                "نام کاربری یا رمز عبور اشتباه است."
            )
            self.password_input.clear()
            self.password_input.setFocus()


# ==========================================================
# اجرای برنامه
# ==========================================================
app = QApplication(sys.argv)
app.setLayoutDirection(Qt.RightToLeft)

window = LoginWindow()
window.show()

sys.exit(app.exec_())