from PySide6.QtWidgets import QVBoxLayout, QLabel, QFormLayout, QLineEdit, QPushButton, QHBoxLayout, QDialog, QMessageBox
from PySide6.QtGui import QRegularExpressionValidator
from PySide6.QtCore import Slot, Signal
from employee import Employee

class EmpNewLayout(QDialog):
    # create custom signal
    file_updated = Signal()

    def __init__(self, widget):
        super().__init__(widget)

        # Label for instruction
        label_instruction = QLabel()
        label_instruction.setText('Please fill in the following details for the new employee:')

        # use form to fill out details
        form_emp_new = QFormLayout()
        self.edit_full_name = QLineEdit()
        validate_full_name = QRegularExpressionValidator(r'\D+')
        form_emp_new.addRow('Full name: ', self.edit_full_name)
        self.edit_full_name.setValidator(validate_full_name)
        
        self. edit_biometric_name = QLineEdit()
        validate_biometric_name = QRegularExpressionValidator(r'.+')
        form_emp_new.addRow('Biometric name: ', self.edit_biometric_name)
        self.edit_biometric_name.setPlaceholderText('Enter name exactly as in biometric device')
        self.edit_biometric_name.setValidator(validate_biometric_name)
        
        self.edit_nric = QLineEdit()
        validate_nric = QRegularExpressionValidator(r'\d{6}-\d{2}-\d{4}')
        form_emp_new.addRow('NRIC: ', self.edit_nric)
        self.edit_nric.setPlaceholderText('E.g. 931102-03-2398')
        self.edit_nric.setValidator(validate_nric)

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
        # details all validated, save to text file
        if self.edit_full_name.hasAcceptableInput():
            if self.edit_biometric_name.hasAcceptableInput():
                if self.edit_nric.hasAcceptableInput():
                    # check if duplicate entry (nric is unique)
                    if self.edit_nric.text() not in Employee.employees:
                        # add employee to existing dictionary of employees
                        Employee.employees[self.edit_nric.text()] = (self.edit_full_name.text().upper(), self.edit_biometric_name.text())

                        # save employee to file-based db
                        with open('employees.txt', 'a', encoding='utf-8') as f:
                            f.write('{};{};{}\n'.format(self.edit_full_name.text().upper(), self.edit_biometric_name.text(), self.edit_nric.text()))
                        
                        # emit signal
                        self.file_updated.emit()

                        # close dialog
                        self.done(0)
                    else:
                        QMessageBox.critical(self, "Input Error",
                               'You already have another staff with identical NRIC.\n' +
                               'Please check that your entries are correct.',
                               QMessageBox.Ok)
                else:
                    QMessageBox.critical(self, "Input Error",
                               "Please fill in the NRIC in the correct format.\n" +
                               "XXXXXX-XX-XXXX",
                               QMessageBox.Ok)
            else:
                QMessageBox.critical(self, "Input Error",
                               "Please fill in the biometric name.",
                               QMessageBox.Ok)
        else:
            QMessageBox.critical(self, "Input Error",
                               "Please fill in the full name.",
                               QMessageBox.Ok)
        
    # slot for cancel btn
    @Slot()
    def btn_cancel_clicked(self):
        # close dialog
        self.done(0)
