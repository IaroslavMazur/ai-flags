"""Flag handler execution and context building."""

from collections.abc import Mapping

from ai_flags.handlers.base import FlagHandler


def wrap_in_xml_tag(tag: str, content: str) -> str:
    """Wrap content in XML tags.

    Args:
        tag: The XML tag name (without angle brackets)
        content: The content to wrap

    Returns:
        Content wrapped in <tag>content</tag> format
    """
    return f"<{tag}>\n{content}\n</{tag}>"


def execute_flag_handlers(
    flags: list[str],
    handlers: Mapping[str, FlagHandler],
    permission_mode: str | None = None,
) -> str:
    """Execute handlers for each flag and build combined XML context.

    Args:
        flags: List of flag letters
        handlers: Dict mapping flag letter to handler instance
        permission_mode: Optional permission mode (e.g., "plan")

    Returns:
        Combined XML context string
    """
    contexts = []

    for flag in flags:
        # Skip -s flag if not in plan mode
        if flag == "s" and permission_mode != "plan":
            continue

        handler = handlers.get(flag)
        if handler:
            content = handler.get_content(permission_mode)
            if content:  # Only add non-empty content
                tag = handler.get_xml_tag()
                wrapped = wrap_in_xml_tag(tag, content)
                contexts.append(wrapped)

    return "\n".join(contexts)
