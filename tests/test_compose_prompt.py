import pytest

from proteus.compose_prompt import ComposeRobotTraitFields, compose_robot_prompt
from proteus.exceptions import BaseTraitMissingError


def test_prompt_without_base_is_rejected() -> None:

    with pytest.raises(BaseTraitMissingError):
        compose_robot_prompt(
            [
                ComposeRobotTraitFields(kind="addon", content="test_content", priority=5),
            ]
        )


def test_prompt_compose_structure_is_correct() -> None:
    traits = traits_fields_list()
    robot_prompt: str = compose_robot_prompt(traits)
    assert robot_prompt == "\n".join([traits[1].content, traits[2].content, traits[0].content])


def traits_fields_list() -> list[ComposeRobotTraitFields]:

    return [
        ComposeRobotTraitFields(kind="addon", content="test_content1", priority=5),
        ComposeRobotTraitFields(kind="base", content="test_content2", priority=1),
        ComposeRobotTraitFields(kind="addon", content="test_content3", priority=2),
    ]
