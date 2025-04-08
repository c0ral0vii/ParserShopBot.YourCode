import asyncpg
import os
from dotenv import load_dotenv

# Загружаем переменные окружения
load_dotenv()

class Database:
    def __init__(self):
        self.db_params = {
            "database": os.getenv("POSTGRES_DB", "postgres"),
            "user": os.getenv("POSTGRES_USER", "postgres"),
            "password": os.getenv("POSTGRES_PASSWORD", "postgres"),
            "host": os.getenv("POSTGRES_HOST", "0.0.0.0"),
            "port": os.getenv("POSTGRES_PORT", "5432")
        }
        self.pool = None

    async def connect(self):
        """Создание пула соединений"""
        if not self.pool:
            self.pool = await asyncpg.create_pool(**self.db_params)

    async def close(self):
        """Закрытие пула соединений"""
        if self.pool:
            await self.pool.close()
            self.pool = None

    async def execute(self, query: str, *args):
        """Выполнить запрос"""
        if not self.pool:
            await self.connect()
        async with self.pool.acquire() as conn:
            return await conn.fetch(query, *args)

    async def execute_single(self, query: str, *args):
        """Выполнить запрос и вернуть один результат"""
        if not self.pool:
            await self.connect()
        async with self.pool.acquire() as conn:
            return await conn.fetchrow(query, *args)

    async def execute_many(self, query: str, args_list):
        """Выполнить запрос для множества параметров"""
        if not self.pool:
            await self.connect()
        async with self.pool.acquire() as conn:
            return await conn.executemany(query, args_list)

# Создаем глобальный экземпляр для использования в других модулях
db = Database() 