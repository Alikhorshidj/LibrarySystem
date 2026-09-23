# 📚 Library Management System

A desktop-based Library Management System developed with **Python**, **PyQt5**, and **SQLite**.

This application provides a Persian graphical user interface for managing library books, members, loans, returns, late fines, reports, and database backups.

---

## ✨ Features

- User login interface
- Persian graphical user interface
- Dashboard with real-time statistics
- Add, edit, delete, and search books
- Add, edit, delete, and search members
- Prevent duplicate national codes
- Book loan and return management
- Automatic update of available book copies
- Late return fine calculation
- Active loans and fines reports
- SQLite database backup support
- Windows executable build support

---

## 🛠 Technologies Used

- **Python**
- **PyQt5**
- **SQLite**
- **PyInstaller**
- **Visual Studio Code**

---

## 📁 Project Structure

```text
LibrarySystem/
│
├── main.py
├── database.py
├── library.db
├── README.md
└── requirements.txt
```

---

## ▶️ How to Run

### 1. Clone the repository

```bash
git clone https://github.com/YOUR-USERNAME/LibrarySystem.git
```

### 2. Open the project folder

```bash
cd LibrarySystem
```

### 3. Install dependencies

```bash
pip install PyQt5
```

### 4. Run the application

```bash
python main.py
```

---

## 🗄 Database

All application data is stored locally in the SQLite database file:

```text
library.db
```

The database includes the following main tables:

- `books`
- `members`
- `loans`
- `categories`

---

## 📦 Build Windows Executable

Install PyInstaller:

```bash
pip install pyinstaller
```

Then run:

```bash
python -m PyInstaller --noconsole --onedir --clean --name LibrarySystem --add-data "library.db;." main.py
```

The executable file will be created in:

```text
dist/LibrarySystem/
```

Run the program by opening:

```text
LibrarySystem.exe
```

> Note: To run the application on another computer, copy the entire `dist/LibrarySystem` folder, not only the `.exe` file.

---

## 👨‍💻 Developer

Developed as a university programming project using Python.

---

## 📄 License

This project is created for educational purposes.
