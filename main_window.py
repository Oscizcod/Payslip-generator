from PySide6.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QLabel, QStackedLayout
from emp_summaryLayout import EmpSummaryLayout
from PySide6.QtCore import Slot
import os

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
        # # add new employment layout to stack - index 1
        self.create_emp_summ_layout()

        # add stacked layout to main layout
        layout_main.addLayout(self.layout_stacked) 
        self.layout_stacked.setCurrentIndex(0)

        # set up our menu bar
        main_menu = self.menuBar()
        file_menu = main_menu.addMenu('File')
        action_file_home = file_menu.addAction('Home')
        action_file_quit = file_menu.addAction('Quit')

        emp_menu = main_menu.addMenu('Employees')
        action_emp_summary = emp_menu.addAction('Summary')
        
        # slots for menu actions
        action_file_home.triggered.connect(lambda: self.change_layout(0))
        action_emp_summary.triggered.connect(lambda: self.change_layout(1))
        action_file_quit.triggered.connect(self.action_file_quit_clicked)

    @Slot()
    def change_layout(self, index):
        self.layout_stacked.setCurrentIndex(index)

    @Slot()
    def action_file_quit_clicked(self):
        self.app.quit()

    @Slot()
    def create_emp_summ_layout(self):
        if self.layout_stacked.count() > 2:
            self.layout_stacked.removeWidget(self.layout_emp_summary)

        # add new employment layout to stack - index 1
        self.layout_emp_summary = EmpSummaryLayout()
        self.layout_stacked.insertWidget(1,self.layout_emp_summary)
        
        # check for signal from emp_summaryLayout
        self.layout_emp_summary.update_emp_summ_layout.connect(self.create_emp_summ_layout)
        
        # set stacked layout to employees summary page 
        self.layout_stacked.setCurrentIndex(1)

