import logging
import aiohttp
from telegram import Update, Chat, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackContext
import html

# Bot Token
API_TOKEN = '8078028361:AAEMZhEuc3H92sz9339OeLfRTYDDm1eeBKw'

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize bot
app = Application.builder().token(API_TOKEN).build()

# Command usage tracking and user management
command_count = {"total": 0, "over_90": 0, "max_reached": 0}
user_like_count = {}  # To track likes per user

# Admin user ID
ADMIN_USER_ID = 1873527787

async def is_subscribed(user_id):
    try:
        # Check channel subscription
        channel_status = await app.bot.get_chat_member(chat_id="@ffwrathbad", user_id=user_id)
        # Check group subscription
        group_status = await app.bot.get_chat_member(chat_id="@wrathbadgap", user_id=user_id)
        return channel_status.status in ["member", "administrator", "creator"] and group_status.status in ["member", "administrator", "creator"]
    except Exception as e:
        logger.exception("بررسی اشتراک ناموفق بود")
        return False

async def like(update: Update, context: CallbackContext):
    user_id = update.effective_user.id
    
    # Private chat restriction
    if update.effective_chat.type == Chat.PRIVATE:
        if not await is_subscribed(user_id):
            keyboard = [
                [InlineKeyboardButton("در کانال عضو شوید", url="https://t.me/ffwrathbad")],
                [InlineKeyboardButton("در گروه عضو شوید", url="https://t.me/wrathbadgap")]
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            await update.message.reply_text(
                "❌ برای ادامه لایک در پیام خصوصی باید به آنها بپیوندید:",
                reply_markup=reply_markup
            )
            return

    # Initialize user like count if not present
    if user_id not in user_like_count:
        user_like_count[user_id] = 0

    # Enforce 2-like limit
    if user_like_count[user_id] >= 1:
        if not await is_subscribed(user_id):
            keyboard = [
                [InlineKeyboardButton("عضو کانال شوید", url="https://t.me/FFWRATHBAd")],
                [InlineKeyboardButton("عضو گروه شوید", url="https://t.me/wrathbadgap")]
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            await update.message.reply_text(
                "برای استفاده از ربات در چنل و گروه زیر عضو شو\n,
                reply_markup=reply_markup
            )
            return

    # Check if UID is provided
    if not context.args:
        await update.message.reply_text("❌ *خطا:* ایدی تون را وارد کنید.\n\nℹ️ *نمونه* `/like 12345678`", parse_mode="Markdown")
        return

    uid = context.args[0]
    if not uid.isdigit():
        await update.message.reply_text("❌ *خطا:* ایدی اشتباه است.", parse_mode="Markdown")
        return

    progress_msg = await update.message.reply_text("Got Your Request. Please Wait...")
    api_url = f"https://community-ffbd.up.railway.app/getlikes?key={key}&uid={uid}"
    
    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(api_url) as resp:
                data = await resp.json()
        except Exception as e:
            logger.exception("API call failed")
            await progress_msg.edit_text("❌ *خطا:* عملیات ربات به دلیل نگهداری API موقتاً متوقف شده است.", parse_mode="Markdown")
            return

    # Extract API response fields
    status = data.get("status")
    likes_given_api = data.get("LikesGivenByAPI", 0)
    likes_after = data.get("LikesafterCommand")
    likes_before = data.get("LikesbeforeCommand")
    player_nickname = data.get("PlayerNickname", "Unknown")

    # Escape special characters for Telegram
    player_nickname = html.escape(player_nickname)