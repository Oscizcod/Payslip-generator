from PySide6.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QLabel, QStackedLayout, QFormLayout, QLineEdit
from payment_summaryLayout import PaymentInvoiceLayout
from PySide6.QtCore import Slot

class MainWindow(QMainWindow):
    def __init__(self, app):
        super().__init__()

        # declare instance variable for app
        self.app = app
        
        # set window title
        self.setWindowTitle('Payslip generator')

         # define generic widget to display main layout
        layout_main = QVBoxLayout()
        self.widget = QWidget()
        self.widget.setLayout(layout_main)
        self.setCentralWidget(self.widget)

        # define home page layout
        self.layout_home_page = QWidget()
        self.layout_home_page.setLayout(QVBoxLayout())
        label_homePage_title = QLabel()
        label_homePage_title.setText('Klinik Muru Employees')
        self.layout_home_page.layout().addWidget(label_homePage_title)

        # define stacked layout
        self.layout_stacked = QStackedLayout()
        # add home page layout to stack - index 0
        self.layout_stacked.addWidget(self.layout_home_page)
        # add payment summary layout to stack - index 1
        self.layout_pay_summary = PaymentInvoiceLayout()
        self.layout_stacked.addWidget(self.layout_pay_summary)

        # add stacked layout to main layout
        layout_main.addLayout(self.layout_stacked) 
        self.layout_stacked.setCurrentIndex(0)

        # set up our menu bar
        main_menu = self.menuBar()
        file_menu = main_menu.addMenu('File')
        action_file_home = file_menu.addAction('Home')
        action_file_quit = file_menu.addAction('Quit')

        emp_menu = main_menu.addMenu('Employees')

        payment_menu = main_menu.addMenu('Payment')
        action_pay_summary = payment_menu.addAction('Summary')
        

        action_file_home.triggered.connect(lambda: self.change_layout(0))
        action_file_quit.triggered.connect(self.action_file_quit_clicked)
        action_pay_summary.triggered.connect(lambda: self.change_layout(1))

    @Slot()
    def change_layout(self, index):
        self.layout_stacked.setCurrentIndex(index)

    def action_file_quit_clicked(self):
        self.app.quit()

        