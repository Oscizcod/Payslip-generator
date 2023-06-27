from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton
import os.path
import os
from emp_newLayout import EmpNewLayout
from PySide6.QtCore import Slot

class EmpSummaryLayout(QWidget):
    def __init__(self):
        super().__init__()

        # layout for summary page
        layout_top_level = QVBoxLayout()
        # label if no employees registered
        label_top = QLabel()
        btn_new_emp = QPushButton()
        btn_new_emp.setText('New')
        btn_new_emp.clicked.connect(self.btn_new_emp_clicked)
        
        # check if employees.txt exists or if empty
        if os.path.exists('employees.txt') and os.stat('employees.txt').st_size != 0:
            label_top.setText('Employee summary: ')
        else:
            label_top.setText('No employees registered.')

        layout_top_level.addWidget(label_top)
        layout_top_level.addWidget(btn_new_emp)
        self.setLayout(layout_top_level)

    @Slot()
    def btn_new_emp_clicked(self):
        dialog_new_emp = EmpNewLayout(self)
        dialog_new_emp.exec()
