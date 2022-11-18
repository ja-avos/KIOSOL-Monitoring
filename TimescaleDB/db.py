from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
import models
import os

session = None

def connect_database(username, password, host, port, database):
    """Connect to the database and return a connection object."""
    # Connect to the database
    connection_string = f'postgresql://{username}:{password}@{host}:{port}/{database}'
    engine = create_engine(connection_string)
    return engine

def create_tables(engine):
    """Create the tables in the database."""
    models.Base.metadata.create_all(engine)

def drop_tables(engine):
    """Drop the tables in the database."""
    models.Base.metadata.drop_all(engine)

def generate_mock_data(engine):
    """Generate mock data for the database."""

    # Create a session to the database
    Session = sessionmaker(bind=engine)
    session = Session()

    # Create a mock user
    user = models.UserModel(login='test', role=models.Role.ADMIN, email="test@test.com")
    session.add(user)
    session.commit()

# Create session
def create_session(engine):
    Session = sessionmaker(bind=engine)
    session = Session()
    return session

def init_session():
    global session

    """Initialize the database session."""
    # Read the database configuration from the environment
    username = os.environ.get('POSTGRES_USER', 'postgres')
    password = os.environ.get('POSTGRES_PASSWORD', 'postgres')
    host = os.environ.get('POSTGRES_HOST', 'localhost')
    port = os.environ.get('POSTGRES_PORT', '5432')
    database = os.environ.get('POSTGRES_DB', 'postgres')
    username = 'labmonitoring'
    password = 'IOT2022!'
    database = 'solarlabmonitoring'

    # Connect to the database
    engine = connect_database(username, password, host, port, database)

    session = create_session(engine)

init_session()

if __name__ == '__main__':
    # Read the database configuration from the environment
    username = os.environ.get('POSTGRES_USER', 'postgres')
    password = os.environ.get('POSTGRES_PASSWORD', 'postgres')
    host = os.environ.get('POSTGRES_HOST', 'localhost')
    port = os.environ.get('POSTGRES_PORT', '5432')
    database = os.environ.get('POSTGRES_DB', 'postgres')
    username = 'labmonitoring'
    password = 'IOT2022!'
    database = 'solarlabmonitoring'

    # Connect to the database
    engine = connect_database(username, password, host, port, database)

    with engine.connect() as connection:
        # Drop the tables
        drop_tables(engine)

        # Create the tables
        create_tables(engine)

        # Generate mock data
        generate_mock_data(engine)