from fastapi import FastAPI
from database import engine, Base
from routes import preferences, digests, highlights
from fastapi.middleware.cors import CORSMiddleware



app = FastAPI(title="MLB Highlights Project")


# Define the allowed origins
origins = [
    "*",
    "http://localhost:5173/",  # Vite development server
      # Your production frontend URL
]

# Add the CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # List of allowed origins
    allow_credentials=True,  # If you need to send cookies or authentication headers
    allow_methods=["*"],  # HTTP methods allowed (GET, POST, etc.)
    allow_headers=["*"],  # HTTP headers allowed
)

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
