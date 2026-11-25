import sqlite3
from contextlib import closing
database_file = "app.db"

def init_db():
    conn = sqlite3.connect(database_file)
    cursor = conn.cursor()
    cursor.execute('''PRAGMA foreign_keys = ON;''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS notes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER ,
            content TEXT NOT NULL,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
        )
    ''')

    conn.commit()
    conn.close()


def add_user(new_user : dict) -> bool:
    username = new_user["username"]
    password = new_user["password"]
    conn = sqlite3.connect(database_file)
    try:
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO users
            (username, password) VALUES (?, ?) ''', 
            (username, password)
        )
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        conn.rollback()
        return False
    finally:
        conn.close()

def get_user_by_user(username : str) -> dict | None:
    with  closing(sqlite3.connect(database_file)) as conn:
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute('''
            SELECT id, username, password FROM users WHERE username = ?
        ''', (username,))

        user = cursor.fetchone()

    if user is None:
        return None
    
    return dict(user) if user else None


def delete_user_by_username(username : str) -> bool:
    with closing(sqlite3.connect(database_file)) as conn:
        cursor = conn.cursor()
        cursor.execute('''PRAGMA foreign_keys = ON;''')
        cursor.execute('''DELETE FROM users WHERE username = ?''', (username,))
        conn.commit()
        return cursor.rowcount > 0


# Notes

def add_note(user_id : int, content : str) -> int:
    with closing(sqlite3.connect(database_file)) as conn:
        cursor = conn.cursor()
        cursor.execute('''
        INSERT INTO notes (user_id, content)VALUES (?, ?)''', (user_id, content))
        conn.commit()
        return cursor.lastrowid

def delete_note(id_note, user_id) -> bool:
    with closing(sqlite3.connect(database_file)) as conn:
        cursor = conn.cursor()
        cursor.execute('''
            DELETE FROM notes WHERE id = ? AND user_id = ?''', (id_note, user_id))
        conn.commit()
        return cursor.rowcount > 0

def get_all_notes(user_id : int):
    with closing(sqlite3.connect(database_file)) as conn:
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute('''
            SELECT * FROM notes WHERE user_id = ?''',
            (user_id,)
        )
        notes : list[dict] = cursor.fetchall()
        return notes

def update_note(note_id : int , user_id: int, new_content : str):
    with closing(sqlite3.connect(database_file)) as conn:
        cursor = conn.cursor()
        cursor.execute('''
            UPDATE notes
            SET content = ?
            WHERE id = ? AND user_id = ?
            RETURNING id, content
        ''', (new_content, note_id, user_id))
        updated_col = cursor.fetchone()
        conn.commit()
        return updated_col