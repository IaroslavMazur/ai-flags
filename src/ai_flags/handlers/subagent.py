"""Handler for -s (subagent) flag."""

from ai_flags.handlers.base import FlagHandler

DEFAULT_CONTENT = """After you come up with the implementation plan, consider how to split the work among parallel subagents using the Task tool:

- If the work can be fully parallelized (independent tasks with no dependencies), spawn multiple subagents in a single message with multiple Task tool calls
- If the work must be done sequentially (each step depends on the previous), spawn a single subagent for the entire workflow
- If you need to do some sequential work first before parallelizing, start with a subagent for that sequential portion, then spawn parallel subagents for the independent work afterwards

Delegate implementation details to subagents. Your role is to orchestrate, not implement directly."""


class SubagentHandler(FlagHandler):
    """Handler for -s flag: Append subagent orchestration instructions."""

    def __init__(self, content: str | None = None):
        """Initialize with optional custom content."""
        self._custom_content = content

    @property
    def flag_letter(self) -> str:
        return "s"

    def get_xml_tag(self) -> str:
        return "subagent_delegation"

    def get_content(self, permission_mode: str | None = None) -> str:
        """Return subagent delegation instructions.

        Note: Only active when permission_mode == "plan"
        """
        # Skip if not in plan mode
        if permission_mode != "plan":
            return ""

        return self._custom_content if self._custom_content else DEFAULT_CONTENT
