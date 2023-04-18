import pandas as pd
from openpyxl import load_workbook
from openpyxl import Workbook
import view
from tkinter import filedialog as fd
import db
import os
import xlwt
import xlsxwriter

def Workers():
    workers = []
    temp = db.Read_workers()
    for item in temp:
        workers.append(item[0])
    return workers


def Create_db():
    file = fd.askopenfilename()
    wb = load_workbook(file)
    sheet = wb.worksheets[0]
    ar = {}  # общий массив данных
    result = []
    temp = []
    for i in range(6, sheet.max_row + 1):
        for j in range(2, 21):
            data = sheet.cell(row=i, column=j).value
            if (data == '' or data is None or data == '\n' or 'parsec' in data or '/' in data):
                continue
            if data == '--\n--\n--':
                temp.append('0,0,0')
            else:
                temp.append(data.replace("\n", ', ').replace(':', '.').replace(' ', ''))
        if i%2 == 0:
            continue
        else:
            if len(temp)>0:
                result.append(list(temp))
        temp.clear()
    for item in result:
        item[0] = item[0].replace(',', ' ')
        for i in range(1, len(item)):
            item[i] = (item[i].split(',')).pop(2).replace('--', '0')
        if len(item) < 32:
            for i in range(len(item), 32):
                item.append('0')
        key = item[0]
        item.pop(0)
        ar[key] = item
    return ar


def Insert_db_data():
    ar = Create_db()
    db.Create_table_workers()
    workers = db.Read_workers()
    add_workers = []
    if len(workers) == 0:
         for keys, val in ar.items():
             db.Add_worker(keys, 0, 0)
    else:
        for item in ar.keys():
            flag = 0
            for val in workers:
                if item in val[0]:
                    flag+=1
                    break
            if flag == 0:
                add_workers.append(item)
    if add_workers:
        view.Add_workers_form(add_workers)
    check_tables = db.Select_work_days(view.db_date)
    if check_tables == 1 or check_tables == 0:
        db.Create_new_table_work_day(view.db_date)
        for item in list(ar):
            db.Input_new_workdays(view.db_date, item)
    else:
        ar = list(ar.items())
        for item in ar:
            flag = 0
            for val in check_tables:
                if item[0] in val[0]:
                    flag+=1
                    break
            if flag > 0:
                db.Update_new_workdays(view.db_date, item)
            else:
                db.Input_new_workdays(view.db_date, item)

def Create_salary():
    salary = {}
    work_days = db.Select_work_days(view.db_date)
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
                for i in range(1, len(day)):
                    wage = 0
                    elabor = 0
                    res =[]
                    if float(day[i]) ==0:
                        wage = 0
                    elif float(day[i]) > 9.10:
                        elabor = (float(day[i]) - 9) * float(name[2])
                        wage = name[1]
                        work_day += 1
                        elab_day += 1
                        elab_time += (float(day[i]) - 9)
                        sal_elabor+= (float(day[i]) - 9)*name[2]
                    elif float(day[i]) <= 9.10:
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
    return salary


def Create_salary_for_one(data):
    salary = {}
    wag = db.Read_worker(data[0])
    temp_days = data[1].split(';')
    work_day = 0
    sal = 0
    elab_day = 0
    elab_time = 0
    sal_elabor = 0
    for i in range(len(temp_days)):
        wage = 0
        elabor = 0
        res =[]
        if (temp_days[i] != '--,--,--' and len(temp_days[i])>2):
            times = temp_days[i].split(",")
            if times[2] != '--':
                work_day += 1
                if round(float(times[2])) <= 9:
                    wage = ((int(wag[0][1]))/8) * float(times[2])
                else:
                    elab_day+=1
                    wage = int(wag[0][1])
                    elabor = (round(float(times[2])) - 9)*(int(wag[0][2]))
                    elab_time += (float(times[2]) - 9)
                    sal_elabor += elabor
        sal += wage
        res = []
        res.append(work_day)
        res.append(round(sal, 2))
        res.append(elab_day)
        res.append(round(elab_time, 2))
        res.append(round(sal_elabor, 2))
        salary[data[0]] = res

    return salary

def Write_salary_worker(name, salary):
    salary_workers = []
    salary_workers = db.Read_salary_workers(view.db_date)
    if salary_workers == 0 or len(salary_workers)==0:
        db.Create_table_salarys()
        db.Add_salary_worker(name, salary)
    else:
        for item in salary_workers:
            if name == item[0]:
                db.Update_salary_workers(name,salary)
                break
        count = 0
        if name not in item:
            db.Add_salary_worker(name, salary)
            count += 1


