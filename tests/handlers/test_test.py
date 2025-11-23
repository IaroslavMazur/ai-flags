"""Tests for test handler."""

from ai_flags.handlers.test import CoverageHandler


class TestCoverageHandler:
    """Test CoverageHandler for -t flag."""

    def test_flag_letter(self):
        """Should return 't'."""
        handler = CoverageHandler()
        assert handler.flag_letter == "t"

    def test_xml_tag(self):
        """Should return 'test_instructions'."""
        handler = CoverageHandler()
        assert handler.get_xml_tag() == "test_instructions"

    def test_default_content(self):
        """Should return testing instructions."""
        handler = CoverageHandler()
        content = handler.get_content()
        assert len(content) > 0
        # Verify test-related keywords from original tests
        assert "test coverage" in content.lower()

    def test_default_content_mentions_unit_tests(self):
        """Should mention unit tests."""
        handler = CoverageHandler()
        content = handler.get_content()
        assert "unit tests" in content.lower()

    def test_default_content_mentions_integration_tests(self):
        """Should mention integration tests."""
        handler = CoverageHandler()
        content = handler.get_content()
        assert "integration tests" in content.lower()

    def test_default_content_mentions_comprehensive_coverage(self):
        """Should emphasize comprehensive test coverage."""
        handler = CoverageHandler()
        content = handler.get_content()
        assert "comprehensive" in content.lower()
        assert "coverage" in content.lower()

    def test_custom_content(self):
        """Should use custom content when provided."""
        custom = "Custom test requirements"
        handler = CoverageHandler(content=custom)
        assert handler.get_content() == custom

    def test_permission_mode_ignored(self):
        """Should work regardless of permission mode."""
        handler = CoverageHandler()
        content_none = handler.get_content(permission_mode=None)
        content_plan = handler.get_content(permission_mode="plan")
        content_normal = handler.get_content(permission_mode="normal")

        assert content_none == content_plan == content_normal
        assert len(content_none) > 0

    def test_custom_content_permission_mode_ignored(self):
        """Custom content should also ignore permission mode."""
        custom = "Write tests for everything"
        handler = CoverageHandler(content=custom)

        assert handler.get_content(permission_mode=None) == custom
        assert handler.get_content(permission_mode="plan") == custom
        assert handler.get_content(permission_mode="disabled") == custom
