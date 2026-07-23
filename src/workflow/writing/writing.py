from src.workflow.post_writer import create_post


class WritingWorkflow:
    def write(self, prompt: str, is_rewrite: bool = False) -> str:
        """Return the LinkedIn post body as plain text."""
        return create_post(prompt, is_rewrite=is_rewrite)