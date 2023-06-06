import datetime
import math

import controller
import pandas as pd
from openpyxl import load_workbook
from openpyxl import Workbook
import view
from tkinter import filedialog as fd
import db
import os
import xlwt
import xlsxwriter
import datetime
from datetime import time


def Create_salary_in_one_month(date1, date2, month):
    date1 = int(date1)
    date2 = int(date2)
    salary_all = {}
    result = []
    data = db.Select_work_days_join_workers(month)
    for item in data:
        name = str(item[0])
        work_time = datetime.datetime(2000, 1, 1, 9, 0)
        work_day = 0
        salary = 0
        elabor_time = datetime.datetime(2000, 1, 1, 0, 0)
        elabor_salary = 0
        wage = item[1]
        elab = item[2]
        houre_wage = wage / 8
        result = []
        for i in range(3+date1, 4+date2):
            temp = item[i].split('.')
            if len(temp) > 1:
                curent_time = datetime.datetime(2000, 1, 1, int(temp[0]), int(temp[1]))
                if curent_time.hour < work_time.hour:
                    day_wage = (float(item[i]) - 1) * houre_wage
                    salary += day_wage
                    work_day += 1
                else:
                    salary += wage
                    elab_time = curent_time - work_time
                    elabor_time += elab_time
                    work_day += 1
        elab_time = str(elabor_time.time()).replace(':', '.').replace('.00', '')
        month_salary = salary + round(float(elab_time) * elab, 2)
        # print(f"Рабочих дней - {work_day}")
        # print(f"Зарплата - {round(salary, 2)}")
        # print(f"Общее время переработки - {elabor_time.time()}")
        # print(f"Зарплата за переработку - {round(float(elab_time) * elab, 2)}")
        # print(f"Зарплата за месяц - {month_salary}")
        # print("------------------------------------")
        controller.Write_salary_worker(item[0], month_salary, month)

        result.append(work_day) #Кол-во отработаных дней
        result.append(elab_time) #Сумма часов переработки
        result.append(round(salary, 2)) #Зарплата за отработанные дни
        result.append(round(float(elab_time) * elab, 2)) #Зарплата за переработку
        result.append(round(month_salary, 2)) #Зарплата за месяц
        print(name)
        print(result)
        salary_all[name] = result
    return salary

sallary = Create_salary_in_one_month('01', '31', '05 2023')
for key, val in sallary.items():
    print(key)
    print(val)





