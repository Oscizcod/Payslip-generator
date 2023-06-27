from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QHBoxLayout
import os.path
import os
from emp_newLayout import EmpNewLayout
from employee import Employee
from PySide6.QtCore import Slot, Signal

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
        btn_new_emp.setText('New')
        btn_new_emp.clicked.connect(self.btn_new_emp_clicked)
        
        # check if employees.txt exists or if empty
        if os.path.exists('employees.txt') and os.stat('employees.txt').st_size != 0:
            self.label_top.setText('Employee summary: ')
            layout_top_level.addWidget(self.label_top)

            with open('employees.txt', 'r', encoding='utf-8') as emps:
                for emp in emps:
                    emp_details = emp.split(';')

                    # create employee object
                    obj_emp = Employee(emp_details[0], emp_details[1], emp_details[2].strip())
                    label_emp = QLabel()
                    label_emp.setText(obj_emp.__str__())
                    
                    # create horizontal layout for emp details
                    layout_emp_details = QHBoxLayout()
                    layout_emp_details.addWidget(label_emp)

                    # add buttons for each employee
                    layout_emp_btns = QVBoxLayout()
                    btn_emp_edit = QPushButton()
                    btn_emp_edit.setText('Edit')
                    btn_emp_remove = QPushButton()
                    btn_emp_remove.setText('Remove')

                    layout_emp_btns.addWidget(btn_emp_edit)
                    layout_emp_btns.addWidget(btn_emp_remove)
                    layout_emp_details.addLayout(layout_emp_btns)
                    layout_top_level.addLayout(layout_emp_details)
                    
        else:
            self.label_top.setText('No employees registered.')
            layout_top_level.addWidget(self.label_top)


        layout_top_level.addWidget(btn_new_emp)
        self.setLayout(layout_top_level)

        # initialise emp_newLayout
        self.dialog_new_emp = EmpNewLayout(self)
        # connect file_created signal to custom slot
        self.dialog_new_emp.file_updated.connect(self.update_layout)
        
    @Slot()
    def btn_new_emp_clicked(self):
        self.dialog_new_emp.exec()

    @Slot()
    def update_layout(self):
        # emit custom signal for main_window.py
        self.update_emp_summ_layout.emit()
