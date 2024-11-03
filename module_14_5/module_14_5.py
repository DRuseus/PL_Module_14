import asyncio
import logging

from aiogram import Bot, Dispatcher, F
from aiogram.filters.command import CommandStart
from aiogram.filters.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import ReplyKeyboardMarkup
from aiogram.utils.keyboard import CallbackData, InlineKeyboardBuilder
from aiogram.utils.keyboard import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import KeyboardButton
from aiogram.types.input_file import FSInputFile

from api_key import API
from crud_functions import *


class RegistrationState(StatesGroup):
    username = State()
    email = State()
    age = State()
    balance = State()


class UserState(StatesGroup):
    age = State()
    growth = State()
    weight = State()


# Собственный фильтр, который пришлось создать, чтоб InlineKeyboardButton мог перехватываться
class MyFilter(CallbackData, prefix='my'):
    action: str

# Initialisation of Bot and Router
bot = Bot(token=API)
dp = Dispatcher(storage=MemoryStorage())
# Files
prod_1_img = FSInputFile('prod_1.png')
prod_2_img = FSInputFile('prod_2.png')
prod_3_img = FSInputFile('prod_3.png')
prod_4_img = FSInputFile('prod_4.png')
# Button
#start_button_1 = KeyboardButton(text='Расчёт нормы калорий')
#info_button = KeyboardButton(text='Информация о боте')
#buy_button = KeyboardButton(text='Купить товар')
il_button_calc = InlineKeyboardButton(text='Начать расчёт', callback_data=MyFilter(action='start').pack())
il_button_info = InlineKeyboardButton(text='Формула расчёта',
                                      callback_data=MyFilter(action='formula').pack())
# Keyboard
il_markup_1 = InlineKeyboardMarkup(inline_keyboard=[[il_button_calc, il_button_info]])
il_markup_2 = InlineKeyboardMarkup(inline_keyboard=[[il_button_calc]])
markup_1 = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text='Расчёт нормы калорий'), KeyboardButton(text='Информация о боте')],
                                         [KeyboardButton(text='Купить товар')],
                                         [KeyboardButton(text='Регистрация')]
                                         ],
                               resize_keyboard=True, one_time_keyboard=True)


# Отвечает на нажатие кнопки в IL-клавиатуре "Формула расчёта"
@dp.callback_query(MyFilter.filter(F.action == 'formula'))
async def formula(call):
    logging.info(f'Пользователь {call.message.from_user.full_name} ввёл {call.message.text}')
    await call.message.answer('Формула Миффлина-Сан Жеора\n'
                              'Для мужчин: 10 х вес (кг) + 6,25 x рост (см) – 5 х возраст (г) + 5\n'
                              'Для женщин: 10 x вес (кг) + 6,25 x рост (см) – 5 x возраст (г) – 161',
                              reply_markup=il_markup_2)
    await call.answer()

# Отвечает на нажатие кнопки в IL-клавиатуре "начать расчёт"
@dp.callback_query(MyFilter.filter(F.action == 'start'))
async def start_calc(call, state: FSMContext):
    logging.info(f'Пользователь {call.message.from_user.full_name} ввёл {call.message.text}')
    await state.set_state(UserState.age)
    await call.message.answer('Введите свой возраст в полных годах:')
    await call.answer()


@dp.callback_query(MyFilter.filter(F.action.contains('prod')))
async def confirm_buying_product_1(call):
    logging.info(f'Пользователь {call.message.from_user.full_name} ввёл {call.message.text}')
    data = call.data[-1]
    try:
        await call.message.answer_photo(FSInputFile(f'prod_{data}.png'), f'Вы успешно приобрели продукт №{data}!')
    except:
        # Это отлов ошибки отсутствия изображения
        await call.message.answer_photo(FSInputFile('no_img.jpg'), f'Вы успешно приобрели продукт №{data}!')
    await call.answer()


@dp.message(F.text.lower() == 'регистрация')
async def sign_up(message, state: FSMContext):
    logging.info(f'Пользователь {message.from_user.full_name} ввёл {message.text}')
    await state.set_state(RegistrationState.username)
    await message.answer('Введите имя пользователя (только латинский алфавит):')


@dp.message(RegistrationState.username)
async def set_username(message, state: FSMContext):
    if check_user(message.text):
        await state.set_state(RegistrationState.username)
        await message.answer('Пользователь существует, введите другое имя')
    else:
        await state.update_data(username=str(message.text))
        await state.set_state(RegistrationState.email)
        await message.answer('Введите свой email:')


@dp.message(RegistrationState.email)
async def set_email(message, state: FSMContext):
    await state.update_data(email=str(message.text))
    await state.set_state(RegistrationState.age)
    await message.answer('Введите свой возраст:')


@dp.message(RegistrationState.age)
async def set_age(message, state: FSMContext):
    await state.update_data(age=str(message.text))
    data = await state.get_data()
    add_user(**data)
    await message.answer(f'Регистрация прошла успешно')
    await state.clear()


