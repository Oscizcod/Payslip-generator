from PySide6.QtWidgets import QMainWindow

class MainWindow(QMainWindow):
    def __init__(self, app):
        super().__init__()

        # declare instance variable for app
        self.app = app
        
        # set window title
        self.setWindowTitle('Payslip generator')

        # set up our menu bar
        main_menu = self.menuBar()
        emp_menu = main_menu.addMenu('Employees')
        file_menu = main_menu.addMenu('Payment')
