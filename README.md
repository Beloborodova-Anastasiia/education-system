# Система для обучения

Тестовое задание для HardQode.

### Технологии

Python 3.78
Django 4.2
Django REST framework 3.14.0

### Локальный запуск проекта

Клонировать репозиториий и перейти в папку проекта в команддной строке:
```
git clone https://github.com/Beloborodova-Anastasiia/education-system.git
```

```
cd education-system/
```

Создать и активировать виртуальное окружение:

```
для Mac и Linux:
python3 -m venv env
source venv/bin/activate
```
```
для Windows:
python -m venv venv
source venv/Scripts/activate 
```

Установить зависимости из файла requirements.txt:

```
для Mac и Linux:
python3 -m pip install --upgrade pip
```
```
для Windows:
python -m pip install --upgrade pip
```

```
pip install -r requirements.txt
```

Выполнить миграции:

```
cd education-system/

```
```
для Mac и Linux:
python3 manage.py migrate
```
```
для Windows:
python manage.py migrate
```

Перенести данные в базу данных:
```
python manage.py loaddata db_data.json
```

Запустить проект:

```
для Mac и Linux:
python3 manage.py runserver
```
```
для Windows:
python manage.py runserver
```
Проект запустится локально по адресу:

```
http://127.0.0.1:8000/
```


### Доступные API

Получение JWT-токена для имеющихся в базе данных пользователей:

```
POST: /auth/jwt/create/
```
```
Тело запроса:
{
  "username": "admin",
  "password": "123"
}
или
{
  "username": "user",
  "password": "123"
}
```

Получение списка всех уроков, доступных пользователю:

```
GET: /api/lessons/
```

Получение списка уроков по конкретному продукту, доступному пользователю:

```
GET: /api/lessons_in_product/{id}/
```
(в базе данных доступны продукты с id 1,2 или 3)

Получение статистики по всем продуктам:

```
GET: /api/statistics/
```

### Автор

Анастасия Белобородова 

anastasiia.beloborodova@gmail.com