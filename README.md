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


### Доступные API

В базе данных доступны два пользователя:
```
username
```



