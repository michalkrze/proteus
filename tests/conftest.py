from collections.abc import Iterator

import pytest
from sqlalchemy import Engine, create_engine
from sqlalchemy.orm import Session
from testcontainers.community.postgres import PostgresContainer

from proteus.models import Base, Robot, RobotTrait, Trait, User


@pytest.fixture(scope="session")
def engine() -> Iterator[Engine]:
    with PostgresContainer(image="postgres:18", driver="psycopg") as postgres:
        engine = create_engine(postgres.get_connection_url())
        Base.metadata.create_all(engine)
        yield engine
        engine.dispose()


@pytest.fixture()
def session(engine: Engine) -> Iterator[Session]:
    with engine.connect() as connection:
        transaction = connection.begin()
        with Session(bind=connection, join_transaction_mode="create_savepoint") as session:
            yield session

        transaction.rollback()


@pytest.fixture
def user(session: Session) -> User:
    user = User(email="test@example.com")
    session.add(user)
    session.flush()

    return user


@pytest.fixture
def base_trait(session: Session) -> Trait:
    trait = Trait(
        slug="test_slug",
        name="test_name",
        content="test_content",
        priority=1,
        kind="base",
    )
    session.add(trait)
    session.flush()

    return trait


@pytest.fixture
def addon_trait(session: Session) -> Trait:
    trait = Trait(
        slug="test_slug_addon",
        name="test_name_addon",
        content="test_content_addon",
        priority=10,
        kind="addon",
    )
    session.add(trait)
    session.flush()

    return trait


@pytest.fixture
def robot(session: Session, user: User, base_trait: Trait) -> Robot:
    robot = Robot(name="test_robot", owner_id=user.id, base_trait_id=base_trait.id)
    session.add(robot)
    session.flush()

    return robot


@pytest.fixture
def robot_trait(session: Session, robot: Robot, addon_trait: Trait) -> RobotTrait:
    robot_trait = RobotTrait(robot_id=robot.id, trait_id=addon_trait.id)
    session.add(robot_trait)
    session.flush()

    return robot_trait
