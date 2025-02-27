import os
import importlib
import telebot
from commands.ytb.search import search_yt
from commands.ytb.video import video_yt
from commands.aichat.chat import chat_gpt
from commands.game.ppt_game import setup_game
from commands.game.dovui_game import setup_game
from commands.money.money import setup_money
from commands.aichat.gemini import chat_gemini
from config import TOKEN
bot = telebot.TeleBot(TOKEN)

COMMANDS_FOLDER = "commands"
GAME_FOLDER = "commands/game"

commands_list = []
game_list = {}

# ============================ 📌 LOAD LỆNH ============================ #

def load_commands():
    global commands_list
    commands_list.clear()

    for root, _, files in os.walk(COMMANDS_FOLDER):
        for file in files:
            if file.endswith(".py") and not file.startswith("__"):
                relative_path = os.path.relpath(root, COMMANDS_FOLDER)
                module_name = file[:-3]  # Bỏ ".py"

                # Tạo đường dẫn module (vd: commands.youtube)
                if relative_path == ".":
                    module_path = f"commands.{module_name}"
                else:
                    module_path = f"commands.{relative_path.replace(os.sep, '.')}.{module_name}"

                try:
                    module = importlib.import_module(module_path)
                    if hasattr(module, "COMMAND_INFO"):  # Lấy thông tin từ mỗi file
                        commands_list.append(module.COMMAND_INFO)
                        print(f"✅ Loaded command: {module_path}")
                except Exception as e:
                    print(f"❌ Không thể load {module_path}: {e}")

# ============================ 🎮 LOAD GAME ============================ #

def load_games():
    global game_list
    game_list.clear()

    for root, _, files in os.walk(GAME_FOLDER):
        for file in files:
            if file.endswith("_game.py"):  # Chỉ load file có "_game.py"
                relative_path = os.path.relpath(root, GAME_FOLDER)
                module_name = file[:-3]  # Bỏ ".py"

                # Tạo đường dẫn module (vd: commands.game.ppt_game)
                if relative_path == ".":
                    module_path = f"commands.game.{module_name}"
                else:
                    module_path = f"commands.game.{relative_path.replace(os.sep, '.')}.{module_name}"

                module = importlib.import_module(module_path)

                if hasattr(module, "setup_game"):
                    module.setup_game(bot)
                    game_list[module_path] = module
                    print(f"✅ Loaded game: {module_path}")

# ============================ 🆘 LỆNH HELP ============================ #
@bot.message_handler(commands=['help'])
def send_help(message):
    load_commands()  # Cập nhật danh sách lệnh
    load_games()  # Cập nhật danh sách game

    help_text = "🆘 **Danh sách lệnh:**\n"
    for cmd, desc in commands_list:
        help_text += f"📌 {cmd} - {desc}\n"

    help_text += "\n🎮 **Danh sách game:**\n"
    for game in game_list:
        game_cmd = "/" + game.split(".")[-1].replace("_game", "")  # Lấy tên game từ file
        help_text += f"🎮 {game_cmd}\n"

    bot.reply_to(message, help_text, parse_mode="Markdown")

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Chào! Tôi là bot Telegram By ntmdz.\nGõ /help để xem các lệnh.")

@bot.message_handler(commands=['reload'])
def reload_commands(message):
    load_commands()
    bot.reply_to(message, "🔄 Đã load lại lệnh!")

# ============================ 🚀 CHẠY BOT ============================ #
load_commands()
load_games()
search_yt(bot)
video_yt(bot)
chat_gpt(bot)
chat_gemini(bot)
setup_game(bot)
setup_money(bot)


# 🚀 Chạy bot
print("🔥 Bot Telegram đang chạy...")
bot.polling()
