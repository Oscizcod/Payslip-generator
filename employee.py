import os.path
import os

class Employee():
    employees = {}
    URL_emps = 'employees.txt'

    def __init__(self, full_name, biometric_name, nric, working_days='',
                 base_pay='', charge_ot='', charge_late='',
                 charge_early=''):
        # instantiate all instance vars
        self.full_name = full_name.upper()
        self.biometric_name = biometric_name
        self.nric = nric 
        self.working_days = working_days
        self.base_pay = base_pay
        self.charge_ot = charge_ot
        self.charge_late = charge_late
        self.charge_early = charge_early


    @classmethod              
    def load_employees(cls):
        if os.path.exists(cls.URL_emps) and os.stat(cls.URL_emps).st_size != 0:
            with open(cls.URL_emps, 'r', encoding='utf-8') as emps:
                for emp in emps:
                    emp_details = emp.split(';')

                    # use nric as key
                    # store (full name, biom name) as 2-tuple
                    cls.employees[emp_details[2].strip()] = (emp_details[0], emp_details[1])
        else:
            pass
        
    def __str__(self):
        return 'Employee: {}\n'.format(self.full_name) + 'NRIC: {}\n'.format(self.nric) + 'Biometric name: {}'.format(self.biometric_name) 