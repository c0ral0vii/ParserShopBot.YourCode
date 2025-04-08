from db.database import db


async def create_user(user_id: int, username: str):
    """Создание пользователей"""
    try:
        return await db.execute_single(
            "INSERT INTO users (user_id, username) VALUES ($1, $2) RETURNING id",
            user_id, username
        )
    except Exception as e:
        return True

async def create_order(link: str, price: float, fee: float):
    """Создание заказа"""
    return await db.execute_single(
        "INSERT INTO orders (link, price, fee) VALUES ($1, $2, $3) RETURNING id",
        link, price, fee
    )

async def create_fee(fee: float):
    """Создание комиссии"""
    
    return await db.execute_single(
        "INSERT INTO fee (fee) VALUES ($1) RETURNING id",
        fee
    )

async def get_all_orders():
    """Получение всех заказов"""
    return await db.execute("SELECT * FROM orders")

async def get_fees():
    """Получение комиссии"""
    return await db.execute("SELECT * FROM fee")

async def get_all_users():
    """Получение всех пользователей"""
    return await db.execute("SELECT * FROM users")

async def get_user_by_id(user_id: int):
    """Получение пользователя по ID"""
    return await db.execute_single(
        "SELECT * FROM users WHERE user_id = $1",
        user_id
    )

async def get_order_by_id(order_id: int):
    """Получение заказа по ID"""
    return await db.execute_single(
        "SELECT * FROM orders WHERE id = $1",
        order_id
    )

async def get_latest_fee():
    """Получение последней комиссии"""
    return await db.execute_single(
        "SELECT * FROM fee ORDER BY id DESC LIMIT 1"
    )