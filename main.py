from aiogram import Bot, Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from append import append_data_to_sheet

class Reg(StatesGroup):
    name = State()
    age = State()
    email = State()
    phone = State()


BOT_TOKEN = "7475860566:AAFKC9j1e3w9Idcs2IyZOxBq9LFFDRuqOmk"
bot = Bot(BOT_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)

@dp.message_handler(commands=['start'])
async def start_command(message: types.Message):
    await message.answer("Salom! Men Google Sheets bilan ishlovchi botman.\n\nBoshlash uchun ism va familiyangizni yuboring:")
    await Reg.name.set()

@dp.message_handler(state=Reg.name)
async def name(message: types.Message, state: FSMContext):
    await state.update_data(name=message.text)
    await message.answer(f"Juda yaxshi endi esa yoshingizni yuboring:")
    await Reg.age.set()

@dp.message_handler(state=Reg.age)
async def age(message: types.Message, state: FSMContext):
    await state.update_data(age=message.text)
    await message.answer(f"Juda yaxshi endi esa emailingizni yuboring:")
    await Reg.email.set()

@dp.message_handler(state=Reg.email)
async def email(message: types.Message, state: FSMContext):
    await state.update_data(email=message.text)
    await message.answer(f"Juda yaxshi endi esa telefon raqamingizni yuboring:")
    await Reg.phone.set()

@dp.message_handler(state=Reg.phone)
async def phone(message: types.Message, state: FSMContext):
    await state.update_data(phone=message.text)
    user_data = await state.get_data()
    append_data_to_sheet(message.from_user.id, user_data['name'], user_data['age'], user_data['email'], user_data['phone'])
    await message.answer(f"Juda yaxshi endi esa sizning ma'lumotlaringiz:\n\n"
                         f"Ism: {user_data['name']}\n"
                         f"Yosh: {user_data['age']}\n"
                         f"Email: {user_data['email']}\n"
                         f"Telefon raqami: {user_data['phone']}")
    await state.finish()

if __name__ == '__main__':
    from aiogram import executor
    executor.start_polling(dp, skip_updates=True)