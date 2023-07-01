from PySide6.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QLabel, QStackedLayout, QGroupBox, QHBoxLayout
from PySide6.QtCore import Slot
from emp_summaryLayout import EmpSummaryLayout
from company_summaryLayout import CoSummLayout
from company import Company

class MainWindow(QMainWindow):
    def __init__(self, app):
        super().__init__()

        # declare instance variable for app
        self.app = app

        # initialise UI
        self.initUI()
        
        # connect signals to slots
        self.action_file_home.triggered.connect(lambda: self.change_layout(0))
        self.action_emp_summary.triggered.connect(lambda: self.change_layout(1))
        self.action_file_quit.triggered.connect(self.action_file_quit_clicked)

    @Slot()
    def change_layout(self, index):
        self.layout_stacked.setCurrentIndex(index)

    @Slot()
    def action_file_quit_clicked(self):
        self.app.quit()

    @Slot()
    def empUI(self):
        if self.layout_stacked.count() > 2:
            self.layout_stacked.removeWidget(self.layout_emp_summary)

        # add new employment layout to stack - index 1
        self.layout_emp_summary = EmpSummaryLayout()
        self.layout_stacked.insertWidget(1,self.layout_emp_summary)
        
        # check for signal from emp_summaryLayout
        self.layout_emp_summary.update_emp_summ_layout.connect(self.empUI)
        
        # set stacked layout to employees summary page 
        self.layout_stacked.setCurrentIndex(1)

    def initUI(self):
        # set window title
        self.setWindowTitle('Payslip Generator')

        # set menu bar
        self.menu_bar()

        # define stacked layout
        self.layout_stacked = QStackedLayout()
        # add home page layout to stack - index 0
        self.layout_home = CoSummLayout()
        self.layout_stacked.addWidget(self.layout_home)
        # # add new employment layout to stack - index 1
        self.empUI()

        # set central widget and add stacked layout
        widget_central = QWidget()
        self.setCentralWidget(widget_central)
        widget_central.setLayout(self.layout_stacked)
        self.layout_stacked.setCurrentIndex(0)

    def menu_bar(self):    
        # set up our menu bar
        main_menu = self.menuBar()
        file_menu = main_menu.addMenu('File')
        self.action_file_home = file_menu.addAction('Home')
        self.action_file_quit = file_menu.addAction('Quit')
        emp_menu = main_menu.addMenu('Employees')
        self.action_emp_summary = emp_menu.addAction('Summary')
