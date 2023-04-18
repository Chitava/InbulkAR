import sqlite3
import customtkinter
import view


# def Create_table_work_day(add_date):
#     try:
#         con = sqlite3.connect("database/inbulk.db")
#         cursor = con.cursor()
#         q = """CREATE TABLE IF NOT EXISTS "{}" (name TEXT PRIMARY KEY, data TEXT)""".format(add_date)
#         cursor.execute(q)
#         cursor.close()
#     except sqlite3.Error as error:
#         view.Messagebox("Внимание", error)

def Create_new_table_work_day(add_date):
    try:
        con = sqlite3.connect("database/inbulk.db")
        cursor = con.cursor()
        q = """CREATE TABLE IF NOT EXISTS "{}" 
        (name TEXT PRIMARY KEY UNIQUE, 
        '01' TEXT,
        '02' TEXT,
        '03' TEXT,
        '04' TEXT,
        '05' TEXT,
        '06' TEXT,
        '07' TEXT,
        '08' TEXT,
        '09' TEXT,
        '10' TEXT,
        '11' TEXT,
        '12' TEXT,
        '13' TEXT,
        '14' TEXT,
        '15' TEXT,
        '16' TEXT,
        '17' TEXT,
        '18' TEXT,
        '19' TEXT,
        '20' TEXT,
        '21' TEXT,
        '22' TEXT,
        '23' TEXT,
        '24' TEXT,
        '25' TEXT,
        '26' TEXT,
        '27' TEXT,
        '28' TEXT,
        '29' TEXT,
        '30' TEXT,
        '31' TEXT
        )""".format(add_date)
        cursor.execute(q)
        cursor.close()
    except sqlite3.Error as error:
        view.Messagebox("Внимание", error)

def Input_new_workdays(name, res):
        res[1].insert(0,res[0])
        try:
            con = sqlite3.connect("database/inbulk.db")
            cursor = con.cursor()
            querry = f"""INSERT INTO '{name}' (name, '01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12', '13', '14', '15', '16', 
            '17', '18', '19', '20', '21', '22', '23', '24', '25', '26', '27', '28', '29', '30', '31') VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?,
             ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"""
            cursor.execute(querry,res[1])
            con.commit()
            cursor.close()
        except sqlite3.Error as error:
            view.Messagebox("Внимание Input", error)
            cursor.close()


def Update_new_workdays(name, res):
        res[1].append(res[0])
        try:
            con = sqlite3.connect("database/inbulk.db")
            cursor = con.cursor()
            querry = f"""UPDATE '{name}' SET '01' = ?, '02' = ?, '03'= ?, '04'= ?, '05'= ?, '06'= ?, '07' = ?, '08'= ?,
             '09'= ?, '10'= ?, '11'= ?, '12'= ?, '13'= ?, '14'= ?, '15'= ?, '16'= ?, '17'= ?, '18'= ?, '19'= ?, '20'= ?,
              '21'= ?, '22'= ?, '23'= ?, '24'= ?, '25'= ?, '26'= ?, '27'= ?, '28'= ?, '29'= ?, '30'= ?, '31'= ? where name = ?"""
            cursor.execute(querry, res[1])
            con.commit()
            cursor.close()
        except sqlite3.Error as error:
            view.Messagebox("Внимание Update", error)
            cursor.close()














# def Input_workdays(name, res):
#     for key, val in res.items():
#         value = ";".join(val)
#         try:
#             con = sqlite3.connect("database/inbulk.db")
#             cursor = con.cursor()
#             querry = f"""INSERT INTO '{name}' (name, data) VALUES (?, ?)"""
#             param =(key, value)
#             cursor.execute(querry, param)
#             con.commit()
#             cursor.close()
#         except sqlite3.Error as error:
#             view.Messagebox("Внимание Input", error)
#             cursor.close()


def Input_workdays_one_worker(name_db, name, res):
    res=";".join(res)
    try:
        con = sqlite3.connect("database/inbulk.db")
        cursor = con.cursor()
        querry = f"""INSERT INTO '{name_db}' (name, data) VALUES (?, ?)"""
        param =(name, res)
        cursor.execute(querry, param)
        con.commit()
        cursor.close()
    except sqlite3.Error as error:
        view.Messagebox("Внимание Input", error)
        cursor.close()



def Update_workdays(name, res):
    for key, value in res.items():
        value = ";".join(value)
        try:
            con = sqlite3.connect("database/inbulk.db")
            cursor = con.cursor()
            querry = f"""UPDATE '{name}' SET data = ? where name = ?"""
            param = (value, key)
            cursor.execute(querry, param)
            con.commit()
            cursor.close()
        except sqlite3.Error as error:
            view.Messagebox("Внимание Update", error)
            cursor.close()


def Update_workdays_one_worker(name_db, name, res):
    res = ";".join(res)
    try:
        con = sqlite3.connect("database/inbulk.db")
        cursor = con.cursor()
        querry = f"""UPDATE '{name_db}' SET data = ? where name = ?"""
        param = (res, name)
        cursor.execute(querry, param)
        con.commit()
        cursor.close()
    except sqlite3.Error as error:
        view.Messagebox("Внимание Update", error)
        cursor.close()


