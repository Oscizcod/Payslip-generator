from PySide6.QtWidgets import QWidget, QLabel, QComboBox, QPushButton, QVBoxLayout, QHBoxLayout, QLineEdit, QFileDialog, QMessageBox
from PySide6.QtGui import QIntValidator, QDoubleValidator
from PySide6.QtCore import Slot
from employee import Employee
from payslip import Payslip


class EmpPaySlipSelLayout(QWidget):
    def __init__(self):
        super().__init__()
        
        self.initUI()

        # slots and signals
        self.btn_payslip.clicked.connect(self.btn_payslip_clicked)
        self.btn_browse_attn_file.clicked.connect(self.btn_browse_attn_file_clicked)

    def initUI(self):
        # inputs and labels
        # select employee
        label_select_emp = QLabel()
        label_select_emp.setText('Select employee: ')
        self.combo_select_emp = QComboBox()
        self.combo_select_emp.addItems(self.get_combo_list())
        # for browsing attendance file
        self.input_attn_url = QLineEdit()  # accept file path url
        self.btn_browse_attn_file = QPushButton()
        self.btn_browse_attn_file.setText('Browse')
        # for annual leave
        # validator for all leave
        validator_leave = QIntValidator(self)
        validator_leave.setRange(0,31)
        label_al = QLabel()
        label_al.setText('Annual leave: ')
        self.edit_al = QLineEdit()
        self.edit_al.setText('0')
        self.edit_al.setValidator(validator_leave)
        # for public hols
        label_public_hol = QLabel()
        label_public_hol.setText('Public holidays: ')
        self.edit_public_hol = QLineEdit()
        self.edit_public_hol.setText('0')
        self.edit_public_hol.setValidator(validator_leave)
        # closed for personal reasons
        label_close_personal = QLabel()
        label_close_personal.setText('Closed (personal reasons): ')
        self.edit_close_personal = QLineEdit()
        self.edit_close_personal.setText('0')
        self.edit_close_personal.setValidator(validator_leave)
        # for allowance
        # validator for allowance amount
        validator_allowance = QDoubleValidator()
        validator_allowance.setRange(0, 99999, 2)
        label_allowance_rm = QLabel()
        label_allowance_rm.setText('Allowance: RM')
        label_allowance_remark = QLabel()
        label_allowance_remark.setText('Allowance remark: ')
        self.edit_allowance_rm = QLineEdit()
        self.edit_allowance_rm.setText('0')
        self.edit_allowance_rm.setValidator(validator_allowance)
        self.edit_allowance_remark = QLineEdit()
        self.edit_allowance_remark.setText('NIL')        
        # btn for generating payslip
        self.btn_payslip = QPushButton()
        self.btn_payslip.setText('Generate payslip')

        # layouts
        # top level
        layout_top = QVBoxLayout()
        # for selecting employees
        layout_select = QHBoxLayout()
        layout_select.addWidget(label_select_emp)
        layout_select.addWidget(self.combo_select_emp)
        # for browsing attendance files
        layout_browse = QHBoxLayout()
        layout_browse.addWidget(self.input_attn_url)
        layout_browse.addWidget(self.btn_browse_attn_file)
        # for inputting annual leave
        layout_al = QHBoxLayout()
        layout_al.addWidget(label_al)
        layout_al.addWidget(self.edit_al)
        # for inputting public hols
        layout_public_hol = QHBoxLayout()
        layout_public_hol.addWidget(label_public_hol)
        layout_public_hol.addWidget(self.edit_public_hol)
        # for inputting closed due to personal reasons
        layout_close_personal = QHBoxLayout()
        layout_close_personal.addWidget(label_close_personal)
        layout_close_personal.addWidget(self.edit_close_personal)
        # for inputting allowance remark
        layout_allowance_remark = QHBoxLayout()
        layout_allowance_remark.addWidget(label_allowance_remark)
        layout_allowance_remark.addWidget(self.edit_allowance_remark)
        # for inputting allowance amount
        layout_allowance_rm = QHBoxLayout()
        layout_allowance_rm.addWidget(label_allowance_rm)
        layout_allowance_rm.addWidget(self.edit_allowance_rm)
        # construct final layout
        layout_top.addLayout(layout_select)
        layout_top.addLayout(layout_browse)
        layout_top.addLayout(layout_al)
        layout_top.addLayout(layout_public_hol)
        layout_top.addLayout(layout_close_personal)
        layout_top.addLayout(layout_allowance_remark)
        layout_top.addLayout(layout_allowance_rm)
        layout_top.addWidget(self.btn_payslip)
        self.setLayout(layout_top)

    def get_combo_list(self):
        combo_list = []

        for id, emp in Employee.get_employees().items():
            combo_list.append('{} ({})'.format(emp.get_full_name(), id))

        return combo_list

    @Slot()
    def btn_payslip_clicked(self):
        # check that all input boxes have acceptable input
        if self.edit_al.hasAcceptableInput():
            if self.edit_public_hol.hasAcceptableInput():
                if self.edit_allowance_rm.hasAcceptableInput():
                    # extract id from combobox text
                    id = self.combo_select_emp.currentText()[-3:-1]
                    emp = Employee.get_employees()[id]
                
                    # pass employee instance into Payslip class
                    is_executed = Payslip(self.input_attn_url.text(), emp, int(self.edit_al.text()), int(self.edit_public_hol.text()),
                                          int(self.edit_close_personal.text()), float(self.edit_allowance_rm.text()),
                                          self.edit_allowance_remark.text()).generate_records()
                    
                    # successful execution
                    if is_executed:
                        # message box indicating successful generation of files
                        QMessageBox.information(self, "Success",
                                                "Your files have been successfully generated!",
                                                QMessageBox.Ok)
                else:
                    self.error_box()
            else:
                self.error_box()
        else:
            self.error_box()

    def error_box(self):
        QMessageBox.warning(self, "Error",
                                "Please make sure all fields are filled correctly.",
                                QMessageBox.Ok)

    @Slot()
    def btn_browse_attn_file_clicked(self):
        file_dialog = QFileDialog()
        file_url = QFileDialog.getOpenFileName(file_dialog,"Open Attendance Sheet", "C:/", "Excel Files (*.xls *.xlsm *.xlsx *.xlsb *xlam)")

        # set input field to selected file
        self.input_attn_url.setText(file_url[0])
