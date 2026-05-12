import sqlite3
import json
from datetime import date


class DataBase:
    def __init__(self, db_name="db/game_stats.db", jsonfile='temp/rank_multipliers.json'):
        """Инициализация"""
        self.db_name = db_name
        self.json_ranks = self.load_rank_multipliers(jsonfile)

        connection = sqlite3.connect(self.db_name)
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
                            points INTEGER DEFAULT 0,
                            FOREIGN KEY (user_id) REFERENCES users (user_id) ON DELETE CASCADE
                        )
                    """)

        connection.commit()
        connection.close()

    def add_user(self, user_id, username) -> None:
        """Добавление юзера"""
        if username == 'testing_tg_api_bot':
            return
        connection = sqlite3.connect(self.db_name)
        cursor = connection.cursor()
        try:
            cursor.execute("INSERT INTO users (user_id, username, date, total) VALUES (?, ?, ?, ?)",
                           (user_id, username, date.today().strftime("%d.%m.%Y"), 0))
            cursor.execute("INSERT INTO ranks (user_id, rang, points) VALUES (?, ?, ?)",
                           (user_id, "Новичок", 0))
            connection.commit()
        except sqlite3.IntegrityError:
            cursor.execute(
                "UPDATE users SET username = ? WHERE user_id = ?",
                (username, user_id)
            )
            connection.commit()
        finally:
            connection.close()

    @staticmethod
    def load_rank_multipliers(filename) -> dict:
        """Загрузка json"""
        with open(filename, 'r', encoding='utf-8') as f:
            return json.load(f)

    def get_points_multiplier(self, rang) -> dict:
        """Узнать множитель очков по званию"""
        return self.json_ranks.get(rang)["multipliers"]

    def add_total(self, user_id) -> None:
        """Обновление угаданных мест"""
        connection = sqlite3.connect(self.db_name)
        cursor = connection.cursor()
        cursor.execute("UPDATE users SET total = total + 1 WHERE user_id = ?", (user_id,))
        connection.commit()
        connection.close()

    def add_points(self, user_id, is_correct=True) -> None:
        """Добавление или удаление очков по итогу ответа"""
        rang = self.get_rang_user(user_id)
        multiplier = self.get_points_multiplier(rang)

        if is_correct:
            points_to_change = multiplier["add"]
        else:
            points_to_change = -multiplier["remove"]

        connection = sqlite3.connect(self.db_name)
        cursor = connection.cursor()
        cursor.execute("UPDATE ranks SET points = points + ? WHERE user_id = ?",
                       (points_to_change, user_id))
        connection.commit()
        connection.close()

        self.update_rank_by_score(user_id)

    def get_points(self, user_id) -> int:
        """Получение очков"""
        connection = sqlite3.connect(self.db_name)
        cursor = connection.cursor()
        cursor.execute("SELECT points FROM ranks WHERE user_id = ?", (user_id,))
        result = cursor.fetchone()
        connection.close()
        return result[0] if result else 0

    def get_rank_by_points(self, points: int) -> str:
        """Узнать ранг по очкам после ответа"""
        for rank_name, config in self.json_ranks.items():
            min_pts = config["points_min"]
            max_pts = config["points_max"]

            if points >= min_pts:
                if max_pts is None or points <= max_pts:
                    return rank_name
        return "Новичок"

    def update_rank_by_score(self, user_id) -> None:
        """Обновление ранга"""
        points = self.get_points(user_id)
        new_rank = self.get_rank_by_points(points)

        connection = sqlite3.connect(self.db_name)
        cursor = connection.cursor()
        cursor.execute("UPDATE ranks SET rang = ? WHERE user_id = ?", (new_rank, user_id))
        connection.commit()
        connection.close()

    def get_rang_user(self, user_id) -> str:
        """Узнать ранг"""
        connection = sqlite3.connect(self.db_name)
        cursor = connection.cursor()
        cursor.execute("SELECT rang FROM ranks WHERE user_id = ?", (user_id,))
        result = cursor.fetchone()
        connection.close()
        return result[0] if result else "Новичок"

    def get_user_total(self, user_id) -> int:
        """Узнать сколько угаданных мест"""
        connection = sqlite3.connect(self.db_name)
        cursor = connection.cursor()
        cursor.execute("SELECT total FROM users WHERE user_id = ?", (user_id,))
        result = cursor.fetchone()
        connection.close()
        return result[0] if result else 0

    def process_answer(self, user_id: int, is_correct: bool) -> dict:
        """Вывод данных после ответа игрока"""
        result = {
            'points': 0,
            'rang': None,
            'points_changed': 0,
            'total': None
        }

        self.add_points(user_id, is_correct=is_correct)

        if is_correct:
            self.add_total(user_id)
            result['total'] = self.get_user_total(user_id)

        result['points'] = self.get_points(user_id)
        result['rang'] = self.get_rang_user(user_id)

        multiplier = self.get_points_multiplier(result['rang'])
        result['points_changed'] = multiplier["add"] if is_correct else multiplier["remove"]

        return result

    def get_top_players(self, limit=5) -> list[tuple]:
        """Получить топ игроков"""
        connection = sqlite3.connect(self.db_name)
        cursor = connection.cursor()
        cursor.execute("""
                SELECT u.username, u.total, r.rang, r.points
                FROM users u
                LEFT JOIN ranks r ON u.user_id = r.user_id
                ORDER BY r.points DESC 
                LIMIT ?
            """, (limit,))
        result = cursor.fetchall()
        connection.close()
        return result

    def get_date(self, user_id) -> str:
        """Получить дату"""
        connection = sqlite3.connect(self.db_name)
        cursor = connection.cursor()
        cursor.execute("SELECT date FROM users WHERE user_id = ?", (user_id,))
        date = cursor.fetchone()
        return date[0] if date else "Неизвестно"

    def get_active_users(self) -> list[int]:
        """узнать всех юзеров"""
        connection = sqlite3.connect(self.db_name)
        cursor = connection.cursor()
        cursor.execute("SELECT user_id FROM users")
        users = cursor.fetchall()
        connection.close()
        return [user[0] for user in users]


db = DataBase()
