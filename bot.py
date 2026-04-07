import os
import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

# Railway environment variable se token uthayega
API_TOKEN = os.getenv('8619415332:AAH5T5JW2ffE2Ut-fqnbEW0eOihSvEAzkKk')
bot = telebot.TeleBot(API_TOKEN)

@bot.message_handler(commands=['start'])
def welcome(message):
    # Caption jo aapne screenshot mein dikhayi hai
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

    # Buttons banane ke liye
    markup = InlineKeyboardMarkup()
    btn1 = InlineKeyboardButton("💎 Get Premium", callback_data="get_premium")
    btn2 = InlineKeyboardButton("🎬 Premium Demo", url="https://t.me/your_demo_link")
    btn3 = InlineKeyboardButton("📖 How To Get Premium", callback_data="how_to")
    
    # Buttons ko layout mein set karein
    markup.add(btn1)
    markup.row(btn2)
    markup.add(btn3)

    # Photo ke saath message bhejne ke liye
    # Note: 'photo_url' ki jagah apni image ka link ya file ID daalein
    photo_url = "https://your-image-link.com/photo.jpg" 
    
    bot.send_photo(
        message.chat.id, 
        photo_url, 
        caption=caption, 
        parse_mode="Markdown", 
        reply_markup=markup
    )

# Button click hone par kya response dena hai
@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    if call.data == "get_premium":
        bot.answer_callback_query(call.id, "Payment process start ho raha hai...")
        bot.send_message(call.message.chat.id, "Payment karne ke liye admin ko contact karein: @YourAdminUsername")
    elif call.data == "how_to":
        bot.send_message(call.message.chat.id, "Premium lene ke liye 'Get Premium' button par click karein aur payment screenshot bheinjein.")

bot.polling()

