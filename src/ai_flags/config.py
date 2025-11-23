"""Configuration models."""

from pydantic import BaseModel, Field


class FlagConfig(BaseModel):
    """Configuration for a single flag."""

    enabled: bool = Field(default=True, description="Whether this flag is enabled")
    content: str | None = Field(default=None, description="Custom content (None = use default)")


class AiFlagsConfig(BaseModel):
    """Main configuration for ai-flags."""

    # Individual flag configs
    subagent: FlagConfig = Field(default_factory=FlagConfig, description="Subagent flag (-s)")
    commit: FlagConfig = Field(default_factory=FlagConfig, description="Commit flag (-c)")
    test: FlagConfig = Field(default_factory=FlagConfig, description="Test flag (-t)")
    debug: FlagConfig = Field(default_factory=FlagConfig, description="Debug flag (-d)")
    no_lint: FlagConfig = Field(default_factory=FlagConfig, description="No-lint flag (-n)")

    def get_enabled_flags(self) -> set[str]:
        """Return set of enabled flag letters."""
        enabled = set()
        if self.subagent.enabled:
            enabled.add("s")
        if self.commit.enabled:
            enabled.add("c")
        if self.test.enabled:
            enabled.add("t")
        if self.debug.enabled:
            enabled.add("d")
        if self.no_lint.enabled:
            enabled.add("n")
        return enabled

    def get_flag_config(self, flag_letter: str) -> FlagConfig | None:
        """Get config for a specific flag letter."""
        flag_map = {
            "s": self.subagent,
            "c": self.commit,
            "t": self.test,
            "d": self.debug,
            "n": self.no_lint,
        }
        return flag_map.get(flag_letter)
