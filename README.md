Важно!
в db_fake_data_fill.py 1251 кодировка.
Не забываем реопен делать, если планируете править.

Старт проекта (инструкция):

Создаем .venv 

Пример для VS code:

CTRL+SHIFT+P

"Python:Create Environment.."

Версия Python 3.11.9.

Пример .env

```
BOT_TOKEN = ''
DJANGO_SECRET_KEY = 'django-insecure-2n7'
DJANGO_DEBUG = True
ALLOWED_HOSTS = '["127.0.0.1", ".fvds.ru"]'
CROSS_OR = '["http://*.fvds.ru"]'
VK_SERVICE_ACCESS_KEY = '65cc8c6765cc8c6765cc8c67e466d4ebb4665fe65cc8c6703qwea96d78517798bcde495'
ADMIN_ID = '521825152'
```

Api VK ключ можно получить, следуя [инструкции](https://id.vk.com/about/business/go/docs/ru/vkid/latest/vk-id/connection/tokens/service-token).
![image](https://github.com/user-attachments/assets/5bbb9c90-bf51-44eb-b188-076055885933)


Делаем стартовую миграцию:
```
py backend/manage.py migrate
```
Создаем админа:
```
py backend/manage.py createsuperuser
```
Открываем shell:
```
py backend/manage.py shell
```
Команда для заполнения базы данных
```
with open('extra_scripts/db_fake_data_fill.py') as f:
    exec(f.read())
```

Запускаем Django (локально):
```
py backend/manage.py runserver
```
Запускаем бота в другом терминале:
```
py backend/manage.py runbot
```
