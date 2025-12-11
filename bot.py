# bot.py — Nexus Veritas Telegram Bridge
import json, logging, time
from telegram import Update, ParseMode
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

# load config
with open("config.json","r") as f:
    cfg = json.load(f)

BOT_TOKEN = cfg.get("BOT_TOKEN")
AUTHORIZED = set(cfg.get("AUTHORIZED_IDS", []))

logging.basicConfig(level=logging.INFO)

from core.answerer import answer_query

def is_auth(uid):
    return uid in AUTHORIZED

def start(update: Update, context: CallbackContext):
    uid = update.effective_user.id
    if not is_auth(uid):
        update.message.reply_text("Not authorized.")
        return
    update.message.reply_text("Astra Veritas Engine online! Send your query or use !update <topic>.")

def handle_message(update: Update, context: CallbackContext):
    uid = update.effective_user.id
    if not is_auth(uid):
        update.message.reply_text("Not authorized.")
        return

    text = update.message.text.strip()

    if text.startswith("!update "):
        key = text.replace("!update ","").strip()
        res = answer_query(key, force_update=True)
    else:
        res = answer_query(text)

    ans = res["answer"]
    src = res.get("sources", "No source")
    conf = res.get("confidence", 0.0)
    cached = res.get("cached", False)
    last = res.get("last_updated")
    last_str = time.ctime(last) if last else "N/A"

    reply = f"*Answer:*\n{ans[:1200]}\n\n*Source:* {src}\n*Last updated:* {last_str}\n*Confidence:* {conf:.2f}\n*Cached:* {cached}"
    update.message.reply_text(reply, parse_mode=ParseMode.MARKDOWN)

def main():
    if not BOT_TOKEN:
        print("ERROR: Bot token missing in config.json")
        return

    updater = Updater(BOT_TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_message))

    print("Bot starting...")
    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()
