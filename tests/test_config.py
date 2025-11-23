"""Tests for configuration loading and saving."""

import pytest
import yaml

from ai_flags.config import AiFlagsConfig, FlagConfig
from ai_flags.config_loader import (
    load_config,
    save_config,
    reset_config,
    get_default_config,
)


@pytest.fixture
def temp_config_path(tmp_path, monkeypatch):
    """Use temporary config path for tests."""
    config_path = tmp_path / "config.yaml"
    monkeypatch.setattr("ai_flags.config_loader.CONFIG_PATH", config_path)
    monkeypatch.setattr("ai_flags.config_loader.CONFIG_DIR", tmp_path)
    return config_path


class TestLoadConfig:
    """Test config loading."""

    def test_load_default_when_missing(self, temp_config_path):
        """Should return default config when file doesn't exist."""
        config = load_config()
        assert isinstance(config, AiFlagsConfig)
        # All flags should be enabled by default
        assert config.subagent.enabled
        assert config.commit.enabled
        assert config.test.enabled
        assert config.debug.enabled
        assert config.no_lint.enabled

    def test_load_from_file(self, temp_config_path):
        """Should load config from YAML file."""
        # Create config file
        config_data = {
            "subagent": {"enabled": False, "content": None},
            "commit": {"enabled": True, "content": "Custom"},
            "test": {"enabled": True, "content": None},
            "debug": {"enabled": True, "content": None},
            "no_lint": {"enabled": True, "content": None},
        }

        with open(temp_config_path, "w") as f:
            yaml.safe_dump(config_data, f)

        config = load_config()
        assert not config.subagent.enabled
        assert config.commit.content == "Custom"

    def test_load_malformed_returns_default(self, temp_config_path):
        """Should return default config on malformed YAML."""
        with open(temp_config_path, "w") as f:
            f.write("invalid: yaml: content:")

        config = load_config()
        assert isinstance(config, AiFlagsConfig)

    def test_load_partial_config(self, temp_config_path):
        """Should handle partial config with defaults for missing fields."""
        # Only specify some flags
        config_data = {
            "subagent": {"enabled": False, "content": None},
            "commit": {"enabled": False, "content": None},
        }

        with open(temp_config_path, "w") as f:
            yaml.safe_dump(config_data, f)

        config = load_config()
        # Specified flags should be loaded
        assert not config.subagent.enabled
        assert not config.commit.enabled
        # Missing flags should have defaults
        assert config.test.enabled
        assert config.debug.enabled
        assert config.no_lint.enabled

    def test_load_empty_file(self, temp_config_path):
        """Should return default config for empty file."""
        with open(temp_config_path, "w") as f:
            f.write("")

        config = load_config()
        assert isinstance(config, AiFlagsConfig)
        assert config.subagent.enabled

    def test_load_preserves_custom_content(self, temp_config_path):
        """Should preserve custom content when loading."""
        custom_content = "My custom instructions"
        config_data = {
            "subagent": {"enabled": True, "content": custom_content},
            "commit": {"enabled": True, "content": None},
            "test": {"enabled": True, "content": None},
            "debug": {"enabled": True, "content": None},
            "no_lint": {"enabled": True, "content": None},
        }

        with open(temp_config_path, "w") as f:
            yaml.safe_dump(config_data, f)

        config = load_config()
        assert config.subagent.content == custom_content


class TestSaveConfig:
    """Test config saving."""

    def test_save_creates_directory(self, temp_config_path):
        """Should create config directory if it doesn't exist."""
        config = get_default_config()
        save_config(config)

        assert temp_config_path.parent.exists()
        assert temp_config_path.exists()

    def test_save_writes_yaml(self, temp_config_path):
        """Should write valid YAML."""
        config = get_default_config()
        config.commit.enabled = False
        save_config(config)

        with open(temp_config_path, "r") as f:
            data = yaml.safe_load(f)

        assert data["commit"]["enabled"] is False

    def test_save_preserves_all_fields(self, temp_config_path):
        """Should preserve all config fields when saving."""
        config = get_default_config()
        config.subagent.enabled = False
        config.commit.content = "Custom commit message"
        config.test.enabled = False
        save_config(config)

        with open(temp_config_path, "r") as f:
            data = yaml.safe_load(f)

        assert data["subagent"]["enabled"] is False
        assert data["commit"]["content"] == "Custom commit message"
        assert data["test"]["enabled"] is False

    def test_save_overwrites_existing(self, temp_config_path):
        """Should overwrite existing config file."""
        # Create initial config
        config1 = get_default_config()
        config1.commit.enabled = False
        save_config(config1)

        # Overwrite with new config
        config2 = get_default_config()
        config2.commit.enabled = True
        config2.test.enabled = False
        save_config(config2)

        # Verify new config is saved
        with open(temp_config_path, "r") as f:
            data = yaml.safe_load(f)

        assert data["commit"]["enabled"] is True
        assert data["test"]["enabled"] is False

    def test_save_handles_nested_directories(self, tmp_path, monkeypatch):
        """Should create nested directories if needed."""
        nested_path = tmp_path / "deep" / "nested" / "config.yaml"
        nested_dir = nested_path.parent
        monkeypatch.setattr("ai_flags.config_loader.CONFIG_PATH", nested_path)
        monkeypatch.setattr("ai_flags.config_loader.CONFIG_DIR", nested_dir)

        config = get_default_config()
        save_config(config)

        assert nested_path.exists()
        assert nested_path.parent.exists()


