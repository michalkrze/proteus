from sqlalchemy import Engine, create_engine
from sqlalchemy.orm import Session

from proteus.models import Trait
from proteus.settings import Settings


def new_engine() -> Engine:
    settings = Settings()
    return create_engine(settings.db_url)


def new_session() -> None:
    engine = new_engine()
    with Session(engine) as session, session.begin():
        run_one_time_seed(session)


def run_one_time_seed(session: Session) -> None:
    trait = Trait(
        slug="test_slug",
        name="test_name",
        content="test_content",
        priority=1,
        kind="base",
    )
    session.add(trait)


if __name__ == "__main__":
    new_session()
