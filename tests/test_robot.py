import uuid

import pytest
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from proteus.models import Robot, Trait


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
