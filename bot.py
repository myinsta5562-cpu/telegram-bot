import os
import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

# Railway token
API_TOKEN = '8619415332:AAH5T5JW2ffE2Ut-fqnbEW0eOihSvEAzkKk'
bot = telebot.TeleBot(API_TOKEN)

@bot.message_handler(commands=['start'])
def welcome(message):
    caption = (
        "**Video Channel 🌸**\n\n"
        "**For Desi Content Lovers 😋**\n\n"
        "**No Sn#p, Pure Desi Content 😚**\n\n"
        "**rare Desi le#ks ever.... 🎀**\n\n"
        "**Just pay and get entry...**\n\n"
        "**No - Ads Sh#t 🔥**\n\n"
        "**Price :- ₹199 /-**\n\n"
        "**Validity :- lifetime**"
    )

    markup = InlineKeyboardMarkup()
    btn1 = InlineKeyboardButton("💎 Get Premium", callback_data="get_premium")
    btn2 = InlineKeyboardButton("🎬 Premium Demo", url="https://t.me/your_demo_link")
    btn3 = InlineKeyboardButton("📖 How To Get Premium", callback_data="how_to")
    
    markup.add(btn1)
    markup.add(btn2)
    markup.add(btn3)

    # Local file 'start.jpg' ko open karke bhejne ke liye
    try:
        with open('start.jpg', 'rb') as photo:
            bot.send_photo(
                message.chat.id, 
                photo, 
                caption=caption, 
                parse_mode="Markdown", 
                reply_markup=markup
            )
    except FileNotFoundError:
        # Agar file nahi mili toh sirf text bhej dega
        bot.send_message(message.chat.id, caption, parse_mode="Markdown", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    if call.data == "get_premium":
        bot.send_message(call.message.chat.id, "Payment ke liye Admin ko contact karein: @YourAdminUsername")
    elif call.data == "how_to":
        bot.send_message(call.message.chat.id, "1. Payment karein\n2. Screenshot bheinjein\n3. Link mil jayegi.")

bot.polling()
