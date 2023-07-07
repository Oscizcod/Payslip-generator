from constants import API_KEY
from conversiontools import ConversionClient
import shutil
import re
import pandas as pd
from company import Company
import os
import datetime as dt
from PySide6.QtWidgets import QMessageBox

class Payslip():
    dict_months = {'01': 'January', '02': 'February', '03': 'March', '04':'April', '05': 'May', '06': 'June',
                   '07': 'July', '08': 'August', '09': 'September', '10': 'October', '11': 'November', '12': 'December'}

    def __init__(self, url_attn_file, emp, al, public_hol, close_personal, allowance_rm, allowance_remark):
        self.url_attn_file = url_attn_file
        # get the employee instance varibles
        self.full_name = emp.get_full_name()
        self.nric = emp.get_nric()
        self.biometric_name = emp.get_biometric_name()
        self.base_pay = emp.get_base_pay()
        self.shifts = emp.get_shifts()
        self.charge_ot = emp.get_charge_ot()
        self.charge_late = emp.get_charge_late()
        self.charge_early = emp.get_charge_early()
        # eis
        self.eis_employee = emp.get_eis()
        self.eis_employer = emp.get_eis()
        # get employee's working hours
        self.working_hours = self.get_working_hours()
        # get closed days
        self.closed_days = Company.get_closed()
        # get allowance, leave and hols
        self.al = al
        self.public_hol = public_hol
        self.close_personal = close_personal
        self.allowance_rm = allowance_rm
        self.allowance_remark = allowance_remark

        # get company payment details
        # epf
        self.epf_employee = Company.get_epf_employee()
        self.epf_employer = Company.get_epf_employer()
        # socso
        self.socso_employee = Company.get_socso_employee()
        self.socso_employer = Company.get_socso_employer()
    
    def generate_records(self):
        # catch all exceptions
        try:
            url_xls = self.xml_to_xls()
            clean_df = self.clean_data(url_xls)  # generate clean data as log csv file
            self.write_payslip()  # generate payslip
            self.write_attendance(clean_df)  # generate attendance

            # execution successful
            return True
        
        except:
            # generate error message box
            err_box = QMessageBox()
            err_box.setText("Error")
            err_box.setInformativeText("Your files could not be generated. Please refer to the manual to troubleshoot potential problems.")
            err_box.setStandardButtons(QMessageBox.Ok)
            err_box.exec()

            return False

    def write_attendance(self, df):
        with open('./new-attendance/{}_attendance_{}_{}.txt'.format(self.biometric_name, self.month_df, self.year_df), 'w', encoding='utf-8') as f:
            # total width of a line
            total_width = 70
        
            # file header
            f.write('KLINIK MURU SDN BHD\n')
            f.write('36B, JALAN KOLAM AIR, 80100, JOHOR BAHRU\n')
            f.write('ATTENDANCE FOR THE MONTH OF {} {}\n\n'.format(self.month_df.upper(), self.year_df))

            # personal details and shifts
            f.write('Name: {}'.format(self.full_name))
            f.write('\n')
            f.write('NRIC: {}'.format(self.nric))
            f.write('\n')
            # create shifts string
            emp_shifts = ''
            for shift in self.shifts:
                for days, times in Company.get_shifts()[shift].items():
                    emp_shifts += str(times[0]) + '-' + str(times[1]) + '\n['
                    
                    for day in days:
                        emp_shifts += Company.get_dict_days()[day] + ','
                    emp_shifts = emp_shifts.rstrip(',')
                    emp_shifts += ']\n\n'
                    
            f.write('Shifts: ')
            f.write('\n')
            f.write(emp_shifts)
            f.write('-' * total_width)
            f.write('\n\n')

            # column names
            f.write('Day' + ' '*15 + 'Date' + ' '*26 + 'Time in' + ' '*21 + 'Time out')
            f.write('\n')

            # loop through clean df and write to file
            for i, row in df.iterrows():
                # re-write date in dd/mm/yyyy format
                date = row[0]
                day = row[1]
                new_date = date[-2:] + '.' + date[0:2] + '.' + str(self.year_df)

                if day == 'Thurs':
                    day = day[:3]
                
                if row[2] == '-':
                    f.write(day + ' '*15 + new_date + ' '*24 + row[2] + ' '*26 + row[3])
                    f.write('\n')
                else:
                    # write data into file
                    f.write(day + ' '*15 + new_date + ' '*20 + row[2] + ' '*20 + row[3])
                    f.write('\n')

    def write_payslip(self):
        with open('./payslip/{}_payslip_{}_{}.txt'.format(self.biometric_name, self.month_df, self.year_df), 'w', encoding='utf-8') as f:
            # total width of a line
            total_width = 70
        
            # file header
            f.write('KLINIK MURU SDN BHD\n')
            f.write('36B, JALAN KOLAM AIR, 80100, JOHOR BAHRU\n')
            f.write('SALARY SLIP FOR THE MONTH OF {} {}\n\n'.format(self.month_df.upper(), self.year_df))

            # personal details and shifts
            f.write('Name: {}'.format(self.full_name))
            f.write('\n')
            f.write('NRIC: {}'.format(self.nric))
            f.write('\n')
            # create shifts string
            emp_shifts = ''
            for shift in self.shifts:
                for days, times in Company.get_shifts()[shift].items():
                    emp_shifts += str(times[0]) + '-' + str(times[1]) + '\n['
                    
                    for day in days:
                        emp_shifts += Company.get_dict_days()[day] + ','
                    emp_shifts = emp_shifts.rstrip(',')
                    emp_shifts += ']\n\n'
                    
            f.write('Shifts: ')
            f.write('\n')
            f.write(emp_shifts)
            f.write('-' * total_width)
            f.write('\n\n')

            # earnings
            f.write('Description')
            f.write('Earnings'.rjust(total_width-len('Description')))
            f.write('\n\n')
            # base pay
            f.write('Basic Pay')
            f.write('RM {}'.format(self.base_pay).rjust(total_width-9))
            f.write('\n')
            # allowance
            allowance = 'Allowance: {}'.format(self.allowance_remark)
            f.write(allowance)
            f.write('RM {}'.format(self.allowance_rm).rjust(total_width-len(allowance)))
            f.write('\n')
            # overtime
            ot = 'Overtime'
            f.write(ot)
            f.write('RM {}'.format(self.ot_rm).rjust(total_width-len(ot)))
            f.write('\n')
            f.write('-' * total_width)
            f.write('\n\n')
            
            # deductions
            f.write('Deductions'.rjust(total_width))
            f.write('\n\n')
            # epf
            epf_empe = 'Employee EPF'
            f.write(epf_empe)
            epf_employee_rm = round(self.epf_employee * self.base_pay, 2)
            f.write('RM {}'.format(str(epf_employee_rm)).rjust(total_width-len(epf_empe)))
            f.write('\n')
            # eis
            eis_empe = 'Employee EIS'
            f.write(eis_empe)
            f.write('RM {}'.format(str(self.eis_employee)).rjust(total_width-len(eis_empe)))
            f.write('\n')
            # socso
            socso_empe = 'Employee SOCSO'
            f.write(socso_empe)
            f.write('RM {}'.format(str(self.socso_employee)).rjust(total_width-len(socso_empe)))
            f.write('\n')
            # late arrival / early departure
            misc_deduct = 'Late arrival/ early departure'
            f.write(misc_deduct)
            f.write('RM {}'.format(self.misc_deduct_rm).rjust(total_width-len(misc_deduct)))
            f.write('\n')
            f.write('-' * total_width)
            f.write('\n\n')

            # nett salary
            nett_salary = 'Nett salary'
            f.write(nett_salary)
            nett_rm = round(self.base_pay + self.allowance_rm + self.ot_rm - epf_employee_rm - self.eis_employee - self.socso_employee - self.misc_deduct_rm, 2)
            f.write('RM {}'.format(str(nett_rm)).rjust(total_width-len(nett_salary)))
            f.write('\n')
            f.write('-' * total_width)
            f.write('\n\n')

            # employer contributions
            # epf
            f.write('Employer contribution'.rjust(total_width))
            f.write('\n\n')
            epf_empr = 'Employer EPF'
            f.write(epf_empr)
            epf_employer_rm = round(self.epf_employer * self.base_pay, 2)
            f.write('RM {}'.format(str(epf_employer_rm)).rjust(total_width-len(epf_empr)))
            f.write('\n')
            # eis
            eis_empr = 'Employer EIS'
            f.write(eis_empr)
            f.write('RM {}'.format(str(self.eis_employer)).rjust(total_width-len(eis_empr)))
            f.write('\n')
            # socso
            socso_empr = 'Employer SOCSO'
            f.write(socso_empr)
            socso_employer_rm = round(self.socso_employer, 2)
            f.write('RM {}'.format(str(socso_employer_rm)).rjust(total_width-len(socso_empr)))
            f.write('\n')
            f.write('-' * total_width)
            f.write('\n\n')

            # working days summary
            # total
            f.write('Working days summary'.rjust(total_width))
            f.write('\n\n')
            total_days = 'Total days in the month'
            f.write(total_days)
            f.write('{}'.format(str(self.days_df)).rjust(total_width-len(total_days)))
            f.write('\n')
            # closed
            closed_days = 'Closed'
            f.write(closed_days)
            f.write('{}'.format(str(self.count_closed_days)).rjust(total_width-len(closed_days)))
            f.write('\n')
            # public hols
            title_public_holidays = 'Public holidays'
            f.write(title_public_holidays)
            f.write('{}'.format(str(self.public_hol)).rjust(total_width-len(title_public_holidays)))
            f.write('\n')
            # closed for personal reasons
            title_close_personal = 'Closed (personal reasons)'
            f.write(title_close_personal)
            f.write('{}'.format(str(self.close_personal)).rjust(total_width-len(title_close_personal)))
            f.write('\n')
            # annual leave
            title_annual_leave = 'Annual leave'
            f.write(title_annual_leave)
            f.write('{}'.format(str(self.al)).rjust(total_width-len(title_annual_leave)))
            f.write('\n')
            # medical leave
            title_med_leave = 'Medical leave'
            f.write(title_med_leave)
            med_leave = self.days_df - self.count_closed_days - self.public_hol - self.al - self.close_personal - self.count_worked_days
            f.write('{}'.format(str(med_leave)).rjust(total_width-len(title_med_leave)))
            f.write('\n')
            # days worked
            worked_days = 'Total days worked'
            f.write(worked_days)
            f.write('{}'.format(str(self.count_worked_days)).rjust(total_width-len(worked_days)))

    def xml_to_xls(self):
        # extract file name
        regex_file = r'.*(RE\d+_\d+.XLS)$'
        file_name = re.search(regex_file, self.url_attn_file).groups()[0]
        
        # create all dirs
        if not os.path.exists('./old-attendance/'):
            os.mkdir('./old-attendance/')
        if not os.path.exists('./payslip/'):
            os.mkdir('./payslip/')
        if not os.path.exists('./new-attendance/'):
            os.mkdir('./new-attendance/')
        if not os.path.exists('./log/'):
            os.mkdir('./log/')

        # copy file to attendance/ dir
        shutil.copy2(self.url_attn_file, './old-attendance/' + file_name)
        input_file = './old-attendance/' + file_name
        output_file = './old-attendance/' + file_name

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

        # extract date
        date_df = df.iloc[3,12]
        regex_dates = r'\d{2}'
        dates_df = re.findall(regex_dates, date_df)
        self.year_df = int('20' + dates_df[0])
        self.month_df = self.get_dict_months()[dates_df[1]]
        self.days_df = int(dates_df[-1])

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
                # initialise counters for num of closed days and total days worked
                self.count_closed_days = 0
                self.count_worked_days = 0

                # iterate through dates in first half of month
                for j, row in df.iloc[25*(i-1) + 8:25*i -1].iterrows():
                    date.append(row[0])
                    day.append(row[1])
                    timings = []
            
                    # check if closed day
                    if row[1] in self.closed_days:
                        self.count_closed_days += 1

                    # collect all timings
                    for k in range(2,8):
                        try:
                            # convert timings into time objs
                            time_str = row[k].split(':')
                            time = dt.time(int(time_str[0]), int(time_str[1]))
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
                            start_time = time[0]
                            end_time = time[1]
                    
                    # if no timing, set time_in and time_out to 0
                    if len(timings) == 0:
                        time_in.append('-')
                        time_out.append('-')
                    # if single time value, use 12 PM as demarcation if time in/out
                    elif len(timings) == 1:
                        # count as working day
                        self.count_worked_days += 1

                        if timings[0] > dt.time(12,0):
                            time_out.append(str(timings[0]))
                            time_in.append(str(start_time))
                        else:
                            time_in.append(str(timings[0]))
                            time_out.append(str(end_time))
                    # for all other lengths, find min/max
                    else:
                        # count as working day
                        self.count_worked_days += 1
                        
                        time_in.append(str(min(timings)))
                        time_out.append(str(max(timings)))
              
                # iterate through latter half of month
                for l, row in df.iloc[25*(i-1) + 8:25*i -1].iterrows():
                    # check if empty date, terminate loop
                    if type(row[8]) == float:
                        break
            
                    # check if closed day
                    if row[1] in self.closed_days:
                        self.count_closed_days += 1

                    # continue if got date
                    date.append(row[8])
                    day.append(row[9])
                    timings = []
            
                    # collect all timings
                    for m in range(10,16):
                        try:
                            # convert timings into time objs
                            time_str = row[m].split(':')
                            time = dt.time(int(time_str[0]), int(time_str[1]))
                        except ValueError:
                            continue
            
                        # check no duplicates
                        if time not in timings:
                            timings.append(time)
                        else:
                            continue

                    # decide which start time to use depending on day
                    for days, time in self.working_hours.items():
                        if row[9] in days:
                            start_time = time[0]
                            end_time = time[1]
                            
                    # if no timing, set time_in and time_out to 0
                    if len(timings) == 0:
                        time_in.append('-')
                        time_out.append('-')
                    # if single time value, use 12 PM as demarcation if time in/out
                    elif len(timings) == 1:
                        # count as working day
                        self.count_worked_days += 1

                        if timings[0] > dt.time(12,0):
                            time_out.append(str(timings[0]))
                            time_in.append(str(start_time))
                        else:
                            time_in.append(str(timings[0]))
                            time_out.append(str(end_time))
                     # for all other lengths, find min/max
                    else:
                        # count as working day
                        self.count_worked_days += 1

                        time_in.append(str(min(timings)))
                        time_out.append(str(max(timings)))
                
                break
            else:
                continue

        # create new dataframe and return
        data = {'date': date, 'day': day, 'time_in': time_in, 'time_out': time_out}
        df_emp = pd.DataFrame(data)
        df_emp['late_arr_mins'] = df_emp.apply(self.calculate_late_arr_mins, axis=1)
        df_emp['overtime_mins'] = df_emp.apply(self.calculate_overtime_mins,axis=1)
        df_emp['early_dep_mins'] = df_emp.apply(self.calculate_early_dep_mins,axis=1)
        df_emp['deduct_late_arr'] = df_emp.late_arr_mins.apply(self.deduct_late_arr)
        df_emp['deduct_early_dep'] = df_emp.early_dep_mins.apply(self.deduct_early_dep)
        df_emp['pay_overtime'] = df_emp.overtime_mins.apply(self.pay_overtime)

        # calculate mins and charges
        self.ot_mins = df_emp.overtime_mins.sum()
        self.misc_deduct_mins = df_emp.late_arr_mins.sum() + df_emp.early_dep_mins.sum()
        self.ot_rm = round(df_emp.pay_overtime.sum(), 2)
        self.misc_deduct_rm = round(df_emp.deduct_late_arr.sum() + df_emp.deduct_early_dep.sum(), 2)

        # write to file
        df_emp.to_csv('./log/{}_attendance_log.csv'.format(self.biometric_name), index=False) 

        return df_emp
   
    def get_working_hours(self):
        working_hours = {}

        for shift in self.shifts:
            # get dictionary of working days to timings
            working_hours.update(Company.get_shifts()[shift])

        return working_hours
    
    def calculate_late_arr_mins(self, df):
        if df.time_in == '-':
            return 0    
        else:
            # decide which start time to use depending on day
            for days, time in self.working_hours.items():
                if df.day in days:
                    start_time = time[0]

            # check if early
            if dt.datetime.strptime(df.time_in, '%H:%M:%S').time() < start_time:
                return 0
            
            late_arr_secs = dt.timedelta(hours=dt.datetime.strptime(df.time_in,'%H:%M:%S').time().hour,
                                         minutes=dt.datetime.strptime(df.time_in,'%H:%M:%S').time().minute) - dt.timedelta(hours=start_time.hour,
                                                                                                                  minutes=start_time.minute)
            return round(late_arr_secs.seconds / 60)
        
    def calculate_overtime_mins(self,df):
        if df.time_in == '-':
            return 0    
        else:
            # decide which start time to use depending on day
            for days, time in self.working_hours.items():
                if df.day in days:
                    end_time = time[1]

            # check if overtime
            if dt.datetime.strptime(df.time_out, '%H:%M:%S').time() < end_time:
                return 0
            
            ot_secs = dt.timedelta(hours=dt.datetime.strptime(df.time_out,'%H:%M:%S').time().hour,
                                         minutes=dt.datetime.strptime(df.time_out,'%H:%M:%S').time().minute) - dt.timedelta(hours=end_time.hour,
                                                                                                                  minutes=end_time.minute)
            return round(ot_secs.seconds / 60)
        
    def calculate_early_dep_mins(self,df):
        if df.time_in == '-':
            return 0   
        else:
            # decide which start time to use depending on day
            for days, time in self.working_hours.items():
                if df.day in days:
                    end_time = time[1]

            # check if early dep
            if dt.datetime.strptime(df.time_out, '%H:%M:%S').time() > end_time:
                return 0
            
            early_secs = dt.timedelta(hours=end_time.hour, minutes=end_time.minute) - dt.timedelta(hours=dt.datetime.strptime(df.time_out,'%H:%M:%S').time().hour,
                                                                                                   minutes=dt.datetime.strptime(df.time_out,'%H:%M:%S').time().minute)
            return round(early_secs.seconds / 60)

    def deduct_late_arr(self,mins):
        return self.charge_late * mins
    
    def deduct_early_dep(self,mins):
        return self.charge_early * mins

    def pay_overtime(self,mins):
        return self.charge_ot * mins
    
    @classmethod
    def get_dict_months(cls):
        return cls.dict_months
    

if __name__ == '__main__':
    from employee import Employee

    emp = Employee(23, 'Fatin Nurimah','Nurin','950323-34-3433',
                   '13',1000,1,1,1)
    
    url = 'old-attendance/RE001_06.XLS'
    Payslip(url, emp, 0, 0, 0, 'NIL')