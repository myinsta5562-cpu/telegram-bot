import telebot
import requests
import random
import time
import urllib.parse
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, InputMediaVideo

TOKEN = "8619415332:AAH5T5JW2ffE2Ut-fqnbEW0eOihSvEAzkKk"
bot = telebot.TeleBot(TOKEN)

# ===== USER ORDER STORAGE =====
user_orders = {}

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

Price :- ₹5 /-  
Validity :- lifetime"""

    markup = InlineKeyboardMarkup(row_width=1)
    markup.add(
        InlineKeyboardButton("💎 Get Premium", callback_data="get_premium"),
        InlineKeyboardButton("🥵 Demo Videos", callback_data="demo"),
        InlineKeyboardButton("📖 How To Get Premium", callback_data="how_to")
    )

    bot.send_message(message.chat.id, text, reply_markup=markup)

# ===== CALLBACK =====
@bot.callback_query_handler(func=lambda call: True)
def callback(call):

    # ===== DEMO START =====
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

        if action == "next":
            if index < len(demo_videos) - 1:
                index += 1
        else:
            if index > 0:
                index -= 1

        markup = InlineKeyboardMarkup(row_width=2)

        buttons = []
        if index > 0:
            buttons.append(InlineKeyboardButton("👉 Previous", callback_data=f"prev_{index}"))
        if index < len(demo_videos) - 1:
            buttons.append(InlineKeyboardButton("👉 Next", callback_data=f"next_{index}"))

        if buttons:
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

    # ===== GET PREMIUM =====
    elif call.data == "get_premium":
        upi = "paytm.s1zxmoz@pty"
        amount = "5"
        name = "ANUJ BOTS"

        orderid = f"ORD_{int(time.time())}_{random.randint(1000,9999)}"
        user_orders[call.from_user.id] = orderid

        url = f"https://paytm.anujbots.xyz/qr.php?upi={upi}&amount={amount}&name={urllib.parse.quote(name)}"

        try:
            res = requests.get(url).json()

            if res.get("success"):
                qr = res.get("qr")

                markup = InlineKeyboardMarkup()
                markup.add(
                    InlineKeyboardButton("✅ Verify Payment", callback_data="verify")
                )

                bot.send_photo(
                    call.message.chat.id,
                    qr,
                    caption=f"💰 Scan & Pay\n\nUPI: {upi}\nAmount: ₹{amount}\nOrder ID: {orderid}",
                    reply_markup=markup
                )
            else:
                bot.send_message(call.message.chat.id, "❌ QR failed")

        except Exception as e:
            print(e)
            bot.send_message(call.message.chat.id, "❌ Server error")

    # ===== VERIFY =====
    elif call.data == "verify":
        orderid = user_orders.get(call.from_user.id)

        if not orderid:
            bot.send_message(call.message.chat.id, "❌ No order found")
            return

        merchantid = "NzmDCR37225908023870"
        merchantkey = "NzmDCR37225908023870"

        url = f"https://paytm.anujbots.xyz/verify.php?orderid={orderid}&merchantid={merchantid}&merchantkey={merchantkey}"

        try:
            res = requests.get(url).json()
            print(res)

            if res.get("success") and res.get("status") == "TXN_SUCCESS":
                bot.send_message(call.message.chat.id, "✅ Payment Successful 🔓 Access Granted")
            else:
                bot.send_message(call.message.chat.id, "⏳ Payment Pending / Not Found")

        except:
            bot.send_message(call.message.chat.id, "❌ Verification failed")

    # ===== HOW TO =====
    elif call.data == "how_to":
        bot.send_message(
            call.message.chat.id,
            "📖 How To Get Premium:\n\n1. Get Premium dabao\n2. QR scan karke ₹5 pay karo\n3. Verify dabao\n4. Access mil jayega"
        )

# ===== RUN =====
print("Bot running...")
bot.infinity_polling()
