### Тесты для проекта Yatube

Социальная сеть блогеров

## Технологии

Python 3.7
Django 2.2.19

## Запуск проекта в dev-режиме

Клонировать репозиторий и перейти в него в командной строке:

```
https://github.com/Katerinair8/yatube_project.git
```

Cоздать и активировать виртуальное окружение:

```
python -m venv venv
```
В зависимости от операционной системы
```
source venv/Scripts/activate или source venv/bin/activate
```

Установить зависимости из файла requirements.txt:

```
python -m pip install --upgrade pip
```

```
pip install -r requirements.txt
```

Создать и выполнить миграции:

```
python manage.py makemigrations
```

```
python manage.py migrate
```

Запустить проект:

```
python manage.py runserver
