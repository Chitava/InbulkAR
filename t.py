import pandas as pd
import numpy as np
import xlsxwriter

data_set = {
            'Name': ['Rohit', 'Arun', 'Sohit', 'Arun', 'Shubh'],
            'Roll no': ['01', '02', '03', '04', np.nan],
            'maths': ['93', '63', np.nan, '94', '83'],
            'science': ['88', np.nan, '66', '94', np.nan],
            'english': ['93', '74', '84', '92', '87']}

df = pd.DataFrame(data_set)


writer_obj = pd.ExcelWriter('Write.xlsx',engine='xlsxwriter')
df.to_excel(writer_obj, sheet_name='Sheet')
writer_obj.save()
print('Please check out the Write.xlsx file.')
