import aiosqlite
from decouple import config


async def create_table():
    async with aiosqlite.connect(config('DB_NAME')) as db:
        await db.execute('''CREATE TABLE IF NOT EXISTS quiz_state  
                            (user_id INTEGER PRIMARY KEY, question_index INTEGER NOT NULL DEFAULT 0,
                            right_answers INTEGER, wrong_answers INTEGER)''')
        await db.commit()


async def update_quiz_index(user_id, index):
    async with aiosqlite.connect(config('DB_NAME')) as db:
        await db.execute('''INSERT INTO quiz_state (user_id, question_index) VALUES (?, ?)
                         ON CONFLICT(user_id) DO UPDATE SET question_index=excluded.question_index''',
                         (int(user_id), index))
        await db.commit()
        print(f"Updated user {user_id} to question_index {index}")


async def get_quiz_index(user_id):
     async with aiosqlite.connect(config('DB_NAME')) as db:
        async with db.execute('SELECT question_index FROM quiz_state WHERE user_id = ?', (int(user_id),)) as cursor:
            results = await cursor.fetchone()
            if results is None or results[0] is None:
                print(f"User {user_id} has no entry yet. Returning 0")
                return 0
            print(f"User {user_id} question_index {results[0]}")
            return results[0]


async def update_right_answers(user_id, right_answers):
    async with aiosqlite.connect(config('DB_NAME')) as db:
        await db.execute('''INSERT INTO quiz_state (user_id, right_answers) VALUES (?, ?)
            ON CONFLICT(user_id) DO UPDATE SET right_answers=excluded.right_answers
            ''', (user_id, right_answers))
        await db.commit()


async def get_right_answers(user_id):
    async with aiosqlite.connect(config('DB_NAME')) as db:
        async with db.execute('SELECT right_answers FROM quiz_state WHERE user_id = (?)', (user_id,)) as cursor:
            results = await cursor.fetchone()
            if results is None or results[0] is None:
                return 0
            return results[0]


async def update_wrong_answers(user_id, wrong_answers):
    async with aiosqlite.connect(config('DB_NAME')) as db:
        await db.execute('''INSERT INTO quiz_state (user_id, wrong_answers) VALUES (?, ?)
            ON CONFLICT(user_id) DO UPDATE SET wrong_answers=excluded.wrong_answers
            ''', (user_id, wrong_answers))
        await db.commit()


async def get_wrong_answers(user_id):
    async with aiosqlite.connect(config('DB_NAME')) as db:
        async with db.execute('SELECT wrong_answers FROM quiz_state WHERE user_id = (?)', (user_id,)) as cursor:
            results = await cursor.fetchone()
            if results is None or results[0] is None:
                return 0
            return results[0]


async def get_static():
    async with aiosqlite.connect(config('DB_NAME')) as db:
        async with db.execute('SELECT user_id, right_answers, wrong_answers FROM quiz_state') as cursor:
            result = await cursor.fetchall()
            print(result)
            return sorted(result, key=lambda x: x[1], reverse=True)
