from aiogram import F, Router
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery

from keyboards import start_keyboard
from services import new_quiz, get_question, get_answer
from db import (get_quiz_index, update_quiz_index, get_right_answers, get_wrong_answers,
                update_wrong_answers, update_right_answers, get_static, get_quiz_result)
from utils import quiz_data

router = Router()


@router.message(Command("start"))
async def cmd_start(message: Message):
    await message.answer("Добро пожаловать в квиз!", reply_markup=start_keyboard())


@router.message(Command("static"))
async def users_stats_command(message: Message):
    static = await get_static()
    await message.answer(static)


@router.callback_query(F.data == "статистика игроков")
async def users_stats_button(call: CallbackQuery):
    static = await get_static()
    await call.message.answer(static)


@router.message(Command("quiz"))
async def start_quiz_command(message: Message):
    user_id = message.from_user.id
    user_name = message.from_user.username
    print(user_id, user_name)
    await message.answer(f"Давайте начнем квиз!")
    await new_quiz(message, user_id, user_name)


@router.callback_query(F.data == "начать викторину")
async def start_quiz_button(call: CallbackQuery):
    user_id = call.from_user.id
    user_name = call.from_user.username
    print(user_id, user_name)
    await call.message.answer(f"Давайте начнем квиз!")
    await new_quiz(call.message, user_id, user_name)


@router.callback_query(F.data == "right_answer")
async def right_answer(call: CallbackQuery):
    await call.bot.edit_message_reply_markup(
        chat_id=call.from_user.id,
        message_id=call.message.message_id,
        reply_markup=None
    )

    current_last_answer = await get_answer(call.message, call.data)
    current_question_index = await get_quiz_index(call.from_user.id)
    current_right_answers = await get_right_answers(call.from_user.id)
    await call.message.answer(f'Ответ "{current_last_answer}"\nВерный ✅!')

    current_question_index += 1
    await update_quiz_index(call.from_user.id, current_question_index)

    current_right_answers += 1
    await update_right_answers(call.from_user.id, current_right_answers)

    if current_question_index < len(quiz_data):
        await get_question(call.message, call.from_user.id)
    else:
        result = await get_quiz_result(call.from_user.id)
        await call.message.answer("Это был последний вопрос. Квиз завершен!")
        await call.message.answer(f"Твой результат {result}")


@router.callback_query(F.data == "wrong_answer")
async def wrong_answer(call: CallbackQuery):
    await call.bot.edit_message_reply_markup(
        chat_id=call.from_user.id,
        message_id=call.message.message_id,
        reply_markup=None
    )

    current_last_answer = await get_answer(call.message, call.data)
    current_question_index = await get_quiz_index(call.from_user.id)
    current_wrong_answers = await get_wrong_answers(call.from_user.id)
    correct_option = quiz_data[current_question_index]['correct_option']
    await call.message.answer(f'Ответ "{current_last_answer}" Неправильный❌.\nПравильный ответ: {quiz_data[current_question_index]['options'][correct_option]}')

    current_question_index += 1
    await update_quiz_index(call.from_user.id, current_question_index)

    current_wrong_answers += 1
    await update_wrong_answers(call.from_user.id, current_wrong_answers)

    if current_question_index < len(quiz_data):
        await get_question(call.message, call.from_user.id)
    else:
        result = await get_quiz_result(call.from_user.id)
        await call.message.answer("Это был последний вопрос. Квиз завершен!")
        await call.message.answer(f"Твой результат {result}")
