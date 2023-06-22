# class for employees

class Employee():
    def __init__(self, name=None, dob=None, start_working_date=None, end_working_date=None, shifts=None ):
        self.name = name
        self.dob = dob
        self.start_working_date = start_working_date
        self.end_working_date = end_working_date
        self.shifts = shifts