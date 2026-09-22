import sys
import database
from datetime import date, timedelta
from PyQt5.QtWidgets import (
    QApplication, QWidget, QMainWindow, QDialog,
    QLabel, QLineEdit, QPushButton,
    QVBoxLayout, QHBoxLayout, QGridLayout, QFormLayout,
    QMessageBox, QFrame, QComboBox,
    QTableWidget, QTableWidgetItem, QHeaderView
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont

# ==========================================================
# پنجره مدیریت کتاب‌ها
# ==========================================================
class BooksWindow(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowTitle("مدیریت کتاب‌ها")
        self.resize(1000, 650)

        self.create_ui()
        self.load_categories()
        self.load_books()

    def create_ui(self):
        # ---------- عنوان ----------
        title = QLabel("📖 مدیریت کتاب‌ها")
        title.setStyleSheet("""
            color: #1a3b5c;
            font-size: 18px;
            font-weight: bold;
        """)

        description = QLabel(
            "در این بخش می‌توانید کتاب جدید ثبت کنید، جست‌وجو کنید یا حذف کنید."
        )
        description.setStyleSheet("color: #718096;")

        # ---------- فرم افزودن کتاب ----------
        form_frame = QFrame()
        form_frame.setStyleSheet("""
            QFrame {
                background-color: white;
                border: 1px solid #dce3ea;
                border-radius: 8px;
            }
        """)

        form_layout = QGridLayout()
        form_layout.setContentsMargins(20, 18, 20, 18)
        form_layout.setHorizontalSpacing(15)
        form_layout.setVerticalSpacing(10)

        self.title_input = QLineEdit()
        self.title_input.setPlaceholderText("مثال: سمفونی مردگان")

        self.author_input = QLineEdit()
        self.author_input.setPlaceholderText("مثال: عباس معروفی")

        self.publisher_input = QLineEdit()
        self.publisher_input.setPlaceholderText("مثال: نشر ققنوس")

        self.isbn_input = QLineEdit()
        self.isbn_input.setPlaceholderText("مثال: 9786000000000")

        self.category_combo = QComboBox()

        self.copies_input = QLineEdit()
        self.copies_input.setPlaceholderText("مثال: 3")
        self.copies_input.setText("1")

        form_layout.addWidget(QLabel("عنوان کتاب: *"), 0, 0)
        form_layout.addWidget(self.title_input, 0, 1)

        form_layout.addWidget(QLabel("نویسنده: *"), 0, 2)
        form_layout.addWidget(self.author_input, 0, 3)

        form_layout.addWidget(QLabel("ناشر:"), 1, 0)
        form_layout.addWidget(self.publisher_input, 1, 1)

        form_layout.addWidget(QLabel("شابک:"), 1, 2)
        form_layout.addWidget(self.isbn_input, 1, 3)

        form_layout.addWidget(QLabel("دسته‌بندی:"), 2, 0)
        form_layout.addWidget(self.category_combo, 2, 1)

        form_layout.addWidget(QLabel("تعداد نسخه: *"), 2, 2)
        form_layout.addWidget(self.copies_input, 2, 3)

        self.add_button = QPushButton("➕ ثبت کتاب")
        self.add_button.setMinimumHeight(38)
        self.add_button.clicked.connect(self.add_book)

        self.clear_button = QPushButton("پاک کردن فرم")
        self.clear_button.setMinimumHeight(38)
        self.clear_button.setStyleSheet("""
            QPushButton {
                background-color: #718096;
            }
            QPushButton:hover {
                background-color: #536273;
            }
        """)
        self.clear_button.clicked.connect(self.clear_form)

        buttons_layout = QHBoxLayout()
        buttons_layout.addStretch()
        buttons_layout.addWidget(self.clear_button)
        buttons_layout.addWidget(self.add_button)

        form_layout.addLayout(buttons_layout, 3, 0, 1, 4)

        form_frame.setLayout(form_layout)

        # ---------- جست‌وجو و حذف ----------
        search_layout = QHBoxLayout()

        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("🔍 جست‌وجو بر اساس عنوان، نویسنده یا شابک...")
        self.search_input.textChanged.connect(self.load_books)

        self.delete_button = QPushButton("🗑 حذف کتاب انتخاب‌شده")
        self.delete_button.setMinimumHeight(36)
        self.delete_button.setStyleSheet("""
            QPushButton {
                background-color: #c0392b;
            }
            QPushButton:hover {
                background-color: #a93226;
            }
        """)
        self.delete_button.clicked.connect(self.delete_book)

        search_layout.addWidget(self.search_input, 1)
        search_layout.addWidget(self.delete_button)

        # ---------- جدول کتاب‌ها ----------
        self.books_table = QTableWidget()
        self.books_table.setColumnCount(7)
        self.books_table.setHorizontalHeaderLabels([
            "شناسه", "عنوان کتاب", "نویسنده", "ناشر",
            "شابک", "دسته‌بندی", "نسخه‌های موجود"
        ])

        self.books_table.setSelectionBehavior(QTableWidget.SelectRows)
        self.books_table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.books_table.setAlternatingRowColors(True)
        self.books_table.verticalHeader().setVisible(False)

        header = self.books_table.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.Stretch)

        # ---------- چیدمان اصلی ----------
        layout = QVBoxLayout()
        layout.setContentsMargins(25, 25, 25, 25)
        layout.setSpacing(14)

        layout.addWidget(title)
        layout.addWidget(description)
        layout.addWidget(form_frame)
        layout.addLayout(search_layout)
        layout.addWidget(self.books_table)

        self.setLayout(layout)

        # ---------- ظاهر ----------
        self.setStyleSheet("""
            QDialog {
                background-color: #f4f7fb;
                font-family: Tahoma;
                font-size: 12px;
            }

            QLabel {
                color: #334155;
            }

            QLineEdit, QComboBox {
                background-color: white;
                border: 1px solid #b8c4d0;
                border-radius: 5px;
                padding: 7px;
                min-height: 20px;
            }

            QLineEdit:focus, QComboBox:focus {
                border: 2px solid #2c7be5;
            }

            QPushButton {
                background-color: #2c7be5;
                color: white;
                border: none;
                border-radius: 5px;
                padding: 8px 14px;
                font-weight: bold;
            }

            QPushButton:hover {
                background-color: #1b65c2;
            }

            QTableWidget {
                background-color: white;
                border: 1px solid #dce3ea;
                border-radius: 6px;
                gridline-color: #e7edf3;
            }

            QHeaderView::section {
                background-color: #1a3b5c;
                color: white;
                padding: 8px;
                border: none;
                font-weight: bold;
            }

            QTableWidget::item:selected {
                background-color: #cfe4ff;
                color: #1a3b5c;
            }
        """)

    def load_categories(self):
        """خواندن دسته‌بندی‌ها از دیتابیس و نمایش در ComboBox"""
        self.category_combo.clear()

        categories = database.fetch_all(
            "SELECT id, name FROM categories ORDER BY name"
        )

        for category in categories:
            self.category_combo.addItem(category["name"], category["id"])

    def add_book(self):
        """ثبت کتاب جدید در دیتابیس"""
        title = self.title_input.text().strip()
        author = self.author_input.text().strip()
        publisher = self.publisher_input.text().strip()
        isbn = self.isbn_input.text().strip()
        category_id = self.category_combo.currentData()
        copies_text = self.copies_input.text().strip()

        if title == "" or author == "" or copies_text == "":
            QMessageBox.warning(
                self,
                "اطلاعات ناقص",
                "لطفاً عنوان کتاب، نویسنده و تعداد نسخه را وارد کنید."
            )
            return

        try:
            copies = int(copies_text)

            if copies <= 0:
                raise ValueError

        except ValueError:
            QMessageBox.warning(
                self,
                "مقدار نامعتبر",
                "تعداد نسخه باید یک عدد صحیح بزرگ‌تر از صفر باشد."
            )
            self.copies_input.setFocus()
            return

        database.execute_query(
            """
            INSERT INTO books (
                title, author, publisher, isbn,
                category_id, total_copies, available_copies
            )
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            (
                title, author, publisher, isbn,
                category_id, copies, copies
            )
        )

        QMessageBox.information(
            self,
            "ثبت موفق",
            f"کتاب «{title}» با موفقیت ثبت شد."
        )

        self.clear_form()
        self.load_books()

    def load_books(self):
        """نمایش کتاب‌ها در جدول و اعمال جست‌وجو"""
        search_text = self.search_input.text().strip()

        query = """
            SELECT
                books.id,
                books.title,
                books.author,
                books.publisher,
                books.isbn,
                categories.name AS category_name,
                books.available_copies
            FROM books
            LEFT JOIN categories ON books.category_id = categories.id
        """

        parameters = ()

        if search_text != "":
            query += """
                WHERE books.title LIKE ?
                   OR books.author LIKE ?
                   OR books.isbn LIKE ?
            """
            search_value = f"%{search_text}%"
            parameters = (search_value, search_value, search_value)

        query += " ORDER BY books.id DESC"

        books = database.fetch_all(query, parameters)

        self.books_table.setRowCount(0)

        for row_index, book in enumerate(books):
            self.books_table.insertRow(row_index)

            values = [
                str(book["id"]),
                book["title"] or "",
                book["author"] or "",
                book["publisher"] or "-",
                book["isbn"] or "-",
                book["category_name"] or "-",
                str(book["available_copies"])
            ]

            for column_index, value in enumerate(values):
                item = QTableWidgetItem(value)
                item.setTextAlignment(Qt.AlignCenter)
                self.books_table.setItem(row_index, column_index, item)

    def clear_form(self):
        """خالی‌کردن فرم ثبت کتاب"""
        self.title_input.clear()
        self.author_input.clear()
        self.publisher_input.clear()
        self.isbn_input.clear()
        self.copies_input.setText("1")
        self.category_combo.setCurrentIndex(0)
        self.title_input.setFocus()

    def delete_book(self):
        """حذف کتاب انتخاب‌شده از دیتابیس"""
        selected_row = self.books_table.currentRow()

        if selected_row == -1:
            QMessageBox.warning(
                self,
                "انتخاب کتاب",
                "ابتدا یک کتاب را از جدول انتخاب کنید."
            )
            return

        book_id = self.books_table.item(selected_row, 0).text()
        book_title = self.books_table.item(selected_row, 1).text()

        answer = QMessageBox.question(
            self,
            "تأیید حذف",
            f"آیا از حذف کتاب «{book_title}» مطمئن هستید؟",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )

        if answer == QMessageBox.Yes:
            database.execute_query(
                "DELETE FROM books WHERE id = ?",
                (book_id,)
            )

            QMessageBox.information(
                self,
                "حذف موفق",
                "کتاب انتخاب‌شده حذف شد."
            )

            self.load_books()

# ==========================================================
# پنجره مدیریت اعضای کتابخانه
# ==========================================================
class MembersWindow(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowTitle("مدیریت اعضا")
        self.resize(1000, 650)

        self.create_ui()
        self.load_members()

    def create_ui(self):
        # ---------- عنوان ----------
        title = QLabel("👥 مدیریت اعضای کتابخانه")
        title.setStyleSheet("""
            color: #1a3b5c;
            font-size: 18px;
            font-weight: bold;
        """)

        description = QLabel(
            "در این بخش می‌توانید اعضای کتابخانه را ثبت، جست‌وجو یا حذف کنید."
        )
        description.setStyleSheet("color: #718096;")

        # ---------- فرم ثبت عضو ----------
        form_frame = QFrame()
        form_frame.setStyleSheet("""
            QFrame {
                background-color: white;
                border: 1px solid #dce3ea;
                border-radius: 8px;
            }
        """)

        form_layout = QGridLayout()
        form_layout.setContentsMargins(20, 18, 20, 18)
        form_layout.setHorizontalSpacing(15)
        form_layout.setVerticalSpacing(10)

        self.full_name_input = QLineEdit()
        self.full_name_input.setPlaceholderText("مثال: علی احمدی")

        self.national_code_input = QLineEdit()
        self.national_code_input.setPlaceholderText("مثال: 0012345678")

        self.phone_input = QLineEdit()
        self.phone_input.setPlaceholderText("مثال: 09121234567")

        self.email_input = QLineEdit()
        self.email_input.setPlaceholderText("مثال: ali@email.com")

        form_layout.addWidget(QLabel("نام و نام خانوادگی: *"), 0, 0)
        form_layout.addWidget(self.full_name_input, 0, 1)

        form_layout.addWidget(QLabel("کد ملی:"), 0, 2)
        form_layout.addWidget(self.national_code_input, 0, 3)

        form_layout.addWidget(QLabel("شماره تلفن:"), 1, 0)
        form_layout.addWidget(self.phone_input, 1, 1)

        form_layout.addWidget(QLabel("ایمیل:"), 1, 2)
        form_layout.addWidget(self.email_input, 1, 3)

        self.add_button = QPushButton("➕ ثبت عضو")
        self.add_button.setMinimumHeight(38)
        self.add_button.clicked.connect(self.add_member)

        self.clear_button = QPushButton("پاک کردن فرم")
        self.clear_button.setMinimumHeight(38)
        self.clear_button.setStyleSheet("""
            QPushButton {
                background-color: #718096;
            }

            QPushButton:hover {
                background-color: #536273;
            }
        """)
        self.clear_button.clicked.connect(self.clear_form)

        buttons_layout = QHBoxLayout()
        buttons_layout.addStretch()
        buttons_layout.addWidget(self.clear_button)
        buttons_layout.addWidget(self.add_button)

        form_layout.addLayout(buttons_layout, 2, 0, 1, 4)

        form_frame.setLayout(form_layout)

        # ---------- جست‌وجو و حذف ----------
        search_layout = QHBoxLayout()

        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText(
            "🔍 جست‌وجو بر اساس نام، کد ملی یا شماره تلفن..."
        )
        self.search_input.textChanged.connect(self.load_members)

        self.delete_button = QPushButton("🗑 حذف عضو انتخاب‌شده")
        self.delete_button.setMinimumHeight(36)
        self.delete_button.setStyleSheet("""
            QPushButton {
                background-color: #c0392b;
            }

            QPushButton:hover {
                background-color: #a93226;
            }
        """)
        self.delete_button.clicked.connect(self.delete_member)

        search_layout.addWidget(self.search_input, 1)
        search_layout.addWidget(self.delete_button)

        # ---------- جدول اعضا ----------
        self.members_table = QTableWidget()
        self.members_table.setColumnCount(6)
        self.members_table.setHorizontalHeaderLabels([
            "شناسه",
            "نام و نام خانوادگی",
            "کد ملی",
            "شماره تلفن",
            "ایمیل",
            "تاریخ عضویت"
        ])

        self.members_table.setSelectionBehavior(QTableWidget.SelectRows)
        self.members_table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.members_table.setAlternatingRowColors(True)
        self.members_table.verticalHeader().setVisible(False)

        header = self.members_table.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.Stretch)

        # ---------- چیدمان صفحه ----------
        layout = QVBoxLayout()
        layout.setContentsMargins(25, 25, 25, 25)
        layout.setSpacing(14)

        layout.addWidget(title)
        layout.addWidget(description)
        layout.addWidget(form_frame)
        layout.addLayout(search_layout)
        layout.addWidget(self.members_table)

        self.setLayout(layout)

        # ---------- ظاهر ----------
        self.setStyleSheet("""
            QDialog {
                background-color: #f4f7fb;
                font-family: Tahoma;
                font-size: 12px;
            }

            QLabel {
                color: #334155;
            }

            QLineEdit {
                background-color: white;
                border: 1px solid #b8c4d0;
                border-radius: 5px;
                padding: 7px;
                min-height: 20px;
            }

            QLineEdit:focus {
                border: 2px solid #2c7be5;
            }

            QPushButton {
                background-color: #2c7be5;
                color: white;
                border: none;
                border-radius: 5px;
                padding: 8px 14px;
                font-weight: bold;
            }

            QPushButton:hover {
                background-color: #1b65c2;
            }

            QTableWidget {
                background-color: white;
                border: 1px solid #dce3ea;
                border-radius: 6px;
                gridline-color: #e7edf3;
            }

            QHeaderView::section {
                background-color: #1a3b5c;
                color: white;
                padding: 8px;
                border: none;
                font-weight: bold;
            }

            QTableWidget::item:selected {
                background-color: #cfe4ff;
                color: #1a3b5c;
            }
        """)

    def add_member(self):
        """ثبت عضو جدید در دیتابیس"""
        full_name = self.full_name_input.text().strip()
        national_code = self.national_code_input.text().strip()
        phone = self.phone_input.text().strip()
        email = self.email_input.text().strip()

        if full_name == "":
            QMessageBox.warning(
                self,
                "اطلاعات ناقص",
                "لطفاً نام و نام خانوادگی عضو را وارد کنید."
            )
            self.full_name_input.setFocus()
            return

        # جلوگیری از ثبت کد ملی تکراری، در صورتی که وارد شده باشد
        if national_code != "":
            duplicate_member = database.fetch_one(
                "SELECT id FROM members WHERE national_code = ?",
                (national_code,)
            )

            if duplicate_member is not None:
                QMessageBox.warning(
                    self,
                    "عضو تکراری",
                    "عضوی با این کد ملی قبلاً ثبت شده است."
                )
                return

        database.execute_query(
            """
            INSERT INTO members (
                full_name, national_code, phone, email, register_date
            )
            VALUES (?, ?, ?, ?, date('now'))
            """,
            (full_name, national_code, phone, email)
        )

        QMessageBox.information(
            self,
            "ثبت موفق",
            f"عضو «{full_name}» با موفقیت ثبت شد."
        )

        self.clear_form()
        self.load_members()

    def load_members(self):
        """نمایش اعضا در جدول و اعمال جست‌وجو"""
        search_text = self.search_input.text().strip()

        query = """
            SELECT
                id,
                full_name,
                national_code,
                phone,
                email,
                register_date
            FROM members
        """

        parameters = ()

        if search_text != "":
            query += """
                WHERE full_name LIKE ?
                   OR national_code LIKE ?
                   OR phone LIKE ?
            """

            search_value = f"%{search_text}%"
            parameters = (search_value, search_value, search_value)

        query += " ORDER BY id DESC"

        members = database.fetch_all(query, parameters)

        self.members_table.setRowCount(0)

        for row_index, member in enumerate(members):
            self.members_table.insertRow(row_index)

            values = [
                str(member["id"]),
                member["full_name"] or "",
                member["national_code"] or "-",
                member["phone"] or "-",
                member["email"] or "-",
                member["register_date"] or ""
            ]

            for column_index, value in enumerate(values):
                item = QTableWidgetItem(value)
                item.setTextAlignment(Qt.AlignCenter)
                self.members_table.setItem(row_index, column_index, item)

    def clear_form(self):
        """پاک‌کردن فرم ثبت عضو"""
        self.full_name_input.clear()
        self.national_code_input.clear()
        self.phone_input.clear()
        self.email_input.clear()
        self.full_name_input.setFocus()

    def delete_member(self):
        """حذف عضو انتخاب‌شده"""
        selected_row = self.members_table.currentRow()

        if selected_row == -1:
            QMessageBox.warning(
                self,
                "انتخاب عضو",
                "ابتدا یک عضو را از جدول انتخاب کنید."
            )
            return

        member_id = self.members_table.item(selected_row, 0).text()
        member_name = self.members_table.item(selected_row, 1).text()

        # عضوی که امانت فعال دارد نباید حذف شود
        active_loan = database.fetch_one(
            """
            SELECT id FROM loans
            WHERE member_id = ? AND return_date IS NULL
            """,
            (member_id,)
        )

        if active_loan is not None:
            QMessageBox.warning(
                self,
                "امکان حذف وجود ندارد",
                "این عضو کتاب امانت گرفته و هنوز آن را برنگردانده است."
            )
            return

        answer = QMessageBox.question(
            self,
            "تأیید حذف",
            f"آیا از حذف عضو «{member_name}» مطمئن هستید؟",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )

        if answer == QMessageBox.Yes:
            database.execute_query(
                "DELETE FROM members WHERE id = ?",
                (member_id,)
            )

            QMessageBox.information(
                self,
                "حذف موفق",
                "عضو انتخاب‌شده حذف شد."
            )

            self.load_members()

# ==========================================================
# پنجره امانت و بازگشت کتاب
# ==========================================================
class LoansWindow(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowTitle("امانت و بازگشت کتاب")
        self.resize(1050, 680)

        self.create_ui()
        self.load_members()
        self.load_available_books()
        self.load_loans()

    def create_ui(self):
        # ---------- عنوان ----------
        title = QLabel("🔄 امانت و بازگشت کتاب")
        title.setStyleSheet("""
            color: #1a3b5c;
            font-size: 18px;
            font-weight: bold;
        """)

        description = QLabel(
            "در این بخش می‌توانید کتاب را به اعضا امانت دهید و بازگشت آن را ثبت کنید."
        )
        description.setStyleSheet("color: #718096;")

        # ---------- فرم ثبت امانت ----------
        form_frame = QFrame()
        form_frame.setStyleSheet("""
            QFrame {
                background-color: white;
                border: 1px solid #dce3ea;
                border-radius: 8px;
            }
        """)

        form_layout = QGridLayout()
        form_layout.setContentsMargins(20, 18, 20, 18)
        form_layout.setHorizontalSpacing(15)
        form_layout.setVerticalSpacing(10)

        self.member_combo = QComboBox()
        self.book_combo = QComboBox()

        self.loan_date_input = QLineEdit()
        self.loan_date_input.setText(date.today().isoformat())
        self.loan_date_input.setReadOnly(True)

        self.due_date_input = QLineEdit()
        self.due_date_input.setText(
            (date.today() + timedelta(days=14)).isoformat()
        )
        self.due_date_input.setReadOnly(True)

        form_layout.addWidget(QLabel("عضو: *"), 0, 0)
        form_layout.addWidget(self.member_combo, 0, 1)

        form_layout.addWidget(QLabel("کتاب: *"), 0, 2)
        form_layout.addWidget(self.book_combo, 0, 3)

        form_layout.addWidget(QLabel("تاریخ امانت:"), 1, 0)
        form_layout.addWidget(self.loan_date_input, 1, 1)

        form_layout.addWidget(QLabel("مهلت بازگشت (۱۴ روز):"), 1, 2)
        form_layout.addWidget(self.due_date_input, 1, 3)

        self.loan_button = QPushButton("📚 ثبت امانت")
        self.loan_button.setMinimumHeight(40)
        self.loan_button.clicked.connect(self.create_loan)

        form_layout.addWidget(self.loan_button, 2, 0, 1, 4)

        form_frame.setLayout(form_layout)

        # ---------- ابزارهای جدول ----------
        tools_layout = QHBoxLayout()

        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText(
            "🔍 جست‌وجو بر اساس نام عضو یا عنوان کتاب..."
        )
        self.search_input.textChanged.connect(self.load_loans)

        self.return_button = QPushButton("✅ ثبت بازگشت کتاب انتخاب‌شده")
        self.return_button.setMinimumHeight(36)
        self.return_button.setStyleSheet("""
            QPushButton {
                background-color: #00a97f;
            }

            QPushButton:hover {
                background-color: #008a68;
            }
        """)
        self.return_button.clicked.connect(self.return_book)

        tools_layout.addWidget(self.search_input, 1)
        tools_layout.addWidget(self.return_button)

        # ---------- جدول امانت‌ها ----------
        self.loans_table = QTableWidget()
        self.loans_table.setColumnCount(8)
        self.loans_table.setHorizontalHeaderLabels([
            "شناسه",
            "عنوان کتاب",
            "عضو",
            "تاریخ امانت",
            "مهلت بازگشت",
            "تاریخ بازگشت",
            "وضعیت",
            "جریمه"
        ])

        self.loans_table.setSelectionBehavior(QTableWidget.SelectRows)
        self.loans_table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.loans_table.setAlternatingRowColors(True)
        self.loans_table.verticalHeader().setVisible(False)

        header = self.loans_table.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.Stretch)

        # ---------- چیدمان ----------
        layout = QVBoxLayout()
        layout.setContentsMargins(25, 25, 25, 25)
        layout.setSpacing(14)

        layout.addWidget(title)
        layout.addWidget(description)
        layout.addWidget(form_frame)
        layout.addLayout(tools_layout)
        layout.addWidget(self.loans_table)

        self.setLayout(layout)

        # ---------- ظاهر ----------
        self.setStyleSheet("""
            QDialog {
                background-color: #f4f7fb;
                font-family: Tahoma;
                font-size: 12px;
            }

            QLabel {
                color: #334155;
            }

            QLineEdit, QComboBox {
                background-color: white;
                border: 1px solid #b8c4d0;
                border-radius: 5px;
                padding: 7px;
                min-height: 20px;
            }

            QPushButton {
                background-color: #2c7be5;
                color: white;
                border: none;
                border-radius: 5px;
                padding: 8px 14px;
                font-weight: bold;
            }

            QPushButton:hover {
                background-color: #1b65c2;
            }

            QTableWidget {
                background-color: white;
                border: 1px solid #dce3ea;
                border-radius: 6px;
                gridline-color: #e7edf3;
            }

            QHeaderView::section {
                background-color: #1a3b5c;
                color: white;
                padding: 8px;
                border: none;
                font-weight: bold;
            }

            QTableWidget::item:selected {
                background-color: #cfe4ff;
                color: #1a3b5c;
            }
        """)

    def load_members(self):
        """بارگذاری اعضا در لیست انتخاب عضو"""
        self.member_combo.clear()

        members = database.fetch_all("""
            SELECT id, full_name
            FROM members
            ORDER BY full_name
        """)

        if len(members) == 0:
            self.member_combo.addItem("ابتدا یک عضو ثبت کنید", None)
            return

        for member in members:
            self.member_combo.addItem(
                member["full_name"],
                member["id"]
            )

    def load_available_books(self):
        """نمایش فقط کتاب‌هایی که حداقل یک نسخه موجود دارند"""
        self.book_combo.clear()

        books = database.fetch_all("""
            SELECT id, title, author, available_copies
            FROM books
            WHERE available_copies > 0
            ORDER BY title
        """)

        if len(books) == 0:
            self.book_combo.addItem("کتاب قابل امانتی وجود ندارد", None)
            return

        for book in books:
            text = (
                f"{book['title']} | {book['author']} "
                f"(موجودی: {book['available_copies']})"
            )

            self.book_combo.addItem(text, book["id"])

    def create_loan(self):
        """ثبت امانت کتاب و کم کردن موجودی"""
        member_id = self.member_combo.currentData()
        book_id = self.book_combo.currentData()

        if member_id is None:
            QMessageBox.warning(
                self,
                "عضو وجود ندارد",
                "برای ثبت امانت، ابتدا حداقل یک عضو ثبت کنید."
            )
            return

        if book_id is None:
            QMessageBox.warning(
                self,
                "کتاب موجود نیست",
                "برای ثبت امانت، ابتدا کتابی با نسخه موجود ثبت کنید."
            )
            return

        # بررسی دوباره موجودی کتاب از دیتابیس
        book = database.fetch_one(
            "SELECT title, available_copies FROM books WHERE id = ?",
            (book_id,)
        )

        if book is None or book["available_copies"] <= 0:
            QMessageBox.warning(
                self,
                "کتاب ناموجود",
                "این کتاب دیگر نسخه قابل امانت ندارد."
            )
            self.load_available_books()
            return

        loan_date = date.today().isoformat()
        due_date = (date.today() + timedelta(days=14)).isoformat()

        # ثبت امانت
        database.execute_query("""
            INSERT INTO loans (
                book_id, member_id, loan_date, due_date, return_date, fine_amount
            )
            VALUES (?, ?, ?, ?, NULL, 0)
        """, (book_id, member_id, loan_date, due_date))

        # کم کردن یک نسخه از موجودی کتاب
        database.execute_query("""
            UPDATE books
            SET available_copies = available_copies - 1
            WHERE id = ?
        """, (book_id,))

        QMessageBox.information(
            self,
            "امانت ثبت شد",
            f"کتاب «{book['title']}» با موفقیت امانت داده شد.\n"
            f"مهلت بازگشت: {due_date}"
        )

        self.load_available_books()
        self.load_loans()

    def load_loans(self):
        """نمایش امانت‌ها در جدول"""
        search_text = self.search_input.text().strip()

        query = """
            SELECT
                loans.id,
                books.title AS book_title,
                members.full_name AS member_name,
                loans.loan_date,
                loans.due_date,
                loans.return_date,
                loans.fine_amount
            FROM loans
            INNER JOIN books ON loans.book_id = books.id
            INNER JOIN members ON loans.member_id = members.id
        """

        parameters = ()

        if search_text != "":
            query += """
                WHERE books.title LIKE ?
                   OR members.full_name LIKE ?
            """

            search_value = f"%{search_text}%"
            parameters = (search_value, search_value)

        query += " ORDER BY loans.id DESC"

        loans = database.fetch_all(query, parameters)

        self.loans_table.setRowCount(0)

        today = date.today()

        for row_index, loan in enumerate(loans):
            self.loans_table.insertRow(row_index)

            if loan["return_date"] is not None:
                status = "بازگشت داده شده"
            else:
                due_date = date.fromisoformat(loan["due_date"])

                if today > due_date:
                    status = "دیرکرد"
                else:
                    status = "در امانت"

            values = [
                str(loan["id"]),
                loan["book_title"],
                loan["member_name"],
                loan["loan_date"],
                loan["due_date"],
                loan["return_date"] or "-",
                status,
                str(loan["fine_amount"]) + " تومان"
            ]

            for column_index, value in enumerate(values):
                item = QTableWidgetItem(value)
                item.setTextAlignment(Qt.AlignCenter)

                # رنگ‌بندی وضعیت‌ها
                if column_index == 6:
                    if status == "دیرکرد":
                        item.setForeground(Qt.red)
                    elif status == "بازگشت داده شده":
                        item.setForeground(Qt.darkGreen)

                self.loans_table.setItem(row_index, column_index, item)

    def return_book(self):
        """ثبت بازگشت کتاب و افزایش موجودی"""
        selected_row = self.loans_table.currentRow()

        if selected_row == -1:
            QMessageBox.warning(
                self,
                "انتخاب امانت",
                "ابتدا یک امانت را از جدول انتخاب کنید."
            )
            return

        loan_id = self.loans_table.item(selected_row, 0).text()

        loan = database.fetch_one("""
            SELECT
                loans.id,
                loans.book_id,
                loans.due_date,
                loans.return_date,
                books.title AS book_title
            FROM loans
            INNER JOIN books ON loans.book_id = books.id
            WHERE loans.id = ?
        """, (loan_id,))

        if loan["return_date"] is not None:
            QMessageBox.warning(
                self,
                "بازگشت قبلی",
                "بازگشت این کتاب قبلاً ثبت شده است."
            )
            return

        answer = QMessageBox.question(
            self,
            "تأیید بازگشت",
            f"آیا کتاب «{loan['book_title']}» بازگشت داده شده است؟",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )

        if answer != QMessageBox.Yes:
            return

        today = date.today()
        due_date = date.fromisoformat(loan["due_date"])

        # جریمه: برای هر روز دیرکرد، 5000 تومان
        fine_amount = 0

        if today > due_date:
            delayed_days = (today - due_date).days
            fine_amount = delayed_days * 5000

        # ثبت تاریخ بازگشت و مبلغ جریمه
        database.execute_query("""
            UPDATE loans
            SET return_date = ?, fine_amount = ?
            WHERE id = ?
        """, (today.isoformat(), fine_amount, loan_id))

        # افزایش موجودی کتاب
        database.execute_query("""
            UPDATE books
            SET available_copies = available_copies + 1
            WHERE id = ?
        """, (loan["book_id"],))

        message = "بازگشت کتاب با موفقیت ثبت شد."

        if fine_amount > 0:
            message += f"\nمبلغ جریمه دیرکرد: {fine_amount} تومان"

        QMessageBox.information(
            self,
            "بازگشت موفق",
            message
        )

        self.load_available_books()
        self.load_loans()


# ==========================================================
# پنجره اصلی نرم‌افزار
# ==========================================================
class MainWindow(QMainWindow):
    def __init__(self, full_name="کاربر"):
        super().__init__()

        self.full_name = full_name

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
        btn_books.clicked.connect(self.open_books_window)
        btn_members.clicked.connect(self.open_members_window)
        btn_loans.clicked.connect(self.open_loans_window)
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

        welcome = QLabel(f"خوش آمدید، {self.full_name} 👋")
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


    def open_books_window(self):
        self.books_window = BooksWindow(self)
        self.books_window.exec_()

    def open_members_window(self):
        self.members_window = MembersWindow(self)
        self.members_window.exec_()

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

        # بررسی خالی نبودن فیلدها
        if username == "" or password == "":
            QMessageBox.warning(
                self,
                "اطلاعات ناقص",
                "لطفاً نام کاربری و رمز عبور را وارد کنید."
            )
            return

        # بررسی نام کاربری و رمز از دیتابیس
        user = database.fetch_one(
            """
            SELECT * FROM users
            WHERE username = ? AND password = ?
            """,
            (username, password)
        )

        # اگر کاربر در دیتابیس پیدا شد
        if user is not None:
            full_name = user["full_name"]

            # نام کاربر را به پنجره اصلی می‌فرستیم
            self.main_window = MainWindow(full_name)
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
    

database.initialize_database()
# ==========================================================
# اجرای برنامه
# ==========================================================
app = QApplication(sys.argv)
app.setLayoutDirection(Qt.RightToLeft)

window = LoginWindow()
window.show()

sys.exit(app.exec_())