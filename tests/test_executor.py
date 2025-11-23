"""Tests for flag handler execution."""

from ai_flags.executor import execute_flag_handlers, wrap_in_xml_tag
from ai_flags.handlers.base import FlagHandler


# Mock handler for testing
class MockHandler(FlagHandler):
    """Mock flag handler for testing."""

    def __init__(self, letter: str, tag: str, content: str, permission_mode: str | None = None):
        self._letter = letter
        self._tag = tag
        self._content = content
        self._required_permission = permission_mode

    @property
    def flag_letter(self) -> str:
        return self._letter

    def get_xml_tag(self) -> str:
        return self._tag

    def get_content(self, permission_mode: str | None = None) -> str:
        # If handler requires specific permission mode, only return content if mode matches
        if self._required_permission and permission_mode != self._required_permission:
            return ""
        return self._content


class TestWrapInXmlTag:
    """Test wrap_in_xml_tag() function."""

    def test_simple_tag(self) -> None:
        """Test wrapping content with a simple tag."""
        result = wrap_in_xml_tag("test", "content")
        assert result == "<test>\ncontent\n</test>"

    def test_multiline_content(self) -> None:
        """Test wrapping multiline content."""
        content = "line 1\nline 2\nline 3"
        result = wrap_in_xml_tag("instructions", content)
        assert result == "<instructions>\nline 1\nline 2\nline 3\n</instructions>"

    def test_empty_content(self) -> None:
        """Test wrapping empty content."""
        result = wrap_in_xml_tag("empty", "")
        assert result == "<empty>\n\n</empty>"

    def test_content_with_special_characters(self) -> None:
        """Test wrapping content with special characters."""
        content = "IMPORTANT: Use the /commit command"
        result = wrap_in_xml_tag("commit_instructions", content)
        assert (
            result
            == "<commit_instructions>\nIMPORTANT: Use the /commit command\n</commit_instructions>"
        )

    def test_tag_with_underscores(self) -> None:
        """Test tag names with underscores."""
        result = wrap_in_xml_tag("no_lint_instructions", "Don't lint")
        assert result == "<no_lint_instructions>\nDon't lint\n</no_lint_instructions>"

    def test_content_with_xml_characters(self) -> None:
        """Test content containing XML-like characters."""
        content = "Use <tag> and </tag> syntax"
        result = wrap_in_xml_tag("example", content)
        assert result == "<example>\nUse <tag> and </tag> syntax\n</example>"


