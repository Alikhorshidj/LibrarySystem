import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout
from PyQt5.QtCore import Qt


app = QApplication(sys.argv)

window = QWidget()
window.setWindowTitle("سیستم مدیریت کتابخانه")
window.resize(500, 300)

label = QLabel("پنجره برنامه با موفقیت اجرا شد ✅")
label.setAlignment(Qt.AlignCenter)
label.setStyleSheet("""
    font-size: 20px;
    font-weight: bold;
    color: #1a3b5c;
""")

layout = QVBoxLayout()
layout.addWidget(label)

window.setLayout(layout)
window.show()

sys.exit(app.exec_())