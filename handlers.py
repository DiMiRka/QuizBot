from aiogram import F
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery

from create_bot import dp
from keyboards import start_keyboard
from services import new_quiz, get_question
from db import (get_quiz_index, update_quiz_index, get_right_answers, get_wrong_answers,
                update_wrong_answers, update_right_answers, get_static)
from utils import quiz_data


@dp.message(Command("start"))
async def cmd_start(message: Message):
    await message.answer("Добро пожаловать в квиз!", reply_markup=start_keyboard())


@dp.message(Command("quiz"))
@dp.callback_query(F.data == "начать игру")
async def users_stats(call: CallbackQuery):
    static = await get_static()

    text = "Статистика игроков:\n"
    for user in static:
        text += f'\n{user["user_id"]}: {str(user[1])}/{str(user[1]+user[2])}'

    await call.message.answer(text)


@dp.message(Command("static"))
@dp.callback_query(F.data == "статистика игроков")
async def cmd_quiz(call: CallbackQuery):
    await call.message.answer(f"Давайте начнем квиз!")
    await new_quiz(call.message)


@dp.callback_query(F.data == "right_answer")
async def right_answer(call: CallbackQuery):
    await call.bot.edit_message_reply_markup(
        chat_id=call.from_user.id,
        message_id=call.message.message_id,
        reply_markup=None
    )

    current_question_index = await get_quiz_index(call.from_user.id)
    current_right_answers = await get_right_answers(call.from_user.id)
    await call.message.answer(f'Ответ "{call.message.text}" Верен!')

    current_question_index += 1
    await update_quiz_index(call.from_user.id, current_question_index)

    current_right_answers += 1
    await update_right_answers(call.from_user.id, current_right_answers)

    if current_question_index < len(quiz_data):
        await get_question(call.message, call.from_user.id)
    else:
        await call.message.answer("Это был последний вопрос. Квиз завершен!")


@dp.callback_query(F.data == "wrong_answer")
async def wrong_answer(call: CallbackQuery):
    await call.bot.edit_message_reply_markup(
        chat_id=call.from_user.id,
        message_id=call.message.message_id,
        reply_markup=None
    )

    current_question_index = await get_quiz_index(call.from_user.id)
    current_wrong_answers = await get_wrong_answers(call.from_user.id)
    correct_option = quiz_data[current_question_index]['correct_option']
    await call.message.answer(f"Неправильно. Правильный ответ: {quiz_data[current_question_index]['options'][correct_option]}")

    current_question_index += 1
    await update_quiz_index(call.from_user.id, current_question_index)

    current_wrong_answers += 1
    await update_wrong_answers(call.from_user.id, current_wrong_answers)

    if current_question_index < len(quiz_data):
        await get_question(call.message, call.from_user.id)
    else:
        await call.message.answer("Это был последний вопрос. Квиз завершен!")
