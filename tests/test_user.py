import datetime
import uuid

from sqlalchemy.orm import Session

from proteus.models import User


def test_database_generates_id_and_created_at(session: Session) -> None:
    user = User(email="test@example.com")

    session.add(user)
    session.flush()

    assert isinstance(user.id, uuid.UUID)
    assert user.id.version == 7

    assert isinstance(user.created_at, datetime.datetime)
    assert user.created_at.tzinfo is not None
