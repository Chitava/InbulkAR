import sys
import tkinter
import customtkinter
import os
import controller
import db
from PIL import Image
from tkcalendar import Calendar
from functools import partial
from tkinter import filedialog as fd
import tkcalendar
import datetime




db_date = ''
period = ''
def Start_form():
    start_windows = customtkinter.CTk()
    start_windows.title("Расчет зарплаты INBULK")
    start_windows.geometry("700x450")
    start_windows.resizable(width=False, height=False)

    frame_1 = customtkinter.CTkFrame(master=start_windows, width=10)
    frame_1.pack(fill='both', side="left", anchor="nw", padx=5, pady=5)
    frame_2 = customtkinter.CTkFrame(master=start_windows)
    frame_2.pack(fill='both', pady=5, side="top", anchor="nw", expand=1)
    frame_3 = customtkinter.CTkFrame(master=start_windows, width=10)
    frame_3.pack(fill='both', side="bottom", anchor="nw", pady=5)

    image_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "img")
    logo_image = customtkinter.CTkImage(Image.open(os.path.join(image_path, "name.png")), size=(150, 26))
    exit_image = customtkinter.CTkImage(light_image=Image.open(os.path.join(image_path, "exit.png")),
                                        size=(18, 20))

    exit_button = customtkinter.CTkButton(frame_1, corner_radius=0, height=40, border_spacing=10,
                                          text="Выход",
                                          fg_color="transparent", text_color=("gray10", "gray90"),
                                          hover_color=("gray70", "gray30"),
                                          image=exit_image, anchor="w", command=sys.exit)
    exit_button.grid(row=5, column=0, sticky="ew")

    navigation_frame_label = customtkinter.CTkLabel(frame_1, text="", image=logo_image,
                                                    compound="left",
                                                    font=customtkinter.CTkFont(size=15, weight="bold"))
    navigation_frame_label.grid(row=0, column=0, padx=23, pady=20)

    lable_set = customtkinter.CTkLabel(frame_2, text="Установка даты для работы с базой INBULK", font=customtkinter.CTkFont(family="Arial", size=18, weight="bold"))
    lable_set.pack(pady=20)
    label_tm = customtkinter.CTkLabel(frame_3, text='ver. 1.00', font=customtkinter.CTkFont(size=12))
    label_tm.pack(side='right')
    cal = Calendar(frame_2, selectmode='day', locale="ru_RU")
    cal.pack(pady=20)
    date_button = customtkinter.CTkButton(frame_2, text="Установить",
                                          command=partial(controller.Create_db, cal, start_windows)).pack(pady=20)

    start_windows.mainloop()


