import logging
from app import db

logger = logging.getLogger(__name__)

db.Model.metadata.reflect(db.engine)


class Kitty(db.Model):
    """Create a data model for the database to be set up to store kitties

    """
    try:
        __table__ = db.Model.metadata.tables['kitties']
    except:
        logger.warning("'kitties' table not found")

    def __repr__(self):
        return '<Kitty(id: %s, name: %s)>' % (self.id, self.name)

