# Tìm kiếm video trên YouTube
import requests
from config import YOUTUBE_API_KEY

COMMAND_INFO = ("/vytb", "Tìm kiếm video trên YouTube")

def video_yt(bot):
    @bot.message_handler(commands=['vytb', 'youtube'])
    def search_video(message):
        query = message.text.replace('/vytb', '').strip()
        bot.reply_to(message, search_youtube(query))

    def search_youtube(query):
        """Tìm kiếm video trên YouTube"""
        url = f"https://www.googleapis.com/youtube/v3/search?part=snippet&q={query}&type=video&key={YOUTUBE_API_KEY}"
        response = requests.get(url).json()

        if "items" in response and response["items"]:
            video = response["items"][0]
            title = video["snippet"]["title"]
            video_id = video["id"]["videoId"]
            return f"🎬 {title}\n🔗 https://www.youtube.com/watch?v={video_id}"

        return "Không tìm thấy video nào!"