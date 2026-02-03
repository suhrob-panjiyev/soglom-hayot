import sqlite3
from pathlib import Path
import pandas as pd

DB_PATH = Path("data/app.db")
DB_PATH.parent.mkdir(parents=True, exist_ok=True)

def get_conn():
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    conn.execute("PRAGMA journal_mode=WAL;")
    return conn

def init_db():
    conn = get_conn()
    cur = conn.cursor()

    # Food log
    cur.execute("""
    CREATE TABLE IF NOT EXISTS food_log (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        day TEXT NOT NULL,             -- YYYY-MM-DD
        food TEXT NOT NULL,
        portion TEXT NOT NULL,
        calories INTEGER NOT NULL
    )
    """)

    # Weight tracker
    cur.execute("""
    CREATE TABLE IF NOT EXISTS weight_log (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        ts TEXT NOT NULL,              -- ISO datetime
        weight REAL NOT NULL
    )
    """)

    # Settings (daily_target va boshqa key-value)
    cur.execute("""
    CREATE TABLE IF NOT EXISTS settings (
        key TEXT PRIMARY KEY,
        value TEXT NOT NULL
    )
    """)

    # Calculator state (JSONsiz, professional)
    cur.execute("""
    CREATE TABLE IF NOT EXISTS calculator_state (
        id INTEGER PRIMARY KEY CHECK (id = 1),
        age INTEGER,
        sex TEXT,
        weight REAL,
        height REAL,
        activity TEXT,
        goal TEXT
    )
    """)

    conn.commit()
    conn.close()

# ---------- settings ----------
def set_setting(key: str, value: str):
    conn = get_conn()
    conn.execute(
        "INSERT INTO settings(key, value) VALUES (?, ?) "
        "ON CONFLICT(key) DO UPDATE SET value=excluded.value",
        (key, value),
    )
    conn.commit()
    conn.close()

def get_setting(key: str, default: str = "") -> str:
    conn = get_conn()
    cur = conn.execute("SELECT value FROM settings WHERE key=?", (key,))
    row = cur.fetchone()
    conn.close()
    return row[0] if row else default

# ---------- calculator state ----------
def save_calculator(age: int, sex: str, weight: float, height: float, activity: str, goal: str):
    conn = get_conn()
    conn.execute("""
    INSERT INTO calculator_state (id, age, sex, weight, height, activity, goal)
    VALUES (1,?,?,?,?,?,?)
    ON CONFLICT(id) DO UPDATE SET
        age=excluded.age,
        sex=excluded.sex,
        weight=excluded.weight,
        height=excluded.height,
        activity=excluded.activity,
        goal=excluded.goal
    """, (int(age), str(sex), float(weight), float(height), str(activity), str(goal)))
    conn.commit()
    conn.close()

def load_calculator():
    conn = get_conn()
    row = conn.execute("""
        SELECT age, sex, weight, height, activity, goal
        FROM calculator_state
        WHERE id=1
    """).fetchone()
    conn.close()

    if not row:
        return None

    return {
        "age": row[0],
        "sex": row[1],
        "weight": row[2],
        "height": row[3],
        "activity": row[4],
        "goal": row[5],
    }

# ---------- food log ----------
def add_food(day: str, food: str, portion: str, calories: int):
    conn = get_conn()
    conn.execute(
        "INSERT INTO food_log(day, food, portion, calories) VALUES (?, ?, ?, ?)",
        (day, food, portion, int(calories)),
    )
    conn.commit()
    conn.close()

def delete_last_food_for_day(day: str):
    conn = get_conn()
    conn.execute("""
        DELETE FROM food_log
        WHERE id = (SELECT id FROM food_log WHERE day=? ORDER BY id DESC LIMIT 1)
    """, (day,))
    conn.commit()
    conn.close()

def delete_foods_for_day(day: str):
    conn = get_conn()
    conn.execute("DELETE FROM food_log WHERE day=?", (day,))
    conn.commit()
    conn.close()

def load_foods_for_day(day: str) -> pd.DataFrame:
    conn = get_conn()
    df = pd.read_sql_query(
        "SELECT id, day, food, portion, calories FROM food_log WHERE day=? ORDER BY id ASC",
        conn,
        params=(day,),
    )
    conn.close()
    return df

# ---------- weight log ----------
def add_weight(ts: str, weight: float):
    conn = get_conn()
    conn.execute(
        "INSERT INTO weight_log(ts, weight) VALUES (?, ?)",
        (ts, float(weight)),
    )
    conn.commit()
    conn.close()

def load_weights(limit: int = 3650) -> pd.DataFrame:
    conn = get_conn()
    df = pd.read_sql_query(
        "SELECT id, ts, weight FROM weight_log ORDER BY ts ASC LIMIT ?",
        conn,
        params=(limit,),
    )
    conn.close()
    return df

def clear_weights():
    conn = get_conn()
    conn.execute("DELETE FROM weight_log")
    conn.commit()
    conn.close()
