import asyncio

from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command

from src.config_reader import config
from src.get_spacy import get_spacy_answer

# подключение к боту
bot = Bot(token = config.bot_token.get_secret_value())
dp = Dispatcher()

# глобальный словарь для хранения состояний пользователей
users_state = {}

# приветственное сообщение и кнопки
@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    kb = [
        [types.KeyboardButton(text = "Начать анализ")]
        ]
    keyboard = types.ReplyKeyboardMarkup(
        keyboard = kb,
        resize_keyboard = True,
        input_field_placeholder = "Выберите действие"
    )
    await message.answer("""
                         Данный бот создан в качестве тестового задания на вакансию ML-Engineer.

Бот демонстрирует технологию извлечения именованных сущностей на примере описания лекарственного препарата. Извлекаются международное непатентованное название (МНН) и группа препарата (ГРУППА). 

Данная задача решается с помощью обученной на тренеровочных данных модели spaCy.
Автор - t.me/AllexPri
                        """, 
                         reply_markup = keyboard)

# вывод сообщения после нажатия на кнопку
@dp.message(F.text == "Начать анализ")
async def without_puree(message: types.Message):

    # получаем сообщение пользователя
    users_state[message.from_user.id] = "spaCy"

    # приветственное сообщение
    await message.answer(f"Введите описание лекарственного препарата для анализа")

@dp.message(lambda message: users_state.get(message.from_user.id) == "spaCy")
async def process_text(message: types.Message):

    # отправляем запрос в модель 
    result = get_spacy_answer(message.text)

    # отправка текста с отметками
    await message.answer(result, parse_mode = "Markdown", disable_notification = True)    

# запуск процесса поллинга новых апдейтов
async def main():
    await dp.start_polling(bot)

# запуск блока
if __name__ == "__main__":
    asyncio.run(main())
