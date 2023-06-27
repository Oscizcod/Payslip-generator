from PySide6.QtWidgets import QApplication
import sys
from main_window import MainWindow
from employee import Employee

# initialise the event loop listener
app = QApplication(sys.argv)

# load employees from file db
Employee.load_employees()

# initialise main window and show
main_window = MainWindow(app)
main_window.show()

# start event loop listener
app.exec()
