""" Connection to the database """
from sqlalchemy.engine import create_engine, URL
from .models import Base
from sqlalchemy.orm import sessionmaker
import os
from dotenv_vault import load_dotenv

# Load environment variables from .env file
load_dotenv()


def create_session(url: str = None, echo: bool = False, drop_create: bool = False):
    """ Connects to database and creates a new session

    :param url: connection URL
    :type url: str
    :param echo: if True, prints all SQL statements
    :type echo: bool
    :param drop_create: if True, drops all tables and creates them again
    :type drop_create: bool
    :return: New active session - :class:`sqlalchemy.orm.session.Session` object
    """

    if url is None:
        # Production database URL connection
        url = URL.create(
            "mssql+pyodbc",
            username=os.environ.get("DB_USER"),
            password=os.environ.get("DB_PASSWORD"),
            host=os.environ.get("DB_HOST"),
            port=1433,
            database=os.environ.get("DB_NAME"),
            query={
                "driver": "ODBC Driver 18 for SQL Server",
                "TrustServerCertificate": "yes",
                "Encrypt": "yes",
            },
        )

    engine = create_engine(url, echo=echo, connect_args={"timeout": 40})

    if drop_create:
        # Drop all tables
        Base.metadata.drop_all(bind=engine)
        # Create all tables
        Base.metadata.create_all(bind=engine)

    Session = sessionmaker(engine)
    session = Session()
    return session