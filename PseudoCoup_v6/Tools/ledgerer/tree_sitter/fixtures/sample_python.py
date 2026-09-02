"""Pinned census fixture: representative Python constructs. Do not edit."""
from dataclasses import dataclass


@dataclass
class Box:
    width: int
    height: int

    def area(self) -> int:
        return self.width * self.height


def classify(boxes: list) -> dict:
    out = {"big": [], "small": []}
    for b in boxes:
        if b.area() >= 100:
            out["big"].append(b)
        else:
            out["small"].append(b)
    return out


match classify([Box(10, 12), Box(2, 3)]):
    case {"big": big} if big:
        print(f"big: {len(big)}")
    case _:
        print("none")
