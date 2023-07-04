from PySide6.QtWidgets import QWidget, QLabel, QComboBox, QPushButton, QVBoxLayout, QHBoxLayout
from PySide6.QtCore import Slot, Signal
from employee import Employee



class EmpDelLayout(QWidget):
    # create custom signal
    emp_updated = Signal()

    def __init__(self):
        super().__init__()
        
        self.initUI()

        # slots and signals
        self.btn_del.clicked.connect(self.btn_del_clicked)

    def initUI(self):
        # inputs and labels
        label_select_emp = QLabel()
        label_select_emp.setText('Select employee: ')
        self.combo_select_emp = QComboBox()
        self.combo_select_emp.addItems(self.get_combo_list())
        self.btn_del = QPushButton()
        self.btn_del.setText('Delete')

        # layouts
        layout_top = QVBoxLayout()
        layout_select = QHBoxLayout()
        layout_select.addWidget(label_select_emp)
        layout_select.addWidget(self.combo_select_emp)
        layout_top.addLayout(layout_select)
        layout_top.addWidget(self.btn_del)
        self.setLayout(layout_top)

    def get_combo_list(self):
        combo_list = []

        for id, emp in Employee.get_employees().items():
            combo_list.append('{} ({})'.format(emp.get_full_name(), id))

        return combo_list

    @Slot()
    def btn_del_clicked(self):
        # extract id from combobox text
        id = self.combo_select_emp.currentText()[-3:-1]

        # delete employee from dict
        del Employee.get_employees()[id]

        # emit signal 
        self.emp_updated.emit()
