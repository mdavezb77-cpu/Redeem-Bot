import telebot
import time
import random
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from datetime import datetime, timedelta

# Bot token
BOT_TOKEN = '7701905324:AAGrLHNe5wuAIzVHLv2yVRiS1vFaNekvKug'
OWNER_USER_ID = 7303810912
PROOF_CHANNEL_ID = -1002113563800
FORWARD_CHANNEL_IDS = [-1001676737394, -1002181773077, -1002224203739]

bot = telebot.TeleBot(BOT_TOKEN)

required_channels = ["@ModVipRM", "@ModviprmBackup", "@modDirect_download", "@Proofchannelch"]
buttons = [
    ("🔗 ModVipRM", "https://t.me/ModVipRM"),
    ("🔗 ModVipRM Backup", "https://t.me/ModviprmBackup"),
    ("📂 ModVipRM APK", "https://t.me/modDirect_download"),
    ("📢 Proof Channel", "https://t.me/Proofchannelch")
]

# Dictionary to store the mapping of forwarded messages to original users
forwarded_messages = {}

# Define promo links for different services
promo_links = {
    "YouTube": [
        "https://families.google.com/join/promo/StTMvLwjgxuEhNMIIqeUPQA9ZzjJuQ?pli=1",
        "https://families.google.com/join/promo/hIx3V_H3WcEHbgv8Vr9h1YMG5ceGkw?pli=1",
        "https://families.google.com/join/promo/DSgghlmPq1nVoB5npLTqhQJSUq_CGw?pli=1",
        "https://families.google.com/join/promo/-6qah32kH-4yORY2993Wc2qfNRSaBA?pli=1",
        "https://families.google.com/join/promo/nvNKCIgHPNeh3ORtIb0r0FSISxPERw?pli=1"
    ],
    "Crunchyroll": [
        "Email: nitrovai914@gmail.com Pass: Samiul098@",
        "Email: nitrovai914@gmail.com Pass: Samiul098@",
        "Email: nitrovai914@gmail.com Pass: Samiul098@",
        "Email: nitrovai914@gmail.com Pass: Samiul098@",
        "Email: nitrovai914@gmail.com Pass: Samiul098@"
    ],
    "Canva": [
        "Email: example1@canva.com Pass: password1",
        "Email: example2@canva.com Pass: password2"
    ],
    "Hostinger": [
        "Email: example1@hostinger.com Pass: password1",
        "Email: example2@hostinger.com Pass: password2"
    ],
    "Netflix": [
        "Email: example1@netflix.com Pass: password1",
        "Email: example2@netflix.com Pass: password2"
    ],
    "PrimeVideo": [
        "Email: example1@primevideo.com Pass: password1",
        "Email: example2@primevideo.com Pass: password2"
    ],
    "Spotify": [
        "Email: example1@spotify.com Pass: password1",
        "Email: example2@spotify.com Pass: password2"
    ]
}

# Define image URLs for different services
service_images = {
    "YouTube": "https://t.me/abir_x_official_developer/82",
    "Crunchyroll": "https://t.me/abir_x_official_developer/86",
    "Netflix": "https://t.me/abir_x_official_developer/88",
    "PrimeVideo": "https://t.me/abir_x_official_developer/89",
    "Canva": "https://t.me/abir_x_official_developer/91",
    "Spotify": "https://t.me/abir_x_official_developer/93"
}

# Storage for generated codes and redeemed information
generated_codes = {}
redeemed_codes = {}
# Storage for user IDs
user_ids = set()
# Bot start time
start_time = datetime.now()

# Function to check channel join status
def is_user_in_channels(user_id):
    try:
        for channel in required_channels:
            status = bot.get_chat_member(channel, user_id).status
            if status not in ['member', 'administrator', 'creator']:
                return False
        return True
    except Exception as e:
        print(f"Error checking channel status: {e}")
        return False

# Start command handler
@bot.message_handler(commands=['start'])
def start(message):
    user_id = message.from_user.id
    # Store user ID for broadcasting later
    user_ids.add(user_id)
    try:
        if not is_user_in_channels(user_id):
            keyboard = InlineKeyboardMarkup()
            # Arrange buttons in 2-2-1 formation
            keyboard.row(InlineKeyboardButton(text="🔗 ModVipRM", url="https://t.me/ModVipRM"),
                         InlineKeyboardButton(text="🔗 ModVipRM Backup", url="https://t.me/ModviprmBackup"))
            keyboard.row(InlineKeyboardButton(text="📂 ModVipRM APK", url="https://t.me/modDirect_download"),
                         InlineKeyboardButton(text="📢 Proof Channel", url="https://t.me/Proofchannelch"))
            keyboard.add(InlineKeyboardButton(text="✅ Joined", callback_data="joined_check"))
            
            bot.send_photo(
                message.chat.id,
                photo="https://t.me/abir_x_official_developer/77",
                caption=("*Welcome to Redeem Code ABIR XD Bot!*\n\n"
                         "*You can now use the bot.*\n"
                         "*Use /redeem <code> to redeem a code.*\n"
                         "*OWNER: @abirxdhackz*\n"
                         "*Join: ModVipRM*").replace('_', '\\_'),
                reply_markup=keyboard,
                parse_mode="Markdown"
            )
        else:
            bot.send_message(message.chat.id, "*Welcome back! You are already joined! Use /redeem <code> to redeem.*".replace('_', '\\_'), parse_mode="Markdown")
    except telebot.apihelper.ApiTelegramException as e:
        if e.error_code == 403:
            print(f"User {user_id} has blocked the bot.")
        else:
            print(f"Error: {e}")

