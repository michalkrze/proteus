import uuid
from dataclasses import dataclass
from operator import attrgetter
from typing import Literal

from proteus.exceptions import BaseTraitMissingError


@dataclass(frozen=True)
class ComposeRobotTraitFields:
    id: uuid.UUID
    kind: Literal["base", "addon"]
    content: str
    priority: int


def _sort_traits(traits_fields: list[ComposeRobotTraitFields]) -> list[ComposeRobotTraitFields]:
    return sorted(traits_fields, key=attrgetter("priority", "id"))


def compose_robot_prompt(traits_fields: list[ComposeRobotTraitFields]) -> str:
    base_prompt_included = any(trait_field.kind == "base" for trait_field in traits_fields)
    if not base_prompt_included:
        raise BaseTraitMissingError("Base trait missing")

    traits_fields = _sort_traits(traits_fields)
    robot_prompt = "\n".join(trait_field.content for trait_field in traits_fields)

    return robot_prompt
