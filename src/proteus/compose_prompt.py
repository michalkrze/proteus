from dataclasses import dataclass
from typing import Literal

from proteus.exceptions import BaseTraitMissingError


@dataclass(frozen=True)
class ComposeRobotTraitFields:
    kind: Literal["base", "addon"]
    content: str
    priority: int


def _sort_traits(traits_fields: list[ComposeRobotTraitFields]) -> list[ComposeRobotTraitFields]:
    return sorted(traits_fields, key=lambda trait_field: trait_field.priority)


def compose_robot_prompt(traits_fields: list[ComposeRobotTraitFields]) -> str:
    base_prompt_included = any(trait_field.kind == "base" for trait_field in traits_fields)
    if not base_prompt_included:
        raise BaseTraitMissingError("Base trait missing")

    traits_fields = _sort_traits(traits_fields)
    robot_prompt = "\n".join(trait_field.content for trait_field in traits_fields)

    return robot_prompt
