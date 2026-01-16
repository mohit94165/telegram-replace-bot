from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Updater,
    CommandHandler,
    MessageHandler,
    Filters,
    CallbackQueryHandler,
    CallbackContext
)

TOKEN = 8332142684:AAGpqapgvqPSmwF0ya0_eYs2yrY3ovRmmr8

old_word = ""
new_word = ""

def start(update: Update, context: CallbackContext):
    keyboard = [
        [InlineKeyboardButton("♻ Replace Word", callback_data="replace")],
        [InlineKeyboardButton("❌ Reset", callback_data="reset")]
    ]
    update.message.reply_text(
        "🔥 Caption Replace Bot Ready!\n\n"
        "Use:\n/replace OLD | NEW\n\n"
        "Then send videos.",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

def replace_cmd(update: Update, context: CallbackContext):
    global old_word, new_word
    try:
        text = update.message.text.replace("/replace", "").strip()
        old_word, new_word = text.split("|")
        old_word = old_word.strip()
        new_word = new_word.strip()
        update.message.reply_text(
            f"✅ Replace Set:\n\n'{old_word}' ➜ '{new_word}'\n\nNow send videos."
        )
    except:
        update.message.reply_text("❌ Format galat!\nUse:\n/replace old | new")

def video_handler(update: Update, context: CallbackContext):
    if not old_word:
        update.message.reply_text("⚠ Pehle /replace command use karo.")
        return

    caption = update.message.caption or ""
    new_caption = caption.replace(old_word, new_word)

    context.bot.send_video(
        chat_id=update.message.chat_id,
        video=update.message.video.file_id,
        caption=new_caption
    )

def buttons(update: Update, context: CallbackContext):
    global old_word, new_word
    query = update.callback_query
    query.answer()

    if query.data == "replace":
        query.message.reply_text("✍ Use command:\n/replace OLD | NEW")

    elif query.data == "reset":
        old_word = ""
        new_word = ""
        query.message.reply_text("♻ Replacement reset ho gaya.")

updater = Updater(TOKEN, use_context=True)
dp = updater.dispatcher

dp.add_handler(CommandHandler("start", start))
dp.add_handler(CommandHandler("replace", replace_cmd))
dp.add_handler(CallbackQueryHandler(buttons))
dp.add_handler(MessageHandler(Filters.video, video_handler))

updater.start_polling()
updater.idle()