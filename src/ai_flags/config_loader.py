"""Configuration loading and saving."""

from pathlib import Path

import yaml

from ai_flags.config import AiFlagsConfig

CONFIG_DIR = Path.home() / ".config" / "ai-flags"
CONFIG_PATH = CONFIG_DIR / "config.yaml"


def get_default_config() -> AiFlagsConfig:
    """Return default configuration (all flags enabled, no custom content)."""
    return AiFlagsConfig()


def load_config() -> AiFlagsConfig:
    """Load configuration from file, or return default if not exists."""
    if not CONFIG_PATH.exists():
        return get_default_config()

    try:
        with open(CONFIG_PATH) as f:
            data = yaml.safe_load(f)

        if data is None:
            return get_default_config()

        return AiFlagsConfig(**data)
    except Exception:
        # On any error, return default config
        return get_default_config()


def save_config(config: AiFlagsConfig) -> None:
    """Save configuration to file."""
    CONFIG_DIR.mkdir(parents=True, exist_ok=True)

    # Convert to dict for cleaner YAML output
    data = config.model_dump(exclude_none=False)

    with open(CONFIG_PATH, "w") as f:
        yaml.safe_dump(data, f, default_flow_style=False, sort_keys=False)


def reset_config() -> AiFlagsConfig:
    """Reset configuration to defaults."""
    config = get_default_config()
    save_config(config)
    return config
