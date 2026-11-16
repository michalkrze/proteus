"""rename robot_traits to robot_addons

Revision ID: 0ae5ec9c041c
Revises: a229b813542a
Create Date: 2026-11-16 20:24:58.097055

"""

from collections.abc import Sequence

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "0ae5ec9c041c"
down_revision: str | Sequence[str] | None = "a229b813542a"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None

# Written by hand: autogenerate can't detect renames (it would drop the table and create a
# new one, losing the data). Constraint names come from the naming convention, so they are
# renamed too; otherwise they would still say "robot_traits".
CONSTRAINTS = [
    ("pk_robot_traits", "pk_robot_addons"),
    ("fk_robot_traits_robot_id_robots", "fk_robot_addons_robot_id_robots"),
    ("fk_robot_traits_trait_id_traits", "fk_robot_addons_trait_id_traits"),
]


def upgrade() -> None:
    """Upgrade schema."""
    op.rename_table("robot_traits", "robot_addons")
    for old, new in CONSTRAINTS:
        op.execute(f"ALTER TABLE robot_addons RENAME CONSTRAINT {old} TO {new}")


def downgrade() -> None:
    """Downgrade schema."""
    for old, new in CONSTRAINTS:
        op.execute(f"ALTER TABLE robot_addons RENAME CONSTRAINT {new} TO {old}")
    op.rename_table("robot_addons", "robot_traits")
