from dataclasses import dataclass


@dataclass
class UserSettingsModel:
    lastbases: list[str]
    open_last: bool

    @classmethod
    def fromDict(cls, data: dict) -> "UserSettingsModel":
        return cls(
            lastbases=data.get("lastbases", []),
            open_last=data.get("open_last", True),
        )

    def dump(self) -> dict:
        return {
            "lastbases": self.lastbases,
            "open_last": self.open_last,
        }


def make_default() -> UserSettingsModel:
    return UserSettingsModel(
        lastbases=[],
        open_last=True,
    )


@dataclass
class UpdateUserSettingsModel:
    lastbases: list[str] | None = None
    open_last: bool | None = None
