import asyncio
from dataclasses import dataclass, field
from typing import Any, Optional


@dataclass
class PendingSelection:
    stories: list[Any]
    event: asyncio.Event = field(default_factory=asyncio.Event)
    selected_story: Optional[dict[str, Any]] = None


_pending_selection: Optional[PendingSelection] = None


def create_pending_selection(stories: list[Any]) -> PendingSelection:
    global _pending_selection
    _pending_selection = PendingSelection(stories=stories)
    return _pending_selection


def clear_pending_selection() -> None:
    global _pending_selection
    _pending_selection = None


def get_pending_selection() -> Optional[PendingSelection]:
    return _pending_selection


def set_selected_story(selected_story: dict[str, Any]) -> None:
    global _pending_selection
    if _pending_selection is not None:
        _pending_selection.selected_story = selected_story
        _pending_selection.event.set()