# Callback handler for joined button
@bot.callback_query_handler(func=lambda call: call.data == "joined_check")
def joined_check(call):
    user_id = call.from_user.id
    if is_user_in_channels(user_id):
        bot.answer_callback_query(call.id, "You have joined the channels!")
        bot.send_message(call.message.chat.id, "*You can now use the bot. Use /redeem <code> to redeem a code.*".replace('_', '\\_'), parse_mode="Markdown")
    else:
        bot.answer_callback_query(call.id, "Please join all required channels first.", show_alert=True)

# Generate redeem codes (Owner only)
@bot.message_handler(commands=['gen'])
def generate_codes(message):
    if message.from_user.username != "abirxdhackz":
        bot.reply_to(message, "You are not authorized to use this command.")
        return

    try:
        _, count, service_name = message.text.split()
        count = int(count)
    except ValueError:
        bot.reply_to(message, "*Usage: /gen <number_of_codes> <service_name>*".replace('_', '\\_'), parse_mode="Markdown")
        return

    valid_services = [
        "YouTube", "Crunchyroll", "Canva", "Hostinger", "Netflix", "PrimeVideo", "Spotify"
    ]

    if service_name not in valid_services:
        bot.reply_to(message, f"*Invalid service name. Please choose from: {', '.join(valid_services)}*".replace('_', '\\_'), parse_mode="Markdown")
        return

    codes = []
    for _ in range(count):
        code = f"{service_name.upper()}-{random.randint(1000, 9999)}-{random.randint(1000, 9999)}-{random.randint(1000, 9999)}"
        if code not in generated_codes:  # Ensure unique codes
            generated_codes[code] = None
            codes.append(code)

    # Format the codes as per the new requirement
    formatted_codes = "\n".join([f"➔ `{code}` ☑️" for code in codes])

    keyboard = InlineKeyboardMarkup()
    keyboard.add(InlineKeyboardButton(text="🧾 Updates Channel ☑️", url="https://t.me/ModVipRM"))
    keyboard.add(InlineKeyboardButton(text="🤖 Bot Owner ☑️", url="https://t.me/abirxdhackz"))

    bot.reply_to(
        message,
        f"*Hey Bro All The Codes Generated Are Below For {service_name}.*\n\n{formatted_codes}\n\n*Need help? Join our channels or contact the bot owner for assistance!*".replace('_', '\\_'),
        parse_mode="Markdown",
        reply_markup=keyboard
    )

# Post command handler
@bot.message_handler(commands=['post'])
def post_announcement(message):
    if message.from_user.username != "abirxdhackz":
        bot.reply_to(message, "You are not authorized to use this command.")
        return

    if not generated_codes:
        bot.reply_to(message, "No codes have been generated yet.")
        return

    # Extract the service name from the first code
    first_code = next(iter(generated_codes.keys()))
    service_name = first_code.split('-')[0].capitalize()

    # Special case for "PrimeVideo"
    if service_name.lower() == "primevideo":
        service_name = "PrimeVideo"

    # Format the codes for the post
    formatted_codes = "\n".join([f"➔ `{code}` ☑️" for code in generated_codes.keys()])

    # Create the post content
    post_content = (
        f"➡️ ✨ *{service_name} Premium Account Giveaway* ✨ ⬅️\n\n"
        f"🟢 *Generated {len(generated_codes)} Redeem Codes* 🟢:\n\n"
        f"{formatted_codes}\n\n"
        f"➡️ *Redeem The Code By Sending This Command- /redeem {first_code.split('-')[0]}-XXXX-XXXX-XXXX*\n\n"
        f"➡️ *Redeem From This Bot-  Xtreme Redeem ⚡️ [Open Bot To Redeem](https://t.me/Redeem_Ultimate_Bot)*\n\n"
        "🔹 *First 05 Users Will Win It* 🔺\n"
        "🔹 *Hurry Up! Only The First 5 Users Will Win This Giveaway !* ⌛️\n\n"
        "❤️ *Send Screenshot There- @abirxdhackz* ✅ ✔️\n\n"
        "➡️ *Share Our Channel For More Exciting Giveaways* ✅\n"
        "➡️ *For More Enquiry —— ❤️ @abirxdhackz* ✔️\n"
        "➡️ *For More Information Check @ModVipRM* ☝️\n\n"
        "❤️ *Thank You For Staying With Us* ❤️"
    ).replace('\\', '_')

    # Get the image URL for the service
    image_url = service_images.get(service_name, "https://t.me/abir_x_official_developer/82")

    # Define the keyboard
    keyboard = InlineKeyboardMarkup()
    keyboard.add(InlineKeyboardButton(text="✅ Open Bot To Redeem", url="https://t.me/Redeem_Ultimate_Bot"))

    # Send the post to the main channel
    try:
        bot.send_photo(
            message.chat.id,
            photo=image_url,
            caption=post_content,
            reply_markup=keyboard,
            parse_mode="Markdown"
        )
    except Exception as e:
        bot.reply_to(message, f"Error sending post to the main channel: {e}")

    # Forward the post to other channels
    for channel_id in FORWARD_CHANNEL_IDS:
        try:
            bot.send_photo(
                channel_id,
                photo=image_url,
                caption=post_content,
                reply_markup=keyboard,
                parse_mode="Markdown"
            )
        except Exception as e:
            print(f"Error forwarding post to channel {channel_id}: {e}")

