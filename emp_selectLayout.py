from PySide6.QtWidgets import QDialog, QLabel, QComboBox, QPushButton, QVBoxLayout, QHBoxLayout, QLineEdit, QFileDialog
from PySide6.QtCore import Slot, Signal
from employee import Employee
from payslip import Payslip


class EmpSelectLayout(QDialog):
    # create custom signal
    emp_updated = Signal()

    def __init__(self):
        super().__init__()
        
        self.initUI()

        # slots and signals
        self.btn_cancel.clicked.connect(self.btn_cancel_clicked)
        self.btn_del.clicked.connect(self.btn_del_clicked)
        self.btn_payslip.clicked.connect(self.btn_payslip_clicked)
        self.btn_browse_attn_file.clicked.connect(self.btn_browse_attn_file_clicked)
        self.btn_edit.clicked.connect(self.btn_edit_clicked)

    def initUI(self):
        # inputs and labels
        label_select_emp = QLabel()
        label_select_emp.setText('Select employee: ')
        self.combo_select_emp = QComboBox()
        self.combo_select_emp.addItems(self.get_combo_list())
        self.input_attn_url = QLineEdit()  # accept file path url
        self.btn_browse_attn_file = QPushButton()
        self.btn_browse_attn_file.setText('Browse')
        self.btn_edit = QPushButton()
        self.btn_edit.setText('Edit')
        self.btn_payslip = QPushButton()
        self.btn_payslip.setText('Payslip')
        self.btn_del = QPushButton()
        self.btn_del.setText('Delete')
        self.btn_cancel = QPushButton()
        self.btn_cancel.setText('Cancel')

        # layouts
        layout_top = QVBoxLayout()
        layout_select = QHBoxLayout()
        layout_select.addWidget(label_select_emp)
        layout_select.addWidget(self.combo_select_emp)
        layout_top.addLayout(layout_select)
        layout_browse = QHBoxLayout()
        layout_browse.addWidget(self.input_attn_url)
        layout_browse.addWidget(self.btn_browse_attn_file)
        layout_top.addLayout(layout_browse)
        layout_btns = QHBoxLayout()
        layout_btns.addWidget(self.btn_edit)
        layout_btns.addWidget(self.btn_payslip)
        layout_btns.addWidget(self.btn_del)
        layout_btns.addWidget(self.btn_cancel)

        layout_top.addLayout(layout_btns)
        self.setLayout(layout_top)

    def get_combo_list(self):
        combo_list = []

        for id, emp in Employee.get_employees().items():
            combo_list.append('{} ({})'.format(emp.get_full_name(), id))

        return combo_list

    # slot for cancel btn
    @Slot()
    def btn_cancel_clicked(self):
        # close dialog
        self.done(0)

    @Slot()
    def btn_del_clicked(self):
        # extract id from combobox text
        id = self.combo_select_emp.currentText()[-3:-1]

        # delete employee from dict
        del Employee.get_employees()[id]

        # emit signal 
        self.emp_updated.emit()
        # close dialog
        self.done(0)

    @Slot()
    def btn_payslip_clicked(self):
        # extract id from combobox text
        id = self.combo_select_emp.currentText()[-3:-1]
        emp = Employee.get_employees()[id]

        if Payslip(self.input_attn_url.text(), emp):
            # put message box
            print('successful')
            self.done(0)
        else:
            print('error')

    @Slot()
    def btn_browse_attn_file_clicked(self):
        file_dialog = QFileDialog()
        file_url = QFileDialog.getOpenFileName(file_dialog,"Open Attendance Sheet", "C:/", "Excel Files (*.xls *.xlsm *.xlsx *.xlsb *xlam)")

        # set input field to selected file
        self.input_attn_url.setText(file_url[0])

        
    @Slot()
    def btn_ok_clicked(self):
        # delete employee from dict
        Employee.get_employees()[id]

    @Slot()
    def btn_edit_clicked(self):
        pass
