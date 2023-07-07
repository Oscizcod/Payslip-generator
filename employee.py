import os.path
import os
import random
import datetime as dt
from dateutil.relativedelta import relativedelta

class Employee():
    employees = {}
    nric_employees = []
    id_employees = []
    URL_emps = 'employees.txt'

    def __init__(self, id='0', full_name='', biometric_name='', nric='', shifts='13',
                 base_pay=0, charge_ot=0, charge_late=0,
                 charge_early=0):
        # instantiate all instance vars
        self.id = id
        self.full_name = full_name.upper()
        self.biometric_name = biometric_name
        self.nric = nric 
        self.shifts = shifts
        self.base_pay = base_pay
        self.charge_ot = charge_ot
        self.charge_late = charge_late
        self.charge_early = charge_early
        self.age = self.calculate_age()
        self.eis = self.calculate_eis(self.age)
    
    def calculate_eis(self, age):
        if age < 18:
            return 0
        return 2.9

    def calculate_age(self):
        if self.nric == '':
            return 0
        
        # extract day, month and year from nric
        year = int('20' + self.nric[:2])
        month = int(self.nric[2:4])
        day = int(self.nric[4:6])
        dob = dt.date(year, month, day)

        # get today's date
        today = dt.date.today()

        # get age in years
        return relativedelta(today, dob).years

    def get_id(self):
        return self.id
    
    def get_full_name(self):
        return self.full_name
    
    def set_full_name(self, full_name):
        self.full_name = full_name
    
    def get_nric(self):
        return self.nric
    
    def set_nric(self, nric):
        self.nric = nric
    
    def get_shifts(self):
        return self.shifts
    
    def set_shifts(self, shifts):
        self.shifts = shifts

    def get_charge_ot(self):
        return self.charge_ot
    
    def set_charge_ot(self, charge_ot):
        self.charge_ot = charge_ot

    def get_charge_late(self):
        return self.charge_late

    def set_charge_late(self, charge_late):
        self.charge_late = charge_late

    def get_charge_early(self):
        return self.charge_early
    
    def set_charge_early(self, charge_early):
        self.charge_early = charge_early 

    def get_biometric_name(self):
        return self.biometric_name

    def set_biometric_name(self, biometric_name):
        self.biometric_name = biometric_name

    def get_base_pay(self):
        return self.base_pay
    
    def set_base_pay(self, base_pay):
        self.base_pay = base_pay

    def get_eis(self):
        return self.eis

    @classmethod
    def get_id_employees(cls):
        return cls.id_employees

    @classmethod
    def get_nric_employees(cls):
        return cls.nric_employees
    
    @classmethod
    def get_employees(cls):
        return cls.employees

    def output_to_fileDB(self):
        return '{};{};{};{};{};{};{};{};{}\n'.format(self.id,self.full_name, self.biometric_name, self.nric,
                                                self.shifts, self.base_pay, self.charge_ot, self.charge_late,
                                                self.charge_early)
    
    @classmethod              
    def load_from_db(cls):
        if os.path.exists(cls.URL_emps) and os.stat(cls.URL_emps).st_size != 0:
            with open(cls.URL_emps, 'r', encoding='utf-8') as emps:
                for emp in emps:
                    emp_details = emp.split(';')

                    # use id as key
                    # store Employee instance as value
                    cls.employees[emp_details[0]] = Employee(emp_details[0], emp_details[1],
                                                                     emp_details[2], emp_details[3],
                                                                     emp_details[4], float(emp_details[5]),
                                                                     float(emp_details[6]), float(emp_details[7]),
                                                                     float(emp_details[8].strip()))
                    
                    # populate list of employee ids
                    cls.id_employees.append(emp_details[0])

                    # populate list of employee nrics
                    cls.nric_employees.append(emp_details[3])
        else:
            pass

    @classmethod
    def save_to_db(cls):
         with open('employees.txt', 'w', encoding='utf-8') as f:
            for employee in Employee.get_employees().values():
                f.write(employee.output_to_fileDB())
        
    def __str__(self):
        return 'Employee: {}\n'.format(self.full_name) + 'NRIC: {}\n'.format(self.nric) + 'Biometric name: {}'.format(self.biometric_name)

    @classmethod
    def generate_emp_id(cls):
        # generate a unique id for each employee
        while True:
            # generate random id
            id_emp = random.randint(10,99)

            if id_emp in cls.id_employees:
                continue
            # if unique, return id
            return str(id_emp)