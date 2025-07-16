import faker
from random import randint, choice
from create_connection import create_connection 
import psycopg2

STATUSES = [('new',), ('in progress',), ('completed',)]
NUMBER_USERS = 5
NUMBER_TASKS = 15

def generate_fake_data(number_users, number_tasks, statuses) -> tuple():
    fake_users = []# тут зберігатимемо користувачів
    fake_tasks = []# тут зберігатимемо завдання
    
    '''Генерація даних з faker'''
    fake_data = faker.Faker()

# Створимо набір користувачів у кількості number_users
    for _ in range(number_users):
        fake_users.append({"fullname": fake_data.name(), "email": fake_data.email()})

# Згенеруємо тепер завдання кількістю number_tasks'''
    for _ in range(number_tasks):
        fake_tasks.append({
            "title": fake_data.sentence(),
            "description": fake_data.text(),
            "status_id": randint(1, len(statuses)),
            "user_id": randint(1, number_users),
            })

    return fake_users, fake_tasks

 fake_users

def prepare_data(users, tasks, statuses) -> tuple():
# готуємо список кортежів користувачів
    for_users = []
    for user in users:
        for_users.append((user["fullname"], user["email"]))
# готуємо список кортежів завдань
    for_tasks = []
    for task in tasks:
        for_tasks.append((task["title"], task["description"], task["status_id"], task["user_id"]))
# готуємо список кортежів статусів
    for_status = []
    for status in statuses:
        for_status.append((status,))

    return for_users, for_tasks, for_status


def insert_data_to_db(users, tasks, statuses) -> None:
# Створимо з'єднання з нашою БД та отримаємо об'єкт курсора для маніпуляцій з даними
    try:
        with create_connection() as conn:
            with conn.cursor() as cursor:
                # Заповнюємо таблицю users виконуючи скрипт
                sql_to_users = """INSERT INTO users (fullname, email)
                               VALUES (%s, %s)
                               """
                cursor.executemany(sql_to_users, users)
                print("Дані до таблиці users успішно додані")

                # Заповнюємо таблицю status виконуючи скрипт
                sql_to_status = """INSERT INTO status (name)
                               VALUES (%s)"""
                cursor.executemany(sql_to_status, statuses)
                print("Дані до таблиці status успішно додані")

                # Заповнюємо таблицю tasks виконуючи скрипт
                sql_to_tasks = """INSERT INTO tasks (title, description, status_id, user_id)
                               VALUES (%s, %s, %s, %s)"""
                cursor.executemany(sql_to_tasks, tasks)
                print("Дані до таблиці tasks успішно додані")
    except (Exception, psycopg2.Error) as error:
        print("Помилка при внесенні даних до таблиць", error)


if __name__ == "__main__":
    users, tasks = generate_fake_data(NUMBER_USERS, NUMBER_TASKS, STATUSES)

    users_prd, tasks_prd, status_prd = prepare_data(users, tasks, STATUSES)

    insert_data_to_db(users_prd, tasks_prd, status_prd)   