def Start():
    def Salary_for_one():
        def Presalary(date1, date2, avans, name):
            str_date1 = date1.get()
            str_date2 = date2.get()
            date1_for_equels = datetime.datetime.strptime(str_date1, '%d-%m-%Y')
            date2_for_equels = datetime.datetime.strptime(str_date2, '%d-%m-%Y')
            day1 = str_date1[:2]
            day2 = str_date2[:2]
            avans = avans.get()
            if avans is None or avans == "":
                avans = 0
            else:
                avans = float(avans)
            name = name.get()
            for i in range(len(str_date1)):
                if str_date1[i] == '-':
                    date1 = str_date1[i + 1:].replace('-', ' ')
                    break
            for i in range(len(str_date2)):
                if str_date2[i] == '-':
                    date2 = str_date2[i + 1:].replace('-', ' ')
                    break
            salary = {}
            for widgets in frame_2.winfo_children():
                widgets.destroy()
            (combobox_var.get())
            if date1_for_equels.month < date2_for_equels.month:
                salary = controller.Create_salary_in_two_month_for_one(name, str(day1), str(day2), date1, date2)
            elif date1_for_equels.month == date2_for_equels.month:
                salary = controller.Create_salary_in_one_month_for_one(combobox_var.get(), int(day1), int(day2), date2)
            else:
                Messagebox("Ошибка", 'Выбран не верный диапазон дат')
            worker = 0
            workdays = 0
            elab_time = 0
            salary_work_days = 0
            salary_elab = 0
            final_salary = 0
            for key, val in salary.items():
                worker = key
                workdays = val[0]
                elab_time = val[1]
                salary_work_days = val[2]
                salary_elab = val[3]
                final_salary = salary_work_days+salary_elab-avans
            name_lbl = customtkinter.CTkLabel(frame_2,
                                                  text=worker,
                                                  font=customtkinter.CTkFont(family="Arial", size=24)).pack(pady=5)
            res_lbl = customtkinter.CTkLabel(frame_2,
                                                 text=f"Отработано {workdays} дней\n"
                                                      f"Часов переработки {elab_time}\n Зарплата {salary_work_days} р.\n "
                                                      f"Зарплата за переработку {salary_elab} р.",
                                                 font=customtkinter.CTkFont(family="Arial", size=16)).pack(pady=20)
            fin_lbl = customtkinter.CTkLabel(frame_2,
                                                 text=f"Итого за месяц: {salary_work_days+salary_elab} р. минус аванс "
                                                      f"{avans} р.\n\n на руки {final_salary} р.",
                                                 font=customtkinter.CTkFont(family="Arial", size=16)).pack(pady=10)


        for widgets in frame_2.winfo_children():
            widgets.destroy()
        workers = db.Read_workers()
        worker = []
        for item in workers:
            worker.append(item[0])
        worker.sort()
        lable_name = customtkinter.CTkLabel(frame_2, text="Выберете сотрудника для расчета",
                                            font=customtkinter.CTkFont(family="Arial", size=18, weight="bold"))
        lable_name.pack(pady=20, expand=True)
        combobox_var = customtkinter.StringVar(value=worker[0])  # set initial value
        combobox_worker = customtkinter.CTkComboBox(master=frame_2, width=300,
                                             values=worker, variable=combobox_var)
        combobox_worker.pack(padx=20, pady=10)


        lable_date = customtkinter.CTkLabel(frame_2, text="Выберете диапазон дат для расчета",
                                            font=customtkinter.CTkFont(family="Arial", size=18, weight="bold"))
        lable_date.pack(pady=20, expand=True)
        date1 = tkcalendar.DateEntry(frame_2, locale='ru', date_pattern='dd-MM-yyyy')
        date1.pack(pady=30, side='left')
        date2 = tkcalendar.DateEntry(frame_2, locale='ru', date_pattern='dd-MM-yyyy')
        date2.pack(padx=10, pady=30, side='left')
        avans = customtkinter.CTkEntry(master=frame_2, placeholder_text="Аванс", width=100)
        avans.pack(padx=10, pady=30, side='left')
        presalar_button = customtkinter.CTkButton(frame_2, text="Расчитать", width=20,
                                                  command=partial(Presalary, date1, date2, avans, combobox_var))
        presalar_button.pack(padx=10, pady=30, side='left')


    def Salary_for_all():
        def Presalary(date1, date2):
            str_date1 = date1.get()
            str_date2 = date2.get()
            date1_for_equels = datetime.datetime.strptime(str_date1, '%d-%m-%Y')
            date2_for_equels = datetime.datetime.strptime(str_date2, '%d-%m-%Y')
            day1 = str_date1[:2]
            day2 = str_date2[:2]
            for i in range(len(str_date1)):
                if str_date1[i] == '-':
                    date1 = str_date1[i + 1:].replace('-', ' ')
                    break
            for i in range(len(str_date2)):
                if str_date2[i] == '-':
                    date2 = str_date2[i + 1:].replace('-', ' ')
                    break
            salary = {}
            for widgets in frame_2.winfo_children():
                widgets.destroy()
            if date1_for_equels.month < date2_for_equels.month:
                salary = controller.Create_salary_with_last_month(int(day1), int(day2), date1, date2)
            elif date1_for_equels.month == date2_for_equels.month:
                salary = controller.Create_salary_in_one_month(int(day1), int(day2), date2)
            else:
                Messagebox("Ошибка",'Выбран не верный диапазон дат')

            full_pay = 0
            sorted(salary.items())
            for keys, val in salary.items():

                # sal = round((float(val[1]) + float(val[4])), 2)
                # controller.Write_salary_worker(keys, sal)#round(sal-last_month_salary, 2)
                name_lbl = customtkinter.CTkLabel(frame_2,
                                                 text=keys,
                                                 font=customtkinter.CTkFont(family="Arial", size=24)).pack(pady=5)
                res_lbl = customtkinter.CTkLabel(frame_2,
                                                 text=f"Отработано {val[0]} дней\n"
                                                      f"Часов переработки {val[1]}\n Зарплата за дни {val[2]}\n "
                                                      f"Зарплата за переработку {val[3]}",
                                                 font=customtkinter.CTkFont(family="Arial", size=16)).pack(pady=20)
                fin_lbl = customtkinter.CTkLabel(frame_2,
                                                 text=f"Итого за месяц: {val[4]}",
                                                 font=customtkinter.CTkFont(family="Arial", size=16)).pack(pady=10)

                full_pay += val[4]
                # controller.Write_salary_worker(keys, round(sal, 2))
            itog_lbl = customtkinter.CTkLabel(frame_2,
                                              text=f"Всего к выдаче: {round(full_pay, 2)}",
                                              font=customtkinter.CTkFont(family="Arial", size=26,
                                                                         weight="bold")).pack(pady=20)
            print_button = customtkinter.CTkButton(frame_2, text="Распечатать",
                                                   command=partial(controller.Print_all, salary))
            print_button.pack(pady=20)
            excel_button = customtkinter.CTkButton(frame_2, text="Сохранить в Excel",
                                                   command=partial(controller.Save_to_excel, salary, date2))
            excel_button.pack(pady=20)


        for widgets in frame_2.winfo_children():
            widgets.destroy()

        lable_date = customtkinter.CTkLabel(frame_2, text="Выберете диапазон дат для расчета",
                                            font=customtkinter.CTkFont(family="Arial", size=18, weight="bold"))
        lable_date.pack(pady=20, expand=True)
        date1 = tkcalendar.DateEntry(frame_2, locale='ru', date_pattern='dd-MM-yyyy')
        date1.pack(pady=30, side='left')
        date2 = tkcalendar.DateEntry(frame_2, locale='ru', date_pattern='dd-MM-yyyy')
        date2.pack(padx=10, pady=30, side='left')
        calculate = customtkinter.CTkButton(frame_2, text="Расчитать", command=partial(Presalary, date1, date2))
        calculate.pack(side='left')



    def Insert_db_date():
        def Insert_date():
            global db_date
            global period
            db_date = cal.get_date()
            period = db_date[:2]
            for i in range(len(db_date)):
                if db_date[i] == '.':
                    db_date = db_date[i+1:].replace('.', ' ')
                    break



        for widgets in frame_2.winfo_children():
            widgets.destroy()
        lable_set = customtkinter.CTkLabel(frame_2, text="Установка даты для работы с базой INBULK",
                                           font=customtkinter.CTkFont(family="Arial", size=18, weight="bold"))
        lable_set.pack(pady=20)
        cal = Calendar(frame_2, selectmode='day', locale="ru_RU")
        cal.pack(pady=20)
        date_button = customtkinter.CTkButton(frame_2, text="Установить",
                                              command=Insert_date).pack(pady=20)



    def Edit_workers():
        for widgets in frame_2.winfo_children():
            widgets.destroy()
        workers = db.Read_workers()
        worker = []
        for item in workers:
            worker.append(item[0])
        worker.sort()
        def Combobox_act(self):
            for item in workers:
                if combobox_var.get() == item[0]:
                    lbl_salary.configure(text=f"Сейчас {item[1]}")
                    lbl_elabor.configure(text=f"Сейчас {item[2]}")

        combobox_var = customtkinter.StringVar(value=worker[0])  # set initial value
        combobox = customtkinter.CTkComboBox(master=frame_2, width=300,
                                             values=worker, variable=combobox_var, command=Combobox_act)
        combobox.pack(padx=20, pady=10)
        lbl_salary = customtkinter.CTkLabel(frame_2, text="", font=customtkinter.CTkFont(size=12))
        lbl_salary.pack()
        entry_salary = customtkinter.CTkEntry(master=frame_2, placeholder_text="Зарплата")
        entry_salary.pack(padx=20)
        lbl_elabor = customtkinter.CTkLabel(frame_2, text="", font=customtkinter.CTkFont(size=12))
        lbl_elabor.pack()
        entry_elaboration = customtkinter.CTkEntry(master=frame_2, placeholder_text="Переработка")
        entry_elaboration.pack(padx=20)
        edit_button = customtkinter.CTkButton(frame_2, text="Сохранить", command=partial(db.Edit_worker,
                                                                                            entry_salary,
                                                                                            entry_elaboration,
                                                                                            combobox_var)).pack(pady=20)
    def Del_worker():

        for widgets in frame_2.winfo_children():
            widgets.destroy()
        temp = db.Read_workers()
        workers = []
        for item in temp:
            workers.append(item[0])
            workers.sort()
        combobox_var = customtkinter.StringVar(value=workers[0])  # set initial value
        combobox = customtkinter.CTkComboBox(master=frame_2, width=300,
                                             values=workers, variable=combobox_var)
        combobox.pack(padx=20, pady=10)
        del_button = customtkinter.CTkButton(frame_2, text="Удалить сотрудника",
                                             command=partial(db.Del_worker, combobox)).pack(pady=20)




    forms_with_date = customtkinter.CTk()
    forms_with_date.title("Расчет зарплаты INBULK")
    forms_with_date.geometry("700x450")
    frame_1 = customtkinter.CTkFrame(master=forms_with_date, width=10)
    frame_1.pack(fill='both', side="left", anchor="nw", padx=5, pady=5)
    frame_2 = customtkinter.CTkScrollableFrame(master=forms_with_date, width=200, height=200)
    frame_2.pack(fill='both', pady=5, side="top", anchor="nw", expand=1)
    frame_3 = customtkinter.CTkFrame(master=forms_with_date, width=10)
    frame_3.pack(fill='both', side="bottom", anchor="nw", pady=5)
    image_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "img")
    logo_image = customtkinter.CTkImage(Image.open(os.path.join(image_path, "name.png")), size=(150, 26))
    home_image = customtkinter.CTkImage(light_image=Image.open(os.path.join(image_path, "home_dark.png")), size=(20, 20))
    add_user_image = customtkinter.CTkImage(light_image=Image.open(os.path.join(image_path, "user_add_dark.png")), size=(20, 20))
    edit_user_image = customtkinter.CTkImage(light_image=Image.open(os.path.join(image_path, "add_user_dark.png")), size=(20, 20))
    del_user_image = customtkinter.CTkImage(light_image=Image.open(os.path.join(image_path, "del_user_dark.png")),
                                             size=(20, 20))
    open_db_image = customtkinter.CTkImage(light_image=Image.open(os.path.join(image_path, "open_db.png")),
                                             size=(18, 20))
    exit_image = customtkinter.CTkImage(light_image=Image.open(os.path.join(image_path, "exit.png")),
                                           size=(18, 20))
    calendar_image = customtkinter.CTkImage(light_image=Image.open(os.path.join(image_path, "calendar.png")),
                                            size=(18, 20))
    navigation_frame_label = customtkinter.CTkLabel(frame_1, text="", image=logo_image,
                                                         compound="left",
                                                         font=customtkinter.CTkFont(size=15, weight="bold"))
    navigation_frame_label.grid(row=0, column=0, padx=23, pady=20)
    set_data = customtkinter.CTkButton(frame_1, corner_radius=0, height=40, border_spacing=10,
                                      text="Установить дату",
                                      fg_color="transparent", text_color=("gray10", "gray90"),
                                      hover_color=("gray70", "gray30"),
                                      image=calendar_image, anchor="w", command=Insert_db_date)
    set_data.grid(row=1, column=0, sticky="ew")
    open_db = customtkinter.CTkButton(frame_1, corner_radius=0, height=40, border_spacing=10,
                                         text="Записать новые данные",
                                         fg_color="transparent", text_color=("gray10", "gray90"),
                                         hover_color=("gray70", "gray30"),
                                         image=open_db_image, anchor="w", command=controller.Insert_db_data)
    open_db.grid(row=2, column=0, sticky="ew")
    pay_button = customtkinter.CTkButton(frame_1, corner_radius=0, height=40, border_spacing=10,
                                          text="Расчет сотрудника",
                                          fg_color="transparent", text_color=("gray10", "gray90"),
                                          hover_color=("gray70", "gray30"),
                                          image=home_image, anchor="w", command=Salary_for_one)
    pay_button.grid(row=3, column=0, sticky="ew")
    pays_button = customtkinter.CTkButton(frame_1, corner_radius=0, height=40, border_spacing=10,
                                                  text="Расчет всех",
                                                  fg_color="transparent", text_color=("gray10", "gray90"),
                                                  hover_color=("gray70", "gray30"),
                                                  image=home_image, anchor="w", command=Salary_for_all)
    pays_button.grid(row=4, column=0, sticky="ew")
    add_button = customtkinter.CTkButton(frame_1, corner_radius=0, height=40, border_spacing=10,
                                          text="Добавление сотрудника",
                                          fg_color="transparent", text_color=("gray10", "gray90"),
                                          hover_color=("gray70", "gray30"),
                                          image=add_user_image, anchor="w")
    add_button.grid(row=5, column=0, sticky="ew")
    edit_button = customtkinter.CTkButton(frame_1, corner_radius=0, height=40, border_spacing=10,
                                                  text="Редактирование сотрудника",
                                                  fg_color="transparent", text_color=("gray10", "gray90"),
                                                  hover_color=("gray70", "gray30"),
                                                  image=edit_user_image, anchor="w", command=Edit_workers)
    edit_button.grid(row=6, column=0, sticky="ew")

    exit_button = customtkinter.CTkButton(frame_1, corner_radius=0, height=40, border_spacing=10,
                                          text="Удаление сотрудника",
                                          fg_color="transparent", text_color=("gray10", "gray90"),
                                          hover_color=("gray70", "gray30"),
                                          image=del_user_image, anchor="w", command=Del_worker)
    exit_button.grid(row=7, column=0, sticky="ew")
    exit_button = customtkinter.CTkButton(frame_1, corner_radius=0, height=40, border_spacing=10,
                                          text="Выход",
                                          fg_color="transparent", text_color=("gray10", "gray90"),
                                          hover_color=("gray70", "gray30"),
                                          image=exit_image, anchor="w", command=sys.exit)
    exit_button.grid(row=8, column=0, sticky="ew")
    label_tm = customtkinter.CTkLabel(frame_3, text='ver. 1.9701',
                                      font=customtkinter.CTkFont(size=12))
    label_tm.pack(side='right')
    forms_with_date.mainloop()


