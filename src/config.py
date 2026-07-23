from datetime import datetime
import os

from dotenv import load_dotenv

load_dotenv()

# --- LLM selection ---------------------------------------------------------
# LLM_PROVIDER: "ollama" (default, local) or "claude" (Anthropic API).
# Switching is a single env var; get_chat_model() in src/llm.py reads these.
LLM_PROVIDER = (os.getenv("LLM_PROVIDER") or "ollama").lower()
DEFAULT_LLM_MODEL = os.getenv("OLLAMA_MODEL") or "qwen3:4b"
CLAUDE_MODEL = os.getenv("CLAUDE_MODEL") or "claude-opus-4-8"

# --- Storage ---------------------------------------------------------------
MONGODB_URI = os.getenv("MONGODB_URI") or "mongodb://localhost:27017/"
MONGODB_DB_NAME = os.getenv("MONGODB_DB_NAME") or "KnowledgeExtractor"
ARTICLES_COLLECTION = "articles"

# Draft lifecycle statuses (Mongo `status` field is the source of truth).
STATUS_SOURCED = "sourced"    # story picked from a provider, no draft yet
STATUS_DRAFTED = "drafted"    # LLM draft generated, awaiting your approval
STATUS_APPROVED = "approved"  # you approved it; queued for LinkedIn
STATUS_POSTED = "posted"      # published to LinkedIn
STATUS_REJECTED = "rejected"  # you rejected it

# --- Telegram --------------------------------------------------------------
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN") or os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID") or os.getenv("CHAT_ID")
BOT_TOKEN = TELEGRAM_BOT_TOKEN

# --- LinkedIn --------------------------------------------------------------
LINKEDIN_ACCESS_TOKEN = os.getenv("LINKEDIN_ACCESS_TOKEN")
LINKEDIN_AUTHOR_URN = os.getenv("LINKEDIN_AUTHOR_URN")  # e.g. "urn:li:person:xxxx"

POST_WRITING_PROMPT_TEMPLATE = """You are a respected software architect, writer, blogger, podcaster.

Create a Knowledge base.

Topic: {topic}

Rules:
- Maximum 150-250 words
- Professional and practical tone
- Human-like style
- Contrarian if possible
- Avoid generic AI buzzwords
- Do not use emojis at the beginning of lines
- Do not use words like 'dive into,' 'delve,' 'The Truth?' or 'tapestry'
- Include discussion question at the end."""

TOPIC_ANALYSIS_PROMPT_TEMPLATE = """You are a principal architect.

These are current Hacker News discussions:

{text}

Identify:
1. Emerging themes
2. Under-discussed architecture topics
3. Contrarian viewpoints

Return 10 LinkedIn post ideas in structured JSON format.
"""

# Appended to the writing prompt when you tap "Rewrite" on a draft.
REWRITE_PROMPT_SUFFIX = (
    "\n\nThis is a rewrite request. Produce a distinctly different angle from the "
    "previous attempt: change the hook, restructure the argument, and vary the "
    "discussion question."
)

TOPIC_EXTRACTION_PROMPT_TEMPLATE = "Write a concise topic summary for the article titled '{title}'.\n\n{content}"
