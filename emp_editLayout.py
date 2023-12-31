from PySide6.QtWidgets import QVBoxLayout, QLabel, QFormLayout, QLineEdit, QPushButton, QHBoxLayout, QWidget, QMessageBox, QGroupBox, QCheckBox, QButtonGroup
from PySide6.QtGui import QRegularExpressionValidator, QDoubleValidator
from PySide6.QtCore import Slot, Signal
from employee import Employee
from company import Company


class EmpEditLayout(QWidget):
    # create custom signal
    emp_updated = Signal()

    def __init__(self, emp):
        super().__init__()
        # get all instances from employee
        self.emp_id = emp.get_id()
        self.full_name = emp.get_full_name()
        self.biometric_name = emp.get_biometric_name()
        self.nric = emp.get_nric()
        self.shifts = emp.get_shifts()
        self.base_pay = emp.get_base_pay()
        self.charge_ot = emp.get_charge_ot()
        self.charge_early =emp.get_charge_early()
        self.charge_late = emp.get_charge_late()

        # initialise UI
        self.initUI()

        # connect btn signals to slots
        self.btn_save_emp_details.clicked.connect(self.btn_save_clicked)
        self.edit_base_pay.textEdited.connect(self.base_pay_changed)

    def initUI(self):
        # set window title
        self.setWindowTitle('Add new employee')

        # inputs
        self.btn_save_emp_details = QPushButton()
        self.btn_save_emp_details.setText('Save')

        # define layouts
        # horizontal layout for both btns
        layout_btns = QHBoxLayout()
        layout_btns.addWidget(self.btn_save_emp_details)
        layout_top_main = QVBoxLayout()
        label_instruction = QLabel()
        label_instruction.setText('Please fill in the following details for the new employee:')
        layout_top_main.addWidget(label_instruction)
        layout_top_main.addWidget(self.bioUI())
        layout_top_main.addWidget(self.workingUI())
        layout_top_main.addWidget(self.paymentUI())
        layout_top_main.addLayout(layout_btns)
        self.setLayout(layout_top_main)

    def bioUI(self):
        # add all inputs
        # full name
        self.edit_full_name = QLineEdit()
        validate_full_name = QRegularExpressionValidator(r'\D+')
        self.edit_full_name.setValidator(validate_full_name)
        self.edit_full_name.setText(self.full_name)
        # biometric name
        self.edit_biometric_name = QLineEdit()
        validate_biometric_name = QRegularExpressionValidator(r'.+')
        self.edit_biometric_name.setPlaceholderText('Enter name exactly as in biometric device')
        self.edit_biometric_name.setValidator(validate_biometric_name)
        self.edit_biometric_name.setText(self.biometric_name)
        # nric (unique id)
        self.edit_nric = QLineEdit()
        validate_nric = QRegularExpressionValidator(r'\d{6}-\d{2}-\d{4}')
        self.edit_nric.setPlaceholderText('E.g. 931102-03-2398')
        self.edit_nric.setValidator(validate_nric)
        self.edit_nric.setText(self.nric)

        # add layouts
        frame_bio = QGroupBox('Biodata')
        form_emp_new = QFormLayout()
        form_emp_new.addRow('Full name: ', self.edit_full_name)
        form_emp_new.addRow('Biometric name: ', self.edit_biometric_name)
        form_emp_new.addRow('NRIC: ', self.edit_nric)
        frame_bio.setLayout(form_emp_new)

        return frame_bio

    def paymentUI(self):
        # define all inputs
        # validator for all charges
        validate_charges = QDoubleValidator()
        validate_charges.setRange(0, 9999, 2)
        # base pay 
        self.edit_base_pay = QLineEdit()
        self.edit_base_pay.setValidator(validate_charges)
        self.edit_base_pay.setText(str(self.base_pay))
        # epf
        self.edit_epf_employer = QLineEdit()
        self.edit_epf_employer.setReadOnly(True)
        self.edit_epf_employer.setText(str(round(Company.get_epf_employer() * self.base_pay, 2)))
        self.edit_epf_employee = QLineEdit()
        self.edit_epf_employee.setReadOnly(True)
        self.edit_epf_employee.setText(str(round(Company.get_epf_employee() * self.base_pay, 2)))
        # socso
        self.edit_socso_employer = QLineEdit()
        self.edit_socso_employer.setReadOnly(True)
        self.edit_socso_employer.setText(str(Company.get_socso_employer()))
        self.edit_socso_employee = QLineEdit()
        self.edit_socso_employee.setReadOnly(True)
        self.edit_socso_employee.setText(str(Company.get_socso_employee()))
        # ot
        self.edit_charge_overtime = QLineEdit()
        self.edit_charge_overtime.setValidator(validate_charges)
        self.edit_charge_overtime.setText(str(self.charge_ot))
        # deductions - late arrival/ early dep
        self.edit_charge_late_arr = QLineEdit()
        self.edit_charge_late_arr.setValidator(validate_charges)
        self.edit_charge_late_arr.setText(str(self.charge_late))
        self.edit_charge_early_dep = QLineEdit()
        self.edit_charge_early_dep.setValidator(validate_charges)
        self.edit_charge_early_dep.setText(str(self.charge_early))

        # create layout
        # use form for all inputs
        layout_payment = QFormLayout()
        # base pay
        layout_payment.addRow('Base pay: RM', self.edit_base_pay)
        # epf
        layout_payment.addRow('EPF Employer contribution: RM', self.edit_epf_employer)
        layout_payment.addRow('EPF Employee contribution: RM', self.edit_epf_employee)
        # socso
        layout_payment.addRow('Socso Employer contribution: RM', self.edit_socso_employer)
        layout_payment.addRow('Socso Employee contribution: RM', self.edit_socso_employee)
        # ot / deductions
        layout_payment.addRow('Overtime charges: RM', self.edit_charge_overtime)
        layout_payment.addRow('Late arrival charges: RM', self.edit_charge_late_arr)
        layout_payment.addRow('Early departure charges: RM', self.edit_charge_early_dep)

        # add form to groupbox
        frame_payment = QGroupBox('Payment info')
        frame_payment.setLayout(layout_payment)
        
        return frame_payment

    def workingUI(self):
        # define all inputs
        self.checkbox_shift1 = QCheckBox()
        self.checkbox_shift2 = QCheckBox()
        self.checkbox_shift3 = QCheckBox()
        # add shift 1 and 2 to same group
        self.group_btns = QButtonGroup(self)
        self.group_btns.setExclusive(True)
        self.group_btns.addButton(self.checkbox_shift1, 1)
        self.group_btns.addButton(self.checkbox_shift2, 2)
       
        # create layout
        layout_top_working = QVBoxLayout()
        # put all in a group box with vertical layout
        frame_working = QGroupBox('Working info')
        frame_working.setLayout(layout_top_working)
        label_instruction = QLabel()
        label_instruction.setText('Select one of the shifts below:')
        layout_top_working.addWidget(label_instruction)
        # add horizontal layout for shifts 1 and 2
        layout_shifts12 = QHBoxLayout()
        layout_shifts12.addWidget(self.checkbox_shift1)
        label_shift1 = QLabel()
        label_shift1.setText('Shift 1')
        layout_shifts12.addWidget(label_shift1)
        layout_shifts12.addWidget(self.checkbox_shift2)
        label_shift2 = QLabel()
        label_shift2.setText('Shift 2')
        layout_shifts12.addWidget(label_shift2)
        layout_top_working.addLayout(layout_shifts12)
        # add shift 3
        layout_shift3 = QHBoxLayout()
        label_instruction2 = QLabel()
        label_instruction2.setText('Select if appropriate:')
        layout_shift3.addWidget(self.checkbox_shift3)
        label_shift3 = QLabel()
        label_shift3.setText('Shift 3')
        layout_shift3.addWidget(label_shift3)
        layout_top_working.addWidget(label_instruction2)
        layout_top_working.addLayout(layout_shift3)
        # check the shifts
        self.check_shifts()
        # add layout to frame
        frame_working.setLayout(layout_top_working)

        return frame_working

    # slot for save btn
    @Slot()
    def btn_save_clicked(self):
        # details all validated, save to text file
        if self.is_ready_for_saving() :
            # check if duplicate entry (nric is unique)
            if self.edit_nric.text() not in Employee.employees:
                # determine shifts
                if self.checkbox_shift1.isChecked():
                    shifts = '1'
                else:
                    shifts = '2'

                if self.checkbox_shift3.isChecked():
                    shifts += '3'

                # make necessary changes
                Employee.get_employees()[self.emp_id].set_full_name(self.edit_full_name.text().upper().strip())
                Employee.get_employees()[self.emp_id].set_biometric_name(self.edit_biometric_name.text().strip())
                Employee.get_employees()[self.emp_id].set_nric(self.edit_nric.text())
                Employee.get_employees()[self.emp_id].set_shifts(shifts)
                Employee.get_employees()[self.emp_id].set_base_pay(float(self.edit_base_pay.text()))
                Employee.get_employees()[self.emp_id].set_charge_ot(float(self.edit_charge_overtime.text()))
                Employee.get_employees()[self.emp_id].set_charge_late(float(self.edit_charge_late_arr.text()))
                Employee.get_employees()[self.emp_id].set_charge_early(float(self.edit_charge_early_dep.text()))
                        
                # remove old nric and replace with new one
                # do even if not necessarily changed
                Employee.get_nric_employees().remove(self.nric)
                Employee.get_nric_employees().append(self.edit_nric.text())
                
                # emit signal
                self.emp_updated.emit()
            else:
                QMessageBox.critical(self, "Input Error",
                    'You already have another staff with identical NRIC.\n' +
                    'Please check that your entries are correct.',
                    QMessageBox.Ok)
        else:
            QMessageBox.critical(self, "Input Error",
                    "Please enter all details.",
                    QMessageBox.Ok)
            
    def is_ready_for_saving(self):
        # name filled
        if self.edit_full_name.hasAcceptableInput():
            if self.edit_biometric_name.hasAcceptableInput():
                if self.edit_nric.hasAcceptableInput():
                    # check if shift button clicked
                    if self.checkbox_shift1.isChecked() or self.checkbox_shift2.isChecked():
                        if self.edit_base_pay.hasAcceptableInput():
                            if self.edit_charge_early_dep.hasAcceptableInput():
                                if self.edit_charge_late_arr.hasAcceptableInput():
                                    if self.edit_charge_overtime.hasAcceptableInput():
                                        return True
        return False

    @Slot()
    def base_pay_changed(self, text):
        # calculate epf
        self.edit_epf_employee.setText(str(round(Company.get_epf_employee() * float(text), 2)))
        self.edit_epf_employer.setText(str(round(Company.get_epf_employer() * float(text), 2)))
        # calculate socso
        self.edit_socso_employee.setText(str(Company.get_socso_employee()))
        self.edit_socso_employer.setText(str(Company.get_socso_employer()))

    def check_shifts(self):
        # if 2 shifts, one is definitely shift 3
        if len(self.shifts) == 2:
            self.checkbox_shift3.setChecked(True)

        # check the single shift
        if self.shifts[0] == '1':
            self.checkbox_shift1.setChecked(True)
        else:
            self.checkbox_shift2.setChecked(True)
