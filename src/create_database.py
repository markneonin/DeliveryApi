from database.database import engine
from models.tables import Base

Base.metadata.create_all(engine)
