from constants import API_KEY
from conversiontools import ConversionClient
import shutil
import re
import pandas as pd
from company import Company
import os

class Payslip():
    def __init__(self, url_attn_file, emp):
        self.url_attn_file = url_attn_file
        # get the employee instance varibles
        self.biometric_name = emp.get_biometric_name()
        self.shifts = emp.get_shifts()
        self.charge_ot = emp.get_charge_ot()
        self.charge_late = emp.get_charge_late()
        self.charge_early = emp.get_charge_early()
        # get employee's working hours
        self.working_hours = self.get_working_hours()

        self.generate_payslip()
    
    def generate_payslip(self):
        url_xls = self.xml_to_xls()
        self.clean_data(url_xls)

    def xml_to_xls(self):
        # extract file name
        regex_file = r'.*(RE\d+_\d+.XLS)$'
        file_name = re.search(regex_file, self.url_attn_file).groups()[0]
        
        # create attendance dir if not present
        if not os.path.exists('./attendance/'):
            os.mkdir('./attendance/')

        # copy file to attendance/ dir
        shutil.copy2(self.url_attn_file, './attendance/' + file_name)
        input_file = './attendance/' + file_name
        output_file = './attendance/' + file_name

        # instantiate file converter
        client = ConversionClient(API_KEY)
        
        try:
            client.convert('convert.xml_to_excel', input_file, output_file, { 'excel_format': 'xls'})
        except Exception as error:
            print(error)

        return output_file

    def clean_data(self, url_file):
        # create df of attendance file
        df = pd.read_excel(url_file, header=None)

        # determine number of staff
        num_rows = df.shape[0]
        num_staff = int(num_rows / 25)

        # loop through each employee
        for i in range(1,num_staff+1):
            # get biometric name
            df_name = df.iloc[25*(i-1) + 3, 4]
            df_name = df_name[5:]

            # initialise variables to store details
            date = []
            day = []
            time_in = []
            time_out = []
    
            if self.biometric_name == df_name:
                # iterate through dates in first half of month
                for j, row in df.iloc[25*(i-1) + 8:25*i -1].iterrows():
                    date.append(row[0])
                    day.append(row[1])
                    timings = []
            
                    # collect all timings
                    for k in range(2,8):
                        try:
                            time = float(row[k].replace(':','.'))
                        except ValueError:
                            continue
                    
                        # check no duplicates
                        if time not in timings:
                            timings.append(time)
                        else:
                            continue
                    
                    # decide which start time to use depending on day
                    for days, time in self.working_hours.items():
                        if row[1] in days:
                            start_time = float(time[0])
                            end_time = float(time[1])

                    # if no timing, set time_in and time_out to 0
                    if len(timings) == 0:
                        time_in.append(0)
                        time_out.append(0)
                    # if single time value, use 12 PM as demarcation if time in/out
                    elif len(timings) == 1:
                        if timings[0] > 12:
                            time_out.append(timings[0])
                            time_in.append(start_time)
                        else:
                            time_in.append(timings[0])
                            time_out.append(end_time)
                    # for all other lengths, find min/max
                    else:
                        time_in.append(min(timings))
                        time_out.append(max(timings))
              
                # iterate through latter half of month
                for l, row in df.iloc[25*(i-1) + 8:25*i -1].iterrows():
                    # check if empty date, terminate loop
                    if type(row[8]) == float:
                        break
            
                    # continue if got date
                    date.append(row[8])
                    day.append(row[9])
                    timings = []
            
                    # collect all timings
                    for m in range(10,16):
                        try:
                            time = float(row[m].replace(':','.'))
                        except ValueError:
                            continue
            
                        # check no duplicates
                        if time not in timings:
                            timings.append(time)
                        else:
                            continue
                    
                    # decide which start time to use depending on day
                    for days, time in self.working_hours.items():
                        if row[1] in days:
                            start_time = float(time[0])
                            end_time = float(time[1])

                    # if no timing, set time_in and time_out to 0
                    if len(timings) == 0:
                        time_in.append(0)
                        time_out.append(0)
                    # if single time value, use 12 PM as demarcation if time in/out
                    elif len(timings) == 1:
                        if timings[0] > 12:
                            time_out.append(timings[0])
                            time_in.append(start_time)
                        else:
                            time_in.append(timings[0])
                            time_out.append(end_time)
                     # for all other lengths, find min/max
                    else:
                        time_in.append(min(timings))
                        time_out.append(max(timings))
                
                break
            else:
                continue

        # create new dataframe and return
        data = {'date': date, 'day': day, 'time_in': time_in, 'time_out': time_out}
        df_emp = pd.DataFrame(data)
        df_emp['late_arr_mins'] = df_emp.apply(self.calculate_late_arr_mins, axis=1)
        df_emp['leaving_time'] = df_emp.apply(self.calculate_leaving_time, axis=1)
        df_emp['overtime_mins'] = df_emp.leaving_time.apply(lambda x: x if x>0 else 0)
        df_emp['early_dep_mins'] = df_emp.leaving_time.apply(lambda x: x if x<0 else 0)
        df_emp.drop('leaving_time', axis=1, inplace=True)
        df_emp['overtime_mins'] = df_emp.overtime_mins.apply(self.calculate_overtime_mins)
        df_emp['early_dep_mins'] = df_emp.early_dep_mins.apply(self.calculate_early_dep_mins)
        df_emp['deduct_late_arr'] = df_emp.late_arr_mins.apply(self.deduct_late_arr)
        df_emp['deduct_early_dep'] = df_emp.early_dep_mins.apply(self.deduct_early_dep)
        df_emp['pay_overtime'] = df_emp.overtime_mins.apply(self.pay_overtime)
        
        df_emp.to_csv('{}_payslip.csv'.format(self.biometric_name), index=False) 
        return df_emp
   
    def get_working_hours(self):
        working_hours = {}

        for shift in self.shifts:
            working_hours.update(Company.get_shifts()[shift])

        return working_hours
    
    def calculate_late_arr_mins(self, df):
        if df.day in Company.get_closed():
            return 0    
        
        # decide which start time to use depending on day
        for days, time in self.working_hours.items():
            if df.day in days:
                start_time = float(time[0])

        # check if early
        if df.time_in < start_time:
            return 0
        late_arr_time = df.time_in - start_time        
        
        # calculate number of mins late arrival
        if int(late_arr_time) == 0:
            return round(late_arr_time * 100)
        else:
            late_arr_hr_to_mins = int(late_arr_time) * 60
            late_arr_mins = round((late_arr_time / int(late_arr_time)) * 100)
            return late_arr_hr_to_mins + late_arr_mins            

    def calculate_leaving_time(self, df):
        if df.day in Company.get_closed():
            return 0
        
        for days, time in self.working_hours.items():
            if df.day in days:
                end_time = float(time[1])

        if round(df.time_in * 100) == 0 and round(df.time_out * 100) == 0:
            # absent for work (neither early dep nor overtime)
            return 0
        else:
            return df.time_out - end_time
        
    def calculate_overtime_mins(self,time):
        if int(time) == 0:
            return round(time * 100)

        hrs_to_mins = int(time) * 60
        mins = round(time % int(time) * 100)
    
        return hrs_to_mins + mins

    def calculate_early_dep_mins(self,time):
        time *= -1
    
        if int(time) == 0:
            return round(time * 100)
    
        hrs_to_mins = int(time) * 60
        mins = round(time % int(time) * 100)
    
        return hrs_to_mins + mins

    def deduct_late_arr(self,mins):
        return self.charge_late * mins
    
    def deduct_early_dep(self,mins):
        return self.charge_early * mins

    def pay_overtime(self,mins):
        return self.charge_ot * mins
    

if __name__ == '__main__':
    from employee import Employee

    emp = Employee(23, 'Fatin Nurimah','Fatin','950323-34-3433',
                   '13',1000,0.30,0,0.2)
    
    url = 'E:/RE001_06.XLS'
    Payslip(url, emp)