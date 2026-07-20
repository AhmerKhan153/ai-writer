import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
SRC_DIR = REPO_ROOT / "src"

for path in (REPO_ROOT, SRC_DIR):
    path_str = str(path)
    if path_str not in sys.path:
        sys.path.insert(0, path_str)

from src.integration.telegram_bot import send_draft


async def fetch_news_job():

    print("Fetching news...")

    # fake AI output
    post = """
🚀 New LinkedIn Draft

Why developers over-engineer microservices...

Lorem ipsum...

Approve?
"""

    await send_draft(
        post_id=42,
        content=post
    )