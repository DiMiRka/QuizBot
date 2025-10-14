import aiosqlite
from decouple import config


async def create_table():
    async with aiosqlite.connect(config('DB_NAME')) as db:
        await db.execute('''CREATE TABLE IF NOT EXISTS quiz_bot  
                            (user_id INTEGER PRIMARY KEY, question_index INTEGER,
                            right_answers INTEGER, wrong_answers INTEGER)''')
        await db.commit()


async def update_quiz_index(user_id, index):
    async with aiosqlite.connect(config('DB_NAME')) as db:
        await db.execute('INSERT OR REPLACE INTO quiz_state (user_id, question_index) VALUES (?, ?)', (user_id, index))
        await db.commit()


async def get_quiz_index(user_id):
     async with aiosqlite.connect(config('DB_NAME')) as db:
        async with db.execute('SELECT question_index FROM quiz_state WHERE user_id = (?)', (user_id, )) as cursor:
            results = await cursor.fetchone()
            if results is not None:
                return results[0]
            else:
                return 0


async def update_right_answers(user_id, right_answers):
    async with aiosqlite.connect(config('DB_NAME')) as db:
        await db.execute('INSERT OR REPLACE INTO quiz_state (user_id, right_answers) VALUES (?, ?)', (user_id, right_answers))
        await db.commit()


async def get_right_answers(user_id):
    async with aiosqlite.connect(config('DB_NAME')) as db:
        async with db.execute('SELECT right_answers FROM quiz_state WHERE user_id = (?)', (user_id,)) as cursor:
            results = await cursor.fetchone()
            if results is not None:
                return results[0]
            else:
                return 0


async def update_wrong_answers(user_id, wrong_answers):
    async with aiosqlite.connect(config('DB_NAME')) as db:
        await db.execute('INSERT OR REPLACE INTO quiz_state (user_id, wrong_answers) VALUES (?, ?)', (user_id, wrong_answers))
        await db.commit()


async def get_wrong_answers(user_id):
    async with aiosqlite.connect(config('DB_NAME')) as db:
        async with db.execute('SELECT wrong_answers FROM quiz_state WHERE user_id = (?)', (user_id,)) as cursor:
            results = await cursor.fetchone()
            if results is not None:
                return results[0]
            else:
                return 0


async def get_static():
    async with aiosqlite.connect(config('DB_NAME')) as db:
        async with db.execute('SELECT user_id, right_answers, wrong_answers FROM quiz_state') as cursor:
            result = await cursor.fetchall()
            return sorted(result, key=lambda x: x[1], reverse=True)
