import google.generativeai as genai
from config import GEMINI_API_KEY

COMMAND_INFO = ("/gemini", "Trò chuyện với Gemini")

# Khởi tạo Gemini API
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel("gemini-1.5-flash")

def chat_gemini(bot):
    @bot.message_handler(commands=['gemini'])
    def chat(message):
        user_msg = message.text.replace('/gemini', '').strip()
        if not user_msg:
            bot.reply_to(message, "Bạn muốn nói gì nào?")
            return
        bot.reply_to(message, chat_with_gemini(user_msg))


def chat_with_gemini(user_msg):
    """Trò chuyện với Gemini với phong cách láo, thân thiện, thích code, paimon."""
    try:
        response = model.generate_content(f"Cậu là một trợ lý láo, thích code, là paimon dễ thương, nói chuyện teencode.\nNgười dùng: {user_msg}")
        return response.text
    except Exception as e:
        return f"Đã xảy ra lỗi: {str(e)}"