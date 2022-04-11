import sqlite3

conn = sqlite3.connect("db.db", check_same_thread = False)
cursor = conn.cursor()

# set user if not exist
def set_user(user_id):
    cursor.execute('INSERT OR IGNORE INTO users (users_id) VALUES (?)', (user_id,))
    conn.commit()

# function for selecting a language.
def choose_language(language, user_id):
    cursor.execute('UPDATE users SET language = (?) WHERE users_id = (?)', (language, user_id,))
    conn.commit()

# update range in the database
def set_range(initial_num, finite_num, user_id):
    cursor.execute('UPDATE users SET num_start = (?),num_finish = (?) WHERE users_id = (?)', (initial_num, finite_num, user_id,))
    conn.commit()

# get range from database
def get_range(user_id):
    cursor.execute('SELECT num_start, num_finish FROM users WHERE users_id = (?)', (user_id,))
    range = cursor.fetchall()
    conn.commit()
    return range

# get language from database
def get_language(user_id):
    cursor.execute('SELECT language FROM users WHERE users_id = (?)', (user_id,))
    language = cursor.fetchall()
    conn.commit()
    return language[0][0]

# reset initial and final numbers in database
def reset(user_id):
    cursor.execute('UPDATE users SET num_start = 1, num_finish = 100 WHERE users_id = (?)', (user_id,))
    conn.commit()