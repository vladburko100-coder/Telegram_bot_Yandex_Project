import sqlite3


def create_database(db_name="game_stats.db"):
    connection = sqlite3.connect(db_name)
    cursor = connection.cursor()

    cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER UNIQUE,
                username TEXT,
                total INTEGER DEFAULT 0
            )
        """)

    connection.commit()
    connection.close()


def add_user(user_id, username):
    if username == 'testing_tg_api_bot':
        return
    connection = sqlite3.connect('game_stats.db')
    cursor = connection.cursor()
    try:
        cursor.execute("INSERT INTO users (user_id, username, total) VALUES (?, ?, ?)", (user_id, username, 0))
        connection.commit()
    except sqlite3.IntegrityError:
        cursor.execute(
            "UPDATE users SET username = ? WHERE user_id = ?",
            (username, user_id)
        )
        connection.commit()
    finally:
        connection.close()


def add_total(user_id):
    connection = sqlite3.connect('game_stats.db')
    cursor = connection.cursor()
    cursor.execute("UPDATE users SET total = total + 1 WHERE user_id = ?", (user_id,))
    connection.commit()
    connection.close()


def get_user_total(user_id):
    connection = sqlite3.connect('game_stats.db')
    cursor = connection.cursor()
    cursor.execute("SELECT total FROM users WHERE user_id = ?", (user_id,))
    result = cursor.fetchone()
    connection.close()
    return result[0] if result else 0


def get_top_players(limit=5):
    connection = sqlite3.connect('game_stats.db')
    cursor = connection.cursor()

    cursor.execute("""SELECT username, total FROM users ORDER BY total DESC LIMIT ?""", (limit,))
    result = cursor.fetchall()
    connection.close()

    return result