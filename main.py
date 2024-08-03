import telebot
import matplotlib
from saved_texts import *
from manageJsonFiles import *
from telebot.types import Message, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery
token = ""
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

#! start chating method
@bot.message_handler (commands= ["start"])
def start (message : Message):
    customers_data = get_json_data ("customers")
    id_list = customers_data ["selling_processes"]
    name = message.from_user.first_name
    chat_id = message.chat.id
    if chat_id in id_list:
        return bot.send_message (chat_id, second_start_message (name))
    customers_data = add_obj2list ("customers", "selling_processes", str (message.chat.id))
    updata_data ("customers", customers_data)
    bot.send_message (chat_id, first_start_message (name))
    
#! programmer informing message
#! about the bot message
#! sotre main menu buttons
bot.infinity_polling ()