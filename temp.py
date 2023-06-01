import pandas as pd
from openpyxl import load_workbook
from openpyxl import Workbook
import view
from tkinter import filedialog as fd
import db
import os
import xlwt
import xlsxwriter


def Create_salary_in_one_month(date1, date2, month):
    date1 = int(date1)
    date2 = int(date2)
    salary = {}
    work_days = db.Select_work_days(month)
    all_workers = db.Read_workers()
    for name in all_workers:
        for day in work_days:
            temporery = []
            if name[0] == day[0]:
                work_day = 0
                sal = 0
                elab_day = 0
                elab_time = 0
                sal_elabor = 0
                for i in range(date1, date2+1):
                    wage = 0
                    elabor = 0
                    res =[]
                    if float(day[i]) ==0:
                        wage = 0
                    elif float(day[i]) > 9:
                        elabor = (float(day[i]) - 9) * float(name[2])
                        wage = name[1]
                        work_day += 1
                        elab_day += 1
                        elab_time += (float(day[i]) - 9)
                        sal_elabor+= (float(day[i]) - 9)*name[2]
                    elif float(day[i]) <= 9:
                        wage = (name[1]/8)*(float(day[i])-1)
                        work_day+=1
                    sal += round(wage, 2)
                    res = []
                    res.append(work_day)
                    res.append(round(sal, 2))
                    res.append(elab_day)
                    res.append(round(elab_time, 2))
                    res.append(round(sal_elabor, 2))
                salary[name[0]] = res
                Write_salary_worker(name[0], round(sal+sal_elabor, 2), month)
    return salary

Create_salary_in_one_month('01', '31','05 2023')
