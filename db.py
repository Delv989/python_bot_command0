import sqlite3

conn = sqlite3.connect("tgbot.sql")


def insert_user_id_db(user_id: int):
    cursor = conn.cursor()
    cursor.execute(f"INSERT INTO persons(telegramId) VALUES({user_id})")
    conn.commit()
    cursor.close()


def is_user_id_in_db(user_id: int) -> bool:
    cursor = conn.cursor()
    cursor.execute(f"SELECT EXISTS(SELECT * FROM persons WHERE telegramId = {user_id})")
    return cursor.fetchall()[0][0]


def delete_user_id_db(user_id: int):
    cursor = conn.cursor()
    cursor.execute(f"DELETE FROM persons WHERE telegramId = {user_id}")
    conn.commit()
    cursor.close()

