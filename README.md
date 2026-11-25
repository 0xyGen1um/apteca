# Аптека на Django и PostgreSQL

Модульный монолит: accounts, catalog, prescriptions, cart, orders, payments, delivery. Оплата демонстрационная.

## Запуск

1. Создайте базу PostgreSQL и пользователя с правами на неё.
2. Создайте `.env` по образцу `.env.example` и укажите пароль и секретный ключ.
3. `python -m venv .venv`
4. `.venv\\Scripts\\python -m pip install -r requirements.txt`
5. `.venv\\Scripts\\python manage.py migrate`
6. `.venv\\Scripts\\python manage.py seed_data`
7. `.venv\\Scripts\\python manage.py runserver`

Демо-пользователи: `client@example.com`, `pharmacist@example.com`, `courier@example.com`, `admin@example.com`; пароль `Demo12345!`. После знакомства смените его.
