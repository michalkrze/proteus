from sqlalchemy import func, select
from sqlalchemy.orm import Session

from proteus.compose_prompt import ComposeRobotTraitFields
from proteus.models import Robot, RobotAddon, Trait


def create_compose_fields(session: Session, robot: Robot) -> list[ComposeRobotTraitFields]:
    compose_fields: list[ComposeRobotTraitFields] = []

    base_trait_row = session.execute(
        select(Trait.id, Trait.kind, Trait.content, Trait.priority).where(
            Trait.id == robot.base_trait_id
        )
    ).one()

    compose_fields.append(
        ComposeRobotTraitFields(
            id=base_trait_row.id,
            kind=base_trait_row.kind,
            content=base_trait_row.content,
            priority=base_trait_row.priority,
        )
    )

    rows = session.execute(
        select(
            Trait.id,
            Trait.kind,
            Trait.content,
            func.coalesce(RobotAddon.priority_override, Trait.priority).label("priority"),
        )
        .join_from(RobotAddon, Trait)
        .where(RobotAddon.enabled)
        .where(RobotAddon.robot_id == robot.id)
    )

    for row in rows:
        compose_fields.append(
            ComposeRobotTraitFields(
                id=row.id, kind=row.kind, content=row.content, priority=row.priority
            )
        )

    return compose_fields
