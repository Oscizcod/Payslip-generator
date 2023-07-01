import os.path
import os

class Employee():
    employees = {}
    URL_emps = 'employees.txt'

    def __init__(self, full_name, biometric_name, nric, shifts='13',
                 base_pay=0, charge_ot=0, charge_late=0,
                 charge_early=0):
        # instantiate all instance vars
        self.full_name = full_name.upper()
        self.biometric_name = biometric_name
        self.nric = nric 
        self.shifts = shifts
        self.base_pay = base_pay
        self.charge_ot = charge_ot
        self.charge_late = charge_late
        self.charge_early = charge_early

    def output_to_fileDB(self):
        return '{};{};{};{};{};{};{};{}\n'.format(self.full_name, self.biometric_name, self.nric,
                                                self.shifts, self.base_pay, self.charge_ot, self.charge_late,
                                                self.charge_early)
    
    @classmethod              
    def load_from_db(cls):
        if os.path.exists(cls.URL_emps) and os.stat(cls.URL_emps).st_size != 0:
            with open(cls.URL_emps, 'r', encoding='utf-8') as emps:
                for emp in emps:
                    emp_details = emp.split(';')

                    # use nric as key
                    # store (full name, biom name) as 2-tuple
                    cls.employees[emp_details[2].strip()] = Employee(emp_details[0], emp_details[1],
                                                                     emp_details[2], emp_details[3],
                                                                     emp_details[4], emp_details[5],
                                                                     emp_details[6], emp_details[7].strip())
        else:
            pass

    @classmethod
    def save_to_db(cls):
         with open('employees.txt', 'w', encoding='utf-8') as f:
            for employee in Employee.get_employees().values():
                f.write(employee.output_to_fileDB())

    @classmethod
    def get_employees(cls):
        return cls.employees
        
    def __str__(self):
        return 'Employee: {}\n'.format(self.full_name) + 'NRIC: {}\n'.format(self.nric) + 'Biometric name: {}'.format(self.biometric_name) 