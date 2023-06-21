from PySide6.QtWidgets import QApplication, QPushButton
import sys
from main_window import MainWindow

# initialise the event loop listener
app = QApplication(sys.argv)

main_window = MainWindow(app)
main_window.show()

app.exec()
