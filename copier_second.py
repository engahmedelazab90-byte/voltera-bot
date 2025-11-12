import os
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes

SOURCE_CHAT_ID = int(os.getenv("SOURCE_CHAT_ID", "-1002307891907"))  # جروب المصدر
TARGET_CHAT_IDS = [int(x) for x in os.getenv("TARGET_CHAT_IDS", "-1001877613633,-1001831208064,-1003122776203,-1002243512135,-1001945968861,-1002381368613,-1002308429112,-1001816602568,-1002400046352,-1001518389308,-1002741628383,-1001988599283,-1001605571320,-1002378030426").split(",")]  # الجروبات الهدف
SHOW_PREFIX = os.getenv("SHOW_PREFIX", "true").lower() == "true"
PREFIX_TEXT = os.getenv("PREFIX_TEXT", "【via Copier #2】")

BOT_TOKEN = os.getenv("BOT_TOKEN")

async def forward_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    if chat_id == SOURCE_CHAT_ID:
        for target_id in TARGET_CHAT_IDS:
            try:
                if update.message.text:
                    text = f"{PREFIX_TEXT}\n{update.message.text}" if SHOW_PREFIX else update.message.text
                    await context.bot.send_message(chat_id=target_id, text=text)
                elif update.message.photo:
                    caption = f"{PREFIX_TEXT}\n{update.message.caption or ''}" if SHOW_PREFIX else (update.message.caption or '')
                    await context.bot.send_photo(chat_id=target_id, photo=update.message.photo[-1].file_id, caption=caption)
                elif update.message.video:
                    caption = f"{PREFIX_TEXT}\n{update.message.caption or ''}" if SHOW_PREFIX else (update.message.caption or '')
                    await context.bot.send_video(chat_id=target_id, video=update.message.video.file_id, caption=caption)
            except Exception as e:
                print(f"❌ Error sending to {target_id}: {e}")

def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(MessageHandler(filters.ALL, forward_message))
    print(f"✅ Copier #2 running… SOURCE: {SOURCE_CHAT_ID} → TARGETS: {TARGET_CHAT_IDS}")
    app.run_polling()

if name == "__main__":
    main()
