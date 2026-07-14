import json
from pathlib import Path
from typing import Any
from pymongo import MongoClient
from datetime import datetime

OUTPUT_DIR = Path(__file__).resolve().parent
client = MongoClient("mongodb://localhost:27017/")
db = client["KnowledgeExtractor"]
default_values = {
    "is_processed": False,
    "date": datetime.now(),
}


def save_json(data: Any, filename: str = "workflow_result.json") -> Path:
    output_path = OUTPUT_DIR / filename
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    return output_path


def save_db(data: Any) -> Path:
    collection = db["articles"]
    final_document = {**default_values, **data.dict()}
    
    collection.insert_one(final_document)  # Convert Pydantic model to dictionary before inserting
    return data
