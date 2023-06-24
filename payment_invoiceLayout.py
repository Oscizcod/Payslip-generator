from PySide6.QtWidgets import QWidget,QVBoxLayout, QLabel, QHBoxLayout, QFileDialog, QApplication, QLineEdit, QPushButton
from PySide6.QtCore import Slot

class PaymentInvoiceLayout(QWidget):
    def __init__(self):
        super().__init__()

        # add label for file upload
        label_attn_file_upload = QLabel()
        label_attn_file_upload.setText('Please upload your attendance file:')

        # add input box for file upload
        # plus browse button
        layout_attn_upload = QHBoxLayout()
        self.input_attn_url = QLineEdit()  # accept file path url
        layout_attn_upload.addWidget(self.input_attn_url)
        btn_browse_attn_file = QPushButton()
        btn_browse_attn_file.setText('Browse')
        btn_browse_attn_file.clicked.connect(self.btn_browse_attn_file_clicked)
        layout_attn_upload.addWidget(btn_browse_attn_file)

        # add push button for generating payment invoice
        btn_gen_payment_invoice = QPushButton()
        btn_gen_payment_invoice.setText('Generate Payment Invoice')
        btn_gen_payment_invoice.clicked.connect(self.btn_gen_payment_invoice_clicked)

        # add all widgets and layouts to global layout
        self.setLayout(QVBoxLayout())
        self.layout().addWidget(label_attn_file_upload)
        layout_attn_upload.addWidget(self.input_attn_url)
        layout_attn_upload.addWidget(btn_browse_attn_file)
        self.layout().addLayout(layout_attn_upload)
        self.layout().addWidget(btn_gen_payment_invoice)
        
    @Slot()
    def btn_browse_attn_file_clicked(self):
        file_dialog = QFileDialog()
        file_url = QFileDialog.getOpenFileName(file_dialog,"Open Attendance Sheet", "C:/", "Excel Files (*.xls *.xlsm *.xlsx *.xlsb *xlam)")

        # set input field to selected file
        self.input_attn_url.setText(file_url[0])

    @Slot()
    def btn_gen_payment_invoice_clicked(self):
        # TODO: check to see if acceptable input
        # TODO: where to implement layout change
        pass


# TODO: DELETE below code once integrated into whole app

if __name__ == '__main__':
    # initialise the event loop listener
    app = QApplication()
    # initialise main window and show
    main_window = QWidget()
    layout = PaymentInvoiceLayout()
    main_window.setLayout(layout)
    main_window.show()

    # start event loop listener
    app.exec()
