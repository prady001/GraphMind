from app.graph.database import engine
from app.graph.models import Base

Base.metadata.create_all(bind=engine)
print("Database tables created.")
