from db_config import DB_CONFIG 
from contextlib import contextmanager
import psycopg2

@contextmanager
def create_connection(): 
    conn = None
    try:
        # Підключення до бази даних
        conn = psycopg2.connect(**DB_CONFIG)
        yield conn
        conn.commit()
    except (Exception, psycopg2.Error) as error:
        print("Помилка при роботі з PostgreSQL", error)

    finally:
        # Закриття з'єднання
        if conn:
            conn.close()
            # print("З'єднання з базою даних закрито")

if __name__ == "__main__":
    with create_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute("SELECT version();")
            print(f"DBver: {cursor.fetchone()}")