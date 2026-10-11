import pytest
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from proteus.models import Trait


@pytest.mark.parametrize("kind_value", ["", "BASE", "other"])
def test_invalid_kind_is_rejected(session: Session, kind_value: str) -> None:
    trait = Trait(
        slug="test_slug",
        name="test_name",
        content="test_content",
        priority=1,
        kind=kind_value,
    )

    session.add(trait)
    with pytest.raises(IntegrityError, match="ck_traits_kind"):
        session.flush()
