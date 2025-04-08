import psycopg
from psycopg.rows import dict_row
import os
from dotenv import load_dotenv

# Загружаем переменные окружения
load_dotenv()

def init_db():
    # Получаем параметры подключения из переменных окружения
    db_params = {
        "dbname": os.getenv("POSTGRES_DB", "postgres"),
        "user": os.getenv("POSTGRES_USER", "postgres"),
        "password": os.getenv("POSTGRES_PASSWORD", "postgres"),
        "host": os.getenv("POSTGRES_HOST", "0.0.0.0"),
        "port": os.getenv("POSTGRES_PORT", "5432")
    }

    try:
        # Подключаемся к базе данных
        with psycopg.connect(**db_params) as conn:
            # Открываем файл с SQL-запросами
            with open('db/database.sql', 'r') as file:
                sql_commands = file.read()
            
            # Создаем курсор и выполняем SQL-запросы
            with conn.cursor() as cur:
                cur.execute(sql_commands)
            
            # Фиксируем изменения
            conn.commit()
            print("База данных успешно инициализирована!")

    except Exception as e:
        print(f"Ошибка при инициализации базы данных: {e}")
        return "База данных уже создана"

if __name__ == "__main__":
    init_db()