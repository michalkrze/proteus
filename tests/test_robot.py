import uuid

import pytest
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from proteus.models import Robot, Trait, User


def test_robot_with_unknown_owner_is_rejected(session: Session) -> None:
    trait = Trait(
        slug="test_slug",
        name="test_name",
        content="test_content",
        priority=1,
        kind="base",
    )

    session.add(trait)
    session.flush()

    robot = Robot(name="test_robot", owner_id=uuid.uuid7(), base_trait_id=trait.id)

    session.add(robot)
    with pytest.raises(IntegrityError, match="fk_robots_owner_id_users"):
        session.flush()


def test_robot_with_unknown_base_trait_is_rejected(session: Session) -> None:
    user = User(email="test@example.com")

    session.add(user)
    session.flush()

    robot = Robot(name="test_robot", base_trait_id=uuid.uuid7(), owner_id=user.id)

    session.add(robot)
    with pytest.raises(IntegrityError, match="fk_robots_base_trait_id_traits"):
        session.flush()
