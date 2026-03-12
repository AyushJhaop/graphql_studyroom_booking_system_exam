from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# 1. Create a SQLite database connection.
# The database file 'studyrooms.db' will be created in the current directory.
engine = create_engine('sqlite:///studyrooms.db', convert_unicode=True)

# 2. Setup a scoped session.
# This ensures thread safety in web apps where each request gets its own session.
db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine))

# 3. Create a Base class for SQLAlchemy declarative models.
# All our database models will inherit from this class.
Base = declarative_base()
Base.query = db_session.query_property()

def init_db():
    """
    Function to initialize the database setup.
    It imports our models and binds them to the database engine,
    creating the necessary tables if they don't exist yet.
    """
    import models
    Base.metadata.create_all(bind=engine)