@dp.message(F.text.lower() == 'купить товар')
async def get_buying_list(message):
    logging.info(f'Пользователь {message.from_user.full_name} ввёл {message.text}')
    for prod in prod_list:
        try:
            await message.answer_photo(FSInputFile(f'prod_{prod[0]}.png'), f'Название: {prod[1]} | Описание: {prod[2]} | Цена: {prod[3]}')
        except:
            # Это отлов ошибки отсутствия изображения
            await message.answer_photo(FSInputFile('no_img.jpg'),
                                       f'Название: {prod[1]} | Описание: {prod[2]} | Цена: {prod[3]}')
    await message.answer('Выберите продукт для покупки:', reply_markup=builder.as_markup())


@dp.message(F.text == 'Информация о боте')
async def get_info(message):
    logging.info(f'Пользователь {message.from_user.full_name} ввёл {message.text}')
    await message.answer(
        'Это телеграм-бот, который поможет тебе правильно питаться и поддерживать здоровый образ жизни.\n'
        'Выберете опцию:',
        reply_markup=il_markup_1)


@dp.message(CommandStart())
async def start(message):
    logging.info(f'Пользователь {message.from_user.full_name} ввёл {message.text}')
    await message.answer(f'Привет, {message.from_user.username}! Я бот, помогающий твоему здоровью.\n',
                         reply_markup=markup_1)


@dp.message(F.text.contains('нормы калорий'))
async def set_age(message):
    logging.info(f'Пользователь {message.from_user.full_name} ввёл {message.text}')
    await message.answer('Выберите опцию:', reply_markup=il_markup_1)


@dp.message(UserState.age)
async def set_growth(message, state: FSMContext):
    logging.info(f'Пользователь {message.from_user.full_name} ввёл {message.text}')
    await state.update_data(age=float(message.text))
    await state.set_state(UserState.growth)
    await message.answer('Введите свой рост в сантиметрах:')


@dp.message(UserState.growth)
async def set_weight(message, state: FSMContext):
    logging.info(f'Пользователь {message.from_user.full_name} ввёл {message.text}')
    await state.update_data(growth=float(message.text))
    await state.set_state(UserState.weight)
    await message.answer('Введите свой вес в килограммах:')


@dp.message(UserState.weight)
async def send_calories(message, state: FSMContext):
    logging.info(f'Пользователь {message.from_user.full_name} ввёл {message.text}')
    await state.update_data(weight=float(message.text))
    data = await state.get_data()
    age = data['age']
    growth = data['growth']
    weight = data['weight']
    await message.answer(f'Если вы мужчина то ваша норма калорий в день составляет:\n'
                         f'{10 * weight + 6.25 * growth + 5 * age + 5}\n'
                         f'А если в женщина, то ваша дневная норма калорий:\n'
                         f'{10 * weight + 6.25 * growth + 5 * age - 161}')
    await state.clear()


@dp.message(F.text.lower().in_({'спасибо', 'благодар', 'спс','спасибо большое','большое спасибо','благодарочка',
                                'сяб','от души','круто','нифига себе',"класс","классно","неплохо",
                                "премного благодарю","спасибочки","спасибо вам",
                                }))
async def all_messages(message):
    logging.info(f'Пользователь {message.from_user.full_name} ввёл {message.text}')
    await message.answer(f'Всегда пожалуйста!')


@dp.message()
async def all_messages(message):
    logging.info(f'Пользователь {message.from_user.full_name} ввёл {message.text}')
    await message.answer('Введите команду /start, чтобы начать общение.')

# Багует и зависает иногда
"""async def main() -> None:
    logging.basicConfig(filename='t_bot.log', filemode='w', level=logging.INFO, encoding='utf-8',
                        format='%(asctime)s, %(levelname)s, %(message)s')
    await dp.start_polling(bot)"""


if __name__ == "__main__":
    logging.basicConfig(filename='t_bot.log', filemode='w', level=logging.INFO, encoding='utf-8',
                        format='%(asctime)s, %(levelname)s, %(message)s')

    initiate_db()

    put_in_prod(1, 'Продукт №1', 100, description='Дешман, но норм')
    put_in_prod(2, 'Продукт №2', 200, description='Бестселлер')
    put_in_prod(3, 'Продукт №3', 300, description='Улучшеный состав')
    put_in_prod(4, 'Продукт №4', 400, description='Элитный товар')

    prod_list = get_all_products()

    builder = InlineKeyboardBuilder()
    for index in range(1, len(prod_list) + 1):
        builder.button(text=f"Продукт №{index}", callback_data=MyFilter(action=f"prod_{index}").pack())
    builder.adjust(2)

    # Работает надёжнее функции ниже
    dp.run_polling(bot)

    # Багует и Зависает иногда
    #asyncio.run(main())
