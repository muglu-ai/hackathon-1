from fastapi import FastAPI
from database import engine, Base
from routes import preferences, digests, highlights


app = FastAPI(title="MLB Highlights Project")

# Create the database tables
Base.metadata.create_all(bind=engine)

# Include routers
app.include_router(preferences.router)
#app.include_router(digests.router)
app.include_router(highlights.router)
app.include_router(digests.router)


@app.get("/")
def read_root():
    return {"message": "Welcome to the MLB Highlights Project"}