# Function to handle the /redeem command
@bot.message_handler(commands=['redeem'])
def redeem_code(message):
    """ Redeem the code provided by the user """
    user_id = message.from_user.id
    username = message.from_user.username or "N/A"
    full_name = message.from_user.full_name or "N/A"

    if not is_user_in_channels(user_id):
        bot.send_message(message.chat.id, "Please join all required channels first.")
        return

    try:
        _, code = message.text.split()
    except ValueError:
        bot.send_photo(
            message.chat.id,
            photo="https://t.me/abir_x_official_developer/85",
            caption="Please provide a code to redeem."
        )
        return

    if code not in generated_codes:
        bot.send_photo(
            message.chat.id,
            photo="https://t.me/abir_x_official_developer/79",
            caption="Invalid redeem code. Please try again with a valid code."
        )
        return

    if generated_codes[code] is not None:
        redeemer = generated_codes[code]
        bot.send_photo(
            message.chat.id,
            photo="https://t.me/abir_x_official_developer/81",
            caption=(f"🎉 *Code Already Redeemed!*\n"
                     f"👤 *Name:* {redeemer['full_name']}\n"
                     f"📛 *Username:* {redeemer['username']}\n"
                     f"🆔 *ID:* {redeemer['user_id']}\n"
                     f"⏰ *Time:* {redeemer['time']}").replace('_', '\\_'),
            parse_mode="Markdown"
        )
        return

    if user_id in [data['user_id'] for data in generated_codes.values() if data]:
        bot.send_message(message.chat.id, "*You have already redeemed a code.*".replace('_', '\\_'), parse_mode="Markdown")
        return

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    generated_codes[code] = {
        'user_id': user_id,
        'username': username,
        'full_name': full_name,
        'time': timestamp
    }

    # Determine the service from the code and select a promo link and image
    service_name = code.split('-')[0].title()

    if service_name == "Youtube":
        promo_link = random.choice(promo_links["YouTube"])  # Get a link from the predefined list for YouTube
    else:
        promo_link = random.choice(promo_links.get(service_name, ["Email: example@default.com Pass: password"]))  # Default email-pass format if service not found

    image_url = service_images.get(service_name, "https://t.me/abir_x_official_developer/82")  # Default to YouTube image if service not found

    # Check if the promo link is an email/pass format or a URL
    if service_name == "Youtube" or "Email:" not in promo_link:
        keyboard = InlineKeyboardMarkup()
        keyboard.add(InlineKeyboardButton(text=f"🔗 Open {service_name} Premium Link", url=promo_link))
        keyboard.add(InlineKeyboardButton(text="📜 How To Leave Old Family", url="https://t.me/ModVipRM/3530"))

        bot.send_photo(
            message.chat.id,
            photo=image_url,
            caption=(f"🎉 *Code Redeemed Successfully!*\n"
                     f"👤 *Name:* {full_name}\n"
                     f"📛 *Username:* {username}\n"
                     f"🆔 *ID:* {user_id}\n"
                     f"⏰ *Time:* {timestamp}\n"
                     f"🔗 *Your {service_name} Premium link:* {promo_link}").replace('_', '\\_'),
            reply_markup=keyboard,
            parse_mode="Markdown"
        )
    else:
        promo_text = f"🔗 *Your {service_name} Premium account:* {promo_link}"
        keyboard = InlineKeyboardMarkup()
        keyboard.add(InlineKeyboardButton(text="📜 How To Leave Old Family", url="https://t.me/ModVipRM/3530"))

        bot.send_photo(
            message.chat.id,
            photo=image_url,
            caption=(f"🎉 *Code Redeemed Successfully!*\n"
                     f"👤 *Name:* {full_name}\n"
                     f"📛 *Username:* {username}\n"
                     f"🆔 *ID:* {user_id}\n"
                     f"⏰ *Time:* {timestamp}\n"
                     f"{promo_text}").replace('_', '\\_'),
            reply_markup=keyboard,
            parse_mode="Markdown"
        )

    proof_message = (f"🎉 *Code Redeemed Successfully!*\n"
                     f"👤 *Name:* {full_name}\n"
                     f"📛 *Username:* {username}\n"
                     f"🆔 *ID:* {user_id}\n"
                     f"⏰ *Time:* {timestamp}\n\n"
                     f"*Use the bot to get your own {service_name} Premium account!*\n"
                     f"*Join our channels for more updates and giveaways!*").replace('_', '\\_')

    proof_keyboard = InlineKeyboardMarkup()
    proof_keyboard.add(InlineKeyboardButton(text="🤖 Get Premium Account Now ☑️", url="https://t.me/Redeem_Ultimate_Bot"))
    proof_keyboard.add(InlineKeyboardButton(text="📜 Get Redeem Codes ☑️", url="https://t.me/addlist/wskLZdSg8K02NzVl"))

    bot.send_message(PROOF_CHANNEL_ID, proof_message, reply_markup=proof_keyboard, parse_mode="Markdown")

    # Forward the proof message to the owner
    try:
        bot.send_message(OWNER_USER_ID, proof_message, reply_markup=proof_keyboard, parse_mode="Markdown")
    except telebot.apihelper.ApiTelegramException as e:
        print(f"Error sending message to owner: {e}")
        
# Send command handler to broadcast messages
@bot.message_handler(commands=['send'])
def ask_broadcast_message(message):
    if message.from_user.id != OWNER_USER_ID:
        bot.reply_to(message, "You are not authorized to use this command.")
        return

    msg = bot.reply_to(message, "*Please Enter A Message To Broadcast To Users*".replace('_', '\\_'), parse_mode="Markdown")
    bot.register_next_step_handler(msg, broadcast_message)

