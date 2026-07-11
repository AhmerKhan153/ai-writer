import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent
SRC_DIR = ROOT_DIR / "src"
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from src.workflow.publishing.publishing import PublishingWorkflow


def test_publishing_workflow_saves_json(tmp_path):
    from pathlib import Path

    original_data = {"approved": True, "draft": {"draft": "Test draft"}}
    workflow = PublishingWorkflow()
    result = workflow.publish(original_data)

    assert result["published"] is True
    assert "saved_path" in result
    assert Path(result["saved_path"]).exists()
