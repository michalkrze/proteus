from proteus.exceptions import BaseTraitMissingError
from proteus.models import Trait


def _sort_traits(traits: list[Trait]) -> list[Trait]:
    return sorted(traits, key=lambda trait: trait.priority)


def compose_robot_prompt(traits: list[Trait]) -> str:
    base_prompt_included = any(trait.kind == "base" for trait in traits)
    if not base_prompt_included:
        raise BaseTraitMissingError("Base trait missing")

    traits = _sort_traits(traits)
    robot_prompt = "\n".join(trait.content for trait in traits)

    return robot_prompt