def broadcast_message(message):
    if message.from_user.id != OWNER_USER_ID:
        bot.reply_to(message, "You are not authorized to use this command.")
        return

    broadcast_text = f"*📢 [ Broadcast From Owner ] 📢*\n\n{message.text}\n\n*For More Updates, [Join Now](https://t.me/ModVipRM)*".replace('_', '\\_')
    keyboard = InlineKeyboardMarkup()
    keyboard.add(InlineKeyboardButton(text="☑️ Join Our All Community 🥰", url="https://t.me/addlist/wskLZdSg8K02NzVl"))

    for user_id in user_ids:
        try:
            bot.send_message(user_id, broadcast_text, reply_markup=keyboard, parse_mode="Markdown", disable_web_page_preview=True)
        except telebot.apihelper.ApiTelegramException as e:
            print(f"Error sending message to user {user_id}: {e}")

    # Notify the owner that the broadcast was successful
    bot.send_message(OWNER_USER_ID, "*Broadcast successful!*".replace('_', '\\_'), parse_mode="Markdown")

# Stats command handler
@bot.message_handler(commands=['stats'])
def stats(message):
    current_time = datetime.now()
    uptime = current_time - start_time
    hours, remainder = divmod(int(uptime.total_seconds()), 3600)
    minutes, seconds = divmod(remainder, 60)

    keyboard = InlineKeyboardMarkup()
    keyboard.add(InlineKeyboardButton(text="☑️ ᴊᴏɪɴ ᴏᴜʀ ᴄᴏᴅɪɴɢ ᴄʜᴀɴɴᴇʟ ☑️", url="https://t.me/addlist/wskLZdSg8K02NzVl"))

    bot.send_photo(
        message.chat.id,
        photo="https://t.me/abir_x_official_developer/84",
        caption=(
            "➠ 📊 *｢Bot Live Statistics 」* 📊\n"
            "┏━━━━━━━━━━━━━━━━━━━\n"
            f"┣☑️ *Total Users:* {len(user_ids)} *People*\n"
            "┣━━━━━━━━━━━━━━━━━━━\n"
            f"┣☑️ *Uptime :*  {hours} hours {minutes} mins {seconds} secs 📨\n"
            "┗━━━━━━━━━━━━━━━━━━━\n\n"
            "☠️ *ᴠᴇʀꜱɪᴏɴ : Latest*\n\n"
            "🔄 *ʟᴀꜱᴛ ᴜᴘᴅᴀᴛᴇ 24 Dec ,2024*\n\n"
            "☑️ *ʙᴏᴛ ᴄʀᴇᴀᴛᴏʀ : @abirxdhackz*\n\n"
            "☑️ *ᴊᴏɪɴ ᴏᴜʀ ᴄᴏᴅɪɴɢ ᴄʜᴀɴɴᴇʟ ꜰᴏʀ ᴍᴏʀᴇ ʙᴏᴛꜱ ☑️*\n"
        ).replace('_', '\\_'),
        reply_markup=keyboard,
        parse_mode="Markdown"
    )

