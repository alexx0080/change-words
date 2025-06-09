# Импорт библиотек
import aiogram, asyncio, random, config, time, table_with_words
from aiogram import Bot, Dispatcher, F, types
from aiogram.types import Message, CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.filters import Command, CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup



# Создать список запрещенных символов
all_chars = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '.', ',', '?', '!', '+', '-', '*', '/']


# Создать пустую очередь
queue = []


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
    button_add_word = InlineKeyboardButton(text='📚 Добавить 📚', callback_data='add_word')
    button_get_word = InlineKeyboardButton(text='📩 Получить 📩', callback_data='get_word')
    button = InlineKeyboardMarkup(inline_keyboard=[[button_add_word], [button_get_word]])
    await message.answer('Привет 👋\nЯ помогу тебе с запоминанием Английский слов! 😃\nПиши мне проблематичные слова и их перевод, я их буду сохранять и \
когда ты меня попросишь высылать их тебе и запрашивать перевод.', reply_markup=button)
    


# Команда меню
async def menu(message: Message):
    button_add_word = InlineKeyboardButton(text='📚 Добавить 📚', callback_data='add_word')
    button_get_word = InlineKeyboardButton(text='📩 Получить 📩', callback_data='get_word')   
    button = InlineKeyboardMarkup(inline_keyboard=[[button_add_word], [button_get_word]])
    await message.answer('Выберите действие 👇', reply_markup=button)
    


# Команда добавить слово + кнопка
@dp.message(Command('add_word'))
async def add_word_func(message: Message, state: FSMContext):
    await message.answer('Введите Английское слово')
    await state.set_state(AddWord.get_eng_word)

@dp.message(AddWord.get_eng_word)
async def get_english_word(message: Message, state: FSMContext):
    eng_word = message.text
    eng_word = eng_word.lower()
    list_words = word_obj.read_table()
    if eng_word not in list_words:
        if this_word_contain_only_letter(eng_word) == True:
            await state.update_data(english_word = eng_word)
            await message.answer('Введите перевод')
            await state.set_state(AddWord.get_translate)
        else:
            await message.answer('⚠️ Введите корректное слово, состоящее только из букв ⚠️')
    else:
        translate = word_obj.read_string(eng_word)
        await message.answer(f'❗ Слово уже было добавлено ❗\nВот его перевод - {translate.capitalize()}')
        await state.clear()
    

@dp.message(AddWord.get_translate)
async def get_translate(message: Message, state: FSMContext):
    trans = message.text
    if this_word_contain_only_letter(trans) == True:
        trans = trans.lower()
        await state.update_data(translate = trans)
        dictionary = await state.get_data()
        eng_word = dictionary['english_word']
        rus_word = dictionary['translate']
        await state.clear()
        word_obj.add_notice(eng_word, rus_word)
        await message.answer('Отлично, слово добавлено в базу данных! ✅')
        await menu(message)
    else:
        await message.answer('⚠️ Введите корректный перевод, состоящий только из букв ⚠️')

# Button
@dp.callback_query(F.data == 'add_word')
async def add_word_button(callback: CallbackQuery, state: FSMContext):
    await add_word_func(callback.message, state)


# Команда получить + кнопка get_word
@dp.message(Command('get_word'))
async def get_word_func(message: Message, state: FSMContext):
    list_words = word_obj.read_table()
    random_word = random.choice(list_words)
    while random_word in queue:
        random_word = random.choice(list_words)
    await state.update_data(english_word = random_word)
    await message.answer(f'''Итак, вот твое слово - {random_word.capitalize()}\nПереведи его''')
    await state.set_state(GetWord.get_translate)

@dp.message(GetWord.get_translate)
async def get_translate_get_word(message: Message, state: FSMContext):
    translate = message.text
    if this_word_contain_only_letter(translate) == True:
        dictionary = await state.get_data()
        eng_word = dictionary['english_word']
        true_translate = word_obj.read_string(eng_word)
        if translate.lower() == true_translate:
            await message.answer('Молодец, абсолютно верно! ✅')
            add_word_in_queue(eng_word)
        else:
            await message.answer(f'Неправильно ❌\nЭто слово переводится как {true_translate.capitalize()}.')
        await state.clear()
        await menu(message)
    else:
        await message.answer(f'⚠️ Введите корректный перевод, состоящий только из букв ⚠️')

# Button
@dp.callback_query(F.data == 'get_word')
async def get_word_button(callback: CallbackQuery, state: FSMContext):
    await get_word_func(callback.message, state)



# Функция для проверки слова
def this_word_contain_only_letter(word):
    only_letters = True
    for letter in word:
        if letter in all_chars:
            only_letters = False
            break
    return only_letters



# Функция для создание очереди
def add_word_in_queue(word):
    if len(queue) < 50:
        queue.append(word)
    else:
        queue.remove(queue[0])
        queue.append(word)



# Обработка мусорных данных
@dp.message()
async def random_data(message: Message):
    await message.answer('Пожалуйста, введите одну из команд\n\
🗂 Вот список команд:\n📌 /start - Начало работы\n\
📌 /add_word - Добавить слово\n📌 /get_word - Получить слово')



# Запуск
async def main():
    await dp.start_polling(bot)

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except:
        print('goodbye!')