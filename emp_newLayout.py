from PySide6.QtWidgets import QVBoxLayout, QLabel, QWidget, QFormLayout, QLineEdit, QPushButton, QHBoxLayout, QDialog
from PySide6.QtCore import Slot

class EmpNewLayout(QDialog):
    def __init__(self, widget):
        super().__init__(widget)

        # Label for instruction
        label_instruction = QLabel()
        label_instruction.setText('Please fill in the following details for the new employee:')

        # use form to fill out details
        form_emp_new = QFormLayout()
        edit_full_name = QLineEdit()
        form_emp_new.addRow('Full name: ', edit_full_name)
        edit_biometric_name = QLineEdit()
        form_emp_new.addRow('Biometric name: ', edit_biometric_name)
        edit_nric = QLineEdit()
        form_emp_new.addRow('NRIC: ', edit_nric)

        # add form submission buttons
        btn_ok = QPushButton()
        btn_ok.setText('OK')
        btn_ok.clicked.connect(self.btn_ok_clicked)
        btn_cancel = QPushButton()
        btn_cancel.setText('Cancel')
        btn_cancel.clicked.connect(self.btn_cancel_clicked)
        layout_btns = QHBoxLayout()
        layout_btns.addWidget(btn_ok)
        layout_btns.addWidget(btn_cancel)

        # construct final layout
        self.setWindowTitle('Add new employee')
        self.setLayout(QVBoxLayout())
        self.layout().addWidget(label_instruction)
        self.layout().addLayout(form_emp_new)
        self.layout().addLayout(layout_btns)
        
    # slot for ok btn
    @Slot()
    def btn_ok_clicked(self):
        pass
        
    # slot for cancel btn
    @Slot()
    def btn_cancel_clicked(self):
        pass