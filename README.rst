Boarddit - reddit-style борда МФТИ
==================================

Требуется Python 3.4+. Настройка окружения и установка зависимостей::

    virtualenv venv --python=python3
    . venv/bin/activate
    python -m pip install -r requirements.txt

Подготовка БД::

    python manage.py migrate

Запуск тестового сервера::

    python manage.py runserver


Документация по шаблону
-----------------------

You can see the documentation over at **Read the Docs**: `django-project-skeleton
<http://django-project-skeleton.readthedocs.org/en/latest/>`_
