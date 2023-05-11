from logging import INFO, basicConfig
from os import getenv

from dotenv import load_dotenv
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, MessageHandler, filters

from chat import (get_custom_prompt, initial_message, next_message, remove_custom_prompt, remove_prompt,
                  reset_conversation, store_custom_prompt)
from rate_error_handler import rate_error_handler

load_dotenv()

TOKEN = getenv("BOT_TOKEN")

basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=INFO)


def main() -> None:
    application = ApplicationBuilder().token(TOKEN).build()

    start_handler = CommandHandler("start", start)
    application.add_handler(start_handler)

    talk_handler = MessageHandler(filters.TEXT & (~filters.COMMAND), talk)
    application.add_handler(talk_handler)

    reset_handler = CommandHandler("reset", reset)
    application.add_handler(reset_handler)

    prompt_set_handler = CommandHandler("promptset", prompt_set)
    application.add_handler(prompt_set_handler)

    prompt_reset_handler = CommandHandler("promptreset", prompt_reset)
    application.add_handler(prompt_reset_handler)

    prompt_get_handler = CommandHandler("promptget", prompt_get)
    application.add_handler(prompt_get_handler)

    prompt_remove_handler = CommandHandler("promptremove", prompt_remove)
    application.add_handler(prompt_remove_handler)

    application.add_error_handler(rate_error_handler)

    application.run_polling()


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    chat_id = update.effective_chat.id
    message = initial_message(chat_id)
    await context.bot.send_message(chat_id=chat_id, text=message)


async def talk(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    chat_id = update.effective_chat.id
    response = next_message(chat_id, update.message.text)
    await context.bot.send_message(chat_id=chat_id, text=response)


async def reset(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    chat_id = update.effective_chat.id
    reset_conversation(chat_id)
    await context.bot.send_message(chat_id=chat_id, text="Conversation restarted.")
    await start(update, context)


async def prompt_set(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    chat_id = update.effective_chat.id
    reset_conversation(chat_id)
    new_prompt = " ".join(context.args)
    store_custom_prompt(chat_id, new_prompt)
    await context.bot.send_message(chat_id=chat_id, text=f"Prompt set to: **{new_prompt}**")


async def prompt_reset(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    chat_id = update.effective_chat.id
    reset_conversation(chat_id)
    remove_custom_prompt(chat_id)
    await context.bot.send_message(chat_id=chat_id, text="Prompt reset.")


async def prompt_get(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    chat_id = update.effective_chat.id
    custom_prompt = get_custom_prompt(chat_id)
    response = f"Prompt set to: **{custom_prompt}**" if custom_prompt else "No custom prompt configured."
    await context.bot.send_message(chat_id=chat_id, text=response)


async def prompt_remove(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    chat_id = update.effective_chat.id
    reset_conversation(chat_id)
    remove_prompt(chat_id)
    await context.bot.send_message(chat_id=chat_id, text="Prompt removed.")


if __name__ == "__main__":
    main()