# Privacy command handler
@bot.message_handler(commands=['privacy'])
def privacy_policy(message):
    user_id = message.from_user.id

    # Privacy policy content
    privacy_content = (
        "🔒 **ᴘʀɪᴠᴀᴄʏ ᴘᴏʟɪᴄʏ ғᴏʀ ᴜʟᴛɪᴍᴀᴛᴇ ʀᴇᴅᴇᴇᴍ ᴄᴏᴅᴇ ʙᴏᴛ** 🔒\n"
        "━━━━━━━━━━━━━━━━━\n\n"
        "ᴡᴇʟᴄᴏᴍᴇ ᴛᴏ ᴜʟᴛɪᴍᴀᴛᴇ ʀᴇᴅᴇᴇᴍ ᴄᴏᴅᴇ ʙᴏᴛ, ᴛʜᴇ ᴜʟᴛɪᴍᴀᴛᴇ ᴛᴏᴏʟᴋɪᴛ ᴏɴ ᴛᴇʟᴇɢʀᴀᴍ, ᴏғғᴇʀɪɴɢ ᴀ ᴠᴀʀɪᴇᴛʏ ᴏғ ғᴇᴀᴛᴜʀᴇꜱ ᴛᴏ ꜱɪᴍᴘʟɪғʏ ʏᴏᴜʀ ᴛᴀꜱᴋꜱ. ʙʏ ᴜꜱɪɴɢ ᴜʟᴛɪᴍᴀᴛᴇ ʀᴇᴅᴇᴇᴍ ᴄᴏᴅᴇ ʙᴏᴛ, ʏᴏᴜ ᴀɢʀᴇᴇ ᴛᴏ ᴛʜᴇ ᴛᴇʀᴍꜱ ᴀɴᴅ ᴄᴏɴᴅɪᴛɪᴏɴꜱ ᴏғ ᴛʜɪꜱ ᴘᴏʟɪᴄʏ.\n\n"
        "🔹 **ɪɴғᴏʀᴍᴀᴛɪᴏɴ ᴡᴇ ᴄᴏʟʟᴇᴄᴛ** 🔹\n"
        "1. **ᴘᴇʀꜱᴏɴᴀʟ ɪɴғᴏʀᴍᴀᴛɪᴏɴ:**\n"
        "   - ᴜꜱᴇʀ ɪᴅ ᴀɴᴅ ᴜꜱᴇʀɴᴀᴍᴇ: ᴡᴇ ᴄᴏʟʟᴇᴄᴛ ʏᴏᴜʀ ᴜꜱᴇʀ ɪᴅ ᴀɴᴅ ᴜꜱᴇʀɴᴀᴍᴇ ᴛᴏ ᴘʀᴏᴠɪᴅᴇ ᴘᴇʀꜱᴏɴᴀʟɪᴢᴇᴅ ꜱᴇʀᴠɪᴄᴇꜱ.\n"
        "2. **ᴜꜱᴀɢᴇ ᴅᴀᴛᴀ:**\n"
        "   - ᴅᴀᴛᴀ ᴏɴ ᴄᴏᴍᴍᴀɴᴅꜱ ᴜꜱᴇᴅ, ᴛᴏᴏʟꜱ ᴀᴄᴄᴇꜱꜱᴇᴅ, ᴀɴᴅ ꜰʀᴇϙᴜᴇɴᴄʏ ᴏғ ᴜꜱᴇ ᴛᴏ ɪᴍᴘʀᴏᴠᴇ ꜱᴇʀᴠɪᴄᴇꜱ.\n\n"
        "🔹 **ʜᴏᴡ ᴡᴇ ᴜꜱᴇ ʏᴏᴜʀ ɪɴғᴏʀᴍᴀᴛɪᴏɴ** 🔹\n"
        "   - **ꜱᴇʀᴠɪᴄᴇ ᴘʀᴏᴠɪꜱɪᴏɴ:** ᴛᴏ ᴘʀᴏᴠɪᴅᴇ ᴀɴᴅ ᴇɴʜᴀɴᴄᴇ ᴛʜᴇ ꜱᴇʀᴠɪᴄᴇꜱ ᴏғғᴇʀᴇᴅ ʙʏ ᴜʟᴛɪᴍᴀᴛᴇ ʀᴇᴅᴇᴇᴍ ᴄᴏᴅᴇ ʙᴏᴛ.\n"
        "   - **ᴄᴏᴍᴍᴜɴɪᴄᴀᴛɪᴏɴ:** ᴛᴏ ᴄᴏᴍᴍᴜɴɪᴄᴀᴛᴇ ᴡɪᴛʜ ʏᴏᴜ ᴀʙᴏᴜᴛ ᴜᴘᴅᴀᴛᴇꜱ & ɴᴇᴡ ꜰᴇᴀᴛᴜʀᴇꜱ.\n"
        "   - **ꜱᴇᴄᴜʀɪᴛʏ:** ᴛᴏ ᴍᴏɴɪᴛᴏʀ ᴀɴᴅ ᴘʀᴏᴛᴇᴄᴛ ᴀɢᴀɪɴꜱᴛ ᴜɴᴀᴜᴛʜᴏʀɪᴢᴇᴅ ᴀᴄᴄᴇꜱꜱ, ᴀɴᴅ ꜱᴘᴀᴍᴍᴇʀ.\n"
        "   - **ᴘʀᴏᴍᴏᴛɪᴏɴꜱ ᴀɴᴅ ᴀᴅᴠᴇʀᴛɪꜱᴇᴍᴇɴᴛꜱ:** ᴡᴇ ᴍᴀʏ ꜱʜᴀʀᴇ ᴘᴀɪᴅ ᴘʀᴏᴍᴏᴛɪᴏɴꜱ ᴀɴᴅ ᴀᴅᴠᴇʀᴛɪꜱᴇᴍᴇɴᴛꜱ ᴛʜʀᴏᴜɢʜ ᴛʜᴇ ʙᴏᴛ.\n\n"
        "🔹 **ᴅᴀᴛᴀ ꜱᴇᴄᴜʀɪᴛʏ** 🔹\n"
        "   - ᴡᴇ ᴜꜱᴇ ꜱᴇᴄᴜʀɪᴛʏ ᴍᴇᴀꜱᴜʀᴇꜱ ᴛᴏ ᴘʀᴏᴛᴇᴄᴛ ʏᴏᴜʀ ɪɴғᴏʀᴍᴀᴛɪᴏɴ. 100% ꜱᴇᴄᴜʀᴇ ᴀʟʟ ɪɴғᴏ.\n\n"
        "ᴛʜᴀɴᴋ ʏᴏᴜ ғᴏʀ ᴜꜱɪɴɢ ᴜʟᴛɪᴍᴀᴛᴇ ʀᴇᴅᴇᴇᴍ ᴄᴏᴅᴇ ʙᴏᴛ. ᴡᴇ ᴀʀᴇ ᴄᴏᴍᴍɪᴛᴛᴇᴅ ᴛᴏ ᴘʀᴏᴛᴇᴄᴛɪɴɢ ʏᴏᴜʀ ᴘʀɪᴠᴀᴄʏ ᴀɴᴅ ᴇɴꜱᴜʀɪɴɢ ᴀɴ ᴇɴᴊᴏʏᴀʙʟᴇ ᴇxᴘᴇʀɪᴇɴᴄᴇ ᴡɪᴛʜ ᴏᴜʀ ʙᴏᴛ.\n\n"
        "☑️ ᴊᴏɪɴ ᴏᴜʀ ᴄᴏᴅɪɴɢ ᴄʜᴀɴɴᴇʟ ꜰᴏʀ ᴍᴏʀᴇ ʙᴏᴛꜱ ☑️"
    ).replace('_', '\\_')

    keyboard = InlineKeyboardMarkup()
    keyboard.add(InlineKeyboardButton(text="Close", callback_data="close_privacy"))

    bot.send_message(
        message.chat.id,
        privacy_content,
        parse_mode="Markdown",
        reply_markup=keyboard
    )

