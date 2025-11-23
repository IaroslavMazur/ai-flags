"""Flag parsing logic."""

import re


def parse_trailing_flags(prompt: str) -> tuple[str, list[str]] | None:
    """Parse trailing flags from prompt.

    Args:
        prompt: User prompt potentially ending with flags like "task -s -c"

    Returns:
        Tuple of (cleaned_prompt, list_of_flags) if flags found, None otherwise.
        Example: ("task", ["s", "c"]) for "task -s -c"
    """
    # Match: anything followed by one or more -X flags at the end
    # Pattern: (.*?) captures main prompt, ((?:-[a-z]\s*)+) captures flags
    pattern = r"^(.*?)\s+((?:-[a-z]\s*)+)$"
    match = re.match(pattern, prompt.strip(), re.DOTALL)

    if not match:
        return None

    clean_prompt = match.group(1).strip()
    flags_str = match.group(2).strip()

    # Extract individual flag letters: "-s -c" -> ["s", "c"]
    flags = [flag.strip("-") for flag in flags_str.split() if flag.startswith("-")]

    return (clean_prompt, flags)
