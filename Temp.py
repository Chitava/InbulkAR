import pandas as pd
from openpyxl import load_workbook
from openpyxl import Workbook
import view
from tkinter import filedialog as fd
import db
import os
import xlwt
import xlsxwriter

def Create_db():
    file = fd.askopenfilename()
    wb = load_workbook(file)
    sheet = wb.worksheets[0]
    ar = {}  # общий массив данных
    result = []
    temp = []
    for i in range(1, sheet.max_row + 1):
        for j in range(2, 20):
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
        print(item)
    for item in result:
        item[0] = item[0].replace(',', ' ')

        # for i in range(1, len(item)):
        #     item[i] = (item[i].split(',')).pop(2).replace('--', '0')
        if len(item) < 32:
            for i in range(len(item), 32):
                item.append('0')
        key = item[0]
        item.pop(0)
        ar[key] = item
    return ar


Create_db()