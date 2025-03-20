from sqlalchemy.orm import sessionmaker
from app.database.connection import engine

# Create a session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Dependency to get the session in routes
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
