import json
from pathlib import Path
from typing import Any
from pymongo import MongoClient

OUTPUT_DIR = Path(__file__).resolve().parent.parent / "output"
client = MongoClient("mongodb://localhost:27017/")
db = client["KnowledgeExtractor"]

def save_json(data: Any, filename: str = "workflow_result.json") -> Path:
    output_path = OUTPUT_DIR / filename
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    return output_path


def save_db(data: Any) -> Any:
    collection = db["articles"]
    final_document = {**data.dict()} if hasattr(data, "dict") else {**data}
    collection.insert_one(final_document)
    return data
