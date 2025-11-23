"""Output formatting for different modes."""

import json


def wrap_in_xml_tag(tag: str, content: str) -> str:
    """Wrap content in XML tags."""
    return f"<{tag}>\n{content}\n</{tag}>"


def format_hook_output(clean_prompt: str, flags: list[str], flag_contexts: str) -> str:
    """Format output for Claude Code hook (JSON).

    Args:
        clean_prompt: Prompt without flags
        flags: List of flag letters
        flag_contexts: Combined XML context from all flags

    Returns:
        JSON string with hookSpecificOutput structure
    """
    # Build metadata
    flags_str = " ".join(f"-{flag}" for flag in flags)
    metadata = (
        f"Note: Processed flags {flags_str}\nYour actual task (without flags): {clean_prompt}"
    )
    wrapped_metadata = wrap_in_xml_tag("flag_metadata", metadata)

    # Combine metadata + flag contexts
    parts = [wrapped_metadata]
    if flag_contexts:
        parts.append("")  # Blank line separator
        parts.append(flag_contexts)

    additional_context = "\n".join(parts)

    # Build hook output JSON
    output = {
        "hookSpecificOutput": {
            "hookEventName": "UserPromptSubmit",
            "additionalContext": additional_context,
        }
    }

    return json.dumps(output, indent=2)


def format_cli_output(prompt: str, flags: list[str], context: str) -> str:
    """Format output for CLI mode (plain text).

    Args:
        prompt: Cleaned prompt without flags
        flags: List of detected flags
        context: XML context that would be added

    Returns:
        Human-readable formatted text
    """
    flags_str = ", ".join(f"-{flag}" for flag in flags)

    parts = [
        f"Detected flags: {flags_str}",
        f"Cleaned prompt: {prompt}",
        "",
        "Context to be added:",
        context,
    ]

    return "\n".join(parts)
