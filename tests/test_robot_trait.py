from sqlalchemy import select
from sqlalchemy.orm import Session

from proteus.models import Robot, RobotTrait, Trait, User


def test_deleting_robot_deletes_its_traits(session: Session) -> None:
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
    trait_addon = Trait(
        slug="test_slug_addon",
        name="test_name_addon",
        content="test_content_addon",
        priority=10,
        kind="addon",
    )

    session.add(robot)
    session.add(trait_addon)
    session.flush()

    robot_trait = RobotTrait(robot_id=robot.id, trait_id=trait_addon.id)
    session.add(robot_trait)
    session.flush()

    session.delete(robot)
    session.flush()

    stmt = select(RobotTrait).where(RobotTrait.robot_id == robot_trait.robot_id)
    result = session.execute(stmt)

    assert result.all() == []
