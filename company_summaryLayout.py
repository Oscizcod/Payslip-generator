from PySide6.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QLabel, QStackedLayout, QGroupBox, QHBoxLayout
from PySide6.QtCore import Slot
from emp_summaryLayout import EmpSummaryLayout
from company import Company

class CoSummLayout(QWidget):
    def __init__(self):
        super().__init__()

        # initialise UI
        self.initUI()
    
    def initUI(self):
        # labels and inputs
        label_name = QLabel()
        label_name.setText(Company.get_name())
        label_epf_employer = QLabel()
        label_epf_employer.setText('Employer: ' + str(Company.get_epf_employer()*100) + '%')
        label_epf_employee = QLabel()
        label_epf_employee.setText('Employee: ' + str(Company.get_epf_employee()*100) + '%')
        layout_shifts = self.shiftsUI()
        label_closed = QLabel()
        label_closed.setText(str(Company.get_closed()))

        # create widget to insert into stacked layout
        # design layout for widget
        # name
        self.setLayout(QVBoxLayout())
        frame_name = QGroupBox('Company name')
        frame_name.setLayout(QHBoxLayout())
        frame_name.layout().addWidget(label_name)
        self.layout().addWidget(frame_name)
        # epf
        frame_epf = QGroupBox('EPF contribution')
        frame_epf.setLayout(QVBoxLayout())
        frame_epf.layout().addWidget(label_epf_employer)
        frame_epf.layout().addWidget(label_epf_employee)
        self.layout().addWidget(frame_epf)
        # shifts
        frame_shifts = QGroupBox('Shifts')
        frame_shifts.setLayout(layout_shifts)
        self.layout().addWidget(frame_shifts)
        # closed days
        frame_closed = QGroupBox('Closed days')
        frame_closed.setLayout(QHBoxLayout())
        frame_closed.layout().addWidget(label_closed)
        self.layout().addWidget(frame_closed)

    def shiftsUI(self):
        # define layout
        layout_shifts = QVBoxLayout()
      
        # set the display for the shifts
        for shift, details in Company.get_shifts().items():
            if int(details[0][:2]) < 12:
                time_start = details[0] + ' AM'
            else:
                time_start = details[0] + ' PM'

            if int(details[1][:2]) < 12:
                time_end = details[1] + ' AM'
            else:
                time_end = details[1] + ' PM'

            label_shifts = QLabel()
            label_shifts.setText(shift + ': ' + time_start + ' to ' + time_end + ' on ' + str(details[2]))
            layout_shifts.addWidget(label_shifts)

        return layout_shifts
