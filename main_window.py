from PySide6.QtWidgets import QMainWindow, QWidget, QGridLayout, QLabel, QPushButton, QHBoxLayout, QVBoxLayout
from payment_mainLayout import PaymentLayout

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

        payment_menu = main_menu.addMenu('Payment')
        action_pay_summary = payment_menu.addAction('Summary')
        action_pay_summary.triggered.connect(self.payment_action_clicked)

        self.widget = QWidget()
        self.setCentralWidget(self.widget)

    def change_layout(self, new_layout):
        self.widget.setLayout(new_layout)

    def add_emp(self):
        pass

    def payment_action_clicked(self):
        payment_mainLayout = PaymentLayout()
        self.change_layout(payment_mainLayout)


        