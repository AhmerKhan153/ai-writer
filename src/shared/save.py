import json
from pathlib import Path
from typing import Any
from pymongo import MongoClient

from config import DEFAULT_VALUES, MONGODB_DB_NAME, MONGODB_URI

OUTPUT_DIR = Path(__file__).resolve().parent.parent / "output"
client = MongoClient(MONGODB_URI)
db = client[MONGODB_DB_NAME]

default_values = DEFAULT_VALUES

def save_json(data: Any, filename: str = "workflow_result.json") -> Path:
    output_path = OUTPUT_DIR / filename
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    return output_path


def save_db(data: Any) -> Any:
    try:
        collection = db["articles"]
        final_document = {**default_values, **data.dict()}
        collection.insert_one(final_document)
        return data
    except Exception as e:
        print(f"Error saving to database: {e}")
        raise
