"""MongoDB-backed draft repository.

The Mongo `status` field is the single source of truth for a draft's lifecycle:

    sourced  -> a story was picked from a provider (no draft yet)
    drafted  -> an LLM draft exists, awaiting your Telegram approval
    approved -> you approved it; the publish job will post it
    posted   -> published to LinkedIn
    rejected -> you rejected it

Telegram callbacks carry the string _id, so state survives restarts and multiple.
"""

from datetime import datetime
from typing import Any, Dict, List, Optional

from bson import ObjectId
from pymongo import MongoClient

from config import (
    ARTICLES_COLLECTION,
    MONGODB_DB_NAME,
    MONGODB_URI,
    STATUS_APPROVED,
    STATUS_DRAFTED,
    STATUS_SOURCED,
)

_client = MongoClient(MONGODB_URI)
_collection = _client[MONGODB_DB_NAME][ARTICLES_COLLECTION]


def _now() -> datetime:
    return datetime.now()


def insert_sourced(story: Dict[str, Any]) -> str:
    """Persist a freshly sourced story and return its id as a string."""
    doc = {
        "title": story.get("title"),
        "url": story.get("url"),
        "score": story.get("score"),
        "draft": None,
        "status": STATUS_SOURCED,
        "created_at": _now(),
        "updated_at": _now(),
        "posted_at": None,
        "linkedin_url": None,
    }
    result = _collection.insert_one(doc)
    return str(result.inserted_id)


def attach_draft(draft_id: str, draft_text: str) -> None:
    """Store a generated draft and move the record to `drafted`."""
    _collection.update_one(
        {"_id": ObjectId(draft_id)},
        {"$set": {"draft": draft_text, "status": STATUS_DRAFTED, "updated_at": _now()}},
    )


def set_status(draft_id: str, status: str, **extra: Any) -> None:
    """Update a record's status (plus any extra fields, e.g. linkedin_url)."""
    fields = {"status": status, "updated_at": _now(), **extra}
    _collection.update_one({"_id": ObjectId(draft_id)}, {"$set": fields})


def get(draft_id: str) -> Optional[Dict[str, Any]]:
    doc = _collection.find_one({"_id": ObjectId(draft_id)})
    if doc is not None:
        doc["id"] = str(doc["_id"])
    return doc


def find_by_status(status: str) -> List[Dict[str, Any]]:
    docs = list(_collection.find({"status": status}).sort("created_at", 1))
    for doc in docs:
        doc["id"] = str(doc["_id"])
    return docs


def find_approved() -> List[Dict[str, Any]]:
    return find_by_status(STATUS_APPROVED)
