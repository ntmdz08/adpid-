import random
from commands.money.money import add_money, deduct_money, get_money
from config import PPT_PENALTY, PPT_REWARD

CHOICES = ["kéo", "bao", "búa"]
user_choices = {}

def setup_game(bot):
    @bot.message_handler(commands=['ppt'])
    def start_ppt(message):
        bot_choice = random.choice(CHOICES)
        user_choices[message.chat.id] = bot_choice  
        bot.reply_to(message, "🎮 Tớ chọn rồi, cậu chọn đi (Kéo, Bao, Búa)!")

    @bot.message_handler(func=lambda message: message.text.lower() in CHOICES)
    def handle_ppt_reply(message):
        chat_id = message.chat.id
        user_id = message.from_user.id

        if chat_id not in user_choices:
            bot.reply_to(message, "Cậu chưa bắt đầu game! Gõ /ppt để chơi.")
            return

        bot_choice = user_choices.pop(chat_id)
        user_choice = message.text.lower()
        win_money = PPT_REWARD
        lose_money = PPT_PENALTY

        if (
            (user_choice == "kéo" and bot_choice == "bao") or
            (user_choice == "bao" and bot_choice == "búa") or
            (user_choice == "búa" and bot_choice == "kéo")
        ):
            result = f"🎉 Chúc mừng! Cậu thắng {win_money}💰!"
            add_money(user_id, win_money)  # Cộng tiền
        elif user_choice == bot_choice:
            result = "🎭 Hòa nhau rồi!"
        else:
            result = f"😢 Cậu thua rồi, mất {lose_money}💰!"
            deduct_money(user_id, lose_money)  # Trừ tiền

        user_balance = get_money(user_id)
        bot.reply_to(message, f"Tớ chọn {bot_choice.capitalize()}.\nCậu chọn {user_choice.capitalize()}.\n{result}\n💰 Số dư hiện tại: {user_balance}💰")
