from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
import requests
from commands.money.money import add_money, deduct_money, get_money  # Import hệ thống tiền
from config import DOVUI_REWARD, DOVUI_PENALTY  # Lấy giá trị từ config.py

dovui_data = {}  # Lưu câu hỏi theo chat_id

def get_question():
    """Lấy câu hỏi từ API"""
    url = "https://subhatde.id.vn/game/dovui"
    try:
        response = requests.get(url)
        data = response.json().get("data", {})
        return {
            "question": data.get("question", ""),
            "options": data.get("option", []),
            "correct": data.get("correct", "")
        }
    except Exception as e:
        print(f"Lỗi lấy câu hỏi: {e}")
        return None

def setup_game(bot):
    @bot.message_handler(commands=['dovui'])
    def dovui_game(message):
        """Gửi câu hỏi đố vui"""
        question_data = get_question()
        if not question_data:
            bot.send_message(message.chat.id, "🚨 Lỗi khi lấy câu hỏi!")
            return

        question = question_data["question"]
        options = question_data["options"]
        correct_answer = question_data["correct"]

        # Lưu dữ liệu câu hỏi vào dict
        dovui_data[message.chat.id] = {"correct": correct_answer, "options": options}

        # Tạo InlineKeyboard
        markup = InlineKeyboardMarkup()
        for idx, option in enumerate(options):
            markup.add(InlineKeyboardButton(option, callback_data=f"dovui|{idx}"))

        bot.send_message(message.chat.id, f"❓ {question}", reply_markup=markup)

    @bot.callback_query_handler(func=lambda call: call.data.startswith("dovui|"))
    def check_answer(call):
        """Xử lý khi chọn đáp án"""
        chat_id = call.message.chat.id
        user_id = call.from_user.id  # Lấy ID user
        index = int(call.data.split("|")[1])  # Lấy chỉ số đáp án

        # Kiểm tra dữ liệu câu hỏi
        if chat_id not in dovui_data:
            bot.answer_callback_query(call.id, "🚨 Lỗi dữ liệu, thử lại sau!")
            return

        correct_answer = dovui_data[chat_id]["correct"]
        options = dovui_data[chat_id]["options"]
        chosen_answer = options[index]

        msg_id = call.message.message_id

        if chosen_answer == correct_answer:
            add_money(user_id, DOVUI_REWARD)  # Sử dụng giá trị từ config.py
            new_balance = get_money(user_id)
            result = f"🎉 Chính xác! Bạn nhận được **+{DOVUI_REWARD}💰**\n💰 Số dư hiện tại: {new_balance}💰"
        else:
            deduct_money(user_id, DOVUI_PENALTY)  # Sử dụng giá trị từ config.py
            new_balance = get_money(user_id)
            result = f"❌ Sai! Đáp án đúng là: **{correct_answer}**.\n🔻 Bạn bị **-{DOVUI_PENALTY}💰**\n💰 Số dư hiện tại: {new_balance}💰"

        # Xóa tin nhắn câu hỏi sau khi chọn
        bot.delete_message(chat_id, msg_id)
        bot.send_message(chat_id, result)
