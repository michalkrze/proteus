import pytest
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from proteus.models import Robot, RobotTrait, Trait, User


def test_deleting_robot_deletes_its_traits(session: Session) -> None:
    robot = create_robot(session)
    trait_addon = create_trait_addon(session)

    robot_trait = RobotTrait(robot_id=robot.id, trait_id=trait_addon.id)
    session.add(robot_trait)
    session.flush()

    session.delete(robot)
    session.flush()

    stmt = select(RobotTrait).where(RobotTrait.robot_id == robot_trait.robot_id)
    result = session.execute(stmt)

    assert result.all() == []


def test_same_trait_cannot_be_added_twice_to_robot(session: Session) -> None:
    robot = create_robot(session)
    trait_addon = create_trait_addon(session)

    robot_trait = RobotTrait(robot_id=robot.id, trait_id=trait_addon.id)
    session.add(robot_trait)
    session.flush()

    robot_trait_duplicate = RobotTrait(robot_id=robot.id, trait_id=trait_addon.id)
    session.add(robot_trait_duplicate)

    with pytest.raises(IntegrityError, match="pk_robot_traits"):
        session.flush()


def test_in_use_trait_cannot_be_deleted(session: Session) -> None:
    robot = create_robot(session)
    trait_addon = create_trait_addon(session)

    robot_trait = RobotTrait(robot_id=robot.id, trait_id=trait_addon.id)
    session.add(robot_trait)
    session.flush()

    session.delete(trait_addon)
    with pytest.raises(IntegrityError, match="fk_robot_traits_trait_id_traits"):
        session.flush()


def create_robot(session: Session) -> Robot:
    trait = Trait(
        slug="test_slug",
        name="test_name",
        content="test_content",
        priority=1,
        kind="base",
    )
    user = User(email="test@example.com")

    session.add(trait)
    session.add(user)

    session.flush()

    robot = Robot(name="test_robot", base_trait_id=trait.id, owner_id=user.id)
    session.add(robot)
    session.flush()

    return robot


def create_trait_addon(session: Session) -> Trait:
    trait_addon = Trait(
        slug="test_slug_addon",
        name="test_name_addon",
        content="test_content_addon",
        priority=10,
        kind="addon",
    )

    session.add(trait_addon)
    session.flush()

    return trait_addon
