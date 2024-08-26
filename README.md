## Bake Cake

В данном проекте реализован Телеграмм бот для заказа тортов.  
В качестве ORM системы и админки используется Django.

### Как установить

Python3 должен быть установлен версии ~3.11.9. 
Используйте `pip` для установки зависимостей:
```
$ pip install -r requirements.txt
```
Для реализации проекта вам понадобится Telegram бот. Создать можно через [@BotFather](https://t.me/BotFather). 

Бот токен выглядит так: `1234567890:XXXxx0Xxx-xxxX0xXXxXxx0X0XX0XXXXxXx`.  

Для корректной работы потребуется файл .env  
Пример:
```
BOT_TOKEN = ''
DJANGO_SECRET_KEY = 'django-insecure-2n7'
DJANGO_DEBUG = True
ALLOWED_HOSTS = '["127.0.0.1", ".fvds.ru"]'
CROSS_OR = '["http://*.fvds.ru"]'
VK_SERVICE_ACCESS_KEY = '65cc8c6765cc8c6765cc8c67e466d4ebb4665fe65cc8c6703qwea96d78517798bcde495'
ADMIN_ID = '521825152'
SITE_URL = 'http://customer.fast-vds.ru'
```

Api VK ключ можно получить, следуя [инструкции](https://id.vk.com/about/business/go/docs/ru/vkid/latest/vk-id/connection/tokens/service-token).

![image](https://github.com/user-attachments/assets/5bbb9c90-bf51-44eb-b188-076055885933)

### Комманды запуска

Делаем стартовую миграцию:
```
$ py backend/manage.py migrate
```
Создаем админа:
```
$ py backend/manage.py createsuperuser
```
Открываем shell:
```
$ py backend/manage.py shell
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
Для деплоя проекта рекомендуем ознакомиться с [данной](https://docs.djangoproject.com/en/5.0/howto/deployment/) статьей.

### Примеры работы

Пример корректной работы админки:

![image](https://github.com/user-attachments/assets/caadada5-6653-485e-a93d-5badd5468d4a)

Пример работы бота:

![example](https://github.com/user-attachments/assets/a97802c8-f1f1-46ad-b0ec-66bceb0a8916)


### Цель проекта

Код написан в образовательных целях на онлайн-курсе для веб-разработчиков [dvmn.org](https://dvmn.org/).