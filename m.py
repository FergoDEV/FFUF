from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder, CommandHandler, MessageHandler,
    ContextTypes, filters, ConversationHandler
)

ADMINS = [6290847497]  # O'zingizning Telegram ID
ADMINS = [7781534875]  # O'zingizning Telegram ID
ADD_ADMIN, BUYURTMA = range(2)

def admin_check(user_id):
    return user_id in ADMINS

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    tugmalar = [["📦 Mahsulotlar", "📝 Buyurtma berish"],
                ["📍 Manzil", "📞 Bog‘lanish", "🔩 Santexnika", "💡Dusel"]]
    if admin_check(user_id):
        tugmalar.append(["⚙️ Admin panel"])
    markup = ReplyKeyboardMarkup(tugmalar, resize_keyboard=True)
    await update.message.reply_text("Assalomu alaykum! Qurilish Market botiga xush kelibsiz.", reply_markup=markup)

async def tugma_javobi(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    user_id = update.message.from_user.id

    if text == "📦 Mahsulotlar":
        await update.message.reply_text(
            "📦 Mahsulotlar:\n🧱 G‘isht – 1200 so‘m\n🪨 Sement – 30 000\n🏗 Qum – 25 000\n🎨 Kraska – 70 000\n🧴 Ko‘pik – 35 000")
    elif text == "🔩 Santexnika":
        await update.message.reply_text("🔩 Atvot 20 – 1000\nAtvot 25 – 2000\nPol Atvot 20 – 1000")
    elif text == "💡Dusel":
        await update.message.reply_text("💡 Dusel lampalar:\n7W - 7 000\n10W - 10 000\n... va hokazo")
    elif text == "📍 Manzil":
        await update.message.reply_text("📍 Manzil: Marg‘ilon, Toshloq tumani, VARZAK FAYZ 777")
    elif text == "📞 Bog‘lanish":
        await update.message.reply_text("☎️ +998 91 283 81 43")
    elif text == "⚙️ Admin panel" and admin_check(user_id):
        markup = ReplyKeyboardMarkup([["➕ Admin qo‘shish"], ["⬅️ Orqaga"]], resize_keyboard=True)
        await update.message.reply_text("Admin panel:", reply_markup=markup)
    elif text == "⬅️ Orqaga":
        await start(update, context)
    elif text == "📝 Buyurtma berish":
        await update.message.reply_text("📲 Telefon raqamingiz va mahsulot nomini yozing:")
        return BUYURTMA

    return ConversationHandler.END

async def qabul_buyurtma(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    user_id = update.message.from_user.id
    for admin_id in ADMINS:
        try:
            await context.bot.send_message(chat_id=admin_id, text=f"🆕 Buyurtma:\n{text}\n🆔 {user_id}")
        except:
            pass
    await update.message.reply_text("✅ Buyurtma qabul qilindi. Tez orada siz bilan bog‘lanamiz.")
    return ConversationHandler.END

async def admin_panel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not admin_check(update.message.from_user.id):
        await update.message.reply_text("⛔ Sizda ruxsat yo‘q.")
        return ConversationHandler.END
    await update.message.reply_text("🆔 Yangi adminning ID raqamini yuboring:")
    return ADD_ADMIN

async def add_admin(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        new_admin_id = int(update.message.text)
        if new_admin_id not in ADMINS:
            ADMINS.append(new_admin_id)
            await update.message.reply_text(f"✅ Admin qo‘shildi: {new_admin_id}")
        else:
            await update.message.reply_text("⚠️ Bu foydalanuvchi allaqachon admin.")
    except ValueError:
        await update.message.reply_text("❌ Faqat ID raqamini yuboring.")
    return ConversationHandler.END

# Main
app = ApplicationBuilder().token("8068283579:AAE8mEogFjOPIdxUnQcQwizznZRjvrPsW2c").build()

app.add_handler(CommandHandler("start", start))

app.add_handler(ConversationHandler(
    entry_points=[MessageHandler(filters.TEXT & filters.Regex("^➕ Admin qo‘shish$"), admin_panel)],
    states={ADD_ADMIN: [MessageHandler(filters.TEXT, add_admin)]},
    fallbacks=[MessageHandler(filters.TEXT & filters.Regex("^⬅️ Orqaga$"), tugma_javobi)]
))

app.add_handler(ConversationHandler(
    entry_points=[MessageHandler(filters.TEXT & filters.Regex("^📝 Buyurtma berish$"), tugma_javobi)],
    states={BUYURTMA: [MessageHandler(filters.TEXT, qabul_buyurtma)]},
    fallbacks=[]
))

app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, tugma_javobi))

app.run_polling()
