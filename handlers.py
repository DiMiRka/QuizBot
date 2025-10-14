from aiogram import F
from aiogram.filters.command import Command
from aiogram.types import Message, CallbackQuery
from create_bot import dp
from keyboards import start_keyboard
from services import new_quiz, get_question
from db import get_quiz_index, update_quiz_index
from utils import quiz_data


@dp.message(Command("start"))
async def cmd_start(message: Message):
    await message.answer("Добро пожаловать в квиз!", reply_markup=start_keyboard())


@dp.message(Command("quiz"))
@dp.message(F.data == "начать игру")
async def cmd_quiz(call: CallbackQuery):
    await call.message.answer(f"Давайте начнем квиз!")
    await new_quiz(call.message)


@dp.callback_query(F.data == "right_answer")
async def right_answer(call: CallbackQuery):
    # редактируем текущее сообщение с целью убрать кнопки (reply_markup=None)
    await call.bot.edit_message_reply_markup(
        chat_id=call.from_user.id,
        message_id=call.message.message_id,
        reply_markup=None
    )

    current_question_index = await get_quiz_index(call.from_user.id)
    await call.message.answer("Верно!")

    current_question_index += 1
    await update_quiz_index(call.from_user.id, current_question_index)

    if current_question_index < len(quiz_data):
        await get_question(call.message, call.from_user.id)
    else:
        await call.message.answer("Это был последний вопрос. Квиз завершен!")


@dp.callback_query(F.data == "wrong_answer")
async def wrong_answer(call: CallbackQuery):
    # редактируем текущее сообщение с целью убрать кнопки (reply_markup=None)
    await call.bot.edit_message_reply_markup(
        chat_id=call.from_user.id,
        message_id=call.message.message_id,
        reply_markup=None
    )

    current_question_index = await get_quiz_index(call.from_user.id)
    correct_option = quiz_data[current_question_index]['correct_option']
    await call.message.answer(f"Неправильно. Правильный ответ: {quiz_data[current_question_index]['options'][correct_option]}")

    current_question_index += 1
    await update_quiz_index(call.from_user.id, current_question_index)

    if current_question_index < len(quiz_data):
        await get_question(call.message, call.from_user.id)
    else:
        await call.message.answer("Это был последний вопрос. Квиз завершен!")