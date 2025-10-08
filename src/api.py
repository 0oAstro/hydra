"""
FastAPI REST API for ML Reasoning System
Exposes the pipeline as a web service
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import List, Optional
import uvicorn
from datetime import datetime

from main import MLReasoningPipeline

# Initialize FastAPI app
app = FastAPI(
    title="ML Reasoning System API",
    description="AI-powered reasoning system that solves complex puzzles across 7 categories",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Request/Response Models
class ReasoningRequest(BaseModel):
    """Request model for reasoning endpoint"""
    question: str = Field(..., description="The problem statement or question to solve", min_length=10)
    options: List[str] = Field(..., description="List of exactly 5 answer options", min_items=5, max_items=5)
    
    class Config:
        schema_extra = {
            "example": {
                "question": "What is the next number in the sequence: 2, 4, 6, 8, ?",
                "options": ["9", "10", "11", "12", "13"]
            }
        }


class ReasoningResponse(BaseModel):
    """Response model for reasoning endpoint"""
    predicted_answer: int = Field(..., description="The predicted answer option (1-5)")
    answer_text: str = Field(..., description="The actual text of the selected answer")
    confidence: float = Field(..., description="Confidence score (0.0-1.0)")
    reasoning: str = Field(..., description="Detailed step-by-step reasoning")
    category: str = Field(..., description="Detected problem category")
    category_confidence: float = Field(..., description="Category classification confidence")
    timestamp: str = Field(..., description="Processing timestamp")
    
    class Config:
        schema_extra = {
            "example": {
                "predicted_answer": 2,
                "answer_text": "10",
                "confidence": 0.95,
                "reasoning": "This is an arithmetic sequence with a common difference of 2. Starting from 2, we add 2 each time: 2+2=4, 4+2=6, 6+2=8, 8+2=10.",
                "category": "Sequence solving",
                "category_confidence": 0.92,
                "timestamp": "2025-10-08T12:34:56"
            }
        }


class HealthResponse(BaseModel):
    """Health check response"""
    status: str
    version: str
    timestamp: str


# Global pipeline instance (loaded on startup)
pipeline: Optional[MLReasoningPipeline] = None


@app.on_event("startup")
async def startup_event():
    """Initialize pipeline on startup"""
    global pipeline
    print("Initializing ML Reasoning Pipeline...")
    try:
        # Try to load existing model first (faster)
        pipeline = MLReasoningPipeline(train_model=False)
        print("✓ Pipeline loaded successfully (using cached model)")
    except:
        # If no cached model, train from scratch
        print("No cached model found. Training new model...")
        pipeline = MLReasoningPipeline(train_model=True)
        print("✓ Pipeline initialized successfully (new model trained)")


@app.on_event("shutdown")
async def shutdown_event():
    """Cleanup on shutdown"""
    print("Shutting down ML Reasoning Pipeline...")


@app.get("/", response_model=dict)
async def root():
    """Root endpoint with API information"""
    return {
        "message": "ML Reasoning System API",
        "version": "1.0.0",
        "docs": "/docs",
        "health": "/health",
        "endpoints": {
            "solve": "POST /solve - Solve a reasoning problem",
            "health": "GET /health - Health check"
        }
    }


@app.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy" if pipeline else "unhealthy",
        "version": "1.0.0",
        "timestamp": datetime.now().isoformat()
    }


@app.post("/solve", response_model=ReasoningResponse)
async def solve_problem(request: ReasoningRequest):
    """
    Solve a reasoning problem
    
    Takes a question and 5 answer options, returns the predicted answer with reasoning.
    
    - **question**: The problem statement (minimum 10 characters)
    - **options**: Exactly 5 answer options as a list
    
    Returns the predicted answer (1-5), confidence score, and detailed reasoning.
    """
    if pipeline is None:
        raise HTTPException(status_code=503, detail="Pipeline not initialized")
    
    try:
        # Validate options
        if len(request.options) != 5:
            raise HTTPException(
                status_code=400,
                detail=f"Expected exactly 5 options, got {len(request.options)}"
            )
        
        # Process the problem
        result = pipeline.process_single_problem(
            problem=request.question,
            options=request.options
        )
        
        # Get the answer text
        answer_index = result['predicted_answer'] - 1  # Convert to 0-indexed
        if 0 <= answer_index < len(request.options):
            answer_text = request.options[answer_index]
        else:
            answer_text = "Invalid answer index"
        
        # Build response
        response = {
            "predicted_answer": result['predicted_answer'],
            "answer_text": answer_text,
            "confidence": result['confidence'],
            "reasoning": result['reasoning'],
            "category": result['category'],
            "category_confidence": result['category_confidence'],
            "timestamp": datetime.now().isoformat()
        }
        
        return response
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error processing request: {str(e)}"
        )


@app.post("/batch-solve", response_model=List[ReasoningResponse])
async def batch_solve(requests: List[ReasoningRequest]):
    """
    Solve multiple reasoning problems in batch
    
    Takes a list of questions and their options, returns predictions for all.
    """
    if pipeline is None:
        raise HTTPException(status_code=503, detail="Pipeline not initialized")
    
    if len(requests) > 100:
        raise HTTPException(
            status_code=400,
            detail="Maximum 100 requests allowed in batch"
        )
    
    results = []
    
    for req in requests:
        try:
            result = pipeline.process_single_problem(
                problem=req.question,
                options=req.options
            )
            
            answer_index = result['predicted_answer'] - 1
            answer_text = req.options[answer_index] if 0 <= answer_index < len(req.options) else "Invalid"
            
            results.append({
                "predicted_answer": result['predicted_answer'],
                "answer_text": answer_text,
                "confidence": result['confidence'],
                "reasoning": result['reasoning'],
                "category": result['category'],
                "category_confidence": result['category_confidence'],
                "timestamp": datetime.now().isoformat()
            })
        except Exception as e:
            # Add error entry
            results.append({
                "predicted_answer": 3,
                "answer_text": "Error",
                "confidence": 0.0,
                "reasoning": f"Error: {str(e)}",
                "category": "Unknown",
                "category_confidence": 0.0,
                "timestamp": datetime.now().isoformat()
            })
    
    return results


def run_server(host: str = "0.0.0.0", port: int = 8000, reload: bool = False):
    """
    Run the API server
    
    Args:
        host: Host to bind to
        port: Port to listen on
        reload: Enable auto-reload for development
    """
    uvicorn.run(
        "api:app",
        host=host,
        port=port,
        reload=reload,
        log_level="info"
    )


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="ML Reasoning System API Server")
    parser.add_argument("--host", type=str, default="0.0.0.0", help="Host to bind to")
    parser.add_argument("--port", type=int, default=8000, help="Port to listen on")
    parser.add_argument("--reload", action="store_true", help="Enable auto-reload")
    
    args = parser.parse_args()
    
    print("="*80)
    print("ML REASONING SYSTEM API")
    print("="*80)
    print(f"Starting server on http://{args.host}:{args.port}")
    print(f"API Documentation: http://{args.host}:{args.port}/docs")
    print(f"Alternative Docs: http://{args.host}:{args.port}/redoc")
    print("="*80)
    
    run_server(host=args.host, port=args.port, reload=args.reload)

