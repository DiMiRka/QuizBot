from db import update_quiz_index, update_right_answers, update_wrong_answers, get_quiz_index, update_user_name
from utils import quiz_data
from keyboards import quiz_keyboard


async def new_quiz(call):
    user_id = call.from_user.id
    user_name = call.from_user.username
    current_question_index = 0
    current_right_answers = 0
    current_wrong_answers = 0
    print(user_id)
    print(user_name)
    await update_user_name(user_id, user_name)
    await update_quiz_index(user_id, current_question_index)
    await update_right_answers(user_id, current_right_answers)
    await update_wrong_answers(user_id, current_wrong_answers)
    await get_question(call.message, user_id)


async def get_question(message, user_id):
    current_question_index = await get_quiz_index(user_id)
    correct_index = quiz_data[current_question_index]['correct_option']
    opts = quiz_data[current_question_index]['options']

    kb = quiz_keyboard(opts, opts[correct_index])

    await message.answer(f"{quiz_data[current_question_index]['question']}", reply_markup=kb)


async def get_answer(message, call):
    markup = message.reply_markup
    answer = str()

    for row in markup.inline_keyboard:
        for button in row:
            if button.callback_data == call:
                answer = button.text

    return answer
