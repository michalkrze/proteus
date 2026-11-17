from sqlalchemy import select
from sqlalchemy.orm import Session

from proteus.compose_prompt import ComposeRobotTraitFields
from proteus.models import Robot, RobotAddon, Trait


def create_compose_fields(session: Session, robot: Robot) -> list[ComposeRobotTraitFields]:
    stmt = select(RobotAddon).where(RobotAddon.robot_id == robot.id)
    robot_addon = session.scalars(stmt).all()

    traits = [robot.base_trait_id]
    overridden_traits = {}
    for addon in robot_addon:
        traits.append(addon.trait_id)

        if addon.priority_override is not None:
            overridden_traits[addon.trait_id] = addon.priority_override

    traits_objects = session.scalars(select(Trait).where(Trait.id.in_(traits))).all()

    compose_fields: list[ComposeRobotTraitFields] = []
    for trait in traits_objects:
        priority = trait.priority
        if trait.id in overridden_traits:
            priority = overridden_traits[trait.id]

        compose_fields.append(
            ComposeRobotTraitFields(kind=trait.kind, content=trait.content, priority=priority)
        )

    return compose_fields
