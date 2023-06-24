from  PySide6.QtWidgets import QVBoxLayout, QLabel

class EmployeeLayout(QVBoxLayout):
    def __init__(self):
        super().__init__()

        # Label for current staff
        title_active_emp = QLabel()
        title_active_emp.setText('Current employees')