# Callback handler for closing the privacy policy message
@bot.callback_query_handler(func=lambda call: call.data == "close_privacy")
def close_privacy(call):
    bot.delete_message(call.message.chat.id, call.message.message_id)

# Help command handler
@bot.message_handler(commands=['help'])
def help_command(message):
    user_id = message.from_user.id

    # Help content
    help_content = (
        "🔰 **ᴡᴇʟᴄᴏᴍᴇ ᴛᴏ ᴛʜᴇ ʀᴇᴅᴇᴇᴍ ᴄᴏᴅᴇ ᴜʟᴛɪᴍᴀᴛᴇ ʙᴏᴛ!** 🔰\n\n"
        "ʜᴇʀᴇ ᴀʀᴇ ᴛʜᴇ ᴀᴠᴀɪʟᴀʙʟᴇ ᴄᴏᴍᴍᴀɴᴅꜱ:\n\n"
        "☑️ **ꜱᴛᴀʀᴛ - ꜱᴛᴀʀᴛ ᴛʜᴇ ʙᴏᴛ** ☑️\n\n"
        "📊 **ꜱᴛᴀᴛꜱ - ꜱᴇᴇ ꜱᴛᴀᴛɪꜱᴛɪᴄꜱ** 📊\n\n"
        "☑️ **ꜱᴇɴᴅ - ʙʀᴏᴀᴅᴄᴀꜱᴛ ᴍᴇꜱꜱᴀɢᴇ ᴛᴏ ᴜꜱᴇʀꜱ** ☑️\n\n"
        "☑️ **ʀᴇᴅᴇᴇᴍ - ʀᴇᴅᴇᴇᴍ ᴄᴏᴅᴇꜱ** ☑️\n\n"
        "☑️ **ɢᴇɴ - ɢᴇɴᴇʀᴀᴛᴇ ʀᴇᴅᴇᴇᴍ ᴄᴏᴅᴇꜱ** ☑️\n\n"
        "☑️ **ᴘᴏꜱᴛ - ᴀᴜᴛᴏ ᴘᴏꜱᴛ ᴛᴏ ᴍᴜʟᴛɪᴘʟᴇ ᴄʜᴀɴɴᴇʟꜱ** ☑️\n\n"
        "☑️ **ᴘʀɪᴠᴀᴄʏ - ᴘʀɪᴠᴀᴄʏ ᴀɴᴅ ᴘᴏʟɪᴄʏ** ☑️\n\n"
        "☑️ **ʜᴇʟᴘ - ʙᴏᴛ ᴀʟʟ ᴄᴏᴍᴍᴀɴᴅꜱ ᴇxᴘʟᴀɴᴀᴛɪᴏɴ** ☑️\n\n"
        "☑️ **ᴜᴘᴅᴀᴛᴇ - ᴜᴘᴅᴀᴛᴇ ʙᴏᴛ** ☑️\n\n"
        "☑️ **ꜱᴜᴘᴘᴏʀᴛ - ᴄᴏɴᴛᴀᴄᴛ ᴏᴡɴᴇʀ** ☑️\n"
    ).replace('_', '\\_')

    keyboard = InlineKeyboardMarkup()
    keyboard.add(InlineKeyboardButton(text="Close", callback_data="close_help"))

    bot.send_photo(
        message.chat.id,
        photo="https://t.me/abir_x_official_developer/94",
        caption=help_content,
        parse_mode="Markdown",
        reply_markup=keyboard
    )

# Callback handler for closing the help message
@bot.callback_query_handler(func=lambda call: call.data == "close_help")
def close_help(call):
    bot.delete_message(call.message.chat.id, call.message.message_id)

# Update command handler
@bot.message_handler(commands=['update'])
def update_bot(message):
    user_id = message.from_user.id

    # Initial update message with image
    update_message = bot.send_photo(
        message.chat.id,
        photo="https://t.me/abir_x_official_developer/95",
        caption="ʀᴇᴅᴇᴇᴍ ᴜʟᴛɪᴍᴀᴛᴇ ʙᴏᴛ ᴜᴘᴅᴀᴛɪɴɢ..........☑️"
    )

    # Progress bar animation
    progress_bar = ['░'] * 20
    for i in range(1, 21):
        progress_bar[i-1] = '▓'
        progress = ''.join(progress_bar)
        bot.edit_message_caption(
            caption=f"ʀᴇᴅᴇᴇᴍ ᴜʟᴛɪᴍᴀᴛᴇ ʙᴏᴛ ᴜᴘᴅᴀᴛɪɴɢ..........☑️\n[{progress}] {i*5}%",
            chat_id=update_message.chat.id,
            message_id=update_message.message_id
        )
        time.sleep(0.1)  # Simulate progress

    # Delete the update message after animation
    bot.delete_message(update_message.chat.id, update_message.message_id)

    # Final update message with image and button
    final_message = (
        "ʜᴇʏ ʙʀᴏ ! ʙᴏᴛ ᴜᴘᴅᴀᴛᴇᴅ ᴛᴏ ꜱᴜᴘʀᴇᴍᴇ☑️\n"
        "ᴜꜱᴇ /start ᴄᴏᴍᴍᴀɴᴅ ᴛᴏ ꜱᴇᴇ☑️"
    ).replace('_', '\\_')

    # Button for more updates
    keyboard = InlineKeyboardMarkup()
    keyboard.add(InlineKeyboardButton(text="☑️For More Updates Join ☑️", url="https://t.me/ModVipRM"))

    bot.send_photo(
        message.chat.id,
        photo="https://t.me/abir_x_official_developer/96",
        caption=final_message,
        parse_mode="Markdown",
        reply_markup=keyboard
    )

