import aiosqlite
from datetime import datetime
import deadline

# cursor.execute("CREATE TABLE IF NOT EXISTS event (id INTEGER PRIMARY KEY AUTOINCREMENT, name VARCHAR[100], comment VARCHAR[1000], date DATETIME)")
# cursor.execute("CREATE TABLE IF NOT EXISTS persons (id INTEGER PRIMARY KEY AUTOINCREMENT, telegramId INTEGER UNIQUE)")

database_path = "tgbot.sql"


async def start_db():
    async with aiosqlite.connect(database_path) as db:
        await db.execute(
            "CREATE TABLE IF NOT EXISTS event (id INTEGER PRIMARY KEY AUTOINCREMENT, name VARCHAR[100], comment VARCHAR[1000], date DATETIME)")
        await db.execute(
            "CREATE TABLE IF NOT EXISTS persons (id INTEGER PRIMARY KEY AUTOINCREMENT, telegramId INTEGER UNIQUE)")
        await db.commit()


async def insert_user_id_db(user_id: int):
    async with aiosqlite.connect(database_path) as db:
        await db.execute(f"INSERT INTO persons(telegramId) VALUES({user_id})")
        await db.commit()


async def is_user_id_in_db(user_id: int) -> bool:
    async with aiosqlite.connect(database_path) as db:
        async with db.execute(f"SELECT EXISTS(SELECT * FROM persons WHERE telegramId = {user_id})") as cursor:
            res = await cursor.fetchone()
            return bool(res[0])


async def delete_user_id_db(user_id: int):
    async with aiosqlite.connect(database_path) as db:
        await db.execute(f"DELETE FROM persons WHERE telegramId = {user_id}")
        await db.commit()


async def insert_deadline(dl: deadline.Deadline):
    async with aiosqlite.connect(database_path) as db:
        await db.execute(
            f"INSERT INTO event(name, date, comment)  VALUES ('{dl.name}', '{dl.date.strftime('%Y-%m-%d %H:%M:%S')}', '{dl.comment}')")
        await db.commit()


async def delete_deadline_id(id_deadline: int):
    async with aiosqlite.connect(database_path) as db:
        await db.execute(f"DELETE FROM event WHERE id = {id_deadline}")
        await db.commit()


async def delete_deadline_date(date: datetime):
    async with aiosqlite.connect(database_path) as db:
        await db.execute(f"DELETE FROM event WHERE date = '{date.strftime('%Y-%m-%d %H:%M:%S')}'")
        await db.commit()


async def delete_deadline_date_interval(start_date: datetime, finish_date: datetime):
    async with aiosqlite.connect(database_path) as db:
        await db.execute(
            f"DELETE FROM event WHERE date >= '{start_date.strftime('%Y-%m-%d %H:%M:%S')}' AND date <= '{finish_date.strftime('%Y-%m-%d %H:%M:%S')}'")
        await db.commit()


async def show_all_deadlines() -> list[deadline.Deadline]:
    async with aiosqlite.connect(database_path) as db:
        async with db.execute(f"SELECT * FROM event ORDER BY date") as cursor:
            tuple_deadlines = await cursor.fetchall()
            deadlines = []
            for dl in tuple_deadlines:
                cur_deadline = deadline.Deadline(dl[1], dl[2], datetime.strptime(dl[3], "%Y-%m-%d %H:%M:%S"))
                cur_deadline.id = dl[0]
                deadlines.append(cur_deadline)
            return deadlines
