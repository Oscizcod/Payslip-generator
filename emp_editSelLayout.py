from PySide6.QtWidgets import QWidget, QLabel, QComboBox, QPushButton, QVBoxLayout, QHBoxLayout
from PySide6.QtCore import Slot, Signal
from employee import Employee


class EmpEditSelLayout(QWidget):
    # create custom signal
    open_edit_layout = Signal(Employee, int)

    def __init__(self):
        super().__init__()
        
        self.initUI()

        # slots and signals
        self.btn_edit.clicked.connect(self.btn_edit_clicked)

    def initUI(self):
        # inputs and labels
        label_select_emp = QLabel()
        label_select_emp.setText('Select employee to edit: ')
        self.combo_select_emp = QComboBox()
        self.combo_select_emp.addItems(self.get_combo_list())
        self.btn_edit = QPushButton()
        self.btn_edit.setText('Edit')

        # layouts
        layout_top = QVBoxLayout()
        layout_select = QHBoxLayout()
        layout_select.addWidget(label_select_emp)
        layout_select.addWidget(self.combo_select_emp)
        layout_top.addLayout(layout_select)
        layout_top.addWidget(self.btn_edit)
        self.setLayout(layout_top)

    def get_combo_list(self):
        combo_list = []

        for emp_id, emp in Employee.get_employees().items():
            combo_list.append('{} ({})'.format(emp.get_full_name(), emp_id))

        return combo_list

    @Slot()
    def btn_edit_clicked(self):
        # get employee that was selected
        emp_id = self.combo_select_emp.currentText()[-3:-1]

        self.open_edit_layout.emit(Employee.get_employees()[emp_id],5)
