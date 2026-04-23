import sqlite3
from datetime import date


def create_database(db_name="game_stats.db"):
    connection = sqlite3.connect(db_name)
    cursor = connection.cursor()

    cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER UNIQUE,
                username TEXT,
                date TEXT,
                total INTEGER DEFAULT 0
            )
        """)
    cursor.execute("""
            CREATE TABLE IF NOT EXISTS ranks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                rang TEXT NOT NULL,
                user_id INTEGER UNIQUE,
                FOREIGN KEY (user_id) REFERENCES users (user_id) ON DELETE CASCADE
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
        cursor.execute("INSERT INTO users (user_id, username, date, total) VALUES (?, ?, ?, ?)",
                       (user_id, username, date.today().strftime("%d.%m.%Y"), 0))
        cursor.execute("INSERT INTO ranks (user_id, rang) VALUES (?, ?)",
                       (user_id, "Новичок"))
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
    update_rank_by_score(user_id)


def update_rank_by_score(user_id):
    connection = sqlite3.connect('game_stats.db')
    cursor = connection.cursor()

    cursor.execute("SELECT total FROM users WHERE user_id = ?", (user_id,))
    result = cursor.fetchone()

    total_score = result[0]
    if total_score < 4:
        rang = "Новичок"
    elif total_score < 8:
        rang = "Исследователь"
    elif total_score < 12:
        rang = "Знаток"
    elif total_score < 16:
        rang = "Эксперт"
    else:
        rang = "Мастер географии"

    cursor.execute("UPDATE ranks SET rang = ? WHERE user_id = ?", (rang, user_id))

    connection.commit()
    connection.close()


def get_rang_user(user_id):
    connection = sqlite3.connect('game_stats.db')
    cursor = connection.cursor()
    cursor.execute("SELECT rang FROM ranks WHERE user_id = ?", (user_id,))
    result = cursor.fetchone()
    connection.close()
    return result[0]


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
    cursor.execute("""
            SELECT u.username, u.total, r.rang 
            FROM users u
            LEFT JOIN ranks r ON u.user_id = r.user_id
            ORDER BY u.total DESC 
            LIMIT ?
        """, (limit,))
    result = cursor.fetchall()
    return result


def get_date(user_id):
    connection = sqlite3.connect('game_stats.db')
    cursor = connection.cursor()
    cursor.execute("SELECT date FROM users WHERE user_id = ?", (user_id,))
    date = cursor.fetchone()
    return date[0]
