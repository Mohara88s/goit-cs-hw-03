from create_connection import create_connection 
import psycopg2

def create_db():
    # Читаємо файл зі скриптом для створення БД
    try:
        with open('tables.sql', 'r') as f:
            create_tables_query = f.read()
        with create_connection() as conn:
            with conn.cursor() as cursor:
                # Створення таблиць виконуючи скрипт
                cursor.execute(create_tables_query)
                print("Таблиці БД успішно створено")
    except (Exception, psycopg2.Error) as error:
        print("Помилка при створенні таблиць", error)


if __name__ == "__main__":
    create_db()