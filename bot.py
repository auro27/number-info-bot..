#!/usr/bin/env python3

import os
import requests
import json
import logging
import traceback
from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    filters,
    ContextTypes
)
from telegram.error import TelegramError

# ==================== CONFIG ====================
# Token ONLY from environment variable (Railway / Koyeb / GitHub Secrets)
BOT_TOKEN = os.environ.get("BOT_TOKEN")
API_URL = "https://sarkariupdate.online/darkhosting/DarkCore/DarkApiX.php"
# ================================================

logging.basicConfig(
    format="%(asctime)s - %(levelname)s - %(message)s",
    level=logging.INFO
)
logger = logging.getLogger(__name__)


def get_number_info(number: str):
    try:
        url = f"{API_URL}?api=num_to_info&q={number}"
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        }
        response = requests.get(url, headers=headers, timeout=20)
        if response.status_code == 200:
            data = response.json()
            if data.get("status") == "success":
                return data
        return None
    except Exception as e:
        logger.error(f"API Error: {e}")
        return None


def clean_and_limit(data: dict):
    if not data:
        return data
    if "count" in data:
        del data["count"]
    if "data" in data and isinstance(data["data"], list):
        data["data"] = data["data"][:12]
        for record in data["data"]:
            for key in ["oid", "id"]:
                if key in record:
                    del record[key]
    return data


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        await update.message.reply_text(
            "💀 NUMBER INFO BOT\n\n"
            "10 digit number bhejo.\n"
            "Example: 9876543210"
        )
    except Exception as e:
        logger.error(f"Start error: {e}")


async def handle_number(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        text = update.message.text.strip()
        number = text.replace(" ", "").replace("+91", "").replace("-", "")

        if not number.isdigit() or len(number) != 10:
            await update.message.reply_text("❌ Sirf 10 digit number bhejo!")
            return

        msg = await update.message.reply_text("⏳ Searching...")
        data = get_number_info(number)

        if not data:
            await msg.edit_text("❌ No data found!")
            return

        data = clean_and_limit(data)
        result = json.dumps(data, indent=2, ensure_ascii=False)

        if len(result) > 3800:
            result = result[:3800] + "\n... (truncated)"

        try:
            await msg.edit_text(f"```json\n{result}\n```", parse_mode="Markdown")
        except TelegramError:
            await msg.edit_text(result[:4000])

    except Exception as e:
        logger.error(f"Handler error: {e}\n{traceback.format_exc()}")
        try:
            await update.message.reply_text("⚠️ Error aaya, phir try karo.")
        except Exception:
            pass


async def error_handler(update: object, context: ContextTypes.DEFAULT_TYPE):
    logger.error(f"Global error: {context.error}")


def main():
    if not BOT_TOKEN:
        logger.error("❌ BOT_TOKEN environment variable nahi mili!")
        logger.error("Railway/Koyeb pe Variables mein BOT_TOKEN add karo.")
        return

    app = (
        Application.builder()
        .token(BOT_TOKEN)
        .connect_timeout(30.0)
        .read_timeout(30.0)
        .write_timeout(30.0)
        .pool_timeout(30.0)
        .build()
    )

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_number))
    app.add_error_handler(error_handler)

    logger.info("💀 NUMBER INFO BOT started")
    app.run_polling(drop_pending_updates=True, allowed_updates=["message"])


if __name__ == "__main__":
    main()