class TestExecuteFlagHandlers:
    """Test execute_flag_handlers() function."""

    def test_single_flag(self) -> None:
        """Test executing a single flag handler."""
        handlers = {"c": MockHandler("c", "commit_instructions", "Commit content")}
        flags = ["c"]

        result = execute_flag_handlers(flags, handlers, "plan")

        assert "<commit_instructions>" in result
        assert "</commit_instructions>" in result
        assert "Commit content" in result

    def test_multiple_flags(self) -> None:
        """Test executing multiple flag handlers."""
        handlers = {
            "c": MockHandler("c", "commit_instructions", "Commit content"),
            "t": MockHandler("t", "test_instructions", "Test content"),
        }
        flags = ["c", "t"]

        result = execute_flag_handlers(flags, handlers, "plan")

        assert "<commit_instructions>" in result
        assert "Commit content" in result
        assert "</commit_instructions>" in result
        assert "<test_instructions>" in result
        assert "Test content" in result
        assert "</test_instructions>" in result

    def test_all_flags(self) -> None:
        """Test executing all flag handlers."""
        handlers = {
            "s": MockHandler("s", "subagent_delegation", "Subagent content"),
            "c": MockHandler("c", "commit_instructions", "Commit content"),
            "t": MockHandler("t", "test_instructions", "Test content"),
            "d": MockHandler("d", "debug_instructions", "Debug content"),
            "n": MockHandler("n", "no_lint_instructions", "No lint content"),
        }
        flags = ["s", "c", "t", "d", "n"]

        result = execute_flag_handlers(flags, handlers, "plan")

        # All five tags should be present
        assert "<subagent_delegation>" in result
        assert "Subagent content" in result
        assert "<commit_instructions>" in result
        assert "Commit content" in result
        assert "<test_instructions>" in result
        assert "Test content" in result
        assert "<debug_instructions>" in result
        assert "Debug content" in result
        assert "<no_lint_instructions>" in result
        assert "No lint content" in result

    def test_empty_flags(self) -> None:
        """Test executing with no flags."""
        handlers = {
            "c": MockHandler("c", "commit_instructions", "Commit content"),
        }
        flags: list[str] = []

        result = execute_flag_handlers(flags, handlers, "plan")

        assert result == ""

    def test_unknown_flag_skipped(self) -> None:
        """Test that unknown flags are gracefully skipped."""
        handlers = {
            "c": MockHandler("c", "commit_instructions", "Commit content"),
        }
        flags = ["c", "x"]  # x is unknown

        result = execute_flag_handlers(flags, handlers, "plan")

        # Only the c flag should be processed
        assert "<commit_instructions>" in result
        assert "Commit content" in result
        # x flag should not produce any output
        assert result.count("<") == 2  # Only opening and closing for commit

    def test_xml_wrapping_structure(self) -> None:
        """Test that all contexts are properly XML-wrapped."""
        handlers = {
            "c": MockHandler("c", "commit_instructions", "Commit content"),
            "t": MockHandler("t", "test_instructions", "Test content"),
            "d": MockHandler("d", "debug_instructions", "Debug content"),
        }
        flags = ["c", "t", "d"]

        result = execute_flag_handlers(flags, handlers, "plan")

        # Each context should have both opening and closing tags
        assert result.count("<commit_instructions>") == 1
        assert result.count("</commit_instructions>") == 1
        assert result.count("<test_instructions>") == 1
        assert result.count("</test_instructions>") == 1
        assert result.count("<debug_instructions>") == 1
        assert result.count("</debug_instructions>") == 1

    def test_permission_mode_filtering(self) -> None:
        """Test that -s flag is only processed in plan mode."""
        handlers = {
            "s": MockHandler("s", "subagent_delegation", "Subagent content", "plan"),
            "c": MockHandler("c", "commit_instructions", "Commit content"),
        }
        flags = ["s", "c"]

        # Without plan mode, -s should be skipped
        result_no_plan = execute_flag_handlers(flags, handlers, None)
        assert "<subagent_delegation>" not in result_no_plan
        assert "<commit_instructions>" in result_no_plan

        # With plan mode, -s should be included
        result_with_plan = execute_flag_handlers(flags, handlers, "plan")
        assert "<subagent_delegation>" in result_with_plan
        assert "<commit_instructions>" in result_with_plan

    def test_empty_content_not_added(self) -> None:
        """Test that handlers returning empty content are not added to output."""
        handlers = {
            "c": MockHandler("c", "commit_instructions", ""),  # Empty content
            "t": MockHandler("t", "test_instructions", "Test content"),
        }
        flags = ["c", "t"]

        result = execute_flag_handlers(flags, handlers, "plan")

        # Empty content should not create XML tags
        assert "<commit_instructions>" not in result
        # Only test instructions should be present
        assert "<test_instructions>" in result
        assert "Test content" in result

    def test_contexts_joined_with_newline(self) -> None:
        """Test that multiple contexts are joined with newlines."""
        handlers = {
            "c": MockHandler("c", "commit_instructions", "Commit"),
            "t": MockHandler("t", "test_instructions", "Test"),
        }
        flags = ["c", "t"]

        result = execute_flag_handlers(flags, handlers, "plan")

        # Should have newline between contexts
        lines = result.split("\n")
        # Format: <tag1>, content1, </tag1>, <tag2>, content2, </tag2>
        assert len(lines) == 6
        assert lines[0] == "<commit_instructions>"
        assert lines[1] == "Commit"
        assert lines[2] == "</commit_instructions>"
        assert lines[3] == "<test_instructions>"
        assert lines[4] == "Test"
        assert lines[5] == "</test_instructions>"
