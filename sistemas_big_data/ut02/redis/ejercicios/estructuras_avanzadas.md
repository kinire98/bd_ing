# Estructuras avanzadas

```python
import redis
from datetime import datetime
from typing  import List

r = redis.Redis(
        host="localhost",
        port=6379, 
        db=0,
        decode_responses=True
        )

players_hash = "player:"
name_player_key = "name"
country_player_key = "country"
score_player_key = "score"
games_played_player_key = "games_played"

log_played = "unique:players:"

leaderboard = "leaderboard"

def add_player(id: int, name: str, country: str, score: int):
    r.hset(players_hash + str(id), key=name_player_key, value=name)
    r.hset(players_hash + str(id), key=country_player_key, value=country)
    r.hset(players_hash + str(id), key=score_player_key, value=str(score))
    r.hset(players_hash + str(id), key=games_played_player_key, value=str(0))
def update_score(id: int, points: int):
    cur_points = int(r.hget(players_hash + str(id), score_player_key)) # pyright: ignore
    cur_points += points
    r.hset(players_hash + str(id), key=score_player_key, value=str(cur_points))
    cur_games = int(r.hget(players_hash + str(id), games_played_player_key)) + 1 # pyright: ignore
    r.hset(players_hash + str(id), key=games_played_player_key, value=str(cur_games))
    r.zincrby(leaderboard, points, id)
def player_info(id: int):
    print(r.hgetall(players_hash + str(id)))

def show_top_players(n: int):
    print(r.zrevrange(leaderboard, 0, n-1, True))

def register_login(id: int):
    r.pfadd(log_played + datetime.today().strftime("%Y%m%d"), id)
def count_unique_logins(date: datetime):
    print(r.pfcount(log_played + date.today().strftime("%Y%m%d")))
def weekly_report(dates: List[datetime]):
    keys = list(map(lambda x: x.today().strftime("%Y%m%d"), dates))
    week_key = log_played + "week"
    r.pfmerge(week_key, *keys)
    print(r.pfcount(week_key))
def reset_system():
    r.delete(leaderboard)
    cursor = 0
    while True:
        cursor, keys = r.scan(cursor=cursor, match=log_played + "*", count=5000) # pyright: ignore
        if keys:
            r.unlink(*keys)
        if cursor == 0:
            break
    cursor = 0
    while True:
        cursor, keys = r.scan(cursor=cursor, match=players_hash + "*", count=10000) # pyright: ignore
        if keys:
            r.unlink(*keys)
        if cursor == 0:
            break
```
