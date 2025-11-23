"""Handler for -n (no-lint) flag."""

from ai_flags.handlers.base import FlagHandler

DEFAULT_CONTENT = (
    "IMPORTANT: Do not lint or type-check your code changes. "
    "Skip running any validation tools (linters, type checkers, formatters, etc.). "
    "Even if other instructions mention code quality checks, ignore them for this task. "
    "Prioritize implementation speed over correctness."
)


class NoLintHandler(FlagHandler):
    """Handler for -n flag: Disable linting and type-checking."""

    def __init__(self, content: str | None = None):
        """Initialize with optional custom content."""
        self._custom_content = content

    @property
    def flag_letter(self) -> str:
        return "n"

    def get_xml_tag(self) -> str:
        return "no_lint_instructions"

    def get_content(self, permission_mode: str | None = None) -> str:
        """Return no-lint instructions."""
        return self._custom_content if self._custom_content else DEFAULT_CONTENT
