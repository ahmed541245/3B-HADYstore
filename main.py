import telebot
import matplotlib
from saved_texts import *
from manageJsonFiles import *
from telebot.types import Message, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery

token = "7260622545:AAFy-2O067SNaEl7W4PtMPbmfSfXHyqKCSc"
bot = telebot.TeleBot (token)

def converting_time (value, timefrom, timeto):
    "from the smallest to the biggest such as 3600 second = 1 hour"
    times = {
        "se":1,
        "mi":60,
        "ho":60,
        "da":24,
        "mo":30,
        "ye":12
    }

    keys = list (times.keys ())
    indexfrom = keys.index (timefrom) + 1
    indexto = keys.index (timeto)
    lst = keys [indexfrom : indexto + 1]
    if len (keys) - 1 == indexto :
        lst = keys [indexfrom :]
    
    result = value
    for time in lst :
        result = result / times [time]
    return result

#? start chating method
@bot.message_handler (commands= ["start"])
def start (message : Message):
    customers_data = get_json_data ("customers")
    id_list = customers_data ["all_chat_id"]
    name = message.from_user.first_name
    chat_id = message.chat.id
    if chat_id in id_list:
        return bot.send_message (chat_id, second_start_message (name))
    add_obj2list ("customers", "all_chat_id", message.chat.id)
    if chat_id not in admin_ids :
        return bot.send_message (chat_id, first_start_message (name))
    bot.send_message (chat_id, f"Hello, {name}......You are now an admin")
    
#? programmer informing message
@bot.message_handler (commands= ["dev"])
def dev (m : Message):
    markup = InlineKeyboardMarkup (row_width= 5)
    whats_app = "https://wa.me/+201096940855"
    telegram = "https://t.me/AbdElhadyDev"
    instagram = "https://www.instagram.com/abdelhadydev/"
    facebook = "https://www.facebook.com/profile.php?id=100087962405923"
    links = {whats_app : "𝕎𝕙𝕒𝕥𝕤𝔸𝕡𝕡", telegram : "𝕋𝕖𝕝𝕖𝕘𝕣𝕒𝕞", instagram: "𝕀𝕟𝕤𝕥𝕒𝕘𝕣𝕒𝕞", facebook: "𝔽𝕒𝕔𝕖𝕓𝕠𝕠𝕜"}
    for link in links :
        button = InlineKeyboardButton (links [link], url= link)
        markup.add (button)
    bot.send_photo (m.chat.id, open ("myphoto.jpg", "rb"), programmer_text, reply_markup= markup)


#? about the bot message
@bot.message_handler (commands= ["about"])
def about (m: Message):
    data = get_json_data ("customers")
    lst = data ["all_users_rate"]
    rating = sum (lst) / len (lst) if len (lst) > 0 else "لا تقييم للبوت الى الآن"
    rating_comments_txt = ""
    for comment in data ["all_users_comments_rate"]:
        rating_comments_txt += f"♜ {comment} \n"
    message = about_bot (len (data ["all_chat_id"]), len (data ["succed_proccesses"]), rating, rating_comments_txt)
    bot.send_photo (m.chat.id, open ("bot.jpg", "rb"),caption= message)
#! sotre main menu buttons
bot.infinity_polling ()