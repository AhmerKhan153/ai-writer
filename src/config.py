from datetime import datetime
import os

from dotenv import load_dotenv

DEFAULT_LLM_MODEL = "qwen3:4b"
MONGODB_URI = "mongodb://localhost:27017/"
MONGODB_DB_NAME = "KnowledgeExtractor"

DEFAULT_VALUES = {
    "is_processed": False,
    "date": datetime.now(),
}

load_dotenv()
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN") or os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID") or os.getenv("CHAT_ID")
BOT_TOKEN = TELEGRAM_BOT_TOKEN

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

TOPIC_EXTRACTION_PROMPT_TEMPLATE = "Write a concise topic summary for the article titled '{title}'.\n\n{content}"
