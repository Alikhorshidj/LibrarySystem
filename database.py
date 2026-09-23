import sqlite3
import sys
from pathlib import Path


# اگر برنامه به exe تبدیل شده باشد، دیتابیس کنار فایل exe قرار می‌گیرد.
# در حالت اجرای عادی پایتون نیز کنار فایل database.py خواهد بود.
if getattr(sys, "frozen", False):
    BASE_DIR = Path(sys.executable).resolve().parent
else:
    BASE_DIR = Path(__file__).resolve().parent

DB_NAME = BASE_DIR / "library.db"

# # فایل دیتابیس در همان پوشه پروژه ساخته می‌شود
# BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# DATABASE_FILE = os.path.join(BASE_DIR, "library.db")


def get_connection():
    """ایجاد اتصال به دیتابیس"""
    connection = sqlite3.connect(str(DB_NAME))
    connection.row_factory = sqlite3.Row
    return connection


def initialize_database():
    """
    ساخت جدول‌های برنامه در اولین اجرا.
    اگر جدول‌ها قبلاً وجود داشته باشند، دوباره ساخته نمی‌شوند.
    """

    connection = get_connection()
    cursor = connection.cursor()

    # جدول کاربران
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL,
            full_name TEXT NOT NULL
        )
    """)

    # جدول دسته‌بندی کتاب‌ها
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS categories (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL UNIQUE
        )
    """)

    # جدول کتاب‌ها
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS books (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            author TEXT NOT NULL,
            publisher TEXT,
            isbn TEXT,
            category_id INTEGER,
            total_copies INTEGER NOT NULL DEFAULT 1,
            available_copies INTEGER NOT NULL DEFAULT 1,

            FOREIGN KEY (category_id) REFERENCES categories(id)
        )
    """)

    # جدول اعضای کتابخانه
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS members (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            full_name TEXT NOT NULL,
            national_code TEXT,
            phone TEXT,
            email TEXT,
            register_date TEXT NOT NULL
        )
    """)

    # جدول امانت کتاب
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS loans (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            book_id INTEGER NOT NULL,
            member_id INTEGER NOT NULL,
            loan_date TEXT NOT NULL,
            due_date TEXT NOT NULL,
            return_date TEXT,
            fine_amount INTEGER NOT NULL DEFAULT 0,

            FOREIGN KEY (book_id) REFERENCES books(id),
            FOREIGN KEY (member_id) REFERENCES members(id)
        )
    """)

    # ---------- ایجاد کاربر اولیه ----------
    cursor.execute("SELECT COUNT(*) FROM users")
    users_count = cursor.fetchone()[0]

    if users_count == 0:
        cursor.execute("""
            INSERT INTO users (username, password, full_name)
            VALUES (?, ?, ?)
        """, ("admin", "1234", "مدیر سیستم"))

    # ---------- ایجاد دسته‌بندی‌های اولیه ----------
    cursor.execute("SELECT COUNT(*) FROM categories")
    categories_count = cursor.fetchone()[0]

    if categories_count == 0:
        categories = [
            ("رمان",),
            ("علمی",),
            ("تاریخی",),
            ("کامپیوتر",),
            ("کودک",)
        ]

        cursor.executemany(
            "INSERT INTO categories (name) VALUES (?)",
            categories
        )

    connection.commit()
    connection.close()


def fetch_all(query, parameters=()):
    """گرفتن چند ردیف از دیتابیس"""
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(query, parameters)
    rows = cursor.fetchall()

    connection.close()
    return rows


def fetch_one(query, parameters=()):
    """گرفتن یک ردیف از دیتابیس"""
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(query, parameters)
    row = cursor.fetchone()

    connection.close()
    return row


def execute_query(query, parameters=()):
    """اجرای دستورهای INSERT / UPDATE / DELETE"""
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(query, parameters)
    connection.commit()

    last_id = cursor.lastrowid
    connection.close()

    return last_id


# این بخش فقط زمانی اجرا می‌شود که مستقیم database.py را اجرا کنی
if __name__ == "__main__":
    initialize_database()

    print("دیتابیس با موفقیت ساخته شد.")
    print("مسیر دیتابیس:")
    print(DATABASE_FILE)