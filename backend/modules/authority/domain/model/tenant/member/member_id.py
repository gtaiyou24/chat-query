from dataclasses import dataclass


@dataclass(init=False, unsafe_hash=True, frozen=True)
class MemberId:
    value: str

    def __init__(self, value: str):
        assert value, "メンバーIDは必須です。"
        super().__setattr__("value", value)
