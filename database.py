import sqlite3

conn = sqlite3.connect("db.db", check_same_thread = False)
cursor = conn.cursor()

# set user if not exist
def set_user(user_id):
    cursor.execute('INSERT OR IGNORE INTO users (users_id) VALUES (?)', (user_id,))
    conn.commit()

# function for selecting the Russian language.
def choose_russian_language(user_id):
    cursor.execute('UPDATE users SET language = 1 WHERE users_id = (?)', (user_id,))
    conn.commit()

# function for selecting the English language.
def choose_english_language(user_id):
    cursor.execute('UPDATE users SET language = 0 WHERE users_id = (?)', (user_id,))
    conn.commit()

# reset initial and final numbers in database
def reset(user_id):
    cursor.execute('UPDATE users SET num_start = 1, num_finish = 100 WHERE users_id = (?)', (user_id,))
    conn.commit()