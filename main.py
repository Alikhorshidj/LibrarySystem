import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QLineEdit,
    QPushButton, QVBoxLayout, QMessageBox
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont


class LoginWindow(QWidget):
    def __init__(self):
        super().__init__()

        # تنظیمات پنجره
        self.setWindowTitle("ورود | سیستم مدیریت کتابخانه")
        self.setFixedSize(420, 350)

        # ---------- عنوان ----------
        title = QLabel("📚 سیستم مدیریت کتابخانه")
        title.setAlignment(Qt.AlignCenter)
        title.setFont(QFont("Tahoma", 16, QFont.Bold))
        title.setStyleSheet("color: #1a3b5c;")

        subtitle = QLabel("لطفاً نام کاربری و رمز عبور را وارد کنید")
        subtitle.setAlignment(Qt.AlignCenter)
        subtitle.setStyleSheet("color: #6c7a89; font-size: 11px;")

        # ---------- کادر نام کاربری ----------
        username_label = QLabel("نام کاربری:")
        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("مثال: admin")
        self.username_input.setAlignment(Qt.AlignRight)

        # ---------- کادر رمز ----------
        password_label = QLabel("رمز عبور:")
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("رمز عبور را وارد کنید")
        self.password_input.setEchoMode(QLineEdit.Password)
        self.password_input.setAlignment(Qt.AlignRight)

        # ---------- دکمه ورود ----------
        login_button = QPushButton("ورود به سیستم")
        login_button.setMinimumHeight(42)
        login_button.clicked.connect(self.check_login)

        # با زدن Enter در رمز عبور نیز وارد شود
        self.password_input.returnPressed.connect(self.check_login)

        # راهنمای تست
        hint = QLabel("برای تست:  نام کاربری admin  |  رمز عبور 1234")
        hint.setAlignment(Qt.AlignCenter)
        hint.setStyleSheet("color: #8b98a5; font-size: 10px;")

        # ---------- چیدمان ----------
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

        # ظاهر کلی فرم
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
                background-color: #ffffff;
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

            QPushButton:pressed {
                background-color: #124a91;
            }
        """)

        # وقتی فرم باز شد، مکان‌نما روی نام کاربری باشد
        self.username_input.setFocus()

    def check_login(self):
        """بررسی اطلاعات ورود؛ فعلاً نام کاربری و رمز ثابت هستند."""
        username = self.username_input.text().strip()
        password = self.password_input.text().strip()

        # اگر فیلدی خالی باشد
        if username == "" or password == "":
            QMessageBox.warning(
                self,
                "اطلاعات ناقص",
                "لطفاً نام کاربری و رمز عبور را وارد کنید."
            )
            return

        # ورود صحیح
        if username == "admin" and password == "1234":
            QMessageBox.information(
                self,
                "ورود موفق",
                "خوش آمدید، مدیر سیستم!"
            )
        else:
            QMessageBox.critical(
                self,
                "ورود ناموفق",
                "نام کاربری یا رمز عبور اشتباه است."
            )
            self.password_input.clear()
            self.password_input.setFocus()


# ---------- اجرای برنامه ----------
app = QApplication(sys.argv)
app.setLayoutDirection(Qt.RightToLeft)  # راست‌به‌چپ شدن فرم فارسی

window = LoginWindow()
window.show()

sys.exit(app.exec_())