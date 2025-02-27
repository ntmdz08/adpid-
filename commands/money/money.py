import json
import os

MONEY_FILE = "commands/money/money.json"

COMMAND_INFO = ("/money", "Xem số dư của bạn")

# Kiểm tra nếu chưa có file, thì tạo mới
if not os.path.exists(MONEY_FILE):
    with open(MONEY_FILE, "w") as f:
        json.dump({}, f)

# Đọc dữ liệu tiền từ file
def load_money():
    with open(MONEY_FILE, "r") as f:
        return json.load(f)

# Lưu dữ liệu tiền vào file
def save_money(data):
    with open(MONEY_FILE, "w") as f:
        json.dump(data, f, indent=4)

# Lấy số tiền của người chơi
def get_money(user_id):
    data = load_money()
    return data.get(str(user_id), 1000)  # Mặc định 1000 tiền

# Cộng tiền
def add_money(user_id, amount):
    data = load_money()
    user_id = str(user_id)
    data[user_id] = data.get(user_id, 1000) + amount
    save_money(data)

# Trừ tiền
def deduct_money(user_id, amount):
    data = load_money()
    user_id = str(user_id)
    data[user_id] = max(0, data.get(user_id, 1000) - amount)  # Không xuống âm
    save_money(data)

def setup_money(bot):
    @bot.message_handler(commands=['money'])
    def check_money(message):
        user_id = message.from_user.id
        balance = get_money(user_id)
        bot.reply_to(message, f"💰 Số dư của cậu: {balance}💰")