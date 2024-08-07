import telebot
import matplotlib
from saved_texts import *
from manageJsonFiles import *
from telebot.types import Message, InlineKeyboardButton, InlineKeyboardMarkup
from telebot.types import CallbackQuery, KeyboardButton
import random

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

    rating_list = [rate_data ["rate"] for rate_data in lst]

    rating = sum (rating_list) / len (lst) if len (lst) > 0 else "لا تقييم للبوت الى الآن"

    rating_comments_txt = ""

    for comment_data in data ["all_users_comments_rate"]:

        username = comment_data ["username"]

        comment = comment_data ["comment"]

        rating_comments_txt += f"♜ {username} : {comment} \n"

    message = about_bot (len (data ["all_chat_id"]), len (data ["succed_proccesses"]), rating, rating_comments_txt)

    bot.send_photo (m.chat.id, open ("bot.jpg", "rb"),caption= message)

#? get rate from user
@bot.message_handler (commands= ["rateme"])
def rateme (m : Message):

    data = get_json_data ("customers")

    rate_data = get_obj (data, "all_users_rate", "c_id", m.chat.id)
    
    if rate_data :
        rate = rate_data ["rate"]
        bot.send_message (m.chat.id, f"لقد قمت بتقييم المتجر بالفعل  {rate} الآن ستقوم بتغيره :")

    reply = bot.send_message (m.chat.id, "قم بارسال تقيمك للمتجر من 0 الى 10  : ")
    
    def the_rating (m2: Message):
        txt = m2.text
        therate = float (txt)
        chat_id = m2.chat.id
        rate_data = get_obj (data, "all_users_rate", "c_id", chat_id)
        if not float (txt) :
            return bot.send_message (chat_id, "يجب ان يكون التقييم ارقام فقط : ")
        if not (therate <= 10 and therate >= 0) :
            return bot.send_message (chat_id, "يجب ان يكون التقيم ما بين 0 و 10")

        if type (rate_data) != bool :
            update_value ("customers", "all_users_rate", "c_id", m.chat.id, "rate", therate)
        else :
            rate_data = {
            "c_id" : m.chat.id,
            "username" : f"@{m.from_user.username}",
            "rate" : therate }
            add_obj2list ("customers", "all_users_rate", rate_data)
        bot.send_message (chat_id, "شكرا على تزويدنا بتقييمك")
        if therate <= 5:
            bot.send_message (chat_id, f"نرجو تزويدنا بالسبب الذي جعلك تضع هذا التقييم السيئ {myusername}")

    bot.register_next_step_handler (reply, the_rating)

#! get comment from user
@bot.message_handler (commands= ["ratecomment"])
def reatecomment (m: Message):
    data = get_json_data ("customers")
    chat_id = m.chat.id
    comment_data = get_obj (data, "all_users_comments_rate", "c_id", chat_id)
    username = m.from_user.username
    if comment_data :
        comm = comment_data ["comment"]
        bot.send_message (chat_id, 
            f"لقد قيمت المتجر من قبل و هذا كان تقييمك \n{comm}\n سوف يتم تفييره بالتقييم الذي ستقدمه لنا الآن")
    request_message = bot.reply_to (m, "ارسل لنا التقييم الآن : ")
    
    def get_comment (m2 : Message):
        admin_id = admin_ids [0]
        txt = m.text
        agreement_markup = InlineKeyboardMarkup (row_width= 8)
        agree_button = InlineKeyboardButton ("Agree", callback_data= f"AgreeToComment {comment_data ["comment_id"]}")
        disagree_button = InlineKeyboardButton ("Agree", callback_data= f"DisgreeToComment {comment_data ["comment_id"]}")
        comment_id = 10000 + random.randint (0, 4445)
        comment_dict = {
                "c_id": chat_id,
                "comment_id": comment_id,
                "username": f"@{username}",
                "comment": txt
            }
        for button in [agree_button, disagree_button]: agreement_markup.add (button)
        add_obj2list (data, "agreement_comments", comment_dict)
        bot.send_message (admin_id, f"the user : {username} commnted on the sotre : \n {txt} are you agree",
                          reply_markup= agreement_markup)
        bot.reply_to (m2, 
       "تم ارسال تعليقك الى الادمن للموافقه عليه ، سيتم الموافقه على التقييم في حال انه ليس تافه او لا يوجد به تعدي")
    bot.register_next_step_handler (request_message, get_comment)

def AgreeToComment (comment_id):
    comment_obj = get_obj ("customers", "agreement_comments", "comment_id", comment_id)
    remove_obj_from_list ("customers", "agreement_comments", comment_obj)
    add_obj2list ("customers", "all_users_comments_rate", comment_obj)
    bot.send_message (comment_obj ["c_id"], "التقييم بتاعك اتقبل من الادمن")

def DisgreeToComment (comment_id):
    pass

@bot.callback_query_handler (func= lambda call : True)
def call (call : CallbackQuery):
    pass

#! sotre main menu buttons
bot.infinity_polling ()