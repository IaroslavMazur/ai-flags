"""Handler for -c (commit) flag."""

from ai_flags.handlers.base import FlagHandler

DEFAULT_CONTENT = (
    "IMPORTANT: After completing your task, use the SlashCommand tool "
    "to execute the '/commit' slash command to create a git commit."
)


class CommitHandler(FlagHandler):
    """Handler for -c flag: Instruct Claude to execute /commit."""

    def __init__(self, content: str | None = None):
        """Initialize with optional custom content."""
        self._custom_content = content

    @property
    def flag_letter(self) -> str:
        return "c"

    def get_xml_tag(self) -> str:
        return "commit_instructions"

    def get_content(self, permission_mode: str | None = None) -> str:
        """Return commit instructions."""
        return self._custom_content if self._custom_content else DEFAULT_CONTENT
