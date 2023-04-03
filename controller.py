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
    # sheet = wb.get_sheet_by_name('Page 1')
    sheet = wb.worksheets[0]
    # df = pd.DataFrame(sheet.values)
    ar = {}  # общий массив данных
    result = []
    temp = []
    # rows = sheet.max_row
    # cols = sheet.max_column
    for i in range(6, sheet.max_row + 1):
        # место 21 sheet.max_column
        for j in range(1, 21):
            data = sheet.cell(row=i, column=j).value
            if data == '' or data is None:
                continue
            if data == '--\n--\n--':
                temp.append('--,--,--')
            else:
                temp.append(data.replace("\n", ', ').replace(':', '.').replace(' ', ''))
        if len(temp)>0:
            result.append(list(temp))
        temp.clear()
    for item in result:
        for val in item:
            if 'parsec' in val:
                result.remove(item)
    for i in range(len(result) - 1):
        if i % 2 == 0:
            temp.append(result[i] + result[i + 1])
    for i in range(len(temp)):
        if len(temp[i]) == 0:
            continue
        else:
            temp_data = []
            keys = temp[i][1].replace(',', ' ')
            temp[i].pop(0)
            temp[i].pop(0)
            for item in temp[i]:
                temp_data.append(item)
            if (len(temp_data) < 31):
                lenth_data = 31 - len(temp_data)
                for i in range(lenth_data):
                    temp_data.append('--,--,--')
            ar[keys] = temp_data
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
            for val in workers:
               if item in val[0]:
                    break
            else:
                add_workers.append(item)
    check_tables = db.Select_work_days(view.db_date)
    if check_tables == 1 or check_tables == 0:
        db.Create_table_work_day(view.db_date)
        db.Input_workdays(view.db_date, ar)
    else:
        db.Update_workdays(view.db_date, ar)
    if len(add_workers) != 0:
        view.Add_workers_form(add_workers)
    for keys,val in ar.items():
        flag = 0
        for item in check_tables:
            if keys == item[0]:
                flag+=1
                break
        if flag > 0:
            db.Update_workdays_one_worker(view.db_date, keys, val)
        else:
           db.Input_workdays_one_worker(view.db_date, keys, val)


def Create_salary():
    salary = {}
    work_days = db.Select_work_days(view.db_date)
    all_workers = db.Read_workers()

    for name in all_workers:
        print(name[0])
        for day in work_days:
            print(day[0])
            temporery = []
            if name[0] == day[0]:
                temp_days = day[1].split(';')
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
                            if float(times[2]) <= 9:
                                wage = ((int(name[1]))/8) * float(times[2])
                            else:
                                elab_day+=1
                                wage = int(name[1])
                                elabor = (float(times[2]) - 9)*(int(name[2]))
                                elab_time += (float(times[2]) - 9)
                                sal_elabor += elabor
                    sal += wage
                    res = []
                    res.append(work_day)
                    res.append(round(sal, 2))
                    res.append(elab_day)
                    res.append(round(elab_time, 2))
                    res.append(round(sal_elabor, 2))

                    salary[name[0]] = res

    sorted_salary = dict(sorted(salary.items()))
    for key, val in sorted_salary.items():
        print(key)
    now = db.Read_salary_workers(view.db_date)
    # print(sorted_salary)
    # print(now)
    # for keys,val in sorted_salary.items():
    #     flag = 0
    #     for item in now:
    #         print(keys)
    #         print(item)
    #         if keys == item[0]:
    #             flag +=1
    #             break
    #
    #     if flag:
    #         db.Update_salary_workers(keys, (val[1]+val[4]))
    #     else:
    #         db.Add_salary_worker(keys, (val[1]+val[4]))

    return sorted_salary


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


















