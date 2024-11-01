import asyncio
import logging

from aiogram import Bot, Dispatcher, F
from aiogram.filters.command import CommandStart
from aiogram.filters.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import ReplyKeyboardMarkup
from aiogram.utils.keyboard import CallbackData
from aiogram.utils.keyboard import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import KeyboardButton
from aiogram.types.input_file import FSInputFile

from api_key import API


class UserState(StatesGroup):
    age = State()
    growth = State()
    weight = State()


# Собственный фильтр, который пришлось создать, чтоб InlineKeyboardButton мог перехватываться
class MyFilter(CallbackData, prefix='my'):
    action: str


bot = Bot(token=API)
dp = Dispatcher(storage=MemoryStorage())
# Files
prod_1_img = FSInputFile('prod_1.png')
prod_2_img = FSInputFile('prod_2.png')
prod_3_img = FSInputFile('prod_3.png')
prod_4_img = FSInputFile('prod_4.png')
# Button
start_button_1 = KeyboardButton(text='Расчёт нормы калорий')
info_button = KeyboardButton(text='Информация о боте')
buy_button = KeyboardButton(text='Купить товар')
il_button_calc = InlineKeyboardButton(text='Начать расчёт', callback_data=MyFilter(action='start').pack())
il_button_info = InlineKeyboardButton(text='Формула расчёта',
                                      callback_data=MyFilter(action='formula').pack())
il_but_product_1 = InlineKeyboardButton(text='Продукт №1', callback_data=MyFilter(action='prod_1').pack())
il_but_product_2 = InlineKeyboardButton(text='Продукт №2', callback_data=MyFilter(action='prod_2').pack())
il_but_product_3 = InlineKeyboardButton(text='Продукт №3', callback_data=MyFilter(action='prod_3').pack())
il_but_product_4 = InlineKeyboardButton(text='Продукт №4', callback_data=MyFilter(action='prod_4').pack())
# Keyboard
il_markup_1 = InlineKeyboardMarkup(inline_keyboard=[[il_button_calc, il_button_info]])
il_markup_2 = InlineKeyboardMarkup(inline_keyboard=[[il_button_calc]])
il_prod_menu = InlineKeyboardMarkup(inline_keyboard=[[il_but_product_1, il_but_product_2],
                                                     [il_but_product_3, il_but_product_4]])
markup_1 = ReplyKeyboardMarkup(keyboard=[[start_button_1, info_button],
                                         [buy_button]], resize_keyboard=True, one_time_keyboard=True)



@dp.callback_query(MyFilter.filter(F.action == 'formula'))
async def formula(call):
    logging.info(f'Пользователь {call.message.from_user.full_name} ввёл {call.message.text}')
    await call.message.answer('Формула Миффлина-Сан Жеора\n'
                              'Для мужчин: 10 х вес (кг) + 6,25 x рост (см) – 5 х возраст (г) + 5\n'
                              'Для женщин: 10 x вес (кг) + 6,25 x рост (см) – 5 x возраст (г) – 161',
                              reply_markup=il_markup_2)
    await call.answer()


@dp.callback_query(MyFilter.filter(F.action == 'start'))
async def start_calc(call, state: FSMContext):
    logging.info(f'Пользователь {call.message.from_user.full_name} ввёл {call.message.text}')
    await state.set_state(UserState.age)
    await call.message.answer('Введите свой возраст в полных годах:')
    await call.answer()


@dp.callback_query(MyFilter.filter(F.action == 'prod_1'))
async def confirm_buying_product_1(call):
    await call.message.answer_photo(prod_1_img, 'Вы успешно приобрели продукт №1!')
    await call.answer()

@dp.callback_query(MyFilter.filter(F.action == 'prod_2'))
async def confirm_buying_product_2(call):
    await call.message.answer_photo(prod_2_img, 'Вы успешно приобрели продукт №2!')
    await call.answer()

@dp.callback_query(MyFilter.filter(F.action == 'prod_3'))
async def confirm_buying_product_3(call):
    await call.message.answer_photo(prod_3_img, 'Вы успешно приобрели продукт №3!')
    await call.answer()

@dp.callback_query(MyFilter.filter(F.action == 'prod_4'))
async def confirm_buying_product_4(call):
    await call.message.answer_photo(prod_4_img, 'Вы успешно приобрели продукт №4!')
    await call.answer()


@dp.message(F.text == 'Купить товар')
async def get_buying_list(message):
    # await message.answer('Название: Продукт №1 | Описание: Дешман, но норм | Цена: 100р')
    # await message.answer('Название: Продукт №2 | Описание: Бестселлер | Цена: 200р')
    # await message.answer('Название: Продукт №3 | Описание: Улучшеный состав | Цена: 300р')
    # await message.answer('Название: Продукт №4 | Описание: Элитный товар | Цена: 400р')
    await message.answer_photo(prod_1_img, 'Название: Продукт №1 | Описание: Дешман, но норм | Цена: 100р')
    await message.answer_photo(prod_2_img, 'Название: Продукт №2 | Описание: Бестселлер | Цена: 200р')
    await message.answer_photo(prod_3_img, 'Название: Продукт №3 | Описание: Улучшеный состав | Цена: 300р')
    await message.answer_photo(prod_4_img, 'Название: Продукт №4 | Описание: Элитный товар | Цена: 400р')
    await message.answer('Выберите продукт для покупки:', reply_markup=il_prod_menu)


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
async def set_age(message, state: FSMContext):
    logging.info(f'Пользователь {message.from_user.full_name} ввёл {message.text}')
    await state.set_state(UserState.age)
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


async def main() -> None:
    logging.basicConfig(filename='t_bot.log', filemode='w', level=logging.INFO, encoding='utf-8',
                        format='%(asctime)s, %(levelname)s, %(message)s')
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
