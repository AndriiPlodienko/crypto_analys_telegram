from pybit.unified_trading import HTTP
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from config import TOKEN, api_key, api_secret

session = HTTP(
    testnet=False,
    api_key=api_key,
    api_secret=api_secret
)

bot = Bot(TOKEN)
dp = Dispatcher(bot)
b1 = KeyboardButton('/balance')
b2 = KeyboardButton('/limits')
b3 = KeyboardButton('/positions')

kb_client = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
kb_client.add(b1).insert(b2).add(b3)

@dp.message_handler(commands=['start', 'help'])
async def command_start(message: types.Message):
        await bot.send_message(message.from_user.id, "Bot was started!", reply_markup=kb_client)


@dp.message_handler(commands=['balance'])
async def balance(message: types.message):
        positions = session.get_wallet_balance()['result']
        for key, value in positions.item():
                if value['equity'] > 0:
                        data = 'Balance:  '+str(round(value['equity'], 2))+ ' '+key
                        await message.answer(data)


@dp.message_handler(commands=['limits'])
async def limits(message: types.Message):
        doc = []
        all_tickers = session.query_symbol()['result']
        for i in all_tickers:
                data = i['name']
                doc.append(data)
        for x in doc:
                order_data = session.get_active_order(symbol=x, order_status="New")['result']['data']
                if order_data:
                        limits = order_data[0]
                        data = limits['symbol']+', '+str(limits['price'])+'$,'+' '+str(limits['qty'])+' '+limits['side']
                        print(limits)
                        await message.answer(data)


@dp.message_handler(commands=['positions'])
async def positions(message: types.Message):
        positions = session.my_position()['result']
        for x in positions:
                data = x['data']
                if data['size'] > 0:
                        result = data['symbol']+', '+str(data['size'])+' '+data['side']
                        print(data)
                        await message.answer(result)

