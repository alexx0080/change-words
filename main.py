# Импорт библиотек
import aiogram, asyncio, random, config, time
from aiogram import Bot, Dispatcher, F, types
from aiogram.types import Message, CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.filters import Command, CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup



# Создать бота
bot = Bot(config.TOKEN)
dp = Dispatcher()



# Команда start
@dp.message(CommandStart())
async def command_start(message: Message):
    button_add_word = InlineKeyboardButton(text='Добавить', callback_data='add_word')
    button_get_word = InlineKeyboardButton(text='Получить', callback_data='get_word')
    button = InlineKeyboardMarkup(inline_keyboard=[[button_add_word, button_get_word]])
    await message.answer('Привет, я помогу тебе с запоминанием английский слов!\nПиши мне проблематичные слова и их перевод, я их буду сохранять и периодически,\
                         а также когда ты меня попросишь высылать их тебе и запрашивать перевод.', reply_markup=button)



# Запуск
async def main():
    await dp.start_polling(bot)

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except:
        print('goodbye!')