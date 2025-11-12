# copier_second_noprefix.py — نسخ من جروب مصدر لعدة جروبات هدف بدون أي ترويسة
# python-telegram-bot==21.6

import sys, asyncio
from telegram import Update
from telegram.ext import Application, MessageHandler, CommandHandler, ContextTypes, filters

# ===== عدّل التوكن فقط =====
BOT_TOKEN = "8063429512:AAHx-cLSOvW7sIGh_CJMNBSw8ZywWrIj00k"
# ===========================

# جروب المصدر
SOURCE_CHAT_ID = -1002307891907

# الجروبات المستلمة
TARGET_CHAT_IDS = [
    -1001877613633,
    -1001831208064,
    -1003122776203,
    -1002243512135,
    -1001945968861,
    -1002381368613,
    -1002308429112,
    -1001816602568,
    -1002400046352,
    -1001518389308,
    -1002741628383,
    -1001988599283,
    -1001605571320,
    -1002378030426,
]

async def cmd_id(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat = update.effective_chat
    if update.effective_message:
        await update.effective_message.reply_text(f"chat_id: {chat.id}\nchat_type: {chat.type}")

async def copier(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat = update.effective_chat
    msg  = update.effective_message
    if not msg or not chat:
        return
    if chat.id != SOURCE_CHAT_ID:
        return
    # تجاهل الأوامر
    if msg.text and msg.text.startswith("/"):
        return

    # نسخ كما هي (يحافظ على الميديا والفورمات – وبدون أي ترويسة)
    for target in TARGET_CHAT_IDS:
        if target == SOURCE_CHAT_ID:
            continue
        try:
            await context.bot.copy_message(
                chat_id=target,
                from_chat_id=SOURCE_CHAT_ID,
                message_id=msg.message_id,
                protect_content=False
            )
        except Exception as e:
            print(f"[ERR] copy to {target}: {e}")

def build_app() -> Application:
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("id", cmd_id))
    app.add_handler(MessageHandler((filters.ALL & ~filters.StatusUpdate.ALL), copier))
    return app

if name == "__main__":
    # إصلاح الـ event loop على ويندوز
    if sys.platform.startswith("win"):
        try:
            asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
        except Exception:
            pass

    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    app = build_app()
    print(f"✅ Copier #2 (no prefix) running… SOURCE: {SOURCE_CHAT_ID} → TARGETS: {TARGET_CHAT_IDS}")

    try:
        loop.run_until_complete(app.initialize())
        loop.run_until_complete(app.bot.delete_webhook(drop_pending_updates=True))
        loop.run_until_complete(app.start())
        loop.run_until_complete(app.updater.start_polling())
        loop.run_forever()
    except KeyboardInterrupt:
        pass
    finally:
        try:
            loop.run_until_complete(app.updater.stop())
            loop.run_until_complete(app.stop())
            loop.run_until_complete(app.shutdown())
        finally:
            loop.close()
