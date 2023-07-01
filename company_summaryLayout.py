from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QGroupBox, QHBoxLayout, QPushButton
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
            if int(details[0][:2]) < 12:
                time_start = details[0] + ' AM'
            else:
                time_start = details[0] + ' PM'

            if int(details[1][:2]) < 12:
                time_end = details[1] + ' AM'
            else:
                time_end = details[1] + ' PM'

            # get days spelt full
            str_full_days = ''
            for abbr_day in details[2]:
                full_day = Company.get_dict_days()[abbr_day]
                str_full_days += full_day + ', '
            # remove right trailing comma
            str_full_days = str_full_days.rstrip(', ')
            # create label of shifts
            label_shifts = QLabel()
            label_shifts.setText(shift + ': ' + time_start + ' to ' + time_end + ' on\n' + str_full_days)
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
