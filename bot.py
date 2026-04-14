import telebot
import requests
import random
import urllib.parse
import threading
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, InputMediaVideo, InputMediaPhoto

TOKEN = "8703719728:AAFbrguML9SkqrfLV0GS3PFZY8W9qlojbms"
bot = telebot.TeleBot(TOKEN)

user_orders = {}
used_orders = set()  # ✅ FIX

plans = {
    "plan1": {"name": "RP V!D€OS", "price": "99", "link": "https://t.me/+A_WqvGYW64kzMGM1"},
    "plan2": {"name": "€P V!D€OS (50K+)", "price": "149", "link": "https://t.me/+l5vBpSJUvuFiMTg1"},
    "plan3": {"name": "All in One (50 Groups)", "price": "249", "link": "https://t.me/+Pe4fTs485hc2MDRl"},
    "plan4": {"name": "VIP PURE ALL (100K+)", "price": "499", "link": "https://t.me/+s4x5B2nHcZg0ZjM1"}
}

demo_videos = [
    "BAACAgUAAxkBAAMFadnE8mxyor-7smxKU1OzT8cb9roAAgEeAAJyntBWays3dkcW3kw7BA",
    "BAACAgUAAxkBAAMHadnE-QIyedCeSUzBNXDsSmabsrQAAgIeAAJyntBWFW0F_KXtzjo7BA",
    "BAACAgUAAxkBAAMNadnFcGhAH8eLAAHjWlPBV7BeL8fcAAIGHgACcp7QVpcQAxgYWn8SOwQ",
    "BAACAgUAAxkBAAMLadnFDgGd0o4K_ZCziXO6W6v8zcsAAgQeAAJyntBWsCrglr7PFy07BA",
    "BAACAgUAAxkBAAMJadnE_qpBc_ZvDz0wOLv6ITAJm7gAAgMeAAJyntBWkHh3hpbpOyE7BA"
]

@bot.message_handler(commands=['start'])
def start(message):
    text = """🎬 𝐀𝐯𝐚𝐢𝐥𝐚𝐛𝐥𝐞 𝐕𝐢𝐝𝐞𝐨𝐬 𝐂𝐨𝐥𝐥𝐞𝐜𝐭𝐢𝐨𝐧

𝟏. 𝐌𝟎𝐌 𝐒𝟎𝐍 𝐯𝐢𝐝𝐞𝐨𝐬 - 𝟓𝟎𝟎𝟎+

𝟐. 𝐒!𝐬𝐭𝐞𝐫 𝐁𝐫𝟎𝐭𝐡𝐞𝐫 𝐯𝐢𝐝𝐞𝐨𝐬 -𝟐𝟎𝟎𝟎+

𝟑. €𝐏 𝐯𝐢𝐝𝐞𝐨𝐬 - 𝟏𝟓𝟎𝟎𝟎+

𝟒. 𝐑𝐏 - 𝟑𝟎𝟎𝟎+

𝟓. 𝐓𝐞𝐞𝐧 𝐆𝐢𝐫𝐥. 𝐕𝐢𝐝𝐞𝐨𝐬 - 𝟔𝟎𝟎𝟎+

𝟔. 𝐈𝐧𝐝𝐢𝐚𝐧 𝐝𝐞𝐬𝐢 𝐯𝐢𝐝𝐞𝐨𝐬 - 𝟏𝟎𝟎𝟎𝟎+

𝟕. 𝐇𝐢𝐝𝐝𝐞𝐧 𝐜𝐚𝐦 𝐯𝐢𝐝𝐞𝐨𝐬 - 𝟐𝟎𝟎𝟎+
"""

    markup = InlineKeyboardMarkup(row_width=1)
    markup.add(
        InlineKeyboardButton("💎 Get Premium", callback_data="get_premium"),
        InlineKeyboardButton("🥵 Demo Videos", callback_data="demo"),
        InlineKeyboardButton("📖 How To Get Premium", url="https://t.me/+sjhIa5apzEE0MTE1")
    )

    photo = open("start.jpg", "rb")
    bot.send_photo(message.chat.id, photo, caption=text, reply_markup=markup)


