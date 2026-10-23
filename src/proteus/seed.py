import uuid

from sqlalchemy import Engine, create_engine, select
from sqlalchemy.orm import Session

from proteus.models import Robot, RobotTrait, Trait, User
from proteus.settings import Settings


def new_engine() -> Engine:
    settings = Settings()
    return create_engine(settings.db_url)


def main() -> None:
    engine = new_engine()
    with Session(engine) as session, session.begin():
        run_one_time_seed(session)


def already_run(session: Session) -> bool:
    stmt = select(Robot)
    result = session.execute(stmt)

    return result.first() is not None


def run_one_time_seed(session: Session) -> None:
    if already_run(session):
        raise Exception("Already seeded, truncate first")

    traits = patient_traits()
    user = User(email="test2@example.com")

    session.add_all(traits)
    session.add(user)
    session.flush()

    base_trait_id: uuid.UUID | None = None
    addon_traits_ids: list[uuid.UUID] = []
    for trait in traits:
        trait_id = trait.id
        if trait.kind == "base":
            base_trait_id = trait_id
        else:
            addon_traits_ids.append(trait_id)

    robot = Robot(name="Patient", owner_id=user.id, base_trait_id=base_trait_id)
    session.add(robot)
    session.flush()

    for addon_trait_id in addon_traits_ids:
        session.add(RobotTrait(robot_id=robot.id, trait_id=addon_trait_id))


def patient_traits() -> list[Trait]:
    return [
        Trait(
            slug="patient-in-therapy",
            kind="base",
            name="Patient in therapy",
            content=(
                "You are a patient in a session with a psychologist (the user). "
                "Speak only as the patient. You don't tell everything at once "
                "and never analyse yourself like a therapist. Never break character."
            ),
            priority=1,
        ),
        Trait(slug="man", kind="addon", name="Man", content="You are a man.", priority=2),
        Trait(
            slug="speaks-english",
            kind="addon",
            name="Speaks English",
            content="You speak only English, informally and naturally.",
            priority=3,
        ),
        Trait(
            slug="recent-breakup",
            kind="addon",
            name="Recent breakup",
            content=(
                "Your partner ended your long relationship recently. You think it was your fault."
            ),
            priority=6,
        ),
        Trait(
            slug="avoids-painful-topics",
            kind="addon",
            name="Avoids painful topics",
            content=(
                "You avoid painful topics at first and change the subject. "
                "You open up only when asked directly and gently."
            ),
            priority=8,
        ),
        Trait(
            slug="low-mood",
            kind="addon",
            name="Low mood",
            content=(
                "For months you have felt flat and tired, sleep badly and have lost "
                "interest in hobbies. You answer briefly and blame yourself easily."
            ),
            priority=9,
        ),
        Trait(
            slug="age-20s",
            kind="addon",
            name="In their twenties",
            content="You are in your twenties.",
            priority=10,
        ),
        Trait(
            slug="job-search-pressure",
            kind="addon",
            name="Job search pressure",
            content=(
                "You haven't found a job yet, your family keeps asking, "
                "and you feel behind your friends."
            ),
            priority=14,
        ),
        Trait(
            slug="recent-graduate",
            kind="addon",
            name="Recent graduate",
            content="You finished university a few months ago.",
            priority=15,
        ),
    ]


if __name__ == "__main__":
    main()
