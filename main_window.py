from PySide6.QtWidgets import QMainWindow, QWidget, QStackedLayout
from PySide6.QtCore import Slot
from emp_summaryLayout import EmpSummaryLayout
from emp_newLayout import EmpNewLayout
from emp_delLayout import EmpDelLayout
from emp_editSelLayout import EmpEditSelLayout
from emp_editLayout import EmpEditLayout
from emp_payslipSelLayout import EmpPaySlipSelLayout
from company_summaryLayout import CoSummLayout
from employee import Employee

class MainWindow(QMainWindow):
    def __init__(self, app):
        super().__init__()

        # declare instance variable for app
        self.app = app

        # initialise UI
        self.initUI()

        # connect signal from new employee layout when saved
        self.action_file_home.triggered.connect(lambda: self.change_layout(0))
        self.action_emp_summary.triggered.connect(lambda: self.change_layout(1))
        self.action_emp_new.triggered.connect(lambda: self.change_layout(2))
        self.action_emp_delete.triggered.connect(lambda: self.change_layout(3))
        self.action_emp_edit.triggered.connect(lambda: self.change_layout(4))
        self.action_emp_payslip.triggered.connect(lambda: self.change_layout(6))
        self.action_file_quit.triggered.connect(self.action_file_quit_clicked)

    @Slot(Employee, int)
    def change_edit_layout(self, emp, index):
        # remove current emp edit layout
        self.layout_stacked.removeWidget(self.layout_editEmp)
        # insert new layout
        self.layout_editEmp = EmpEditLayout(emp)
        self.layout_stacked.insertWidget(index, self.layout_editEmp)
        # change layout to edit page
        self.layout_stacked.setCurrentIndex(index)
        # connect signal and slot
        self.layout_editEmp.emp_updated.connect(self.empUI)

    @Slot()
    def change_layout(self, index):
        self.layout_stacked.setCurrentIndex(index)

    @Slot()
    def action_file_quit_clicked(self):
        Employee.save_to_db()
        self.app.quit()

    @Slot()
    def empUI(self):
        if self.layout_stacked.count() > 2:
            self.layout_stacked.removeWidget(self.layout_emp_summary)
            self.layout_stacked.removeWidget(self.layout_newEmp)
            self.layout_stacked.removeWidget(self.layout_delEmp)
            self.layout_stacked.removeWidget(self.layout_editSelect)
            self.layout_stacked.removeWidget(self.layout_payslipLayout)

        # add new employment layout to stack - index 1
        self.layout_emp_summary = EmpSummaryLayout()
        self.layout_stacked.insertWidget(1,self.layout_emp_summary)
        # add new employment layout to stack - index 2
        self.layout_newEmp = EmpNewLayout()
        self.layout_stacked.insertWidget(2, self.layout_newEmp)
        # add delete employee layout to stack - index 3
        self.layout_delEmp = EmpDelLayout()
        self.layout_stacked.insertWidget(3, self.layout_delEmp)
        # add edit selection layout to stack - index 4
        self.layout_editSelect = EmpEditSelLayout()
        self.layout_stacked.insertWidget(4, self.layout_editSelect) 
        # add edit employee layout to stack - index 5
        emp = Employee()
        self.layout_editEmp = EmpEditLayout(emp)
        self.layout_stacked.insertWidget(5, self.layout_editEmp)
        # add payslip generator layout to stack - index 6
        self.layout_payslipLayout = EmpPaySlipSelLayout()
        self.layout_stacked.insertWidget(6, self.layout_payslipLayout)
        
        # check for signal from emp_summaryLayout
        self.layout_newEmp.emp_updated.connect(self.empUI)
        self.layout_delEmp.emp_updated.connect(self.empUI)
        self.layout_editEmp.emp_updated.connect(self.empUI)
        self.layout_editSelect.open_edit_layout.connect(self.change_edit_layout)
        
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
        self.layout_stacked.insertWidget(0, self.layout_home)
        # add all employment windows
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
        self.action_emp_new = emp_menu.addAction('New')
        self.action_emp_edit = emp_menu.addAction('Edit')
        self.action_emp_payslip = emp_menu.addAction('Generate payslip')
        self.action_emp_delete = emp_menu.addAction('Delete')

    # define close event
    # save changes to employees.txt before closing app
    def closeEvent(self, event):
        Employee.save_to_db()
        event.accept()