def Add_workers_form(names):

    def Save():
        name = names[0]
        wage = entry_wage.get()
        elabor = entry_elaboration.get()
        db.Add_worker(name, wage, elabor)
        names.remove(names[0])
        if len(names) > 0:
            lable_name.configure(text=names[0])
        else:
            app.destroy()

    app = customtkinter.CTk()
    app.title("Добавление сотрудника INBULK")
    app.geometry("400x500")
    frame = customtkinter.CTkScrollableFrame(master=app, width=200, height=200)
    frame.pack(side="left", padx=5, pady=5, expand=True, fill="both")
    lable = customtkinter.CTkLabel(frame, text=f"Был добавлен новый сотрудник",
                                       font=customtkinter.CTkFont(family="Arial", size=18, weight="bold"))
    lable.pack()
    lable_name = customtkinter.CTkLabel(frame, text=names[0],
                                       font=customtkinter.CTkFont(family="Arial", size=18, weight="bold"))
    lable_name.pack()
    entry_wage = customtkinter.CTkEntry(master=frame, placeholder_text="Зарплата")
    entry_wage.pack(padx=20, pady=10)
    entry_elaboration = customtkinter.CTkEntry(master=frame, placeholder_text="Переработка")
    entry_elaboration.pack(padx=20, pady=10)
    save_button = customtkinter.CTkButton(frame, text="Сохранить", command=Save).pack(pady=20)
    app.mainloop()



def Messagebox(title, text):
    app = customtkinter.CTk()
    app.title(title)
    app.geometry("400x200")
    lable = customtkinter.CTkLabel(app, text=text,
                                   font=customtkinter.CTkFont(family="Arial", size=16))
    lable.pack(pady=20)
    close_button = customtkinter.CTkButton(app, text="Закрыть", command=app.destroy).pack(pady=20)
    app.mainloop()


