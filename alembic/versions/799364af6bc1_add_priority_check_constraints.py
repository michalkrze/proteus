"""add priority check constraints

Revision ID: 799364af6bc1
Revises: 0ae5ec9c041c
Create Date: 2026-11-22 17:28:30.271631

"""

from collections.abc import Sequence

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "799364af6bc1"
down_revision: str | Sequence[str] | None = "0ae5ec9c041c"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    """Upgrade schema."""

    op.create_check_constraint(
        constraint_name=op.f("ck_traits_addon_priority"),
        table_name="traits",
        condition="kind <> 'addon' OR priority > 1",
    )
    op.create_check_constraint(
        constraint_name=op.f("ck_traits_base_priority"),
        table_name="traits",
        condition="kind <> 'base' OR priority = 1",
    )
    op.create_check_constraint(
        constraint_name=op.f("ck_robot_addons_priority_override"),
        table_name="robot_addons",
        condition="priority_override > 1",
    )


def downgrade() -> None:
    """Downgrade schema."""

    op.drop_constraint(constraint_name=op.f("ck_traits_addon_priority"), table_name="traits")
    op.drop_constraint(constraint_name=op.f("ck_traits_base_priority"), table_name="traits")
    op.drop_constraint(
        constraint_name=op.f("ck_robot_addons_priority_override"), table_name="robot_addons"
    )
