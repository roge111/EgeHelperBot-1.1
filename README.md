# EgeHelperBot-1.1
Описание проекта предыдущей версии можно прочитать [здесь](https://github.com/roge111?tab=repositories).
В новой версии обновилась консоль админа `console.py`. Теперь обновлять данные по тарифному плану можно через телеграмм бот. Добавились новые команды `/admin` и `/user_id`. Команды доступны только админу бота, например, мне. 
1) `/admin` - команда, которая будет по id пользователя обновлять его тарифный план. С командой вместе через пробел идут id, наименование тарифного плана, и флаг 1 или 0 (1 - ежемесячная оплата, 0 - на весь учебный год)
2) `/user_id` - помогает по никнейму (username) узнать id пользователя

### Console

Вот как теперь выглядет код административной консоли

```
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

```

### /admin
---
```
@dp.message(Command('admin'))
async def admin_manager(message: types.Message):
  
    
    if str(message.from_user.id) == ADMIN_ID:
        # Разбираем команду (формат: "/admin user_id tariff count_month")
        parts = message.text.replace('/admin', '').strip().split()
        if len(parts) != 3:
            await message.answer('❌ Неверный формат команды. Используйте: /admin user_id tariff count_month')
            return
            
        user_id_new, tariff, count_month = parts
        
        await message.answer('✅ Запрос принят в обработку')
        
        # Преобразуем user_id в int и вызываем метод
        try:
            result = admin.update_follow(
                user_id=user_id_new,
                tariff=tariff,
                count_month=count_month
            )
            
            await message.answer(result if result else '✅ Данные обновлены')
        except Exception as e:
            await message.answer(f'❌ Возникла ошибка:  {e}.')
    else:
        await message.answer('❌ У вас нет доступа!')
```

### /user_id
```
@dp.message(Command('user_id'))
async def id_of_user(message: types.Message):
    if message.from_user.id == int(ADMIN_ID):
        user_name = message.text.split()[1]
        user_id =db.query_database(f"select user_id from users where user_name_tg = '{user_name}';")[0][0]
        await message.answer(f'id пользователя {user_name} = {user_id}')
    else:
        await message.answer(f'Нет доступа!')

```
