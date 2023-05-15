from logging import DEBUG, basicConfig
from os import getenv

from dotenv import load_dotenv
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ConversationHandler, ContextTypes, MessageHandler
from telegram.ext.filters import COMMAND, TEXT

from chat import (get_custom_prompt, initial_message, next_message, remove_custom_prompt, remove_prompt,
                  reset_conversation, store_custom_prompt)
from user_filer import user_filter

INPUT_PROMPT_STATE, = range(1)


def main() -> None:
    load_dotenv()
    basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=DEBUG)
    bot = ApplicationBuilder().token(getenv("BOT_TOKEN")).build()
    bot.add_handler(CommandHandler("start", start, user_filter))
    bot.add_handler(CommandHandler("restart", restart, user_filter))
    bot.add_handler(prompt_set_handler())
    bot.add_handler(CommandHandler("promptreset", prompt_reset, user_filter))
    bot.add_handler(CommandHandler("promptget", prompt_get, user_filter))
    bot.add_handler(CommandHandler("promptremove", prompt_remove, user_filter))
    bot.add_handler(CommandHandler("cancel", cancel, user_filter))
    bot.add_handler(MessageHandler(user_filter & TEXT & ~COMMAND, talk))
    bot.run_polling()


async def start(update: Update, _: ContextTypes.DEFAULT_TYPE) -> None:
    message = initial_message(update.effective_chat.id)
    await update.message.reply_text(message)


async def restart(update: Update, _: ContextTypes.DEFAULT_TYPE) -> None:
    reset_conversation(update.effective_chat.id)
    await update.message.reply_text("Conversation restarted.")


def prompt_set_handler() -> ConversationHandler:
    entry_handler = CommandHandler("promptset", prompt_set)
    new_prompt_handler = MessageHandler(user_filter & TEXT & ~COMMAND, handle_new_prompt)
    cancel_handler = CommandHandler("cancel", cancel_prompt_set, user_filter)
    return ConversationHandler(
        entry_points=[entry_handler],
        states={INPUT_PROMPT_STATE: [new_prompt_handler, cancel_handler]},
        fallbacks=[cancel_handler]
    )


async def prompt_set(update: Update, _: ContextTypes.DEFAULT_TYPE) -> int:
    await update.message.reply_text("Input new prompt, or /cancel:")
    return INPUT_PROMPT_STATE


async def handle_new_prompt(update: Update, _: ContextTypes.DEFAULT_TYPE) -> int:
    new_prompt = update.message.text
    store_custom_prompt(update.effective_chat.id, new_prompt)
    await update.message.reply_text(f"Prompt set to: {new_prompt}")
    return ConversationHandler.END


async def cancel_prompt_set(update: Update, _: ContextTypes.DEFAULT_TYPE) -> int:
    await update.message.reply_text("Prompt not changed.")
    return ConversationHandler.END


async def prompt_reset(update: Update, _: ContextTypes.DEFAULT_TYPE) -> None:
    chat_id = update.effective_chat.id
    reset_conversation(chat_id)
    remove_custom_prompt(chat_id)
    await update.message.reply_text("Prompt reset.")


async def prompt_get(update: Update, _: ContextTypes.DEFAULT_TYPE) -> None:
    custom_prompt = get_custom_prompt(update.effective_chat.id)
    response = f"Prompt set to: {custom_prompt}" if custom_prompt else "No custom prompt configured."
    await update.message.reply_text(response)


async def prompt_remove(update: Update, _: ContextTypes.DEFAULT_TYPE) -> None:
    chat_id = update.effective_chat.id
    reset_conversation(chat_id)
    remove_prompt(chat_id)
    await update.message.reply_text("Prompt removed.")


async def cancel(update: Update, _: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("No operation to cancel.")


async def talk(update: Update, _: ContextTypes.DEFAULT_TYPE) -> None:
    response = next_message(update.effective_chat.id, update.message.text)
    await update.message.reply_text(response)


if __name__ == "__main__":
    main()
