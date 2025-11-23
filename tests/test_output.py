"""Tests for output formatting."""

import json

import pytest

from ai_flags.output import format_cli_output, format_hook_output


class TestFormatHookOutput:
    """Test format_hook_output() for hook mode."""

    def test_single_flag_context(self) -> None:
        """Test building output with single flag and context."""
        flags = ["c"]
        clean_prompt = "my task"
        flag_contexts = "<commit_instructions>Commit instruction</commit_instructions>"

        result = format_hook_output(clean_prompt, flags, flag_contexts)

        # Parse JSON to verify structure
        output = json.loads(result)
        context = output["hookSpecificOutput"]["additionalContext"]

        assert "<flag_metadata>" in context
        assert "</flag_metadata>" in context
        assert "Processed flags -c" in context
        assert "Your actual task (without flags): my task" in context
        assert "<commit_instructions>Commit instruction</commit_instructions>" in context

    def test_multiple_flags_multiple_contexts(self) -> None:
        """Test building output with multiple flags and contexts."""
        flags = ["c", "t"]
        clean_prompt = "my task"
        flag_contexts = (
            "<commit_instructions>Commit instruction</commit_instructions>\n"
            "<test_instructions>Test instruction</test_instructions>"
        )

        result = format_hook_output(clean_prompt, flags, flag_contexts)

        output = json.loads(result)
        context = output["hookSpecificOutput"]["additionalContext"]

        assert "<flag_metadata>" in context
        assert "Processed flags -c -t" in context
        assert "Your actual task (without flags): my task" in context
        assert "</flag_metadata>" in context
        assert "<commit_instructions>Commit instruction</commit_instructions>" in context
        assert "<test_instructions>Test instruction</test_instructions>" in context

    def test_empty_contexts(self) -> None:
        """Test building output with flags but no contexts."""
        flags = ["c"]
        clean_prompt = "my task"
        flag_contexts = ""

        result = format_hook_output(clean_prompt, flags, flag_contexts)

        output = json.loads(result)
        context = output["hookSpecificOutput"]["additionalContext"]

        assert "<flag_metadata>" in context
        assert "Processed flags -c" in context
        assert "Your actual task (without flags): my task" in context
        assert "</flag_metadata>" in context

    def test_output_formatting(self) -> None:
        """Test that output is properly formatted with newlines and XML structure."""
        flags = ["c", "t"]
        clean_prompt = "my task"
        flag_contexts = (
            "<commit_instructions>Context 1</commit_instructions>\n"
            "<test_instructions>Context 2</test_instructions>"
        )

        result = format_hook_output(clean_prompt, flags, flag_contexts)

        output = json.loads(result)
        context = output["hookSpecificOutput"]["additionalContext"]

        lines = context.split("\n")
        # Should have: <flag_metadata>, Note:, Your actual task:, </flag_metadata>, blank line, contexts
        assert "<flag_metadata>" in lines[0]
        assert "Note: Processed flags" in context
        assert "Your actual task" in context
        assert "</flag_metadata>" in context

    def test_metadata_wrapping(self) -> None:
        """Test that metadata is properly wrapped in XML tags."""
        flags = ["c"]
        clean_prompt = "implement feature"
        flag_contexts = "<commit_instructions>Test</commit_instructions>"

        result = format_hook_output(clean_prompt, flags, flag_contexts)

        output = json.loads(result)
        context = output["hookSpecificOutput"]["additionalContext"]

        # Extract the metadata section
        assert context.startswith("<flag_metadata>")
        metadata_end = context.index("</flag_metadata>")
        metadata_section = context[: metadata_end + len("</flag_metadata>")]

        assert "Note: Processed flags -c" in metadata_section
        assert "Your actual task (without flags): implement feature" in metadata_section

    def test_json_structure(self) -> None:
        """Output should be valid JSON with correct structure."""
        flags = ["c"]
        clean_prompt = "my task"
        flag_contexts = "<commit_instructions>Test</commit_instructions>"

        result = format_hook_output(clean_prompt, flags, flag_contexts)

        # Should be valid JSON
        output = json.loads(result)

        # Verify structure
        assert "hookSpecificOutput" in output
        assert "hookEventName" in output["hookSpecificOutput"]
        assert "additionalContext" in output["hookSpecificOutput"]
        assert output["hookSpecificOutput"]["hookEventName"] == "UserPromptSubmit"
        assert isinstance(output["hookSpecificOutput"]["additionalContext"], str)

    def test_all_flags_in_metadata(self) -> None:
        """Test that all flags are listed in metadata."""
        flags = ["s", "c", "t", "d", "n"]
        clean_prompt = "implement feature"
        flag_contexts = ""

        result = format_hook_output(clean_prompt, flags, flag_contexts)

        output = json.loads(result)
        context = output["hookSpecificOutput"]["additionalContext"]

        assert "Processed flags -s -c -t -d -n" in context

    def test_complex_prompt_preserved(self) -> None:
        """Test that complex prompts are preserved correctly."""
        flags = ["c"]
        clean_prompt = "Complex task:\n- Step 1\n- Step 2\n\nWith details"
        flag_contexts = "<commit_instructions>Test</commit_instructions>"

        result = format_hook_output(clean_prompt, flags, flag_contexts)

        output = json.loads(result)
        context = output["hookSpecificOutput"]["additionalContext"]

        assert "Complex task:\n- Step 1\n- Step 2\n\nWith details" in context

    def test_blank_line_separator(self) -> None:
        """Test that blank line separates metadata from flag contexts."""
        flags = ["c"]
        clean_prompt = "task"
        flag_contexts = "<commit_instructions>Test</commit_instructions>"

        result = format_hook_output(clean_prompt, flags, flag_contexts)

        output = json.loads(result)
        context = output["hookSpecificOutput"]["additionalContext"]

        # Should have blank line after metadata
        parts = context.split("\n\n")
        assert len(parts) >= 2
        assert "<flag_metadata>" in parts[0]
        assert "</flag_metadata>" in parts[0]


