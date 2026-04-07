import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, InputMediaVideo

TOKEN = "8619415332:AAH5T5JW2ffE2Ut-fqnbEW0eOihSvEAzkKk"
@bot.message_handler(content_types=['video'])
def get_file_id(message):
    file_id = message.video.file_id
    bot.reply_to(message, f"FILE ID:\n{file_id}")
bot = telebot.TeleBot(TOKEN)

# ===== DEMO VIDEOS (yaha apne 5 video file_id ya link daalo) =====
demo_videos = [
    "VIDEO_FILE_ID_1",
    "VIDEO_FILE_ID_2",
    "VIDEO_FILE_ID_3",
    "VIDEO_FILE_ID_4",
    "VIDEO_FILE_ID_5"
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

# ===== CALLBACK HANDLER =====
@bot.callback_query_handler(func=lambda call: True)
def callback(call):

    # ===== DEMO VIDEOS START =====
    if call.data == "demo":
        index = 0

        markup = InlineKeyboardMarkup(row_width=2)
        markup.add(
            InlineKeyboardButton("👉 Previous", callback_data=f"prev_{index}"),
            InlineKeyboardButton("👉 Next", callback_data=f"next_{index}")
        )
        markup.add(
            InlineKeyboardButton("💎 Get Premium", callback_data="get_premium")
        )

        bot.send_video(
            call.message.chat.id,
            demo_videos[index],
            caption=f"🔞 Demo Video {index+1}",
            reply_markup=markup
        )

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

    # ===== VIDEO NAVIGATION =====
    elif call.data.startswith("next_") or call.data.startswith("prev_"):
        data = call.data.split("_")
        action = data[0]
        index = int(data[1])

        if action == "next":
            index += 1
            if index >= len(demo_videos):
                index = 0

        elif action == "prev":
            index -= 1
            if index < 0:
                index = len(demo_videos) - 1

        markup = InlineKeyboardMarkup(row_width=2)
        markup.add(
            InlineKeyboardButton("👉 Previous", callback_data=f"prev_{index}"),
            InlineKeyboardButton("👉 Next", callback_data=f"next_{index}")
        )
        markup.add(
            InlineKeyboardButton("💎 Get Premium", callback_data="get_premium")
        )

        try:
            bot.edit_message_media(
                media=InputMediaVideo(
                    demo_videos[index],
                    caption=f"🔞 Demo Video {index+1}"
                ),
                chat_id=call.message.chat.id,
                message_id=call.message.message_id,
                reply_markup=markup
            )
        except:
            pass

# ===== SCREENSHOT RECEIVE =====
@bot.message_handler(content_types=['photo'])
def screenshot(message):
    bot.reply_to(message, "✅ Screenshot sent for verification.")

# ===== RUN =====
print("Bot running...")
bot.infinity_polling()
