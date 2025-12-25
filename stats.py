import json
from pathlib import Path
from datetime import date

# stats.json лежить в тому ж каталозі, що й stats.py
STATS_PATH = Path(__file__).with_name("stats.json")


def load_stats_dict() -> dict:
    """
    Прочитати stats.json і повернути словник.
    Якщо файлу немає – повертаємо порожню структуру.
    """
    if STATS_PATH.exists():
        with STATS_PATH.open("r", encoding="utf-8") as f:
            return json.load(f)
    return {"players": {}}


def save_stats_dict(stats: dict):
    """
    Записати словник у stats.json.
    """
    with STATS_PATH.open("w", encoding="utf-8") as f:
        json.dump(stats, f, ensure_ascii=False, indent=4)


def update_player_stats(
    player_name: str,
    won: bool,
    attempts: int,
    score_change: int,
    difficulty: str
):
    """
    Оновити статистику одного гравця і зберегти у файл.
    """
    stats = load_stats_dict()

    if "players" not in stats:
        stats["players"] = {}

    player = stats["players"].get(player_name)
    if player is None:
        player = {
            "games": 0,
            "wins": 0,
            "score": 0,
            "last_difficulty": None,
            "last_attempts": 0,
            "avg_attempts": 0.0,
            "last_play": None
        }
        stats["players"][player_name] = player

    player["games"] += 1
    if won:
        player["wins"] += 1

    player["score"] += score_change

    old_avg = player["avg_attempts"]
    n = player["games"]
    player["avg_attempts"] = round(((old_avg * (n - 1)) + attempts) / n, 2)

    player["last_attempts"] = attempts
    player["last_difficulty"] = difficulty
    player["last_play"] = date.today().isoformat()

    save_stats_dict(stats)
if __name__ == "__main__":
    print("stats.py loaded")
    print("Functions:", dir())
