import requests
from config import YOUTUBE_API_KEY

COMMAND_INFO = ("/sytb", "Tìm kiếm kênh YouTube")

def search_yt(bot):
    @bot.message_handler(commands=['sytb'])
    def channel_info(message):
        channel_name = message.text.replace('/sytb', '').strip()
        bot.reply_to(message, get_channel_info(channel_name))
    def get_channel_info(channel_name):
        """Lấy thông tin kênh YouTube theo tên"""
        url = f"https://www.googleapis.com/youtube/v3/search?part=snippet&q={channel_name}&type=channel&key={YOUTUBE_API_KEY}"
        response = requests.get(url).json()
        
        if "items" in response and response["items"]:
            channel = response["items"][0]
            title = channel["snippet"]["title"]
            channel_id = channel["id"]["channelId"]

            url_stats = f"https://www.googleapis.com/youtube/v3/channels?part=statistics&id={channel_id}&key={YOUTUBE_API_KEY}"
            stats = requests.get(url_stats).json()["items"][0]["statistics"]

            subs = stats.get("subscriberCount", "Không rõ")
            videos = stats.get("videoCount", "Không rõ")
            views = stats.get("viewCount", "Không rõ")

            return f"📺 Kênh: {title}\n👥 Sub: {subs}\n🎥 Video: {videos}\n👀 Lượt xem: {views}\n🔗 https://www.youtube.com/channel/{channel_id}"

        return "Không tìm thấy kênh nào!"
