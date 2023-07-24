from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.dispatcher import FSMContext
from config import API_TOKEN
from commands import COMMANDS_LIST
from keyboards import keyboard_commands as kb_c
from keyboards import get_cancel
from user_with_tasks import User

storage = MemoryStorage()
bot = Bot(API_TOKEN)
dp = Dispatcher(bot=bot, storage=storage)


class ClientStatesGroup(StatesGroup):

    title = State()
    description = State()
    done_index = State()
    delete_index = State()

#cancel

@dp.message_handler(commands=['cancel'], state='*')
async def cancel_cmd(message: types.Message, state= FSMContext) -> None:
    current_state = await state.get_state()
    if current_state is None:
        return
    await message.reply('Отмена')
    await state.finish()

#cancel

#start

@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    await message.delete()
    await bot.send_message(chat_id=message.from_user.id, text="Hi!", reply_markup=kb_c)
    await bot.send_sticker(chat_id=message.from_user.id, sticker='CAACAgIAAxkBAAI3bGS8U4DEHDnPkueBtYpNdlXS5bJkAAJBAAMoD2oU8OnTI3UcRmEvBA')
    await bot.send_message(chat_id=message.from_user.id, text=COMMANDS_LIST)

#start
#Добавление задачи

@dp.message_handler(commands=['add'])
async def add_cmd(message: types.Message):
    await message.delete()
    await ClientStatesGroup.title.set()
    await message.answer("Запишите задачу в формате: Заголовок(описание)", reply_markup=get_cancel())


@dp.message_handler(state=ClientStatesGroup.title)
async def add_title_and_description(message: types.Message, state= FSMContext):
    user_id = message.from_user.id
    user_id = str(user_id)
    user = User(user_id)
    async with state.proxy() as data:
        data['title'] = message.text
        index = data['title'].find('(')
        if index == -1:
            title = data['title']
            description = ''
            data['title'] = title
            data['description'] = description
        else:
            max_index = len(data['title'])
            title = data['title'][0:index]
            description = data['title'][index:max_index]
            data['title'] = title
            data['description'] = description
        result = user.create_task(data['title'], data['description'])
        await state.finish()
    if result == "Упс что-то пошло не так...":
        await message.reply(result)
    else:
        task_index = user.find_last_index()
        task = user.find_task(task_index)
        task_str= f'▢  <b>{task[2]}</b> - {task[4]} {task[5]}'
        await bot.send_message(chat_id=message.from_user.id, text=task_str, parse_mode='HTML', reply_markup=kb_c)

#Добавление задачи

#выполнение задачи

@dp.message_handler(commands=['done'])
async def done_cmd(message: types.Message):
    await message.delete()
    await ClientStatesGroup.done_index.set()
    await bot.send_message(chat_id=message.from_user.id, text="Введите номер задачи которую вы хотите завершить!", reply_markup=get_cancel())


@dp.message_handler(lambda message: not message.text.isdigit(), state=ClientStatesGroup.done_index)
async def check_index_done(message: types.Message):
    return await message.reply("Нужно отправить номер задачи!")


@dp.message_handler(state=ClientStatesGroup.done_index)
async def done_task(message: types.Message, state= FSMContext):
    await ClientStatesGroup.next()
    user_id = message.from_user.id
    user_id = str(user_id)
    user = User(user_id)
    async with state.proxy() as data:
        data['done_index'] = message.text
        index_done = data['done_index']
        max_index = user.find_last_index()
        if int(index_done) > max_index or index_done == None:
            await bot.send_message(chat_id=message.from_user.id, text="Попробуйте ввести номер поменьше", reply_markup=kb_c)
        else:
            user.complete_task(index_done)
            task = user.find_task(index_done)
            task_str= f'✓  <b>{task[2]}</b> - {task[4]} {task[5]}'
            await bot.send_message(chat_id=message.from_user.id, text=task_str, parse_mode='HTML', reply_markup=kb_c)
        await state.finish()

#выполнение задачи

#отображение всех задач

@dp.message_handler(commands=['list'])
async def list_cmd(message: types.Message):
    await message.delete()
    user_id = message.from_user.id
    user_id = str(user_id)
    user = User(user_id)
    tasks = user.get_tasks()
    tasks_list = []
    for row in tasks:
        done = ''
        task_str = ''
        if row[3] == 1:
            done = '✓'
        elif row[3] == 0:
            done = '▢'
        task_str= f'{done}  <b>{row[2]}</b> - {row[4]} {row[5]}'
        tasks_list.append(task_str)
    all_tasks = "\n".join(tasks_list)
    if tasks:
        await bot.send_message(chat_id=message.from_user.id, text=all_tasks, parse_mode='HTML')
    else:
        status = "У вас нет задач!"
        await bot.send_message(chat_id=message.from_user.id, text=status)

#отображение всех задач

#удаление задачи

@dp.message_handler(commands=['delete'])
async def delete_cmd(message: types.Message):
    await message.delete()
    await ClientStatesGroup.delete_index.set()
    await bot.send_message(chat_id=message.from_user.id, text="Какую задачу вы хотите удалить ?", reply_markup=get_cancel())


@dp.message_handler(lambda message: not message.text.isdigit(), state=ClientStatesGroup.delete_index)
async def check_index_delete(message: types.Message):
    return await message.reply("Нужно отправить номер задачи!")


@dp.message_handler(state=ClientStatesGroup.delete_index)
async def delete_task(message: types.Message, state= FSMContext):
    await ClientStatesGroup.next()
    user_id = message.from_user.id
    user_id = str(user_id)
    user = User(user_id)
    async with state.proxy() as data:
        data['delete_index'] = message.text
        index_delete = data['delete_index']
        max_index = user.find_last_index()
        if int(index_delete) > max_index or index_delete == None:
            await bot.send_message(chat_id=message.from_user.id, text="Попробуйте ввести номер поменьше", reply_markup=kb_c)
        else:
            user.delete_task(index_delete)
            await message.reply('Задача удалена!', reply_markup=kb_c)
    await state.finish()

#удаление задачи

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
