from pytube import Playlist
import telebot

token = "7260622545:AAFy-2O067SNaEl7W4PtMPbmfSfXHyqKCSc"
bot = telebot.TeleBot (token)

def get_playlist_video_titles(playlist_url):
    # بنعمل كائن من بلاي ليست باستخدام الرابط
    playlist = Playlist(playlist_url)
    
    # بنجيب عناوين الفيديوهات
    video_titles = [video.title for video in playlist.videos]
    
    # بنرتب عناوين الفيديوهات
    video_titles.sort()
    
    return video_titles

# استبدل برابط البلاي ليست اللي عايز تجيب منها البيانات
playlist_url = "https://www.youtube.com/playlist?list=PLp14ekVfgMsr-czwdqGKubzqNMvTRy-Zc"

video_titles = get_playlist_video_titles(playlist_url)
mess = ""
for title in video_titles:
    title = f"\n{title}\n"
    print (title)
    mess += title

bot.send_message (6852863205, mess)
bot.infinity_polling ()