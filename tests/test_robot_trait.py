import pytest
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from proteus.models import Robot, RobotTrait, Trait


def test_deleting_robot_deletes_its_traits(
    session: Session, robot: Robot, robot_trait: RobotTrait
) -> None:
    session.delete(robot)
    session.flush()

    stmt = select(RobotTrait).where(RobotTrait.robot_id == robot_trait.robot_id)
    result = session.execute(stmt)

    assert result.all() == []


def test_same_trait_cannot_be_added_twice_to_robot(
    session: Session, robot_trait: RobotTrait
) -> None:
    robot_trait_duplicate = RobotTrait(robot_id=robot_trait.robot_id, trait_id=robot_trait.trait_id)
    session.expunge(robot_trait)
    session.add(robot_trait_duplicate)

    with pytest.raises(IntegrityError, match="pk_robot_traits"):
        session.flush()


def test_in_use_trait_cannot_be_deleted(
    session: Session, robot_trait: RobotTrait, addon_trait: Trait
) -> None:
    session.delete(addon_trait)
    with pytest.raises(IntegrityError, match="fk_robot_traits_trait_id_traits"):
        session.flush()
