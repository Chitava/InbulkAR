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

def Create_salary_in_one_month_for_one(name, date1, date2, month):
    salary = []
    data = db.Select_work_days_for_one_worker(name, month)
    date1 = int(date1)
    date2 = int(date2)
    salary_all = {}
    result = []
    for item in data:
        name = str(item[0])
        work_time = datetime.datetime(2000, 1, 1, 9, 0)
        work_day = 0
        salary = 0
        elabor_time = datetime.datetime(2000, 1, 1, 0, 0)
        elabor_salary = 0
        all_elab_time = datetime.datetime(2000, 1, 1, 0, 0)
        wage = item[1]
        elab = item[2]
        houre_wage = wage / 8
        result = []
        for i in range(3 + date1, 4 + date2):
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
                    all_elab_time += elab_time
                    work_day += 1

        fin_elab_time =  datetime.time((all_elab_time.day - 1) * 24 + all_elab_time.hour, all_elab_time.minute)
        month_salary = salary + (float(f"{fin_elab_time.hour}.{fin_elab_time.minute}") * elab)
        Write_salary_worker(item[0], month_salary, month)
        result.append(work_day)  # Кол-во отработаных дней
        result.append(f"{fin_elab_time.hour},{fin_elab_time.minute}")  # Сумма часов переработки
        result.append(round(salary, 2))  # Зарплата за отработанные дни
        result.append(float(f"{fin_elab_time.hour}.{fin_elab_time.minute}") * elab)  # Зарплата за переработку
        result.append(round(month_salary, 2))  # Зарплата за месяц
        salary_all[name] = result
    return salary_all

print(Create_salary_in_one_month_for_one("Абдурахманов Фирдавс", "30", "31", "05 2023"))




