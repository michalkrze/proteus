from collections.abc import Iterator

import pytest
from sqlalchemy import Engine, create_engine
from testcontainers.community.postgres import PostgresContainer

from proteus.models import Base


@pytest.fixture(scope="session")
def engine() -> Iterator[Engine]:
    with PostgresContainer(image="postgres:18", driver="psycopg") as postgres:
        engine = create_engine(postgres.get_connection_url())
        Base.metadata.create_all(engine)
        yield engine
        engine.dispose()
