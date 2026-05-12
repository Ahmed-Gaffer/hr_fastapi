import pandas as pd
import os

files = ['employees.xlsx', 'database.xlsx', 'database new.xlsx', 'embloyees .1.xlsx']
for f in files:
    path = os.path.join(os.getcwd(), f)
    if os.path.exists(path):
        try:
            df = pd.read_excel(path)
            print('FILE', f)
            print('COLUMNS', list(df.columns)[:50])
            print('ROWS', len(df))
            print('---')
        except Exception as e:
            print('ERR', f, e)
    else:
        print('MISSING', f)
