import argparse
import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent
SRC_DIR = ROOT_DIR / "src"
for path in (ROOT_DIR, SRC_DIR):
    path_str = str(path)
    if path_str not in sys.path:
        sys.path.insert(0, path_str)

from graphs.workflow import graph
from shared.save import save_json

import asyncio

from apscheduler.schedulers.asyncio import AsyncIOScheduler

from telegram.ext import (
    Application,
    CallbackQueryHandler
)

from config import TELEGRAM_BOT_TOKEN

from scheduler.jobs import fetch_news_job

from integration.telegram_handler import callback_handler
from integration.telegram_bot import send_draft


async def main():
    app = Application.builder().token(TELEGRAM_BOT_TOKEN).build()

    app.add_handler(
        CallbackQueryHandler(callback_handler)
    )

    scheduler = AsyncIOScheduler()

    scheduler.add_job(
        fetch_news_job,
        "interval",
        minutes=1
    )

    scheduler.start()

    print("Bot running...")

    await app.initialize()
    await app.start()

    try:
        await send_draft(
            post_id=999,
            content=(
                "🧪 Startup test message\n\n"
                "This is a dummy Telegram test from the AI Writer bot.\n"
                "Please tap one of the buttons to verify callbacks."
            ),
        )
        print("Test message sent to Telegram.")
    except Exception as exc:
        print(f"Failed to send startup test message: {exc}")

    await app.updater.start_polling()

    while True:
        await asyncio.sleep(3600)



    # parser = argparse.ArgumentParser(description="Run the AI Writer workflow.")
    # parser.add_argument("--save", action="store_true", help="Save workflow output to output/workflow_result.json")
    # args = parser.parse_args()

    # result = graph.invoke({"provider": "hackernews"})

    # print(result.get("selected_story"))
    # print("\nGenerated LinkedIn post on topic:\n")
    # print(result.get("published") or result.get("post"))
    # print("\nProcess completed.")

    # if args.save:
    #     path = save_json(result, "workflow_result.json")
    #     print(f"Saved workflow output to {path}")


if __name__ == "__main__":
    asyncio.run(main())
    