# Support command handler
@bot.message_handler(commands=['support'])
def support_command(message):
    user_id = message.from_user.id

    # Provide a cancel button
    keyboard = InlineKeyboardMarkup()
    keyboard.add(InlineKeyboardButton(text="Cancel", callback_data="cancel_support"))

    # Prompt the user for their problem with an image
    support_message = bot.send_photo(
        message.chat.id,
        photo="https://t.me/abir_x_official_developer/97",
        caption="ʜᴇʏ ʙʀᴏ ʏᴏᴜ ᴍɪɢʜᴛ ʙᴇ ꜰᴇᴛᴄʜɪɴɢ ᴘʀᴏʙʟᴇᴍ ᴡɪᴛʜ ʙᴏᴛ ᴘʟᴇᴀꜱᴇ ᴛᴇʟʟ ᴜꜱ ʏᴏᴜʀ ᴘʀᴏʙʟᴇᴍ",
        reply_markup=keyboard
    )

    # Register next step handler for the user's response
    bot.register_next_step_handler(support_message, handle_support_message)

# Handle the support message from the user
def handle_support_message(message):
    if message.text:
        # Forward the user's message to the bot owner
        forwarded_message = bot.forward_message(OWNER_USER_ID, message.chat.id, message.message_id)

        # Store the mapping of the forwarded message to the original user
        forwarded_messages[forwarded_message.message_id] = message.chat.id

        # Notify the user that their message has been forwarded with an image
        bot.send_photo(
            message.chat.id,
            photo="https://t.me/abir_x_official_developer/103",
            caption="ʏᴏᴜʀ ᴍᴇꜱꜱᴀɢᴇ ʜᴀꜱ ʙᴇᴇɴ ꜱᴇɴᴛ ᴛᴏ ᴛʜᴇ ʙᴏᴛ ᴏᴡɴᴇʀ. ᴛʜᴇʏ ᴡɪʟʟ ʀᴇᴘʟʏ ᴛᴏ ʏᴏᴜ ꜱʜᴏʀᴛʟʏ."
        )

        # Notify the owner that a new support message has been received with an image
        bot.send_photo(
            OWNER_USER_ID,
            photo="https://t.me/abir_x_official_developer/102",
            caption=f"ɴᴇᴡ ꜱᴜᴘᴘᴏʀᴛ ᴍᴇꜱꜱᴀɢᴇ ꜰʀᴏᴍ @{message.from_user.username} (ID: {message.from_user.id}). ʀᴇᴘʟʏ ᴅɪʀᴇᴄᴛʟʏ ᴛᴏ ᴛʜɪꜱ ᴍᴇꜱꜱᴀɢᴇ ᴛᴏ ʀᴇꜱᴘᴏɴᴅ."
        )

# Callback handler for canceling support input
@bot.callback_query_handler(func=lambda call: call.data == "cancel_support")
def cancel_support(call):
    bot.delete_message(call.message.chat.id, call.message.message_id)
    bot.send_photo(
        call.message.chat.id,
        photo="https://t.me/abir_x_official_developer/98",
        caption="ᴏᴡɴᴇʀ ᴄᴏɴᴛᴀᴄᴛ ᴄᴀɴᴄᴇʟʟᴇᴅ."
    )
    # Clear the step handler to avoid processing further messages
    bot.clear_step_handler_by_chat_id(call.message.chat.id)

# Handle replies from the bot owner
@bot.message_handler(func=lambda message: message.reply_to_message and message.reply_to_message.message_id in forwarded_messages)
def handle_owner_reply(message):
    original_user_id = forwarded_messages.get(message.reply_to_message.message_id)

    if original_user_id:
        bot.send_photo(
            original_user_id,
            photo="https://t.me/abir_x_official_developer/101",
            caption=f"ᴏᴡɴᴇʀ ʀᴇᴘʟʏ ᴛᴏ ʏᴏᴜʀ ᴍᴇꜱꜱᴀɢᴇ: {message.text}"
        )

        # Notify the owner that their reply has been sent
        bot.send_message(
            OWNER_USER_ID,
            "ʏᴏᴜʀ ʀᴇᴘʟʏ ʜᴀꜱ ʙᴇᴇɴ ꜱᴇɴᴛ ᴛᴏ ᴛʜᴇ ᴜꜱᴇʀ."
        )

