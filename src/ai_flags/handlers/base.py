"""Base handler interface."""

from abc import ABC, abstractmethod


class FlagHandler(ABC):
    """Base class for all flag handlers."""

    @abstractmethod
    def get_content(self, permission_mode: str | None = None) -> str:
        """Get the context content for this flag.

        Args:
            permission_mode: Optional permission mode (e.g., "plan")

        Returns:
            The context content (without XML wrapper)
        """
        pass

    @abstractmethod
    def get_xml_tag(self) -> str:
        """Get the XML tag name for this flag's content.

        Returns:
            Tag name without angle brackets (e.g., "subagent_delegation")
        """
        pass

    @property
    @abstractmethod
    def flag_letter(self) -> str:
        """Return the single-letter flag identifier."""
        pass
