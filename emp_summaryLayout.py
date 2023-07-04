from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel
from employee import Employee

class EmpSummaryLayout(QWidget):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        # inputs and labels
        self.label_top = QLabel()  # displayed at top of page
        
        # layout for summary page
        layout_top_level = QVBoxLayout()
        # check how many emps registered
        if len(Employee.get_employees()) != 0:
            # title of layout
            self.label_top.setText('Employee summary: ')
            layout_top_level.addWidget(self.label_top)

            for id, emp in Employee.get_employees().items():
                # label
                label_emp = QLabel()
                label_emp.setText(emp.__str__())
                # append to top layout
                layout_top_level.addWidget(label_emp)
        else:
            self.label_top.setText('No employees registered.')
            layout_top_level.addWidget(self.label_top)

        # set layout for widget
        self.setLayout(layout_top_level)
        