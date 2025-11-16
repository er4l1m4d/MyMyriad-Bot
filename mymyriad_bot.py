import logging
import requests
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

# --- Configuration ---
TELEGRAM_BOT_TOKEN = 'my bot API key' # Make sure your token is still here
# The CORRECT API endpoint and parameters discovered
MYRIAD_API_URL = 'https://api.polkamarkets.com/markets'
API_PARAMS = {'state': 'open', 'slug': 'myriad'}
HEADERS = {'User-Agent': 'MyMyriadBot/0.2'}

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# --- Command Handlers ---
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Sends a welcome message."""
    user = update.effective_user
    welcome_message = (
        f"👋 Hello, {user.first_name}!\n\n"
        "Welcome to MyMyriad, your personal assistant for Myriad Markets.\n\n"
        "The connection is now working! Use the /markets command to see the latest active markets.\n\n"
        "Type /help to see all available commands."
    )
    await update.message.reply_text(welcome_message)

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Sends a list of available commands."""
    help_text = (
        "Here are the commands you can use:\n\n"
        "/start - Welcome message\n"
        "/help - Shows this help message\n"
        "/markets - View the top 5 active markets"
    )
    await update.message.reply_text(help_text)

async def markets(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Fetches and displays active markets from the Myriad API."""
    await update.message.reply_text("Fetching the latest markets, please wait...")

    try:
        # Make the API request with confirmed working settings
        response = requests.get(MYRIAD_API_URL, params=API_PARAMS, headers=HEADERS, timeout=15)
        response.raise_for_status()  # Raise an exception for bad status codes

        markets_data = response.json()

        if not markets_data:
            await update.message.reply_text("Couldn't find any active markets right now.")
            return

        # Format the message using Markdown
        message = "🔥 *Top 5 Active Markets on Myriad:*\n\n"
        for market in markets_data[:5]:
            # Use .get() for safety in case a key is missing
            title = market.get('title', 'No Title').strip()
            outcomes = ", ".join(market.get('answers', ['Yes', 'No']))
            
            message += f"➡️ *{title}*\n"
            message += f"   _Options: {outcomes}_\n\n"

        await update.message.reply_text(message, parse_mode='Markdown')

    except requests.exceptions.RequestException as e:
        logger.error(f"API request failed: {e}")
        await update.message.reply_text("Sorry, I couldn't connect to the Myriad Markets API. Please try again later.")
    except Exception as e:
        logger.error(f"An unexpected error occurred: {e}")
        await update.message.reply_text("An unexpected error occurred. Please try again.")

# --- Main Bot Logic ---
def main() -> None:
    """Start the bot."""
    application = Application.builder().token(TELEGRAM_BOT_TOKEN).build()

    # Register the command handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("markets", markets))

    # Start the Bot
    logger.info("Starting bot...")
    application.run_polling()

if __name__ == '__main__':
    main()