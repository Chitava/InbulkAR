import sqlite3
import customtkinter
import view


def Create_table_work_day(add_date):
    try:
        con = sqlite3.connect("database/inbulk.db")
        cursor = con.cursor()
        q = """CREATE TABLE IF NOT EXISTS "{}" (name TEXT PRIMARY KEY, data TEXT)""".format(add_date)
        cursor.execute(q)
        cursor.close()
    except sqlite3.Error as error:
        view.Messagebox("Внимание", error)


def Input_workdays(name, res):
    for key, val in res.items():
        value = ";".join(val)
        try:
            con = sqlite3.connect("database/inbulk.db")
            cursor = con.cursor()
            querry = f"""INSERT INTO '{name}' (name, data) VALUES (?, ?)"""
            param =(key, value)
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
        return 1
        cursor.close()

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


