"""Handler for -d (debug) flag."""

from ai_flags.handlers.base import FlagHandler

DEFAULT_CONTENT = (
    "IMPORTANT: Use the Task tool to invoke the debugger subagent "
    "for systematic root cause analysis. The debugger will:\n"
    "1. Capture error messages and stack traces\n"
    "2. Identify reproduction steps\n"
    "3. Isolate the failure location\n"
    "4. Implement minimal fix\n"
    "5. Verify solution works"
)


class DebugHandler(FlagHandler):
    """Handler for -d flag: Invoke debugger agent for root cause analysis."""

    def __init__(self, content: str | None = None):
        """Initialize with optional custom content."""
        self._custom_content = content

    @property
    def flag_letter(self) -> str:
        return "d"

    def get_xml_tag(self) -> str:
        return "debug_instructions"

    def get_content(self, permission_mode: str | None = None) -> str:
        """Return debug instructions."""
        return self._custom_content if self._custom_content else DEFAULT_CONTENT
