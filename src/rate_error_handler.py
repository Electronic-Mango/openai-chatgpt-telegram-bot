from openai.error import RateLimitError
from telegram.ext import ContextTypes

from chat import RATE_LIMIT_MESSAGE


async def rate_error_handler(update: object, context: ContextTypes.DEFAULT_TYPE) -> None:
    error = context.error
    message = RATE_LIMIT_MESSAGE if isinstance(error, RateLimitError) else error
    await context.bot.send_message(update.effective_chat.id, message)
