from sqlalchemy.orm import Session

from proteus.compose_prompt import ComposeRobotTraitFields
from proteus.models import Robot, RobotAddon, Trait
from proteus.queries import create_compose_fields


def test_prompt_trait_load_correct(
    session: Session, robot: Robot, robot_addon: RobotAddon, base_trait: Trait, addon_trait: Trait
) -> None:
    expected_fields = {
        ComposeRobotTraitFields(
            id=base_trait.id, kind="base", content=base_trait.content, priority=base_trait.priority
        ),
        ComposeRobotTraitFields(
            id=addon_trait.id,
            kind="addon",
            content=addon_trait.content,
            priority=addon_trait.priority,
        ),
    }

    compose_fields = create_compose_fields(session, robot)
    assert set(compose_fields) == expected_fields


def test_override_replaces_trait_priority(
    session: Session, robot: Robot, robot_addon: RobotAddon, base_trait: Trait, addon_trait: Trait
) -> None:
    robot_addon.priority_override = 30

    expected_fields = {
        ComposeRobotTraitFields(
            id=base_trait.id, kind="base", content=base_trait.content, priority=base_trait.priority
        ),
        ComposeRobotTraitFields(
            id=addon_trait.id,
            kind="addon",
            content=addon_trait.content,
            priority=robot_addon.priority_override,
        ),
    }

    compose_fields = create_compose_fields(session, robot)
    assert set(compose_fields) == expected_fields


def test_disabled_addon_is_skipped(
    session: Session, robot: Robot, robot_addon: RobotAddon, base_trait: Trait, addon_trait: Trait
) -> None:
    robot_addon.enabled = False

    expected_fields = {
        ComposeRobotTraitFields(
            id=base_trait.id, kind="base", content=base_trait.content, priority=base_trait.priority
        ),
    }

    compose_fields = create_compose_fields(session, robot)
    assert set(compose_fields) == expected_fields
