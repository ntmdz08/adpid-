import openai
from config import OPENAI_API_KEY

COMMAND_INFO = ("/gpt", "Trò chuyện với OpenAI")

def chat_gpt(bot):
    @bot.message_handler(commands=['gpt'])
    def chat(message):
        user_msg = message.text.replace('/gpt', '').strip()
        if not user_msg:
            bot.reply_to(message, "Bạn muốn nói gì nào?")
            return
        bot.reply_to(message, chat_with_gpt(user_msg))

def chat_with_gpt(user_msg):
    """Trò chuyện với OpenAI với phong cách láo, thân thiện, thích code"""
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Cậu là một trợ lý láo, thân thiện, thích code, nói chuyện teencode, paimon dễ thương."},
                {"role": "user", "content": user_msg}
            ],
            api_key=OPENAI_API_KEY
        )
        return response["choices"][0]["message"]["content"]
    except Exception as e:
        return f"Đã xảy ra lỗi: {str(e)}"