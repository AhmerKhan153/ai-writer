from typing import Any, Dict

from workflow.post_writer import create_post


class WritingWorkflow:
    def write(self, prompt: str) -> Dict[str, Any]:
        response = create_post(prompt)
        if hasattr(response, "dict"):
            response = response.dict()
        return response if isinstance(response, dict) else {"draft": response}
