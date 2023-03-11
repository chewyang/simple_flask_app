from flask_sqlalchemy import SQLAlchemy
import logging

logger = logging.getLogger("flask.app")
# Create the SQLAlchemy object to be initialized later in init_db()
db = SQLAlchemy()

def init_db(app):
    """Initialize the SQLAlchemy app"""
    Users.init_db(app)


######################################################################
#  P E R S I S T E N T   B A S E   M O D E L
######################################################################
class PersistentBase:
    """Base class added persistent methods"""

    def __init__(self):
        self.id = None  # pylint: disable=invalid-name

    def create(self):
        """
        Creates a Account to the database
        """
        logger.info("Creating %s", self.name)
        self.id = None  # id must be none to generate next primary key
        db.session.add(self)
        db.session.commit()

    @classmethod
    def update(cls, name, email):
        """
        Updates a Account to the database
        """
        user = cls.query.filter(cls.name == name).first()
        user.email = email
        logger.info("Updating %s", name)
        db.session.commit()

    def delete(self):
        """Removes a Account from the data store"""
        logger.info("Deleting %s", self.name)
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def init_db(cls, app):
        """Initializes the database session"""
        logger.info("Initializing database")
        cls.app = app
        # This is where we initialize SQLAlchemy from the Flask app
        db.init_app(app)
        app.app_context().push()
        db.create_all()  # make our sqlalchemy tables

    @classmethod
    def all(cls):
        """Returns all of the records in the database"""
        logger.info("Processing all records")
        return cls.query.all()

    @classmethod
    def find(cls, by_id):
        """Finds a record by it's ID"""
        logger.info("Processing lookup for id %s ...", by_id)
        return cls.query.filter_by(by_id)



class Users(db.Model, PersistentBase):

    _id = db.Column("id", db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(100))
    # db.create_all()
    # db.session.commit()
    def __init__(self, name, email):
        self.name = name
        self.email = email

    @classmethod
    def find_by_name(cls, name):
        """Returns all Accounts with the given name
        Args:
            name (string): the name of the Accounts you want to match
        """
        logger.info("Processing name query for %s ...", name)
        return cls.query.filter(cls.name == name).first()

