# Импорт библиотек
import aiogram, asyncio, random, config, time, table_with_words
from aiogram import Bot, Dispatcher, F, types
from aiogram.types import Message, CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.filters import Command, CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup



# Создать объект класса TableWord
word_obj = table_with_words.TableWords()



# Создать машину состояний для добавления слова и перевода
class AddWord(StatesGroup):
    get_eng_word = State()
    get_translate = State()

# Создать машину состояний для получения слова
class GetWord(StatesGroup):
    get_translate = State()



# Создать бота
bot = Bot(config.TOKEN)
dp = Dispatcher()



# Команда start
@dp.message(CommandStart())
async def command_start(message: Message):
    button_add_word = InlineKeyboardButton(text='Добавить', callback_data='add_word')
    button_get_word = InlineKeyboardButton(text='Получить', callback_data='get_word')
    button = InlineKeyboardMarkup(inline_keyboard=[[button_add_word], [button_get_word]])
    await message.answer('Привет, я помогу тебе с запоминанием Английский слов!\nПиши мне проблематичные слова и их перевод, я их буду сохранять и периодически,\
а также когда ты меня попросишь высылать их тебе и запрашивать перевод.', reply_markup=button)
    

# Команда добавить слово + кнопка
@dp.message(Command('add_word'))
async def add_word_func(message: Message, state: FSMContext):
    await message.answer('Введите Английское слово')
    await state.set_state(AddWord.get_eng_word)

@dp.message(AddWord.get_eng_word)
async def get_english_word(message: Message, state: FSMContext):
    eng_word = message.text
    if eng_word.isalpha():
        eng_word = eng_word.lower()
        await state.update_data(english_word = eng_word)
        await message.answer('Введите перевод')
        await state.set_state(AddWord.get_translate)
    else:
        await message.answer('Введите корректное слово, состоящее только из букв')

@dp.message(AddWord.get_translate)
async def get_translate(message: Message, state: FSMContext):
    trans = message.text
    if trans.isalpha():
        trans = trans.lower()
        await state.update_data(translate = trans)
        dictionary = await state.get_data()
        eng_word = dictionary['english_word']
        rus_word = dictionary['translate']
        await state.clear()
        word_obj.add_notice(eng_word, rus_word)
        await message.answer('Отлично, слово добавлено в базу данных!')
    else:
        await message.answer('Введите корректный перевод, состоящий только из букв')

# Button
@dp.callback_query(F.data == 'add_word')
async def add_word_button(callback: CallbackQuery, state: FSMContext):
    await add_word_func(callback.message, state)


# Команда получить + кнопка get_word
@dp.message(Command('get_word'))
async def get_word_func(message: Message, state: FSMContext):
    list_words = word_obj.read_table()
    random_word = random.choice(list_words)
    await state.update_data(english_word = random_word)
    await message.answer(f'''Итак, вот твое слово: {random_word.capitalize()}\nПереведи его''')
    await state.set_state(GetWord.get_translate)

@dp.message(GetWord.get_translate)
async def get_translate_get_word(message: Message, state: FSMContext):
    translate = message.text
    if translate.isalpha():
        dictionary = await state.get_data()
        eng_word = dictionary['english_word']
        true_translate = word_obj.read_string(eng_word)
        if translate.lower() == true_translate:
            await message.answer('Молодец, абсолютно верно!')
        else:
            await message.answer(f'Неправильно. Это слово переводится как {true_translate}')
        await state.clear()
    else:
        await message.answer(f'Введите корректный перевод, состоящий только из букв')

# Button
@dp.callback_query(F.data == 'get_word')
async def get_word_button(callback: CallbackQuery, state: FSMContext):
    await get_word_func(callback.message, state)



# Запуск
async def main():
    await dp.start_polling(bot)

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except:
        print('goodbye!')