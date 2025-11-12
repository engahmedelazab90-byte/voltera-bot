# copier_second.py — ينسخ الرسائل من جروب مصدر لعدة جروبات هدف (بوت تاني)
# متوافق مع python-telegram-bot==21.6 و Python 3.14 على ويندوز

import sys, asyncio
from telegram import Update
from telegram.ext import Application, MessageHandler, CommandHandler, ContextTypes, filters

# ======= عدّل ده بس =======
BOT_TOKEN = "حط_هنا_توكن_البوت_التاني_بين_علامتين"  # مثال: "82685...:AAE..."
# ==========================

# جروب المصدر (المرسِل)
SOURCE_CHAT_ID = -1002307891907

# الجروبات المستلِمة (المرسَل إليها)
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

# ترويسة لتمييز البوت التاني (اختياري)
SHOW_PREFIX = True
PREFIX_TEXT = "【via Copier #2】"

# أمر /id للمساعدة
async def cmd_id(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat = update.effective_chat
    if update.effective_message:
        await update.effective_message.reply_text(f"chat_id: {chat.id}\nchat_type: {chat.type}")

# يبعت الرسالة لكل الجروبات الهدف (نسخ كامل يحافظ على الميديا والفورمات)
async def send_to_targets(context: ContextTypes.DEFAULT_TYPE, msg):
    for target in TARGET_CHAT_IDS:
        if target == SOURCE_CHAT_ID:
            continue
        try:
            if SHOW_PREFIX and PREFIX_TEXT:
                await context.bot.send_message(chat_id=target, text=PREFIX_TEXT)

            await context.bot.copy_message(
                chat_id=target,
                from_chat_id=SOURCE_CHAT_ID,
                message_id=msg.message_id,
                protect_content=False
            )
            print(f"[OK] Copied {msg.message_id} → {target}")
        except Exception as e:
            print(f"[ERR] copy to {target}: {e}")

# الهاندلر الأساسي: يلتقط رسائل المصدر وينسخها
async def copier(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat = update.effective_chat
    msg  = update.effective_message

    # تجاهل تحديثات مالهاش رسالة (انضمام/مغادرة... إلخ)
    if not msg or not chat:
        return

    # اشتغل فقط داخل جروب المصدر
    if chat.id != SOURCE_CHAT_ID:
        return

    # تجاهل الأوامر
    if msg.text and msg.text.startswith("/"):
        return

    await send_to_targets(context, msg)

def build_app() -> Application:
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("id", cmd_id))
    # ALL بدون StatusUpdate عشان نتجنب NoneType errors
    app.add_handler(MessageHandler((filters.ALL & ~filters.StatusUpdate.ALL), copier))
    return app

if __name__ == "__main__":
    # إصلاح الـ event loop على ويندوز
    if sys.platform.startswith("win"):
        try:
            asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
        except Exception:
            pass

    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    app = build_app()
    print(f"✅ Copier #2 running… SOURCE: {SOURCE_CHAT_ID} → TARGETS: {TARGET_CHAT_IDS}")
    print("تأكد إن البوت Admin في جروب المصدر وكل جروبات الهدف / Privacy: Disable")

    try:
        # تهيئة وإلغاء أي Webhook لتفادي Conflict
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
