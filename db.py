import aiosqlite
from decouple import config


async def create_table():
    async with aiosqlite.connect(config('DB_NAME')) as db:
        await db.execute('''CREATE TABLE IF NOT EXISTS quiz_state  
                            (user_id INTEGER PRIMARY KEY, user_name VARCHAR, question_index INTEGER NOT NULL DEFAULT 0,
                            right_answers INTEGER, wrong_answers INTEGER)''')
        await db.commit()


async def update_user_name(user_id, user_name):
    async with aiosqlite.connect(config('DB_NAME')) as db:
        await db.execute('UPDATE quiz_state SET user_name = ? WHERE user_id = ?', (user_name, user_id))
        await db.commit()


async def update_quiz_index(user_id, index):
    async with aiosqlite.connect(config('DB_NAME')) as db:
        await db.execute('''INSERT INTO quiz_state (user_id, question_index) VALUES (?, ?)
                         ON CONFLICT(user_id) DO UPDATE SET question_index=excluded.question_index''',
                         (int(user_id), index))
        await db.commit()


async def get_quiz_index(user_id):
     async with aiosqlite.connect(config('DB_NAME')) as db:
        async with db.execute('SELECT question_index FROM quiz_state WHERE user_id = ?', (int(user_id),)) as cursor:
            results = await cursor.fetchone()
            if results is None or results[0] is None:
                return 0
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
        async with db.execute('SELECT user_name, right_answers, wrong_answers FROM quiz_state') as cursor:
            result = await cursor.fetchall()
            result = sorted(result, key=lambda x: x[1], reverse=True)

            text = "Статистика игроков:\n"
            for row in result:
                text += f'\n{row[0]} результат {str(row[1])}/{str(row[1] + row[2])}'

            return text


async def get_quiz_result(user_id):
    async with aiosqlite.connect(config('DB_NAME')) as db:
        async with db.execute('SELECT right_answers, wrong_answers FROM quiz_state WHERE user_id = (?)', (user_id,)) as cursor:
            result = await cursor.fetchone()
            print(result)
            text = f"{result[0]}/{result[0]+result[1]}"
            return text
