from fastapi import FastAPI
from app.routes.word import router as word_router
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="WordWise API",
    description="AI-powered word lookup with literary context",
    version="1.0.0",
)

# Allow Android app to call this API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Tighten this in production
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(word_router, prefix="/api/v1")


@app.get("/health")
def health_check():
    return {"status": "ok"}