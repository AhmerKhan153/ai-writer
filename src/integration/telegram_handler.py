"""Telegram callback dispatch — the human-in-the-loop orchestrator.

Callback data is "<action>:<draft_id>". Each action does one chunk of work using
the Mongo record identified by draft_id, then stops:

    pick     -> run fetch->write subgraph, store draft, send it for approval
    approve  -> mark approved (publish job will post it)
    reject   -> mark rejected
    rewrite  -> regenerate the draft from a different angle, resend
"""

import asyncio

from telegram import Update
from telegram.ext import ContextTypes

from workflow.content_graph import generate_draft
from integration.telegram_bot import send_draft
from repository import draft_repository
from config import STATUS_APPROVED, STATUS_REJECTED


async def _draft_and_send(draft_id: str, title: str, url: str, is_rewrite: bool) -> None:
    """Generate a draft off the event loop, persist it, and send it for review."""
    draft = await asyncio.to_thread(generate_draft, title, url, is_rewrite)
    await asyncio.to_thread(draft_repository.attach_draft, draft_id, draft)
    await send_draft(draft_id, draft)


async def callback_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if not query.data or ":" not in query.data:
        return

    action, draft_id = query.data.split(":", 1)
    record = draft_repository.get(draft_id)
    if record is None:
        await query.edit_message_text("This item is no longer available.")
        return

    if action == "pick":
        title = record.get("title") or ""
        await query.edit_message_text(f"✅ Selected: {title}\n\nWriting a draft...")
        await _draft_and_send(draft_id, title, record.get("url"), is_rewrite=False)

    elif action == "approve":
        draft_repository.set_status(draft_id, STATUS_APPROVED)
        await query.edit_message_text("✅ Approved — queued for LinkedIn.")

    elif action == "reject":
        draft_repository.set_status(draft_id, STATUS_REJECTED)
        await query.edit_message_text("❌ Rejected.")

    elif action == "rewrite":
        await query.edit_message_text("✍️ Rewriting from a different angle...")
        await _draft_and_send(
            draft_id, record.get("title") or "", record.get("url"), is_rewrite=True
        )
