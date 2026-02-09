"""
FastAPI application for BrainScanAI API.
"""

from fastapi import FastAPI

app = FastAPI(
    title="BrainScanAI API",
    description="API for brain tumor detection using semi-supervised learning",
    version="0.1.0",
)


@app.get("/")
async def root():
    return {"message": "BrainScanAI API is running"}


@app.get("/health")
async def health_check():
    return {"status": "healthy"}
