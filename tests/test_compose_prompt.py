import pytest
from proteus.compose_prompt import compose_robot_prompt
from proteus.exceptions import BaseTraitMissingError

from proteus.models import Trait


def test_prompt_without_base_is_rejected() -> None:
    trait = Trait(
        slug="test_slug",
        name="test_name",
        content="test_content",
        priority=5,
        kind="addon",
    )

    with pytest.raises(BaseTraitMissingError):
        compose_robot_prompt([trait])


def test_prompt_compose_structure_is_correct() -> None:
    traits = traits_list()
    robot_prompt: str = compose_robot_prompt(traits)
    assert robot_prompt == "\n".join([traits[1].content, traits[2].content, traits[0].content])


def traits_list() -> list[Trait]:
    trait1 = Trait(
        slug="test_slug1",
        name="test_name1",
        content="test_content1",
        priority=5,
        kind="addon",
    )

    trait2 = Trait(
        slug="test_slug2",
        name="test_name2",
        content="test_content2",
        priority=1,
        kind="base",
    )

    trait3 = Trait(
        slug="test_slug3",
        name="test_name3",
        content="test_content3",
        priority=2,
        kind="addon",
    )

    return [trait1, trait2, trait3]
