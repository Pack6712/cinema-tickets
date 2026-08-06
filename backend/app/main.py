from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

# Lifespan events
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    print("🚀 Cinema Tickets Backend started")
    yield
    # Shutdown
    print("⛔ Cinema Tickets Backend stopped")

# Create FastAPI app
app = FastAPI(
    title="Cinema Tickets API",
    description="Online cinema ticket booking platform",
    version="1.0.0",
    lifespan=lifespan
)

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Change in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Health check endpoint
@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "message": "Cinema Tickets API is running"
    }

# Root endpoint
@app.get("/")
async def root():
    return {
        "name": "Cinema Tickets API",
        "version": "1.0.0",
        "status": "running"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
