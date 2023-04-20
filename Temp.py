import pandas as pd
from openpyxl import load_workbook
from openpyxl import Workbook
import view
from tkinter import filedialog as fd
import db
import os
import xlwt
import xlsxwriter





def Create_salary_with_last_month(date1, date2, last_month, month):
    salary = {}
    now_work_days = db.Select_work_days(month)
    last_work_days = db.Select_work_days(last_month)
    all_workers = db.Read_workers()
    for name in all_workers:
        work_day = 0
        sal = 0
        elab_day = 0
        elab_time = 0
        sal_elabor = 0
        wage = 0
        elabor = 0
        res = []
        for day in last_work_days:
            temporery = []
            if name[0] == day[0]:
                work_day = 0
                sal = 0
                elab_day = 0
                elab_time = 0
                sal_elabor = 0
                wage = 0
                elabor = 0
                res = []
                for i in range(int(date1), len(day)):
                    if float(day[i]) ==0:
                        wage = 0
                    elif float(day[i]) > 9:
                        elabor = (float(day[i]) - 9) * float(name[2])
                        wage = int(name[1])
                        work_day += 1
                        elab_day += 1
                        elab_time += (float(day[i]) - 9)
                        sal_elabor+= (float(day[i]) - 9)*name[2]
                    elif float(day[i]) <= 9:
                        wage = (int(name[1])/8)*(float(day[i])-1)
                        work_day+=1
                    sal += round(wage, 2)
        for day in now_work_days:
            if name[0] == day[0]:
                for i in range(1, int(date2)+1):
                    if float(day[i]) == 0:
                        wage = 0
                    elif float(day[i]) > 9:
                        elabor = (float(day[i]) - 9) * float(name[2])
                        wage = name[1]
                        work_day += 1
                        elab_day += 1
                        elab_time += (float(day[i]) - 9)
                        sal_elabor += (float(day[i]) - 9) * name[2]
                    elif float(day[i]) <= 9:
                        wage = (int(name[1])/8) * (float(day[i]) - 1)
                        work_day += 1
                    sal += round(wage, 2)
        res = []
        res.append(work_day)
        res.append(round(sal, 2))
        res.append(elab_day)
        res.append(round(elab_time, 2))
        res.append(round(sal_elabor, 2))
        salary[name[0]] = res
        # Write_salary_worker(name[0], round(sal+sal_elabor, 2), month)
    for key, val in salary.items():
        print(key)
        print(val)


Create_salary_with_last_month('01', '20', '03 2023', '04 2023')