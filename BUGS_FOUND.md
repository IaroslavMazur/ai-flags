# Bugs Found During Integration Testing

## Critical Bugs Preventing Tests from Passing

### Bug 1: Unpacking None from parse_trailing_flags

**Location:** `/Users/prb/projects/ai-flags/src/ai_flags/cli.py:66`

**Issue:** When a prompt has no flags, `parse_trailing_flags()` returns `None`, but the code tries to unpack it:

```python
cleaned_prompt, flags = parse_trailing_flags(prompt)  # Line 66
```

This causes a `TypeError: cannot unpack non-iterable NoneType object`.

**Fix:** Handle the `None` case:

```python
result = parse_trailing_flags(prompt)
if result is None:
    # No flags detected - output empty JSON
    click.echo(json.dumps({
        "hookSpecificOutput": {
            "hookEventName": "UserPromptSubmit",
            "additionalContext": ""
        }
    }))
    return

cleaned_prompt, flags = result
```

**Impact:** Currently all prompts without flags crash and trigger the exception handler (lines 89-97), returning empty
JSON.

---

### Bug 2: format_hook_output signature mismatch

**Location:** `/Users/prb/projects/ai-flags/src/ai_flags/cli.py:86`

**Issue:** The function is called with 1 argument:

```python
output = format_hook_output(context)  # Line 86
```

But the signature in `output.py:11` expects 3 arguments:

```python
def format_hook_output(
    clean_prompt: str, flags: list[str], flag_contexts: str
) -> str:
```

**Fix:** Pass all required arguments:

```python
output = format_hook_output(cleaned_prompt, flags, context)
```

**Impact:** This causes a `TypeError` which is caught by the exception handler, returning empty JSON. All flag
processing fails silently.

---

### Bug 3: Same issue in \_handle_cli_mode

**Location:** `/Users/prb/projects/ai-flags/src/ai_flags/cli.py:107`

**Issue:** Same unpacking issue:

```python
cleaned_prompt, flags = parse_trailing_flags(prompt)  # Line 107
```

**Fix:** Same as Bug 1:

```python
result = parse_trailing_flags(prompt)
if result is None:
    click.echo("Error: No flags detected in prompt", err=True)
    sys.exit(1)

cleaned_prompt, flags = result
```

---

## Test Results Summary

### test_config.py

- **Status:** ✅ All 30 tests PASSING
- **Coverage:** Complete coverage of config loading, saving, persistence
- No bugs found in config module

### test_cli.py

- **Status:** ⚠️ 14/30 tests FAILING (due to bugs above)
- **Passing tests:** Mostly error handling and config commands
- **Failing tests:** All tests that expect successful flag processing

Once the 3 bugs above are fixed, all integration tests should pass.

---

## Test Statistics

- **Total test cases:** 60
- **Total lines:** 814 (429 in test_cli.py, 385 in test_config.py)
- **Config tests:** 30/30 passing
- **CLI tests:** 16/30 passing (14 blocked by bugs)
- **Test classes:** 9
  - TestHandleCommand (18 tests)
  - TestConfigCommands (6 tests)
  - TestEndToEndWorkflows (6 tests)
  - TestLoadConfig (6 tests)
  - TestSaveConfig (5 tests)
  - TestResetConfig (3 tests)
  - TestAiFlagsConfig (8 tests)
  - TestFlagConfig (4 tests)
  - TestConfigPersistence (4 tests)

---

## Next Steps

1. Fix the 3 bugs in `cli.py`
2. Run `pytest tests/test_cli.py -v` to verify all tests pass
3. Run full test suite: `pytest tests/ -v`
4. Consider adding type checking (mypy) to catch signature mismatches
