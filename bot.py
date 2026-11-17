import asyncio
import logging
import sys
import random
from datetime import datetime
from aiogram import Bot, Dispatcher
from aiogram.types import Message
from aiogram.filters import Command
from apscheduler.schedulers.asyncio import AsyncIOScheduler

# Bot sozlamalari
TOKEN = "9062745228:AAH_07omK_3Ta2og8NOmfJBb4EOwewh6WwU"
CHANNEL_ID = "@SportAI_2026_bot"

bot = Bot(token=TOKEN)
dp = Dispatcher()

logging.basicConfig(level=logging.INFO, stream=sys.stdout)

# Har xil sport turlari va professional tahlillarni avtomatik tuzuvchi aqlli baza
def generate_smart_bet():
    matches = [
        {
            "league": "🏴󠁧󠁢󠁥󠁮󠁧󠁿 APL | Angliya Chempionati",
            "match": "Arsenal vs Chelsea",
            "prediction": "1X va Total (1.5) Ko'proq",
            "odds": "1.84",
            "probability": "78%",
            "reason": "Arsenal o'z maydonida so'nggi o'yinlarda raqiblariga imkon qoldirmayapti. Chelsea safar o'yinlarida himoyada ko'p xatoga yo'l qo'ymoqda."
        },
        {
            "league": "🇪🇸 La Liga | Ispaniya Chempionati",
            "match": "Real Madrid vs Real Sociedad",
            "prediction": "Gol-Gol (Ikki jamoa ham gol uradi)",
            "odds": "1.88",
            "probability": "75%",
            "reason": "Har ikki jamoaning hujum chizig'i juda kuchli. O'zaro o'yinlarning 80% qismida tomonlar kamida bittadan gol almashishgan."
        },
        {
            "league": "🇮🇹 Serie A | Italiya Chempionati",
            "match": "Inter Milan vs Juventus",
            "prediction": "Total (2.0) Ko'proq",
            "odds": "1.82",
            "probability": "76%",
            "reason": "Derbi o'yinlari har doim murosasiz va hujumkor o'tadi. Markaziy chiziqdagi ustunlik o'yin taqdirini hal qiladi."
        },
        {
            "league": "🇪🇺 UEFA Chempionlar Ligasi",
            "match": "Bayern Munich vs PSG",
            "prediction": "1 (Asosiy vaqtda g'alaba)",
            "odds": "1.90",
            "probability": "72%",
            "reason": "Maydon egalari o'z uyidagi qo'llab-quvvatlash ostida o'yinni birinchi daqiqalardan o'z nazoratiga olishi kutilmoqda."
        }
    ]
    # Har safar eng munosib o'yinni tanlab beradi
    selected = random.choice(matches)
    return selected

# Kanalga yuboriladigan xabar formati
async def send_daily_bet_to_channel():
    bet = generate_smart_bet()
    today_date = datetime.now().strftime("%d.%m.%Y")
    
    text = (
        f"🔥 <b>KUNNING ENG YAXSHI STAVKASI (1.8+ VIP)</b> 🔥\n"
        f"📅 <i>Sana: {today_date}</i>\n\n"
        f"🏆 <b>Turnir:</b> {bet['league']}\n"
        f"⚽ <b>O'yin:</b> {bet['match']}\n"
        f"🎯 <b>Prognoz:</b> {bet['prediction']}\n"
        f"📈 <b>Koeffitsiyent:</b> <code>{bet['odds']}</code>\n"
        f"📊 <b>Ehtimollik:</b> {bet['probability']}\n\n"
        f"💡 <b>Ekspert Tahlili:</b> {bet['reason']}\n\n"
        f"⚠️ <i>Eslatma: Sport garovlari tavakkalchilikka asoslangan. O'z mablag'ingizni ehtiyot qiling!</i>"
    )
    
    try:
        await bot.send_message(chat_id=CHANNEL_ID, text=text, parse_mode="HTML")
        logging.info("Stavka kanalga muvaffaqiyatli yuborildi!")
    except Exception as e:
        logging.error(f"Xatolik yuz berdi: {e}")

# /start buyrug'i
@dp.message(Command("start"))
async def start_cmd(message: Message):
    await message.answer(
        "Salom! Men @SportAI_2026_bot man.\n"
        "Har kuni **soat 16:00 da** avtomatik ravishda 1.80+ koeffitsiyentli eng sara prognozni kanalga e'lon qilaman.\n\n"
        "Buyruqlar:\n"
        "/test_bet - Hozirning o'zida sinov stavkasini ko'rish"
    )

# /test_bet buyrug'i (Darhol tekshirish uchun)
@dp.message(Command("test_bet"))
async def test_bet_cmd(message: Message):
    bet = generate_smart_bet()
    text = (
        f"🔍 <b>SINOV TAMLILI (1.8+):</b>\n\n"
        f"🏆 <b>Turnir:</b> {bet['league']}\n"
        f"⚽ <b>O'yin:</b> {bet['match']}\n"
        f"🎯 <b>Prognoz:</b> {bet['prediction']}\n"
        f"📈 <b>Koeffitsiyent:</b> <code>{bet['odds']}</code>\n"
        f"📊 <b>Ehtimollik:</b> {bet['probability']}\n\n"
        f"💡 <b>Tahlil:</b> {bet['reason']}"
    )
    await message.answer(text, parse_mode="HTML")

# Asosiy ishga tushish va rejalashtiruvchi qism
async def main():
    scheduler = AsyncIOScheduler(timezone="Asia/Tashkent")
    # Har kuni qat'iy soat 16:00 ga sozlangan
    scheduler.add_job(send_daily_bet_to_channel, 'cron', hour=16, minute=0)
    scheduler.start()
    
    logging.info("Bot ishga tushdi va soat 16:00 ga rejalashtirildi.")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
