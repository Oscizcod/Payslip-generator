from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QHBoxLayout
from PySide6.QtCore import Slot, Signal
import os
from emp_newLayout import EmpNewLayout
from emp_selectLayout import EmpSelectLayout
from employee import Employee

class EmpSummaryLayout(QWidget):
    # create custom signal to update layout
    update_emp_summ_layout = Signal()

    def __init__(self):
        super().__init__()

        self.initUI()

        # initialise layouts
        self.dialog_new_emp = EmpNewLayout(self)
        self.select_dialog = EmpSelectLayout()
        # connect file_updated signal to custom slot
        self.select_dialog.emp_updated.connect(self.update_layout)
        self.dialog_new_emp.emp_updated.connect(self.update_layout)
        self.btn_new_emp.clicked.connect(self.btn_new_emp_clicked)
        self.btn_select_emp.clicked.connect(self.btn_select_emp_clicked)

    def initUI(self):
        # inputs and labels
        self.label_top = QLabel()  # displayed at top of page
        self.btn_new_emp = QPushButton()
        self.btn_new_emp.setText('New')
        # edit btn 
        self.btn_select_emp = QPushButton()
        self.btn_select_emp.setText('Select')
        
        # layout for summary page
        layout_top_level = QVBoxLayout()
        # check how many emps registered
        if len(Employee.get_employees()) != 0:
            # title of layout
            self.label_top.setText('Employee summary: ')
            layout_top_level.addWidget(self.label_top)

            for id, emp in Employee.get_employees().items():
                # label
                label_emp = QLabel()
                label_emp.setText(emp.__str__())
                # append to top layout
                layout_top_level.addWidget(label_emp)
        else:
            self.label_top.setText('No employees registered.')
            layout_top_level.addWidget(self.label_top)

        # horizontal layout for buttons
        layout_btns = QHBoxLayout()
        layout_btns.addWidget(self.btn_new_emp)
        layout_btns.addWidget(self.btn_select_emp)
        layout_top_level.addLayout(layout_btns)
        self.setLayout(layout_top_level)

    @Slot()
    def btn_select_emp_clicked(self):
        self.select_dialog.setWindowTitle('Select Employee')
        self.select_dialog.exec()
        
    @Slot()
    def btn_new_emp_clicked(self):
        self.dialog_new_emp.exec()

    @Slot()
    def update_layout(self):
        # emit custom signal for main_window.py
        self.update_emp_summ_layout.emit()
