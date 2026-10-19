from dataclasses import dataclass


@dataclass
class UserSettingsModel:
    lastbases: list[str]
    open_last: bool
    ttk_theme: str

    @classmethod
    def fromDict(cls, data: dict) -> "UserSettingsModel":
        return cls(
            lastbases=data.get("lastbases", []),
            open_last=data.get("open_last", True),
            ttk_theme=data.get("ttk_theme", "default"),
        )

    def dump(self) -> dict:
        return {
            "lastbases": self.lastbases,
            "open_last": self.open_last,
            "ttk_theme": self.ttk_theme,
        }


def make_default() -> UserSettingsModel:
    return UserSettingsModel(
        lastbases=[],
        open_last=True,
        ttk_theme="default",
    )


@dataclass
class UpdateUserSettingsModel:
    lastbases: list[str] | None = None
    open_last: bool | None = None
    ttk_theme: str | None = None