def Read_last_month_salary(name):
    last_month = []
    date_now = view.db_date.split()

    if date_now[0] == '01':
        last_month.append(12)
        last_month.append(int(date_now[1])-1)
    else:
        str_date = '0'+str(int(date_now[0])-1)
        last_month.append(str_date)
        last_month.append(date_now[1])
        last_month = " ".join(last_month)
        last_month_salarys = db.Read_salary_workers(last_month)
        if last_month_salarys == 1 or last_month_salarys == 0:
            return 0
        else:
            for item in last_month_salarys:
                if item[0] == name:
                    if item[1] < 0:
                        return item[1]*(-1)
                    else:
                        return item[1]


def Print_all(data, avans):
    date_now = view.db_date.split()
    last_month = []
    if date_now[0] == '01':
        last_month.append(12)
        last_month.append(int(date_now[1]) - 1)
    else:
        str_date = '0' + str(int(date_now[0]) - 1)
        last_month.append(str_date)
        last_month.append(date_now[1])
        last_month = " ".join(last_month)
    last = db.Read_salary_workers(last_month)
    for keys, val in data.items():
        file.write(f"{keys}\n\n")
        last_month_salary = 0
        for item in last:
            if keys == item[0]:
                if item[1] < 0:
                    avan=item[1]*(-1)
        file.write(f"Долг за прошлый месяц: {avan}\n")
        file.write(f"Отработано: - {val[2]} дней\n")
        file.write(f"Заработал: {val[1]} р.\n")
        file.write(f"Аванс: {avans} р.\n ")
        file.write(f"Часов переработки: {val[3]}\n")
        file.write(f"Заработал за перерработку: {val[4]} р.\n")
        file.write(f"Итого за месяц - {round(float(val[2])+float(val[4])-float(avans)-float(avan), 2)} р.\n\n")
        file.write("******************************************************************\n")
    file.close()
    os.startfile("temp.txt", "print")



def Save_to_excel(salarys, avans):
    date_now = view.db_date.split()
    last_month = []

    if date_now[0] == '01':
        last_month.append(12)
        last_month.append(int(date_now[1]) - 1)
    else:
        str_date = '0' + str(int(date_now[0]) - 1)
        last_month.append(str_date)
        last_month.append(date_now[1])
        last_month = " ".join(last_month)
    last = db.Read_salary_workers(last_month)

    book = xlsxwriter.Workbook(f"Зарплата за {view.db_date}.xlsx")
    sheet = book.add_worksheet("Зарплата")
    row = 0
    column = 0
    content = ["№", "Имя", "Рабочие дни", "Часы перерработки", "Зарплата за месяц", "Зарплата за переработку", "Аванс",
               "Долг за прошлый месяц", "Итого на руки"]
    for item in content:
        sheet.write(row, column, item)
        column += 1

    row = 1
    column = 0
    result = []
    for keys, val in salarys.items():
        values = []
        values.append(row)
        values.append(keys)
        values.append(val[0])
        values.append(val[3])
        values.append(val[1])
        values.append(val[4])
        values.append(float(avans))
        if last !=0:
            for item in last:
                if keys == item[0]:
                    values.append(item[1])
                    if item[1] < 0:
                        app = float(val[1]) + float(val[4]) + float(item[1]) - float(avans)
                        values.append(round(app, 2))
                    else:
                        app = float(val[1]) + float(val[4]) + float(item[1]) - float(avans)
                        values.append(round(app, 2))
        else:
            values.append(0)
            values.append(float(val[1]) + float(val[4]) - float(avans))
        row+=1
        result.append(values)
    row = 1

    for item in result:
        column = 0
        for val in item:
            sheet.write(row, column, val)
            column += 1
        row+=1
    book.close()



    #         sheet1.write(i+1, 0, i+1)
    #         sheet1.write(i+1, 1, key)
    #         sheet1.write(i+1, 2, val[0])
    #         sheet1.write(i+1, 3, val[3])
    #         sheet1.write(i+1, 4, val[1])
    #         sheet1.write(i+1, 5, val[4])
    #         sheet1.write(i+1, 6, avans)
    #         sheet1.write(i+1, 7, "Долг за прошлый месяц")
    #         sheet1.write(i+1, 8, (round(float(val[1])+float(val[4])-float(avans))))


