@bot.callback_query_handler(func=lambda call: True)
def callback(call):

    if call.data == "demo":
        index = 0

        markup = InlineKeyboardMarkup(row_width=2)
        markup.add(InlineKeyboardButton("👉 Next", callback_data=f"next_{index}"))
        markup.add(
            InlineKeyboardButton("💎 Get Premium", callback_data="get_premium"),
            InlineKeyboardButton("🔙 Back", callback_data="back_start")
        )

        msg = bot.send_video(
            call.message.chat.id,
            demo_videos[index],
            caption=f"🔞 Demo Video {index+1}",
            reply_markup=markup,
            supports_streaming=True
        )

        def delete_msg():
            try:
                bot.delete_message(call.message.chat.id, msg.message_id)
            except:
                pass

        threading.Timer(120, delete_msg).start()

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
            InlineKeyboardButton("💎 Get Premium", callback_data="get_premium"),
            InlineKeyboardButton("🔙 Back", callback_data="back_start")
        )

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

        def delete_msg():
            try:
                bot.delete_message(call.message.chat.id, call.message.message_id)
            except:
                pass

        threading.Timer(120, delete_msg).start()

    elif call.data == "get_premium":
        markup = InlineKeyboardMarkup(row_width=1)
        markup.add(
            InlineKeyboardButton("👉 RP V!D€OS - ₹99", callback_data="buy_plan1"),
            InlineKeyboardButton("👉 €P V!D€OS - ₹149", callback_data="buy_plan2"),
            InlineKeyboardButton("👉 All in One (50 Groups) - ₹249", callback_data="buy_plan3"),
            InlineKeyboardButton("👉 VIP PURE ALL Vdos (100K+ VIDEOS) - ₹499", callback_data="buy_plan4"),
            InlineKeyboardButton("🔙 Back", callback_data="back_start")
        )

        bot.edit_message_media(
            media=InputMediaPhoto(
                open("plans.jpg", "rb"),
                caption="🔥 Choose Your Plan:"
            ),
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            reply_markup=markup
        )

    elif call.data.startswith("buy_"):
        plan_key = call.data.split("_")[1]
        plan = plans.get(plan_key)

        if not plan:
            bot.send_message(call.message.chat.id, "❌ Plan not found")
            return

        user_orders[call.from_user.id] = plan_key

        upi = "paytm.s1zssxv@pty"
        amount = plan["price"]
        name = "paikarma"

        upi_encoded = urllib.parse.quote(upi)
        name_encoded = urllib.parse.quote(name)

        url = f"https://paytm.anujbots.xyz/qr.php?upi={upi_encoded}&amount={amount}&name={name_encoded}"

        res = requests.get(url).json()

        if res.get("success"):
            qr = res.get("qr_url")
            orderid = res.get("order_id")

            if not orderid:
                bot.send_message(call.message.chat.id, "❌ Order ID not received")
                return

            user_orders[str(call.from_user.id)+"_order"] = orderid

            markup = InlineKeyboardMarkup(row_width=1)
            markup.add(
                InlineKeyboardButton("✅ GET PRIVATE CHANNEL LINK ", callback_data="verify"),
            )

            bot.edit_message_media(
                media=InputMediaPhoto(
                    qr,
                    caption=f"💰 Plan: {plan['name']}\n💵 Amount: ₹{amount}\n🆔 Order ID: {orderid}"
                ),
                chat_id=call.message.chat.id,
                message_id=call.message.message_id,
                reply_markup=markup
            )

    elif call.data == "verify":
        orderid = user_orders.get(str(call.from_user.id)+"_order")

        if not orderid:
            bot.send_message(call.message.chat.id, "❌ No order found")
            return

        merchantid = "aFpena57399629842621"
        merchantkey = "aFpena57399629842621"

        url = f"https://paytm.anujbots.xyz/verify.php?orderid={orderid}&merchantid={merchantid}&merchantkey={merchantkey}"

        res = requests.get(url).json()

        if res.get("success") and res.get("status") == "TXN_SUCCESS":

            if orderid in used_orders:
                bot.send_message(call.message.chat.id, "⚠️ You have already received access")
                return

            used_orders.add(orderid)

            amount = res.get("amount")

            plan_key = user_orders.get(call.from_user.id)
            plan = plans.get(plan_key)
            link = plan["link"]

            bot.send_message(
                call.message.chat.id,
                f"✅ Payment Successful\n\n💰 Amount: ₹{amount}\n🔓 Access Granted\n\n🔗 {link}"
            )
        else:
            bot.send_message(call.message.chat.id, "🚫 Payment not completed yet")

    elif call.data == "back_start":
        markup = InlineKeyboardMarkup(row_width=1)
        markup.add(
            InlineKeyboardButton("💎 Get Premium", callback_data="get_premium"),
            InlineKeyboardButton("🥵 Demo Videos", callback_data="demo"),
            InlineKeyboardButton("📖 How To Get Premium", url="https://t.me/+sjhIa5apzEE0MTE1")
        )

        bot.edit_message_media(
            media=InputMediaPhoto(
                open("start.jpg", "rb"),
                caption="""🎬 𝐀𝐯𝐚𝐢𝐥𝐚𝐛𝐥𝐞 𝐕𝐢𝐝𝐞𝐨𝐬 𝐂𝐨𝐥𝐥𝐞𝐜𝐭𝐢𝐨𝐧

𝟏. 𝐌𝟎𝐌 𝐒𝟎𝐍 𝐯𝐢𝐝𝐞𝐨𝐬 - 𝟓𝟎𝟎𝟎+

𝟐. 𝐒!𝐬𝐭𝐞𝐫 𝐁𝐫𝟎𝐭𝐡𝐞𝐫 𝐯𝐢𝐝𝐞𝐨𝐬 -𝟐𝟎𝟎𝟎+

𝟑. €𝐏 𝐯𝐢𝐝𝐞𝐨𝐬 - 𝟏𝟓𝟎𝟎𝟎+

𝟒. 𝐑𝐏 - 𝟑𝟎𝟎𝟎+

𝟓. 𝐓𝐞𝐞𝐧 𝐆𝐢𝐫𝐥. 𝐕𝐢𝐝𝐞𝐨𝐬 - 𝟔𝟎𝟎𝟎+

𝟔. 𝐈𝐧𝐝𝐢𝐚𝐧 𝐝𝐞𝐬𝐢 𝐯𝐢𝐝𝐞𝐨𝐬 - 𝟏𝟎𝟎𝟎𝟎+

𝟕. 𝐇𝐢𝐝𝐝𝐞𝐧 𝐜𝐚𝐦 𝐯𝐢𝐝𝐞𝐨𝐬 - 𝟐𝟎𝟎𝟎+
"""
            ),
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            reply_markup=markup
        )

print("Bot running...")
bot.infinity_polling()
