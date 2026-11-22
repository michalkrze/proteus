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


def test_addon_trait_invalid_priority_is_rejected(session: Session) -> None:
    trait = Trait(
        slug="test_slug_addon",
        name="test_name_addon",
        content="test_content_addon",
        priority=1,
        kind="addon",
    )

    session.add(trait)
    with pytest.raises(IntegrityError, match="ck_traits_addon_priority"):
        session.flush()


def test_base_trait_invalid_priority_is_rejected(session: Session) -> None:
    trait = Trait(
        slug="test_slug_base",
        name="test_name_base",
        content="test_content_base",
        priority=2,
        kind="base",
    )

    session.add(trait)
    with pytest.raises(IntegrityError, match="ck_traits_base_priority"):
        session.flush()
