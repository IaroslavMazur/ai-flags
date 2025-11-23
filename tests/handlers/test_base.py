"""Tests for base handler interface."""

import pytest
from ai_flags.handlers.base import FlagHandler


class TestFlagHandler:
    """Test FlagHandler abstract base class."""

    def test_cannot_instantiate_abstract_class(self):
        """Should not be able to instantiate FlagHandler directly."""
        with pytest.raises(TypeError):
            FlagHandler()  # pyright: ignore[reportAbstractUsage]

    def test_requires_implementation(self):
        """Concrete handlers must implement all abstract methods."""

        # Create incomplete handler that only implements some methods
        class IncompleteHandler(FlagHandler):
            @property
            def flag_letter(self) -> str:
                return "x"

        with pytest.raises(TypeError):
            IncompleteHandler()  # pyright: ignore[reportAbstractUsage]

    def test_complete_implementation_works(self):
        """Handler with all methods implemented should instantiate."""

        class CompleteHandler(FlagHandler):
            @property
            def flag_letter(self) -> str:
                return "x"

            def get_xml_tag(self) -> str:
                return "test_tag"

            def get_content(self, permission_mode: str | None = None) -> str:
                return "test content"

        # Should not raise
        handler = CompleteHandler()
        assert handler.flag_letter == "x"
        assert handler.get_xml_tag() == "test_tag"
        assert handler.get_content() == "test content"

    def test_interface_methods_exist(self):
        """Verify the abstract interface defines expected methods."""
        # Check that the abstract class has the expected abstract methods
        abstract_methods = FlagHandler.__abstractmethods__
        assert "get_content" in abstract_methods
        assert "get_xml_tag" in abstract_methods
        assert "flag_letter" in abstract_methods
