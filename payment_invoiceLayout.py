from PySide6.QtWidgets import QVBoxLayout, QLabel, QHBoxLayout, QFileDialog, QLineEdit, QPushButton, QDialog, QFormLayout, QGroupBox, QComboBox, QCheckBox
from PySide6.QtCore import Slot

class PaymentInvoiceLayout(QDialog):
    def __init__(self):
        super().__init__()

        # initialise UI
        self.initUI()

        # connect btn signals to slots
        self.btn_browse_attn_file.clicked.connect(self.btn_browse_attn_file_clicked)
        self.btn_gen_payment_invoice.clicked.connect(self.btn_ok_clicked)
    
    def initUI(self):
        # inputs
        self.btn_gen_payment_invoice = QPushButton()
        self.btn_gen_payment_invoice.setText('OK')
        self.btn_save_emp_details = QPushButton()
        self.btn_save_emp_details.setText('Save')
        self.btn_cancel = QPushButton()
        self.btn_cancel.setText('Cancel')

        # define layouts
        # horizontal layout for both btns
        layout_btns = QHBoxLayout()
        layout_btns.addWidget(self.btn_save_emp_details)
        layout_btns.addWidget(self.btn_gen_payment_invoice)
        layout_btns.addWidget(self.btn_cancel)
        layout_top_main = QVBoxLayout()
        layout_top_main.addWidget(self.workingUI())
        layout_top_main.addWidget(self.paymentUI())
        layout_top_main.addWidget(self.attnFileUI())
        layout_top_main.addLayout(layout_btns)
        self.setLayout(layout_top_main)

    def attnFileUI(self):
        # all components for upload attendance file
        self.input_attn_url = QLineEdit()  # accept file path url
        self.btn_browse_attn_file = QPushButton()
        self.btn_browse_attn_file.setText('Browse')
        
        # layout
        frame_upload = QGroupBox('Attendance file upload')
        layout_attn_upload = QHBoxLayout()
        layout_attn_upload.addWidget(self.input_attn_url)
        layout_attn_upload.addWidget(self.btn_browse_attn_file)
        frame_upload.setLayout(layout_attn_upload)

        return frame_upload

    def paymentUI(self):
        # define all inputs
        edit_base_pay = QLineEdit()
        edit_epf_employer = QLineEdit()
        edit_epf_employee = QLineEdit()
        edit_charge_overtime = QLineEdit()
        edit_charge_late_arr = QLineEdit()
        edit_charge_early_dep = QLineEdit()

        # create layout
        # use form for all inputs
        layout_payment = QFormLayout()
        layout_payment.addRow('Base pay: RM', edit_base_pay)
        layout_payment.addRow('EPF Employer contribution: RM', edit_epf_employer)
        layout_payment.addRow('EPF Employee contribution: RM', edit_epf_employee)
        layout_payment.addRow('Overtime charges: RM', edit_charge_overtime)
        layout_payment.addRow('Late arrival charges: RM', edit_charge_late_arr)
        layout_payment.addRow('Early departure charges: RM', edit_charge_early_dep)

        # add form to groupbox
        frame_payment = QGroupBox('Payment info')
        frame_payment.setLayout(layout_payment)
        
        return frame_payment

    def workingUI(self):
        # define constants
        WORKING_HOURS = self.generate_working_hrs()
        WORKING_DAYS = ['Monday', 'Tuesday', 'Wednesday', 'Thursday',
                        'Friday', 'Saturday', 'Sunday']

        # define all inputs
        edit_start_time = QComboBox()
        edit_start_time.addItems(WORKING_HOURS)
        edit_end_time = QComboBox()
        edit_end_time.addItems(WORKING_HOURS)
        # add options for checkbox
        edit_work_mon = QCheckBox(WORKING_DAYS[0])
        edit_work_tue = QCheckBox(WORKING_DAYS[1])
        edit_work_wed = QCheckBox(WORKING_DAYS[2])
        edit_work_thurs = QCheckBox(WORKING_DAYS[3])
        edit_work_fri = QCheckBox(WORKING_DAYS[4])
        edit_work_sat = QCheckBox(WORKING_DAYS[5])
        edit_work_sun = QCheckBox(WORKING_DAYS[6])

        # create layout
        # put start and end times horizontally
        layout_timing = QHBoxLayout()
        label_start_time = QLabel()
        label_start_time.setText('Start time: ')
        label_end_time = QLabel()
        label_end_time.setText('End time: ')
        layout_timing.addWidget(label_start_time)
        layout_timing.addWidget(edit_start_time)
        layout_timing.addWidget(label_end_time)
        layout_timing.addWidget(edit_end_time)
        # put all in a group box with vertical layout
        frame_working = QGroupBox('Working info')
        layout_top_working = QVBoxLayout()
        frame_working.setLayout(layout_top_working)
        label_working_days = QLabel()
        label_working_days.setText('Select working days: ')
        frame_working.layout().addLayout(layout_timing)
        frame_working.layout().addWidget(label_working_days)
        frame_working.layout().addWidget(edit_work_mon)
        frame_working.layout().addWidget(edit_work_tue)
        frame_working.layout().addWidget(edit_work_wed)
        frame_working.layout().addWidget(edit_work_thurs)
        frame_working.layout().addWidget(edit_work_fri)
        frame_working.layout().addWidget(edit_work_sat)
        frame_working.layout().addWidget(edit_work_sun)

        return frame_working

    def generate_working_hrs(self):
        working_hrs = []

        for hr in range(7, 23):
            working_hrs.append(str(hr) + ':00')
            working_hrs.append(str(hr) + ':30')

        return working_hrs
    
    @Slot()
    def btn_browse_attn_file_clicked(self):
        file_dialog = QFileDialog()
        file_url = QFileDialog.getOpenFileName(file_dialog,"Open Attendance Sheet", "C:/", "Excel Files (*.xls *.xlsm *.xlsx *.xlsb *xlam)")

        # set input field to selected file
        self.input_attn_url.setText(file_url[0])

    @Slot()
    def btn_ok_clicked(self):
        # TODO: check to see if acceptable input
        # TODO: where to implement layout change
        pass