# /info command handler
@bot.message_handler(commands=['info'])
def info_command(message):
    info_text = (
        "ʙᴏᴛ ʟᴀɴɢᴜᴀɢᴇ: ᴘʏᴛʜᴏɴ ☑️\n"
        "ʙᴏᴛ ʟɪʙʀᴀʀʏ: ᴘʏᴛʜᴏɴ ᴛᴇʟᴇʙᴏᴛ ☑️\n"
        "ʙᴏᴛ ʜᴏꜱᴛᴇᴅ ᴏɴ: ᴘᴇʟʟᴀ.ᴀᴘᴘ ☑️\n"
        "ʙᴏᴛ ʜᴏꜱᴛᴇᴅ ʙʏ: @abirxdhackz ☑️\n"
        "ʙᴏᴛ ᴍᴀɪɴᴛᴀɪɴᴇᴅ ʙʏ: @ModVipRM ☑️\n"
        "ʙᴏᴛ ᴜᴘᴅᴀᴛᴇꜱ ᴄʜᴀɴɴᴇʟ: @ModVipRM ☑️\n"
        "ʙᴏᴛ ꜱᴜᴘᴘᴏʀᴛ ɢʀᴏᴜᴘ: @ModVipRM_Discussion ☑️\n"
        "ʙᴏᴛ ꜱᴏᴜʀᴄᴇ ᴄᴏᴅᴇ: ʙʀᴏ ɪᴛ ɪꜱ ᴘᴀɪᴅ ᴅᴍ @abirxdhackz ☑️\n"
        "ʙᴏᴛ ᴘᴀʏᴍᴇɴᴛ ᴄʜᴀɴɴᴇʟ: @Proofchannelch ☑️"
    )

    keyboard = InlineKeyboardMarkup()
    keyboard.add(InlineKeyboardButton(text="Contact Owner ☑️", url="https://t.me/abirxdhackz"))
    keyboard.add(InlineKeyboardButton(text="Update Channel ☑️", url="https://t.me/ModVipRM"))

    # Send the image with the info text as the caption
    image_url = "https://t.me/abir_x_official_developer/105"
    bot.send_photo(message.chat.id, image_url, caption=info_text, reply_markup=keyboard)

def send_faq_menu(chat_id, message_id=None):
    # FAQ questions and answers
    faqs = {
        "ʜᴏᴡ ᴛᴏ ʀᴇᴅᴇᴇᴍ ᴀ ᴄᴏᴅᴇ ?": (
            "☑️ ғɪʀꜱᴛ ᴏᴘᴇɴ ᴛʜᴇ ʙᴏᴛ.\n\n"
            "☑️ ᴛʜᴇɴ ᴊᴏɪɴ ᴀʟʟ ᴄʜᴀɴɴᴇʟꜱ.\n\n"
            "☑️ ᴛʜᴇɴ ᴜꜱᴇ /redeem ᴄᴏᴍᴍᴀɴᴅ ᴀɴᴅ ᴀꜰᴛᴇʀ ɪᴛ ᴘᴀꜱᴛᴇ ʏᴏᴜʀ ʀᴇᴅᴇᴇᴍ ᴄᴏᴅᴇ ꜰᴏᴜɴᴅ ꜰʀᴏᴍ ᴏᴜʀ ᴄʜᴀɴɴᴇʟꜱ.\n\n"
            "☑️ ᴇxᴀᴍᴘʟᴇ\n\n"
            "/redeem CRUNCHYROLL-5350-3031-9889"
        ),
        "ᴡɪʟʟ ᴀ ᴘᴇʀꜱᴏɴ ᴄᴀɴ ʀᴇᴅᴇᴇᴍ ᴍᴜʟᴛɪᴘʟᴇ ᴛɪᴍᴇ?": 
            "❌ ɴᴏ ʙʀᴏ ɴᴏɴᴇ ᴄᴀɴ ʀᴇᴅᴇᴇᴍ ᴍᴜʟᴛɪᴘʟᴇ ᴛɪᴍᴇ ᴀꜱ ᴏᴜʀ ʙᴏᴛ ꜱᴇᴄᴜʀɪᴛʏ ☑️",
        "ɪꜱ ᴛʜᴇ ʙᴏᴛ ᴘᴀɪᴅ?": 
            "❌ ɴᴏ ʙʀᴏ ʙᴏᴛ ɪꜱ ɴᴏᴛ ᴘᴀɪᴅ ʏᴏᴜ ᴊᴜꜱᴛ ʜᴀᴠᴇ ᴛᴏ ᴊᴏɪɴ 4 ᴄʜᴀɴɴᴇʟꜱ ᴛᴏ ᴜꜱᴇ ɪᴛ ☑️",
        "ᴄᴀɴ ᴛʜᴇ ʙᴏᴛ ꜱᴏᴜʀᴄᴇ ᴄᴏᴅᴇ ʙᴇ ꜱʜᴀʀᴇᴅ?": 
            "❌ ɴᴏ ʙʀᴏ ʙᴏᴛ ꜱᴏᴜʀᴄᴇ ᴄᴏᴅᴇ ɪꜱ ᴘᴀɪᴅ ᴅᴍ @abirxdhackz ꜰᴏʀ ɪᴛ. ☑️"
    }

    # Create the caption with questions in bold and answers in normal text
    faq_caption = "☑️ <b>Frequently Asked Questions:</b>\n\n"
    for question, answer in faqs.items():
        faq_caption += f"🔹 <b>{question}</b>\n"
        faq_caption += f"{answer}\n\n"
    
    # Add the inline button
    keyboard = InlineKeyboardMarkup()
    keyboard.add(InlineKeyboardButton(text="🙋 Ask Questions In Community ☑️", url="https://t.me/ModVipRM_Discussion"))

    # Send the image with the caption and inline button
    image_url = "https://t.me/abir_x_official_developer/106"
    if message_id:
        bot.edit_message_media(chat_id=chat_id, message_id=message_id, media=telebot.types.InputMediaPhoto(image_url, caption=faq_caption, parse_mode='HTML'), reply_markup=keyboard)
    else:
        bot.send_photo(chat_id, image_url, caption=faq_caption, reply_markup=keyboard, parse_mode='HTML')

# /faq command handler
@bot.message_handler(commands=['faq'])
def faq_command(message):
    send_faq_menu(message.chat.id)

# Start the bot
print("Bot is running...")
bot.polling()
