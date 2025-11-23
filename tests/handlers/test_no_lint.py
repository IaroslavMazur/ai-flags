"""Tests for no-lint handler."""

from ai_flags.handlers.no_lint import NoLintHandler


class TestNoLintHandler:
    """Test NoLintHandler for -n flag."""

    def test_flag_letter(self):
        """Should return 'n'."""
        handler = NoLintHandler()
        assert handler.flag_letter == "n"

    def test_xml_tag(self):
        """Should return 'no_lint_instructions'."""
        handler = NoLintHandler()
        assert handler.get_xml_tag() == "no_lint_instructions"

    def test_default_content(self):
        """Should return no-lint instructions."""
        handler = NoLintHandler()
        content = handler.get_content()
        assert len(content) > 0
        # Verify mentions skipping validation from original tests
        assert "Do not lint" in content or "lint" in content.lower()

    def test_default_content_mentions_type_checking(self):
        """Should mention skipping type checking."""
        handler = NoLintHandler()
        content = handler.get_content()
        assert "type-check" in content.lower() or "type check" in content.lower()

    def test_default_content_mentions_validation_tools(self):
        """Should mention skipping validation tools."""
        handler = NoLintHandler()
        content = handler.get_content()
        assert "validation tools" in content.lower()

    def test_default_content_emphasizes_do_not_lint(self):
        """Should explicitly say 'Do not lint'."""
        handler = NoLintHandler()
        content = handler.get_content()
        assert "Do not lint" in content

    def test_default_content_mentions_skipping_checks(self):
        """Should mention skipping various code quality checks."""
        handler = NoLintHandler()
        content = handler.get_content()
        content_lower = content.lower()
        assert "skip" in content_lower or "do not" in content_lower
        # Should mention linters, type checkers, formatters, etc.
        assert "lint" in content_lower
        assert "type" in content_lower

    def test_custom_content(self):
        """Should use custom content when provided."""
        custom = "Custom no-lint behavior"
        handler = NoLintHandler(content=custom)
        assert handler.get_content() == custom

    def test_permission_mode_ignored(self):
        """Should work regardless of permission mode."""
        handler = NoLintHandler()
        content_none = handler.get_content(permission_mode=None)
        content_plan = handler.get_content(permission_mode="plan")
        content_normal = handler.get_content(permission_mode="normal")

        assert content_none == content_plan == content_normal
        assert len(content_none) > 0

    def test_custom_content_permission_mode_ignored(self):
        """Custom content should also ignore permission mode."""
        custom = "Skip all checks for speed"
        handler = NoLintHandler(content=custom)

        assert handler.get_content(permission_mode=None) == custom
        assert handler.get_content(permission_mode="plan") == custom
        assert handler.get_content(permission_mode="disabled") == custom
