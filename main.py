from PySide6.QtWidgets import QApplication
import sys
from main_window import MainWindow

# initialise the event loop listener
app = QApplication(sys.argv)
# initialise main window and show
main_window = MainWindow(app)
main_window.show()

# start event loop listener
app.exec()
