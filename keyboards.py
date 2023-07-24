from aiogram import types
from aiogram.types import KeyboardButton, ReplyKeyboardMarkup
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


#keyboards
keyboard_commands = ReplyKeyboardMarkup(resize_keyboard=True)

start_button = KeyboardButton('/start')
add_button = KeyboardButton('/add')
done_button = KeyboardButton('/done')
list_button = KeyboardButton('/list')
delete_button = KeyboardButton('/delete')

keyboard_commands.add(start_button, add_button, done_button, list_button, delete_button)

def get_cancel() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(resize_keyboard=True).add(KeyboardButton('/cancel'))


#Inline keyboards
# inline_keyboard_commands = InlineKeyboardMarkup(row_width=2)

# inline_first_button = InlineKeyboardButton(text='1', callback_data='1')
# inline_second_button = InlineKeyboardButton(text='2', callback_data='2')
# inline_third_button = InlineKeyboardButton(text='3', callback_data='3')
# inline_fourth_button = InlineKeyboardButton(text='4', callback_data='4')
# inline_fifth_button = InlineKeyboardButton(text='5', callback_data='5')
# inline_close_button = InlineKeyboardButton(text='Убрать клавиатуру', callback_data='close')

# inline_keyboard_commands.add(
#     inline_first_button,
#     inline_second_button,
#     inline_third_button,
#     inline_fourth_button,
#     inline_fifth_button,
#     inline_close_button
#     )
