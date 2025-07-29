import sys
from pathlib import Path
from dateutil.relativedelta import relativedelta

ROOT = Path(__file__).parent.parent  # Если файл на 2 уровня глубже (папка/подпапка/файл)
# ROOT = Path(__file__).parent  # Если файл в корневой папке

# Добавляем путь в sys.path (если его там ещё нет)
if str(ROOT) not in sys.path:
    sys.path.append(str(ROOT))

from managers.dataBase import DataBaseManager
from datetime import datetime, timedelta


db = DataBaseManager()
class Admin:
    def __init__(self):
        pass

    

    """
    Данная функция предназанчена для админов и способна изменять данные о подписке пользователя
    """
    def update_follow(self, user_id: int, tariff: str, count_month: str):
        db.query_database(f"update users set follow = 1 where user_id = {user_id};", reg=True)
        curr_date = datetime.now()
        if count_month == '1':
            future_date = curr_date  + relativedelta(months=1)
        else:
            future_date = '2026-07-01'
        format_future_date = future_date.strftime('%Y-%m-%d')

        db.query_database(f"update users set data_end = '{format_future_date}' where user_id = {user_id};", reg=True)
        
        db.query_database(f"update users set  tarrif_plan = '{tariff}' where user_id = {user_id};", reg=True)
        
        
    
        db.query_database(f"update users set count_requests = {0} where user_id = {user_id};", reg=True)
        db.query_database(f"update users set overpayment = {0} where user_id = {user_id};", reg=True)



    