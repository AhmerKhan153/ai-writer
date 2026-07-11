from typing import Dict, Any


class ReviewingWorkflow:
    def review(self, draft: Dict[str, Any]) -> Dict[str, Any]:
        return {"approved": True, "draft": draft}
