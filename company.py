from datetime import time

class Company():
    name = 'KLINIK MURU SDN BHD'
    epf_employer = 0.13
    epf_employee = 0.11
    eis_employer = 0.002
    eis_employee = 0.002
    socso_employer = 0.02
    socso_employee = 0.005   
    shifts = {'1':{('Mon', 'Tue', 'Wed', 'Thurs', 'Fri'):[time(8,0), time(17,0)]},
              '2':{('Mon', 'Tue', 'Wed', 'Thurs', 'Fri'):[time(8,0), time(13,0)]},
              '3':{('Sat',):[time(8,0), time(13,0)]}
              }
    closed = ['Sun', 'Tue', 'Wed']
    dict_days = {'Mon': 'Monday', 'Tue': 'Tuesday', 'Wed': 'Wednesday', 'Thurs': 'Thursday', 'Fri': 'Friday', 'Sat': 'Saturday', 'Sun': 'Sunday'}

    # define getter and setter methods for each of the class variables
    @classmethod
    def get_name(cls):
        return cls.name
    
    @classmethod
    def set_name(cls, name=''):
        cls.name = name.upper()

    @classmethod
    def get_epf_employer(cls):
        return cls.epf_employer
    
    @classmethod
    def set_epf_employer(cls, employer=0):
        cls.epf_employer = employer

    @classmethod
    def get_epf_employee(cls):
        return cls.epf_employee
    
    @classmethod
    def set_epf_employee(cls, employee=0):
        cls.epf_employee = employee

    @classmethod
    def get_eis_employee(cls):
        return cls.eis_employee
    
    @classmethod
    def set_eis_employee(cls, employee=0):
        cls.eis_employee = employee

    @classmethod
    def get_eis_employer(cls):
        return cls.eis_employer
    
    @classmethod
    def set_eis_employer(cls, employer=0):
        cls.eis_employer = employer

    @classmethod
    def get_socso_employee(cls):
        return cls.socso_employee
    
    @classmethod
    def set_socso_employee(cls, employee=0):
        cls.socso_employee = employee

    @classmethod
    def get_socso_employer(cls):
        return cls.socso_employer
    
    @classmethod
    def set_socso_employer(cls, employer=0):
        cls.socso_employer = employer

    @classmethod
    def get_shifts(cls):
        return cls.shifts
    
    @classmethod
    def set_shifts(cls, shifts={}):
        cls.shifts = shifts

    @classmethod
    def get_closed(cls):
        return cls.closed
    
    @classmethod
    def set_closed(cls, closed=[]):
        cls.closed = closed

    @classmethod
    def get_working_days(cls):
        return [x for x in cls.dict_days if x not in cls.closed]
    
    @classmethod
    def get_dict_days(cls):
        return cls.dict_days