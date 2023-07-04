from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QGroupBox, QHBoxLayout, QPushButton
from company import Company
import datetime as dt

class CoSummLayout(QWidget):
    def __init__(self):
        super().__init__()

        # initialise UI
        self.initUI()
    
    def initUI(self):
        # labels and inputs
        # name
        label_name = QLabel()
        label_name.setText(Company.get_name())
        # epf
        label_epf_employer = QLabel()
        label_epf_employer.setText('Employer: ' + str(Company.get_epf_employer()*100) + '%')
        label_epf_employee = QLabel()
        label_epf_employee.setText('Employee: ' + str(Company.get_epf_employee()*100) + '%')
        # eis
        label_eis_employer = QLabel()
        label_eis_employer.setText('Employer: ' + str(Company.get_eis_employer()*100) + '%')
        label_eis_employee = QLabel()
        label_eis_employee.setText('Employee: ' + str(Company.get_eis_employee()*100) + '%')
        # socso
        label_socso_employer = QLabel()
        label_socso_employer.setText('Employer: ' + str(Company.get_socso_employer()*100) + '%')
        label_socso_employee = QLabel()
        label_socso_employee.setText('Employee: ' + str(Company.get_socso_employee()*100) + '%')
        #shifts
        layout_shifts = self.shiftsUI()
        layout_closed = self.closedDaysUI()

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
         # eis
        frame_eis = QGroupBox('Insurance')
        frame_eis.setLayout(QVBoxLayout())
        frame_eis.layout().addWidget(label_eis_employer)
        frame_eis.layout().addWidget(label_eis_employee)
        self.layout().addWidget(frame_eis)
         # socso
        frame_socso = QGroupBox('Insurance')
        frame_socso.setLayout(QVBoxLayout())
        frame_socso.layout().addWidget(label_socso_employer)
        frame_socso.layout().addWidget(label_socso_employee)
        self.layout().addWidget(frame_socso)
        # shifts
        frame_shifts = QGroupBox('Shifts')
        frame_shifts.setLayout(layout_shifts)
        self.layout().addWidget(frame_shifts)
        # closed days
        frame_closed = QGroupBox('Closed days')
        frame_closed.setLayout(layout_closed)
        self.layout().addWidget(frame_closed)

    def shiftsUI(self):
        # define layout
        layout_shifts = QVBoxLayout()
      
        # set the display for the shifts
        for shift, details in Company.get_shifts().items():
            for time in details.values():
                    time_start = str(time[0]) 
                    time_end = str(time[1] )

            # get days spelt full
            str_full_days = ''
            for days in details:
                for abbr_day in days:
                    full_day = Company.get_dict_days()[abbr_day]
                    str_full_days += full_day + ', '
            # remove right trailing comma
            str_full_days = str_full_days.rstrip(', ')
            # create label of shifts
            label_shifts = QLabel()
            label_shifts.setText('Shift ' + shift + ': ' + time_start + ' to ' + time_end + ' on\n' + str_full_days)
            layout_shifts.addWidget(label_shifts)

        return layout_shifts
    
    def closedDaysUI(self):
        # define layout
        layout_closed = QVBoxLayout()

        # get days spelt full
        str_closed_days = ''
        for abbr_day in Company.get_closed():
            full_day = Company.get_dict_days()[abbr_day]
            str_closed_days += full_day + ', '
        # remove right trailing comma
        str_closed_days = str_closed_days.rstrip(', ')
        # create label of shifts
        label_closed = QLabel()
        label_closed.setText(str_closed_days)
        layout_closed.addWidget(label_closed)

        return layout_closed
