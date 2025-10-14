from db import update_quiz_index, get_quiz_index
from utils import quiz_data
from keyboards import quiz_keyboard


async def new_quiz(message):
    user_id = message.from_user.id
    current_question_index = 0
    await update_quiz_index(user_id, current_question_index)
    await get_question(message, user_id)


async def get_question(message, user_id):
    current_question_index = await get_quiz_index(user_id)
    correct_index = quiz_data[current_question_index]['correct_option']
    opts = quiz_data[current_question_index]['options']

    kb = quiz_keyboard(opts, opts[correct_index])

    await message.answer(f"{quiz_data[current_question_index]['question']}", reply_markup=kb)
