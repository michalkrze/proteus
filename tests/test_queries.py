from sqlalchemy.orm import Session

from proteus.compose_prompt import ComposeRobotTraitFields
from proteus.models import Robot, RobotAddon, Trait
from proteus.queries import create_compose_fields


def test_prompt_trait_load_correct(
    session: Session, robot: Robot, robot_addon: RobotAddon, base_trait: Trait, addon_trait: Trait
) -> None:
    expected_fields = {
        ComposeRobotTraitFields(
            kind="base", content=base_trait.content, priority=base_trait.priority
        ),
        ComposeRobotTraitFields(
            kind="addon",
            content=addon_trait.content,
            priority=addon_trait.priority,
        ),
    }

    compose_fields = create_compose_fields(session, robot)
    assert set(compose_fields) == expected_fields