class TestResetConfig:
    """Test config reset."""

    def test_reset_to_defaults(self, temp_config_path):
        """Should reset config to defaults."""
        # Create modified config
        config = get_default_config()
        config.subagent.enabled = False
        config.commit.enabled = False
        save_config(config)

        # Reset
        reset_config()

        # Load and verify
        config = load_config()
        assert config.subagent.enabled  # Back to default (enabled)
        assert config.commit.enabled  # Back to default (enabled)

    def test_reset_clears_custom_content(self, temp_config_path):
        """Should clear custom content on reset."""
        # Create config with custom content
        config = get_default_config()
        config.commit.content = "Custom content"
        save_config(config)

        # Reset
        reset_config()

        # Load and verify
        config = load_config()
        assert config.commit.content is None

    def test_reset_returns_default_config(self, temp_config_path):
        """Should return the default config instance."""
        returned_config = reset_config()
        assert isinstance(returned_config, AiFlagsConfig)
        assert returned_config.subagent.enabled
        assert returned_config.commit.enabled


class TestAiFlagsConfig:
    """Test AiFlagsConfig model."""

    def test_get_enabled_flags(self):
        """Should return set of enabled flag letters."""
        config = AiFlagsConfig()
        enabled = config.get_enabled_flags()
        assert enabled == {"s", "c", "t", "d", "n"}

    def test_get_enabled_flags_partial(self):
        """Should return only enabled flags."""
        config = AiFlagsConfig()
        config.subagent.enabled = False
        config.commit.enabled = False
        enabled = config.get_enabled_flags()
        assert enabled == {"t", "d", "n"}

    def test_get_enabled_flags_none(self):
        """Should return empty set when all flags disabled."""
        config = AiFlagsConfig()
        config.subagent.enabled = False
        config.commit.enabled = False
        config.test.enabled = False
        config.debug.enabled = False
        config.no_lint.enabled = False
        enabled = config.get_enabled_flags()
        assert enabled == set()

    def test_get_flag_config(self):
        """Should retrieve config for specific flag."""
        config = AiFlagsConfig()
        s_config = config.get_flag_config("s")
        assert s_config is not None
        assert s_config == config.subagent
        assert s_config.enabled

    def test_get_flag_config_all_flags(self):
        """Should retrieve config for all flag letters."""
        config = AiFlagsConfig()

        assert config.get_flag_config("s") == config.subagent
        assert config.get_flag_config("c") == config.commit
        assert config.get_flag_config("t") == config.test
        assert config.get_flag_config("d") == config.debug
        assert config.get_flag_config("n") == config.no_lint

    def test_get_flag_config_invalid(self):
        """Should return None for invalid flag."""
        config = AiFlagsConfig()
        assert config.get_flag_config("x") is None
        assert config.get_flag_config("invalid") is None

    def test_default_config_all_enabled(self):
        """Default config should have all flags enabled."""
        config = get_default_config()
        assert config.subagent.enabled
        assert config.commit.enabled
        assert config.test.enabled
        assert config.debug.enabled
        assert config.no_lint.enabled

    def test_default_config_no_custom_content(self):
        """Default config should have no custom content."""
        config = get_default_config()
        assert config.subagent.content is None
        assert config.commit.content is None
        assert config.test.content is None
        assert config.debug.content is None
        assert config.no_lint.content is None


class TestFlagConfig:
    """Test FlagConfig model."""

    def test_default_values(self):
        """Should have correct default values."""
        flag_config = FlagConfig()
        assert flag_config.enabled is True
        assert flag_config.content is None

    def test_custom_values(self):
        """Should accept custom values."""
        flag_config = FlagConfig(enabled=False, content="Custom")
        assert flag_config.enabled is False
        assert flag_config.content == "Custom"

    def test_enabled_only(self):
        """Should allow setting enabled without content."""
        flag_config = FlagConfig(enabled=False)
        assert flag_config.enabled is False
        assert flag_config.content is None

    def test_content_only(self):
        """Should allow setting content without enabled."""
        flag_config = FlagConfig(content="Custom")
        assert flag_config.enabled is True  # Default
        assert flag_config.content == "Custom"


class TestConfigPersistence:
    """Test configuration persistence across save/load cycles."""

    def test_save_load_cycle(self, temp_config_path):
        """Config should persist across save/load cycle."""
        # Create and save config
        config1 = get_default_config()
        config1.subagent.enabled = False
        config1.commit.content = "Custom"
        save_config(config1)

        # Load and verify
        config2 = load_config()
        assert config2.subagent.enabled is False
        assert config2.commit.content == "Custom"

    def test_multiple_save_load_cycles(self, temp_config_path):
        """Should handle multiple save/load cycles."""
        # First cycle
        config1 = get_default_config()
        config1.test.enabled = False
        save_config(config1)
        loaded1 = load_config()
        assert loaded1.test.enabled is False

        # Second cycle
        loaded1.debug.enabled = False
        save_config(loaded1)
        loaded2 = load_config()
        assert loaded2.test.enabled is False
        assert loaded2.debug.enabled is False

    def test_config_isolation(self, temp_config_path):
        """Loaded configs should be independent instances."""
        config1 = get_default_config()
        config1.commit.enabled = False
        save_config(config1)

        # Load two instances
        loaded1 = load_config()
        loaded2 = load_config()

        # Modify one instance
        loaded1.test.enabled = False

        # Other instance should be unaffected
        assert loaded2.test.enabled is True

    def test_yaml_format_readability(self, temp_config_path):
        """Saved YAML should be human-readable."""
        config = get_default_config()
        config.commit.enabled = False
        save_config(config)

        with open(temp_config_path, "r") as f:
            content = f.read()

        # Check that YAML is readable (not flow style)
        assert "commit:" in content
        assert "enabled:" in content
        assert "false" in content.lower()
        # Should not use flow style (inline) format
        assert not content.startswith("{")
