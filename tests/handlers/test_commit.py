"""Tests for commit handler."""

from ai_flags.handlers.commit import CommitHandler


class TestCommitHandler:
    """Test CommitHandler for -c flag."""

    def test_flag_letter(self):
        """Should return 'c'."""
        handler = CommitHandler()
        assert handler.flag_letter == "c"

    def test_xml_tag(self):
        """Should return 'commit_instructions'."""
        handler = CommitHandler()
        assert handler.get_xml_tag() == "commit_instructions"

    def test_default_content(self):
        """Should return commit instructions."""
        handler = CommitHandler()
        content = handler.get_content()
        assert len(content) > 0
        # Verify references from original tests
        assert "SlashCommand" in content or "/commit" in content

    def test_default_content_references_slash_command(self):
        """Should mention the SlashCommand tool."""
        handler = CommitHandler()
        content = handler.get_content()
        assert "SlashCommand tool" in content

    def test_default_content_references_commit_command(self):
        """Should reference the /commit command."""
        handler = CommitHandler()
        content = handler.get_content()
        assert "/commit" in content

    def test_default_content_references_git(self):
        """Should reference git commit."""
        handler = CommitHandler()
        content = handler.get_content()
        assert "git commit" in content

    def test_custom_content(self):
        """Should use custom content when provided."""
        custom = "Custom commit message"
        handler = CommitHandler(content=custom)
        assert handler.get_content() == custom

    def test_permission_mode_ignored(self):
        """Should work regardless of permission mode."""
        handler = CommitHandler()
        content_none = handler.get_content(permission_mode=None)
        content_plan = handler.get_content(permission_mode="plan")
        content_normal = handler.get_content(permission_mode="normal")

        assert content_none == content_plan == content_normal
        assert len(content_none) > 0

    def test_custom_content_permission_mode_ignored(self):
        """Custom content should also ignore permission mode."""
        custom = "Custom instructions"
        handler = CommitHandler(content=custom)

        assert handler.get_content(permission_mode=None) == custom
        assert handler.get_content(permission_mode="plan") == custom
        assert handler.get_content(permission_mode="auto") == custom
