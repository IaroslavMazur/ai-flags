"""Tests for debug handler."""

from ai_flags.handlers.debug import DebugHandler


class TestDebugHandler:
    """Test DebugHandler for -d flag."""

    def test_flag_letter(self):
        """Should return 'd'."""
        handler = DebugHandler()
        assert handler.flag_letter == "d"

    def test_xml_tag(self):
        """Should return 'debug_instructions'."""
        handler = DebugHandler()
        assert handler.get_xml_tag() == "debug_instructions"

    def test_default_content(self):
        """Should return debug instructions."""
        handler = DebugHandler()
        content = handler.get_content()
        assert len(content) > 0
        # Verify debug-related keywords from original tests
        assert "debugger subagent" in content.lower()

    def test_default_content_references_task_tool(self):
        """Should mention the Task tool."""
        handler = DebugHandler()
        content = handler.get_content()
        assert "Task tool" in content

    def test_default_content_mentions_root_cause_analysis(self):
        """Should mention root cause analysis."""
        handler = DebugHandler()
        content = handler.get_content()
        assert "root cause analysis" in content.lower()

    def test_default_content_has_systematic_process(self):
        """Should outline a systematic debugging process."""
        handler = DebugHandler()
        content = handler.get_content()
        # Should mention steps like capture, identify, isolate, fix, verify
        content_lower = content.lower()
        assert "error" in content_lower or "stack trace" in content_lower
        assert "fix" in content_lower
        assert "verify" in content_lower

    def test_custom_content(self):
        """Should use custom content when provided."""
        custom = "Custom debug workflow"
        handler = DebugHandler(content=custom)
        assert handler.get_content() == custom

    def test_permission_mode_ignored(self):
        """Should work regardless of permission mode."""
        handler = DebugHandler()
        content_none = handler.get_content(permission_mode=None)
        content_plan = handler.get_content(permission_mode="plan")
        content_normal = handler.get_content(permission_mode="normal")

        assert content_none == content_plan == content_normal
        assert len(content_none) > 0

    def test_custom_content_permission_mode_ignored(self):
        """Custom content should also ignore permission mode."""
        custom = "Debug everything thoroughly"
        handler = DebugHandler(content=custom)

        assert handler.get_content(permission_mode=None) == custom
        assert handler.get_content(permission_mode="plan") == custom
        assert handler.get_content(permission_mode="auto") == custom
