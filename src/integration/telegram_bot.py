from telegram import (
    Bot,
    InlineKeyboardButton,
    InlineKeyboardMarkup
)

try:
    from src.config import BOT_TOKEN, CHAT_ID
except ImportError:  # pragma: no cover - fallback for direct script execution
    from config import BOT_TOKEN, CHAT_ID

bot = None
chat_id = CHAT_ID


def _get_bot() -> Bot:
    global bot
    if bot is None:
        if not BOT_TOKEN:
            raise RuntimeError(
                "Telegram bot token is not configured. Set TELEGRAM_BOT_TOKEN or BOT_TOKEN."
            )
        bot = Bot(BOT_TOKEN)
    return bot


async def send_text_message(content: str, reply_markup=None):
    if not chat_id:
        raise RuntimeError(
            "Telegram chat ID is not configured. Set TELEGRAM_CHAT_ID or CHAT_ID."
        )

    await _get_bot().send_message(
        chat_id=chat_id,
        text=content,
        reply_markup=reply_markup,
    )


async def send_draft(post_id: int, content: str):

    keyboard = [
        [
            InlineKeyboardButton(
                "Approve",
                callback_data=f"approve:{post_id}"
            ),
            InlineKeyboardButton(
                "Reject",
                callback_data=f"reject:{post_id}"
            ),
        ],
        [
            InlineKeyboardButton(
                "Rewrite",
                callback_data=f"rewrite:{post_id}"
            )
        ]
    ]

    markup = InlineKeyboardMarkup(keyboard)

    await send_text_message(content=content, reply_markup=markup)


async def send_story_selection(stories: list, post_id: int = 1000):
    keyboard = []
    row = []
    for index, story in enumerate(stories, start=1):
        title = getattr(story, "Title", None)
        if title is None and isinstance(story, dict):
            title = story.get("Title") or story.get("title")
        label = f"{index}. {title or 'Story'}"
        row.append(
            InlineKeyboardButton(
                label,
                callback_data=f"story_select:{index}"
            )
        )
        if len(row) == 2:
            keyboard.append(row)
            row = []

    if row:
        keyboard.append(row)

    keyboard.append([
        InlineKeyboardButton("Reject", callback_data=f"story_select:0")
    ])

    content = "Choose a story to continue the workflow:\n\n"
    for index, story in enumerate(stories, start=1):
        title = getattr(story, "Title", None)
        if title is None and isinstance(story, dict):
            title = story.get("Title") or story.get("title")
        content += f"{index}. {title or str(story)}\n"

    await send_text_message(
        content=content,
        reply_markup=InlineKeyboardMarkup(keyboard),
    )