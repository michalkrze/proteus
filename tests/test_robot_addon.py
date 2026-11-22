import pytest
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from proteus.models import Robot, RobotAddon, Trait


def test_deleting_robot_deletes_its_addons(
    session: Session, robot: Robot, robot_addon: RobotAddon
) -> None:
    session.delete(robot)
    session.flush()

    stmt = select(RobotAddon).where(RobotAddon.robot_id == robot_addon.robot_id)
    result = session.execute(stmt)

    assert result.all() == []


def test_same_trait_cannot_be_added_twice_to_robot(
    session: Session, robot_addon: RobotAddon
) -> None:
    robot_addon_duplicate = RobotAddon(robot_id=robot_addon.robot_id, trait_id=robot_addon.trait_id)
    session.expunge(robot_addon)
    session.add(robot_addon_duplicate)

    with pytest.raises(IntegrityError, match="pk_robot_addons"):
        session.flush()


def test_in_use_trait_cannot_be_deleted(
    session: Session, robot_addon: RobotAddon, addon_trait: Trait
) -> None:
    session.delete(addon_trait)
    with pytest.raises(IntegrityError, match="fk_robot_addons_trait_id_traits"):
        session.flush()


def test_invalid_priority_override_is_rejected(
    session: Session, robot: Robot, addon_trait: Trait
) -> None:
    robot_addon = RobotAddon(robot_id=robot.id, trait_id=addon_trait.id)
    robot_addon.priority_override = 1

    session.add(robot_addon)
    with pytest.raises(IntegrityError, match="ck_robot_addon_priority_override"):
        session.flush()
