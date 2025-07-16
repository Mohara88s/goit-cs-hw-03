from create_connection import create_connection 
import psycopg2

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
    separator = '='
# Отримати всі завдання певного користувача.
# Використайте SELECT для отримання завдань конкретного користувача за його user_id.
    user_id = 2
    sql = f"""
        SELECT * FROM tasks
        WHERE user_id = {user_id}
        """
    print(f'\n- QUERY: {sql}')
    print(f'RESULT: {execute_query(sql)}')
    print(separator*100)

# Вибрати завдання за певним статусом.
# Використайте підзапит для вибору завдань з конкретним статусом, наприклад, 'new'.
    status = 'new'
    sql = f"""
        SELECT * FROM tasks
        WHERE status_id = (SELECT id FROM status WHERE name = '{status}') 
        """
    print(f'\n- QUERY: {sql}')
    print(f'RESULT: {execute_query(sql)}')
    print(separator*100)

# Оновити статус конкретного завдання.
# Змініть статус конкретного завдання на 'in progress' або інший статус.
    task_id = 1
    status = 'in progress'
    sql = f"""
        UPDATE tasks
        SET status_id = (SELECT id FROM status WHERE name = '{status}')
        WHERE id = {task_id} 
        """
    print(f'\n- QUERY: {sql}')
    print(f'- RESULT: {execute_query(sql)}')
    print(separator*100)

# Отримати список користувачів, які не мають жодного завдання.
# Використайте комбінацію SELECT, WHERE NOT IN і підзапит.
    sql = f"""
        SELECT * FROM users
        WHERE id NOT IN (SELECT user_id FROM tasks)
        """
    print(f'\n- QUERY: {sql}')
    print(f'- RESULT: {execute_query(sql)}')
    print(separator*100)

# Додати нове завдання для конкретного користувача.
# Використайте INSERT для додавання нового завдання.
    user_id = 1
    new_task_title = 'Get the job!'
    new_task_description = 'Get out of bed and start looking for a job!'
    sql = f"""
        INSERT INTO tasks (title, description, status_id, user_id)
        VALUES ('{new_task_title}', '{new_task_description}', '1', '{user_id}')
        """
    print(f'\n- QUERY: {sql}')
    print(f'- RESULT: {execute_query(sql)}')
    print(separator*100)

# Отримати всі завдання, які ще не завершено.
# Виберіть завдання, чий статус не є 'завершено'.
    status = 'completed'
    sql = f"""
        SELECT * FROM tasks
        WHERE status_id NOT IN (SELECT id FROM status WHERE name = '{status}') 
        """
    print(f'\n- QUERY: {sql}')
    print(f'RESULT: {execute_query(sql)}')
    print(separator*100)

# Видалити конкретне завдання.
# Використайте DELETE для видалення завдання за його id.
    task_id = 21
    sql = f"""
        DELETE FROM tasks
        WHERE id = {task_id} 
        """
    print(f'\n- QUERY: {sql}')
    print(f'- RESULT: {execute_query(sql)}')
    print(separator*100)

# Знайти користувачів з певною електронною поштою.
# Використайте SELECT із умовою LIKE для фільтрації за електронною поштою.
    email = 'jennifermorton@example.net'
    sql = f"""
        SELECT * FROM users
        WHERE email LIKE '{email}' 
        """
    print(f'\n- QUERY: {sql}')
    print(f'- RESULT: {execute_query(sql)}')
    print(separator*100)

# Оновити ім'я користувача. Змініть ім'я користувача за допомогою UPDATE.
    user_id = 1
    new_fullname = 'Bogdan Gorobets'
    sql = f"""
        UPDATE users
        SET fullname = '{new_fullname}'
        WHERE id = {user_id} 
        """
    print(f'\n- QUERY: {sql}')
    print(f'- RESULT: {execute_query(sql)}')
    print(separator*100)

# Отримати кількість завдань для кожного статусу.
# Використайте SELECT, COUNT, GROUP BY для групування завдань за статусами.
    sql = f"""
        SELECT status.name, COUNT(tasks.id)
        FROM status
        LEFT JOIN tasks ON tasks.status_id = status.id
        GROUP BY status.name
        """
    print(f'\n- QUERY: {sql}')
    print(f'- RESULT: {execute_query(sql)}')
    print(separator*100)

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
    print(f'\n- QUERY: {sql}')
    print(f'- RESULT: {execute_query(sql)}')
    print(separator*100)

# Отримати список завдань, що не мають опису. Виберіть завдання, у яких відсутній опис.
    sql = f"""
        SELECT * FROM tasks
        WHERE description IS NULL
        """
    print(f'\n- QUERY: {sql}')
    print(f'- RESULT: {execute_query(sql)}')
    print(separator*100)

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
    print(f'\n- QUERY: {sql}')
    print(f'- RESULT: {execute_query(sql)}')
    print(separator*100)

# Отримати користувачів та кількість їхніх завдань.
# Використайте LEFT JOIN та GROUP BY для вибору користувачів та підрахунку їхніх завдань.
    sql = f"""
        SELECT users.id, users.fullname, COUNT(tasks.id)
        FROM users
        LEFT JOIN tasks ON tasks.user_id = users.id
        GROUP BY users.id, users.fullname

        """
    print(f'\n- QUERY: {sql}')
    print(f'- RESULT: {execute_query(sql)}')
    print(separator*100)