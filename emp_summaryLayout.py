from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QHBoxLayout, QButtonGroup, QRadioButton
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
        btn_new_emp.setText('New')
        btn_new_emp.clicked.connect(self.btn_new_emp_clicked)
        # edit btn to edit existing employees details
        btn_edit_emp = QPushButton()
        btn_edit_emp.setText('Edit')
        # set to disabled by default
        btn_edit_emp.setEnabled(False)
        btn_edit_emp.clicked.connect(self.btn_edit_emp_clicked)
        
        # check if employees.txt exists or if empty
        if len(Employee.get_employees()) != 0:
            # title of layout
            self.label_top.setText('Employee summary: ')
            layout_top_level.addWidget(self.label_top)

            # create group for radio buttons
            group_btns_emps = QButtonGroup(self)
            group_btns_emps.setExclusive(True)

            for id, emp in Employee.get_employees().items():
                # radio button - add to group
                btn_radio_emp = QRadioButton()
                group_btns_emps.addButton(btn_radio_emp, int(id))
                # label
                label_emp = QLabel()
                label_emp.setText(emp.__str__())
                # add label and btn to layout
                layout_emp = QHBoxLayout()
                layout_emp.addWidget(btn_radio_emp)
                layout_emp.addWidget(label_emp)
                # append to top layout
                layout_top_level.addLayout(layout_emp)
        else:
            self.label_top.setText('No employees registered.')
            layout_top_level.addWidget(self.label_top)

        # horizontal layout for buttons
        layout_btns = QHBoxLayout()
        layout_btns.addWidget(btn_new_emp)
        layout_btns.addWidget(btn_edit_emp)
        layout_top_level.addLayout(layout_btns)
        self.setLayout(layout_top_level)

        # initialise emp_newLayout
        self.dialog_new_emp = EmpNewLayout(self)
        # connect file_updated signal to custom slot
        self.dialog_new_emp.file_updated.connect(self.update_layout)
        
    @Slot()
    def btn_new_emp_clicked(self):
        self.dialog_new_emp.exec()

    @Slot()
    def btn_edit_emp_clicked(self):
        pass

    @Slot()
    def update_layout(self):
        # emit custom signal for main_window.py
        self.update_emp_summ_layout.emit()
