from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def start_keyboard():
    kb_list = [
        [InlineKeyboardButton(text="Начать викторину", callback_data='начать викторину')],
        [InlineKeyboardButton(text="Статистика игроков", callback_data='статистика игроков')]
    ]

    keyboard = InlineKeyboardMarkup(
        inline_keyboard=kb_list,
        resize_keyboard=True,
        one_time_keyboard=True)
    return keyboard


def quiz_keyboard(answer_options, right_answer):
    kb_list = []

    for option in answer_options:
        kb_list.append([InlineKeyboardButton(text=option,
                                             callback_data="right_answer" if option == right_answer else "wrong_answer")])

    keyboard = InlineKeyboardMarkup(
        inline_keyboard=kb_list,
        resize_keyboard=True,
        one_time_keyboard=True)
    return keyboard
