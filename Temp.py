import pandas as pd
from openpyxl import load_workbook
from openpyxl import Workbook
import view
from tkinter import filedialog as fd
import db
import os
import xlwt
import xlsxwriter
import controller

view.db_date ='04 2023'
def Insert_db_data():
    ar = controller.Create_db()
    db.Create_table_workers()
    workers = db.Read_workers()
    db.Create_new_table_work_day(view.db_date)
    work_days = db.Select_work_days(view.db_date)
    add_workers = []
    for key, val in ar.items():
        print(key)
        print(val)
    for key, val in ar.items():
        result = []
        result.append(key)
        result = []
        result.append(key)
        for item in val:
            temp = item.split(',')
            if len(temp) != 3:
                result.append('0.0')
            else:
                if (temp[2] == '--' or temp[2] == ''):
                    result.append('0.0')
                else:
                    result.append(float(temp[2]))
        flag = 0
        work_days = db.Select_work_days(view.db_date)
        for i in range(len(work_days)):
            if key in work_days[i][0]:
                flag+=1
                break
        if flag:
            db.Update_new_workdays(view.db_date, result)
        else:
            db.Input_new_workdays(view.db_date, result)
        flag = 0
        for i in range(len(workers)):
            if key in workers[i][0]:
                flag+=1
                break
        if flag:
            view.Add_workers_form(key)






Insert_db_data()