from typing import Dict, Any

from shared.save import save_json


class PublishingWorkflow:
    def publish(self, review_result: Dict[str, Any]) -> Dict[str, Any]:
        payload = {
            "published": True,
            "review_result": review_result,
        }
        path = save_json(payload, filename="workflow_result.json")
        return {
            "published": True,
            "saved_path": str(path),
            "review_result": review_result,
        }
