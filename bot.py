import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, InputMediaVideo

TOKEN = "8619415332:AAH5T5JW2ffE2Ut-fqnbEW0eOihSvEAzkKk"
bot = telebot.TeleBot(TOKEN)

# ===== FILE ID EXTRACTOR (TEMPORARY) =====
@bot.message_handler(content_types=['video'])
def get_file_id(message):
    file_id = message.video.file_id
    bot.reply_to(message, f"FILE ID:\n{file_id}")

# ===== DEMO VIDEOS =====
demo_videos = [
    "BAACAgUAAxkBAAMkadS8phVxKxUtmJQ4kuLXDu1DuBIAAmAhAAKE06lWgs4sanWVVEA7BA",
    "BAACAgUAAxkBAAMwadS-rz_FkHn5Dsd5YZQ9IvxsOJAAAnQhAAKE06lWwsYhNgyJvXA7BA",
    "BAACAgUAAxkBAAMyadS-uqVpPgizUcGpNeKy2mK3bgUAAnYhAAKE06lWbKsvsXZt5kY7BA",
    "BAACAgUAAxkBAAM0adS-vzcwfFe6UwJZ7t23GY1xyokAAnchAAKE06lWOKnU0-KfdcI7BA",
    "BAACAgUAAxkBAAM2adS-0qFCsLomd57XAAGE1pN0X6esAAJ5IQAChNOpVuPO3f0KOI1pOwQ",
    "BAACAgUAAxkBAAM4adS-4C3t9qGRGkO8-0kP-aSwoAcAAnwhAAKE06lWqqdih3__4O87BA"
]

# ===== START =====
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
    markup.add(
        InlineKeyboardButton("💎 Get Premium", callback_data="get_premium"),
        InlineKeyboardButton("🥵 Demo Videos", callback_data="demo"),
        InlineKeyboardButton("📖 How To Get Premium", callback_data="how_to")
    )

    photo = open("start.jpg", "rb")
    bot.send_photo(message.chat.id, photo, caption=text, reply_markup=markup)

# ===== CALLBACK =====
@bot.callback_query_handler(func=lambda call: True)
def callback(call):

    # ===== DEMO =====
    if call.data == "demo":
    index = 0

    markup = InlineKeyboardMarkup(row_width=2)
    markup.add(
        InlineKeyboardButton("👉 Next", callback_data=f"next_{index}")
    )
    markup.add(
        InlineKeyboardButton("💎 Get Premium", callback_data="get_premium")
    )

    bot.send_video(
        call.message.chat.id,
        demo_videos[index],
        caption=f"🔞 Demo Video {index+1}",
        reply_markup=markup,
        supports_streaming=True,
        protect_content=True
    )

    # ===== NEXT / PREV =====
    elif call.data.startswith("next_") or call.data.startswith("prev_"):
    data = call.data.split("_")
    action = data[0]
    index = int(data[1])

    # ✅ NO LOOP (limit set)
    if action == "next":
        if index < len(demo_videos) - 1:
            index += 1
    else:
        if index > 0:
            index -= 1

    # ✅ BUTTON LOGIC
    markup = InlineKeyboardMarkup(row_width=2)

    buttons = []
    if index > 0:
        buttons.append(InlineKeyboardButton("👉 Previous", callback_data=f"prev_{index}"))
    if index < len(demo_videos) - 1:
        buttons.append(InlineKeyboardButton("👉 Next", callback_data=f"next_{index}"))

    markup.add(*buttons)

    markup.add(
        InlineKeyboardButton("💎 Get Premium", callback_data="get_premium")
    )

    try:
        bot.edit_message_media(
            media=InputMediaVideo(
                demo_videos[index],
                caption=f"🔞 Demo Video {index+1}",
                supports_streaming=True
            ),
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            reply_markup=markup
        )
    except Exception as e:
        print(e)

    # ===== PAYMENT =====
    elif call.data == "get_premium":
        markup = InlineKeyboardMarkup()
        markup.add(InlineKeyboardButton("✅ I Have Paid", callback_data="paid"))

        bot.send_message(
            call.message.chat.id,
            """💳 Payment Details:

UPI ID: yourupi@upi  
Amount: ₹199  

Payment karke niche button dabao 👇""",
            reply_markup=markup
        )

    elif call.data == "paid":
        bot.send_message(
            call.message.chat.id,
            "📸 Please send payment screenshot for verification."
        )

    # ===== HOW TO =====
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

# ===== SCREENSHOT =====
@bot.message_handler(content_types=['photo'])
def screenshot(message):
    bot.reply_to(message, "✅ Screenshot sent for verification.")

# ===== RUN =====
print("Bot running...")
bot.infinity_polling()
