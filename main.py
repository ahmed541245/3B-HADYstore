import telebot
import json
import matplotlib

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
    
