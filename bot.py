import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

TOKEN = "8619415332:AAH5T5JW2ffE2Ut-fqnbEW0eOihSvEAzkKk"
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def start(message):
    text = """🎬 Video Channel 🌸

For Desi Content Lovers 😋  
No Sn#p, Pure Desi Content 😚  
rare Desi le#ks ever.... 🎀  

Just pay and get entry...  
No - Ads Sh#t 🔥  

Price :- ₹199 /-  
Validity :- lifetime
"""

    markup = InlineKeyboardMarkup(row_width=1)
    btn1 = InlineKeyboardButton("💎 Get Premium", callback_data="get_premium")
    btn2 = InlineKeyboardButton("🎬 Premium Demo", url="https://t.me/your_demo_channel")
    btn3 = InlineKeyboardButton("📖 How To Get Premium", callback_data="how_to")

    markup.add(btn1, btn2, btn3)

    # 👉 LOCAL IMAGE SEND
    photo = open("start.jpg", "rb")
    bot.send_photo(message.chat.id, photo, caption=text, reply_markup=markup)

@bot.callback_query_handler(func=lambda call: True)
def callback(call):

    if call.data == "get_premium":
        bot.send_message(
            call.message.chat.id,
            """💳 Payment Details:

UPI ID: yourupi@upi
Amount: ₹199

Payment karke niche button dabao 👇""",
            reply_markup=InlineKeyboardMarkup().add(
                InlineKeyboardButton("✅ I Have Paid", callback_data="paid")
            )
        )

    elif call.data == "paid":
        bot.send_message(
            call.message.chat.id,
            "📸 Please send payment screenshot for verification."
        )

    elif call.data == "how_to":
        bot.send_message(
            call.message.chat.id,
            """📖 How To Get Premium:

1. Get Premium button dabao  
2. Payment karo  
3. Screenshot bhejo  
4. Admin verify karega  
5. Access mil jayega ✅"""
        )

@bot.message_handler(content_types=['photo'])
def screenshot(message):
    bot.reply_to(message, "✅ Screenshot sent for verification.")

print("Bot running...")
bot.infinity_polling()
