class Company():
    name = 'KLINIK MURU SDN BHD'
    epf_employer = 0.03
    epf_employee = 0.03   
    shifts = {'Shift 1':('08.00', '17.00', ['Mon', 'Tue', 'Wed', 'Thurs', 'Fri']),
              'Shift 2':('08.00', '13.00', ['Mon', 'Tue', 'Wed', 'Thurs', 'Fri']),
              'Shift 3':('08.00', '13.00', ['Sat'])
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