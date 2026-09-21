# db.py  --  لایه دسترسی به داده (Data Access Layer)
# db.py  --  لایه دسترسی به داده (Data Access Layer)
import sqlite3
import os
import sys

# مسیر دیتابیس را همیشه کنار فایل برنامه قرار می‌دهیم
if getattr(sys, "frozen", False):          # حالت exe
    BASE_DIR = os.path.dirname(sys.executable)
else:                                      # حالت اجرای معمولی
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

DB_NAME = os.path.join(BASE_DIR, "library.db")



def get_connection():
    """ساخت اتصال به دیتابیس SQLite"""
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row      # دسترسی به ستون‌ها با نام، نه شماره
    conn.execute("PRAGMA foreign_keys = ON")   # فعال‌سازی کلید خارجی
    return conn


def execute(query, params=()):
    """اجرای دستورات نوشتنی: INSERT / UPDATE / DELETE"""
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(query, params)
    conn.commit()
    last_id = cur.lastrowid
    conn.close()
    return last_id


def fetch_all(query, params=()):
    """خواندن چند رکورد"""
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(query, params)
    rows = cur.fetchall()
    conn.close()
    return rows


def fetch_one(query, params=()):
    """خواندن یک رکورد"""
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(query, params)
    row = cur.fetchone()
    conn.close()
    return row


# ---------------------------------------------------------------
#                      ساخت جداول
# ---------------------------------------------------------------
def create_tables():
    conn = get_connection()
    cur = conn.cursor()

    cur.executescript("""
    CREATE TABLE IF NOT EXISTS Users (
        UserID   INTEGER PRIMARY KEY AUTOINCREMENT,
        Username TEXT NOT NULL UNIQUE,
        Password TEXT NOT NULL,
        FullName TEXT NOT NULL
    );

    CREATE TABLE IF NOT EXISTS Categories (
        CategoryID INTEGER PRIMARY KEY AUTOINCREMENT,
        Name       TEXT NOT NULL
    );

    CREATE TABLE IF NOT EXISTS Books (
        BookID          INTEGER PRIMARY KEY AUTOINCREMENT,
        Title           TEXT NOT NULL,
        Author          TEXT NOT NULL,
        Publisher       TEXT,
        ISBN            TEXT,
        CategoryID      INTEGER,
        TotalCopies     INTEGER NOT NULL DEFAULT 1,
        AvailableCopies INTEGER NOT NULL DEFAULT 1,
        FOREIGN KEY (CategoryID) REFERENCES Categories(CategoryID)
    );

    CREATE TABLE IF NOT EXISTS Members (
        MemberID     INTEGER PRIMARY KEY AUTOINCREMENT,
        FullName     TEXT NOT NULL,
        NationalCode TEXT,
        Phone        TEXT,
        Email        TEXT,
        RegisterDate TEXT NOT NULL
    );

    CREATE TABLE IF NOT EXISTS Loans (
        LoanID     INTEGER PRIMARY KEY AUTOINCREMENT,
        BookID     INTEGER NOT NULL,
        MemberID   INTEGER NOT NULL,
        LoanDate   TEXT NOT NULL,
        DueDate    TEXT NOT NULL,
        ReturnDate TEXT,                    -- NULL یعنی هنوز برنگشته
        FineAmount INTEGER NOT NULL DEFAULT 0,
        FOREIGN KEY (BookID)   REFERENCES Books(BookID),
        FOREIGN KEY (MemberID) REFERENCES Members(MemberID)
    );
    """)

    conn.commit()
    conn.close()


# ---------------------------------------------------------------
#                      داده‌های نمونه
# ---------------------------------------------------------------
def seed_data():
    # اگر کاربری وجود دارد، یعنی قبلاً پر شده
    if fetch_one("SELECT COUNT(*) AS c FROM Users")["c"] > 0:
        return

    execute("INSERT INTO Users (Username, Password, FullName) VALUES (?,?,?)",
            ("admin", "1234", "مدیر سیستم"))

    cats = ["رمان", "علمی", "تاریخی", "کامپیوتر", "کودک"]
    for c in cats:
        execute("INSERT INTO Categories (Name) VALUES (?)", (c,))

    books = [
        ("بوف کور",        "صادق هدایت",        "امیرکبیر",   "9789640000001", 1, 3, 3),
        ("کلیدر",          "محمود دولت‌آبادی",  "فرهنگ معاصر", "9789640000002", 1, 2, 2),
        ("تاریخ بیهقی",    "ابوالفضل بیهقی",    "سمت",        "9789640000003", 3, 2, 2),
        ("ساختمان داده",   "حسین ابراهیم‌زاده", "نص",          "9789640000004", 4, 4, 4),
        ("مبانی کامپیوتر", "علی مرادی",         "دانش‌پژوه",   "9789640000005", 4, 3, 3),
        ("شاهنامه",        "ابوالقاسم فردوسی",  "قطره",        "9789640000006", 1, 2, 2),
        ("کیهان‌شناسی",    "مریم حسینی",        "نو",          "9789640000007", 2, 1, 1),
    ]
    for b in books:
        execute("""INSERT INTO Books
                   (Title, Author, Publisher, ISBN, CategoryID, TotalCopies, AvailableCopies)
                   VALUES (?,?,?,?,?,?,?)""", b)

    members = [
        ("رضا احمدی",  "0012345678", "09121112233", "reza@mail.com",     "1405/06/01"),
        ("سارا کریمی", "0023456789", "09122223344", "sara@mail.com",     "1405/06/05"),
        ("محمد رضایی", "0034567890", "09123334455", "mohammad@mail.com", "1405/06/10"),
    ]
    for m in members:
        execute("""INSERT INTO Members
                   (FullName, NationalCode, Phone, Email, RegisterDate)
                   VALUES (?,?,?,?,?)""", m)


def init_db():
    """ساخت دیتابیس و پر کردن داده‌های اولیه"""
    create_tables()
    seed_data()


# تست مستقل این فایل
if __name__ == "__main__":
    init_db()
    print("✅ دیتابیس ساخته شد:", os.path.abspath(DB_NAME))
    print("تعداد کتاب‌ها:", fetch_one("SELECT COUNT(*) AS c FROM Books")["c"])