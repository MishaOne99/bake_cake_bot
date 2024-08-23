Старт проекта (инструкция):

Создаем .venv 
CTRL+SHIFT+P
Python:Create Environment..

Версия Python 3.11.9.

Пример .env

```
BOT_TOKEN = ''
DJANGO_SECRET_KEY = 'django-insecure-2n7'
DJANGO_DEBUG = True
ALLOWED_HOSTS = '["127.0.0.1", ".fvds.ru"]'
CROSS_OR = '["http://*.fvds.ru"]'
```

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
