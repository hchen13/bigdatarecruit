from tool import database
import pandas as pd
from json import dumps

sql = '''
    select publisher_id,active_time
    from lagou_hr
'''
res = database.database_exec(sql)
d = pd.DataFrame(res, columns = ['id', 'time'])
res = d.groupby('time').size().sort_values()
print(res.to_json(orient='split'))