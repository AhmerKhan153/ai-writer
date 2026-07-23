"""File-based save helpers.

Draft persistence and lifecycle now live in src/repository/draft_repository.py
(MongoDB). This module only keeps the JSON dump used by the publishing node for
local artifacts/debugging.
"""

import json
from pathlib import Path
from typing import Any

OUTPUT_DIR = Path(__file__).resolve().parent.parent / "output"


def save_json(data: Any, filename: str = "workflow_result.json") -> Path:
    output_path = OUTPUT_DIR / filename
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    return output_path
