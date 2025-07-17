from create_connection import create_connection 
import psycopg2


def printer_func(query, resp):
    print(f'- QUERY: {query}')
    print(f'- RESULT:')
    if isinstance(resp, list):
        for i in resp:
            print()
            print(i)
    else:
        print(resp)
    print('='*100)


def execute_query(sql) -> None:
# Створимо з'єднання з нашою БД та отримаємо об'єкт курсора для маніпуляцій з даними
    try:
        with create_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(sql)
                if sql.strip().upper().startswith('SELECT'):
                    return cursor.fetchall()
                else:
                    return 'OK'

    except (Exception, psycopg2.Error) as error:
        print("Помилка при запиті до БД", error)


if __name__ == "__main__":
# Отримати всі завдання певного користувача.
# Використайте SELECT для отримання завдань конкретного користувача за його user_id.
    user_id = 2
    sql = f"""
        SELECT * FROM tasks
        WHERE user_id = {user_id}
        """
    printer_func(sql, execute_query(sql))


# Вибрати завдання за певним статусом.
# Використайте підзапит для вибору завдань з конкретним статусом, наприклад, 'new'.
    status = 'new'
    sql = f"""
        SELECT * FROM tasks
        WHERE status_id = (SELECT id FROM status WHERE name = '{status}') 
        """
    printer_func(sql, execute_query(sql))


# Оновити статус конкретного завдання.
# Змініть статус конкретного завдання на 'in progress' або інший статус.
    task_id = 1
    status = 'in progress'
    sql = f"""
        UPDATE tasks
        SET status_id = (SELECT id FROM status WHERE name = '{status}')
        WHERE id = {task_id} 
        """
    printer_func(sql, execute_query(sql))


# Отримати список користувачів, які не мають жодного завдання.
# Використайте комбінацію SELECT, WHERE NOT IN і підзапит.
    sql = f"""
        SELECT * FROM users
        WHERE id NOT IN (SELECT user_id FROM tasks)
        """
    printer_func(sql, execute_query(sql))


# Додати нове завдання для конкретного користувача.
# Використайте INSERT для додавання нового завдання.
    user_id = 1
    new_task_title = 'Get the job!'
    new_task_description = 'Get out of bed and start looking for a job!'
    sql = f"""
        INSERT INTO tasks (title, description, status_id, user_id)
        VALUES ('{new_task_title}', '{new_task_description}', '1', '{user_id}')
        """
    printer_func(sql, execute_query(sql))


# Отримати всі завдання, які ще не завершено.
# Виберіть завдання, чий статус не є 'завершено'.
    status = 'completed'
    sql = f"""
        SELECT * FROM tasks
        WHERE status_id NOT IN (SELECT id FROM status WHERE name = '{status}') 
        """
    printer_func(sql, execute_query(sql))


# Видалити конкретне завдання.
# Використайте DELETE для видалення завдання за його id.
    task_id = 21
    sql = f"""
        DELETE FROM tasks
        WHERE id = {task_id} 
        """
    printer_func(sql, execute_query(sql))


# Знайти користувачів з певною електронною поштою.
# Використайте SELECT із умовою LIKE для фільтрації за електронною поштою.
    email = 'jennifermorton@example.net'
    sql = f"""
        SELECT * FROM users
        WHERE email LIKE '{email}' 
        """
    printer_func(sql, execute_query(sql))


# Оновити ім'я користувача. Змініть ім'я користувача за допомогою UPDATE.
    user_id = 1
    new_fullname = 'Bogdan Gorobets'
    sql = f"""
        UPDATE users
        SET fullname = '{new_fullname}'
        WHERE id = {user_id} 
        """
    printer_func(sql, execute_query(sql))


# Отримати кількість завдань для кожного статусу.
# Використайте SELECT, COUNT, GROUP BY для групування завдань за статусами.
    sql = f"""
        SELECT status.name, COUNT(tasks.id)
        FROM status
        LEFT JOIN tasks ON tasks.status_id = status.id
        GROUP BY status.name
        """
    printer_func(sql, execute_query(sql))


# Отримати завдання, які призначені користувачам з певною доменною частиною електронної пошти.
# Використайте SELECT з умовою LIKE в поєднанні з JOIN, щоб вибрати завдання, призначені користувачам,
# чия електронна пошта містить певний домен (наприклад, '%@example.com').
    email_patern = '%@example.com'
    sql = f"""
        SELECT tasks.id, tasks.title, tasks.description, tasks.status_id, users.fullname, users.email
        FROM tasks
        JOIN users ON tasks.user_id = users.id
        WHERE email LIKE '{email_patern}'
        """
    printer_func(sql, execute_query(sql))


# Отримати список завдань, що не мають опису. Виберіть завдання, у яких відсутній опис.
    sql = f"""
        SELECT * FROM tasks
        WHERE description IS NULL
        """
    printer_func(sql, execute_query(sql))


# Вибрати користувачів та їхні завдання, які є у статусі 'in progress'.
# Використайте INNER JOIN для отримання списку користувачів та їхніх завдань із певним статусом.
    status = 'in progress'
    sql = f"""
        SELECT users.id, users.fullname, tasks.id, tasks.title, tasks.description, status.name
        FROM users
        INNER JOIN tasks ON tasks.user_id = users.id 
        INNER JOIN status ON tasks.status_id = status.id
        WHERE status.name = '{status}'
        """
    printer_func(sql, execute_query(sql))


# Отримати користувачів та кількість їхніх завдань.
# Використайте LEFT JOIN та GROUP BY для вибору користувачів та підрахунку їхніх завдань.
    sql = f"""
        SELECT users.id, users.fullname, COUNT(tasks.id)
        FROM users
        LEFT JOIN tasks ON tasks.user_id = users.id
        GROUP BY users.id, users.fullname

        """
    printer_func(sql, execute_query(sql))