class TestFormatCliOutput:
    """Test format_cli_output() for CLI mode."""

    def test_formats_prompt_and_flags(self) -> None:
        """Should display cleaned prompt and detected flags."""
        output = format_cli_output("task", ["s", "c"], "<context>content</context>")

        assert "task" in output
        assert "-s" in output
        assert "-c" in output
        assert "Detected flags:" in output
        assert "Cleaned prompt:" in output

    def test_includes_context_summary(self) -> None:
        """Should include information about what context would be added."""
        output = format_cli_output(
            "task", ["s"], "<subagent_delegation>content</subagent_delegation>"
        )

        assert "Context to be added:" in output
        assert "<subagent_delegation>" in output
        assert "content" in output

    def test_single_flag_formatting(self) -> None:
        """Test output with single flag."""
        output = format_cli_output(
            "my task", ["c"], "<commit_instructions>Test</commit_instructions>"
        )

        assert "Detected flags: -c" in output
        assert "Cleaned prompt: my task" in output
        assert "Context to be added:" in output
        assert "<commit_instructions>Test</commit_instructions>" in output

    def test_multiple_flags_formatting(self) -> None:
        """Test output with multiple flags."""
        context = (
            "<commit_instructions>Commit</commit_instructions>\n"
            "<test_instructions>Test</test_instructions>"
        )
        output = format_cli_output("implement feature", ["c", "t"], context)

        assert "Detected flags: -c, -t" in output
        assert "Cleaned prompt: implement feature" in output
        assert "<commit_instructions>" in output
        assert "<test_instructions>" in output

    def test_all_flags_formatting(self) -> None:
        """Test output with all flags."""
        output = format_cli_output("task", ["s", "c", "t", "d", "n"], "<contexts>")

        assert "Detected flags: -s, -c, -t, -d, -n" in output

    def test_multiline_structure(self) -> None:
        """Test that output has proper multiline structure."""
        output = format_cli_output("task", ["c"], "<context>")

        lines = output.split("\n")
        assert len(lines) >= 4
        assert lines[0].startswith("Detected flags:")
        assert lines[1].startswith("Cleaned prompt:")
        assert lines[2] == ""  # Blank line
        assert lines[3] == "Context to be added:"

    def test_complex_prompt_preserved(self) -> None:
        """Test that complex prompts are preserved in output."""
        prompt = "Multi-line\ntask with\ndetails"
        output = format_cli_output(prompt, ["c"], "<context>")

        assert "Multi-line\ntask with\ndetails" in output

    def test_empty_context(self) -> None:
        """Test output with empty context."""
        output = format_cli_output("task", ["s"], "")

        assert "Detected flags: -s" in output
        assert "Cleaned prompt: task" in output
        assert "Context to be added:" in output

    def test_no_json_structure(self) -> None:
        """Test that CLI output is plain text, not JSON."""
        output = format_cli_output("task", ["c"], "<context>")

        # Should not be valid JSON
        with pytest.raises(json.JSONDecodeError):
            json.loads(output)

    def test_human_readable_format(self) -> None:
        """Test that output is formatted for human reading."""
        output = format_cli_output(
            "implement auth", ["c", "t"], "<commit_instructions>Commit</commit_instructions>"
        )

        # Should use labels and formatting
        assert "Detected flags:" in output
        assert "Cleaned prompt:" in output
        assert "Context to be added:" in output
        # Should use comma-separated list for flags
        assert "-c, -t" in output
