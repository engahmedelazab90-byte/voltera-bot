# copier_multi.py — ينسخ الرسائل من جروب مصدر لعدة جروبات هدف (+ ترويسة باسم البوت)
import sys, asyncio
from telegram import Update
from telegram.ext import Application, MessageHandler, CommandHandler, ContextTypes, filters

BOT_TOKEN = "8268549146:AAEe-iXS4pn_eUnqaozrTZEB1T_sPgIfRU0"            # ← حط التوكن بين " "
SOURCE_CHAT_ID = -1003250786039              # ← chat_id جروب المصدر
TARGET_CHAT_IDS = [                          # ← حط هنا أكتر من جروب هدف
    -1003172224979,
    -1002513344948,
    -1003079805290,
    # زوّد أو قلّل براحتك
]

# لو عايز يظهر سطر في بداية كل رسالة باسم البوت (يبان اسم البوت بوضوح)
SHOW_PREFIX = False
BOT_USERNAME = "@YourBotUsername"            # ← غيّرها ليوزر البوت بتاعك (اختياري)

async def cmd_id(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(f"chat_id: {update.effective_chat.id}")

async def send_to_targets(context: ContextTypes.DEFAULT_TYPE, msg: "Message"):
    # نبعت لكل الجروبات الهدف
    for target in TARGET_CHAT_IDS:
        try:
            # لو عايز يظهر اسم البوت بشكل واضح قبل المحتوى
            if SHOW_PREFIX:
                # نبعت ترويسة بسيطة باسم البوت قبل النسخة
                await context.bot.send_message(
                    chat_id=target,
                    text=f"【via {BOT_USERNAME}】"
                )

            # انسخ الرسالة كما هي (يحافظ على الميديا والفورمات) وبتظهر من البوت
            await context.bot.copy_message(
                chat_id=target,
                from_chat_id=SOURCE_CHAT_ID,
                message_id=msg.message_id,
                protect_content=False
            )
        except Exception as e:
            print(f"Copy error to {target}: {e}")

async def copier(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat = update.effective_chat
    msg = update.effective_message

    # انسخ فقط رسائل جروب المصدر (علشان مايحصلش لوب)
    if chat.id != SOURCE_CHAT_ID:
        return

    # تجاهل أوامر
    if msg.text and msg.text.startswith("/"):
        return

    await send_to_targets(context, msg)

def build_app():
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("id", cmd_id))
    app.add_handler(MessageHandler(filters.ALL & ~filters.COMMAND, copier))
    return app

if __name__ == "__main__":
    # إصلاح loop على ويندوز
    if sys.platform.startswith("win"):
        try:
            asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
        except Exception:
            pass

    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    app = build_app()
    print("✅ Copier running… ضيف البوت Admin في الجروبين وابعت رسالة في جروب المصدر")

    try:
        loop.run_until_complete(app.initialize())
        # مهم: إلغاء أي Webhook قبل الـ polling لتفادي Conflict
        loop.run_until_complete(app.bot.delete_webhook(drop_pending_updates=True))
        loop.run_until_complete(app.start())
        loop.run_until_complete(app.updater.start_polling())
        loop.run_forever()
    except KeyboardInterrupt:
        pass
    finally:
        loop.run_until_complete(app.updater.stop())
        loop.run_until_complete(app.stop())
        loop.run_until_complete(app.shutdown())
        loop.close()

