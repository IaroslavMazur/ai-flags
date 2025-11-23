"""Handler for -t (test) flag."""

from ai_flags.handlers.base import FlagHandler

DEFAULT_CONTENT = (
    "IMPORTANT: Ensure comprehensive test coverage for this task. "
    "Include unit tests for core logic, integration tests for interactions, "
    "and edge case handling. Verify all tests pass before completing."
)


class CoverageHandler(FlagHandler):
    """Handler for -t flag: Add testing emphasis context."""

    def __init__(self, content: str | None = None):
        """Initialize with optional custom content."""
        self._custom_content = content

    @property
    def flag_letter(self) -> str:
        return "t"

    def get_xml_tag(self) -> str:
        return "test_instructions"

    def get_content(self, permission_mode: str | None = None) -> str:
        """Return testing instructions."""
        return self._custom_content if self._custom_content else DEFAULT_CONTENT