def Create_table_workers():
    con = sqlite3.connect("database/inbulk.db")
    cursor = con.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS workers(name text PRIMARY KEY, wagerate FLOAT, processingrate FLOAT);")
    cursor.close()


def Create_table_salarys():
    con = sqlite3.connect("database/inbulk.db")
    cursor = con.cursor()
    cursor.execute(f"CREATE TABLE IF NOT EXISTS 'salarys {view.db_date}' (name text PRIMARY KEY, salary FLOAT);")
    cursor.close()


def Add_salary_worker(name, salary):
    try:
        con = sqlite3.connect("database/inbulk.db")
        cursor = con.cursor()
        sql_insert = f"INSERT INTO 'salarys {view.db_date}' (name, salary) VALUES (?, ?);"
        param = (name, salary)
        cursor.execute(sql_insert, param)
        con.commit()
        cursor.close()
    except sqlite3.Error as error:
        view.Messagebox("Внимание", f'{error}\n {name}')
        cursor.close()

def Read_salary_workers(date_now):
    try:
        con = sqlite3.connect("database/inbulk.db")
        cursor = con.cursor()
        cursor.execute(f"select * from 'salarys {date_now}';")
        result = cursor.fetchall()
        cursor.close()
        return result
    except:
        cursor.close()
        return 0


def Update_salary_workers(name, salary):
    try:
        con = sqlite3.connect("database/inbulk.db")
        cursor = con.cursor()
        querry = f"UPDATE 'salarys {view.db_date}' SET salary = ? where name = ?;"
        param = (salary, name)
        cursor.execute(querry, param)
        con.commit()
        cursor.close()
    except sqlite3.Error as error:
        view.Messagebox("Внимание Update", error)
        cursor.close()

def Read_workers():
    con = sqlite3.connect("database/inbulk.db")
    cursor = con.cursor()
    cursor.execute("""select * from workers""")
    result = cursor.fetchall()
    cursor.close()
    return result


def Read_worker(name):
    con = sqlite3.connect("database/inbulk.db")
    cursor = con.cursor()
    cursor.execute(f"select * from workers where name = '{name}'")
    result = cursor.fetchall()
    cursor.close()
    return result


def Add_worker(name, wagerate, processingrate):
    try:
        con = sqlite3.connect("database/inbulk.db")
        cursor = con.cursor()
        sql_insert = """INSERT INTO workers (name, wagerate, processingrate) VALUES (?, ?, ?);"""
        param = (name, wagerate, processingrate)
        cursor.execute(sql_insert, param)
        con.commit()
        cursor.close()
    except sqlite3.Error as error:
        view.Messagebox("Внимание", error)
        cursor.close()



def Edit_worker(wagerate, processingrate, name):
    name = name.get()
    wage = wagerate.get()
    proces = processingrate.get()
    try:
        con = sqlite3.connect("database/inbulk.db")
        cursor = con.cursor()
        sql_edit = f"UPDATE workers set wagerate = '{wage}', processingrate = '{proces}' where name = '{name}'"
        cursor.execute(sql_edit)
        con.commit()
        view.Messagebox("Операция выполнена успешно", "Запись успешно отредактирована")
        cursor.close()
    except sqlite3.Error as error:
        view.Messagebox("Внимание", error)
        cursor.close()
    view.Workers()


def Del_worker(name):
    name = name.get()
    try:
        con = sqlite3.connect("database/inbulk.db")
        cursor = con.cursor()
        sql_delete = """DELETE FROM workers where name = ?;"""
        param = (name,)
        cursor.execute(sql_delete, param)
        con.commit()
        view.Messagebox("Операция выполнена успешно", "Сотрудник уволен")
        cursor.close()
    except sqlite3.Error as error:
        view.Messagebox("Внимание", error)
        cursor.close()
    view.Workers()


def Add_record(names, wagerates, processingrates):
    # if (isinstance(names, str)):
    #     name = names
    # else:name=names.get()
    # if (isinstance(wagerates, int)):
    #     wagerate = wagerates
    # elif (isinstance(wagerates, float)):
    #     wagerate = wagerates
    # else:wagerate=wagerates.get()

    if (isinstance(processingrates, int)):
        processingrate = processingrates
    elif (isinstance(processingrates, float)):
        processingrate = processingrates
    else:processingrate=processingrates.get()
    Create_table_workers()
    try:
        con = sqlite3.connect("database/inbulk.db")
        cursor = con.cursor()
        sql_insert = """INSERT INTO workers (name, wagerate, processingrate) VALUES (?, ?, ?);"""
        param = (names, wagerates, processingrates)
        cursor.execute(sql_insert, param)
        con.commit()
        cursor.close()
        view.Messagebox("Операция выполнена успешно", "Сотрудник добавлен")
    except sqlite3.Error as error:
        view.Messagebox("Внимание", error)
        cursor.close()

def Select_work_days(add_date):
    try:
        con = sqlite3.connect("database/inbulk.db")
        cursor = con.cursor()
        querry = f"""Select * from '{add_date}' """
        cursor.execute(querry)
        records = cursor.fetchall()
        cursor.close()
        return records
    except sqlite3.Error as error:
        cursor.close()
        return 1


