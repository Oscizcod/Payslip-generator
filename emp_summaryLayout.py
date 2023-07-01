from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QHBoxLayout
from PySide6.QtCore import Slot, Signal
import os.path
import os
from emp_newLayout import EmpNewLayout
from employee import Employee

class EmpSummaryLayout(QWidget):
    # create custom signal to update layout
    update_emp_summ_layout = Signal()

    def __init__(self):
        super().__init__()

        # layout for summary page
        layout_top_level = QVBoxLayout()
        # label if no employees registered
        self.label_top = QLabel()
        btn_new_emp = QPushButton()
        btn_new_emp.setText('Add new employee')
        btn_new_emp.clicked.connect(self.btn_new_emp_clicked)
        
        # check if employees.txt exists or if empty
        if len(Employee.get_employees()) != 0:
            self.label_top.setText('Employee summary: ')
            layout_top_level.addWidget(self.label_top)

            for emp in Employee.get_employees().values():
                label_emp = QLabel()
                label_emp.setText(emp.__str__())
                # append to top layout
                layout_top_level.addWidget(label_emp)
        else:
            self.label_top.setText('No employees registered.')
            layout_top_level.addWidget(self.label_top)


        layout_top_level.addWidget(btn_new_emp)
        self.setLayout(layout_top_level)

        # initialise emp_newLayout
        self.dialog_new_emp = EmpNewLayout(self)
        # connect file_updated signal to custom slot
        self.dialog_new_emp.file_updated.connect(self.update_layout)
        
    @Slot()
    def btn_new_emp_clicked(self):
        self.dialog_new_emp.exec()

    @Slot()
    def update_layout(self):
        # emit custom signal for main_window.py
        self.update_emp_summ_layout.emit()
