

    # Update like count and respond
    if likes_given_api > 0:
        command_count["total"] += 1
        if likes_given_api > 90:
            command_count["over_90"] += 1
            user_like_count[user_id] += 1
        response_text = (
            f"✅ *لایک با موفقیت دریافت شد.* ✅\n\n"
            f"👤 *اسم:* {player_nickname}\n"
            f"♨️ *لایک ها قبل:* {likes_before}\n"
            f"🚀 *لایک ها بعد:* {likes_after}\n"
            f"🎁 *تعداد اضافه شده:* {likes_given_api}\n\n"
            f"ℹ️ مالک و پشتیبانی: @imwrathbad. 💝\n\n"
            f"🚀 لینک چنل تلگرام مون: @ffwrathbad. 🔥"
        )

    elif status == 2 or likes_given_api == 0:
        command_count["max_reached"] += 1
        response_text = (
            f"⚠️ هنوز ۲۴ ساعت تمام نشده. \n\n"
            f"👤 *اسم:* {player_nickname}\n"
            f"🔘 *لایک ها فعلی:* {likes_after}\n\n"
            "ℹ️ لطفا بعد از کامل شدن ۲۴ ساعت دوباره سعی کنید."
        )
    else:
        response_text = "❌ *خطا:* مشکلی پیش آمد. لطفاً UID را بررسی کنید و دوباره امتحان کنید"

    try:
        await progress_msg.edit_text(response_text, parse_mode="Markdown")
    except Exception:
        await progress_msg.delete()
        await update.message.reply_text(response_text)

async def count(update: Update, context: CallbackContext):
    response = (
        f"📊 *Total Usage Stats:*\n\n"
        f"✅ *Total Likes Given:* {command_count['total']}\n"
        f"💯 *90+ Likes Given:* {command_count['over_90']}\n"
        f"❌ *Max Like Reached:* {command_count['max_reached']}"
    )
    await update.message.reply_text(response, parse_mode="Markdown")

async def reset_count(update: Update, context: CallbackContext):
    if update.effective_user.id != ADMIN_USER_ID:
        await update.message.reply_text("❌ *شما مجاز به تنظیم مجدد شمارش نیستید.*", parse_mode="Markdown")
        return
    
    command_count["total"] = 0
    command_count["over_90"] = 0
    command_count["max_reached"] = 0
    user_like_count.clear()
    await update.message.reply_text("✅ *تعداد استفاده بازنشانی شده است.*", parse_mode="Markdown")

# Add command handlers
app.add_handler(CommandHandler("like", like))
app.add_handler(CommandHandler("count", count))
app.add_handler(CommandHandler("resetcount", reset_count))

# Run the bot
if __name__ == "__main__":
    print("Bot is running...")
    app.run_polling()