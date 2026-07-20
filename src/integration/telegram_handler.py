from telegram import Update
from telegram.ext import ContextTypes


async def callback_handler(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
):

    query = update.callback_query

    await query.answer()

    if not query.data:
        return

    action, post_id = query.data.split(":", 1)

    if action == "approve":

        print(f"Publishing {post_id}")

        await query.edit_message_text(
            f"✅ Post {post_id} published."
        )

    elif action == "reject":

        print(f"Rejected {post_id}")

        await query.edit_message_text(
            f"❌ Post {post_id} rejected."
        )

    elif action == "rewrite":

        print(f"Rewrite {post_id}")

        await query.edit_message_text(
            f"✍️ Rewriting post {post_id}..."
        )

    elif action == "story_select":
        choice = int(post_id)
        from integration.telegram_state import get_pending_selection, set_selected_story

        pending = get_pending_selection()
        stories = pending.stories if pending is not None else []
        if 0 < choice <= len(stories):
            selected_story = stories[choice - 1]
            if isinstance(selected_story, dict):
                title = selected_story.get("Title") or selected_story.get("title")
                url = selected_story.get("url") or selected_story.get("URL")
            else:
                title = getattr(selected_story, "Title", None) or str(selected_story)
                url = getattr(selected_story, "url", None) or getattr(selected_story, "URL", None)
            await query.edit_message_text(
                f"✅ Selected: {title}\n\nProceeding with the workflow..."
            )
            set_selected_story({"approved": True, "title": title, "url": url})
        else:
            await query.edit_message_text("❌ Selection cancelled.")
            set_selected_story({"approved": False})
