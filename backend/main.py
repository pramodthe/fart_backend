from fastapi import FastAPI, File, UploadFile, Form, HTTPException
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
import os
import tempfile
import uuid
from pathlib import Path

# Import the fart generation functionality
from fart_generator import generate_fart_sound

app = FastAPI(
    title="Fart Sound Generator API",
    description="API for generating fart sounds based on type and user input",
    version="1.0.0"
)

# Add CORS middleware for Next.js frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",  # Default Next.js development server
        "http://localhost:3001",  # Alternative Next.js development server
        "https://your-nextjs-app.vercel.app",  # Production Next.js app on Vercel
        "https://yourdomain.com"  # Your custom domain
    ],  # Add your actual Next.js app URLs in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class FartRequest(BaseModel):
    fart_type: str
    user_input: str = "Hello! how are you"


@app.get("/")
def read_root():
    return {"message": "Welcome to the Fart Sound Generator API"}


@app.post("/generate-fart/")
async def generate_fart(fart_request: FartRequest):
    """
    Generate a fart sound based on the specified type and user input.
    
    Args:
        fart_type (str): Type of fart to generate ('human', 'dog', 'ai', etc.)
        user_input (str): User input to determine length of fart sound
    
    Returns:
        FileResponse: The generated MP3 file
    """
    try:
        # Validate fart_type
        valid_types = ["human", "dog", "ai", "you"]
        if fart_request.fart_type.lower() not in valid_types:
            fart_request.fart_type = "human"  # Default to human if invalid type provided
        
        # Generate the fart sound
        output_file = generate_fart_sound(fart_request.fart_type, fart_request.user_input)
        
        # Return the generated file
        file_path = Path(output_file)
        if not file_path.exists():
            raise HTTPException(status_code=500, detail="Generated file not found")
        
        return FileResponse(
            path=file_path,
            media_type="audio/mpeg",
            filename=file_path.name
        )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating fart sound: {str(e)}")


@app.post("/generate-fart-url/")
async def generate_fart_url(fart_request: FartRequest):
    """
    Generate a fart sound and return a URL to download it.
    This endpoint is useful when you need to return a URL instead of the file directly.
    """
    try:
        # Validate fart_type
        valid_types = ["human", "dog", "ai", "you"]
        if fart_request.fart_type.lower() not in valid_types:
            fart_request.fart_type = "human"  # Default to human if invalid type provided
        
        # Generate the fart sound
        output_file = generate_fart_sound(fart_request.fart_type, fart_request.user_input)
        
        file_path = Path(output_file)
        if not file_path.exists():
            raise HTTPException(status_code=500, detail="Generated file not found")
        
        # In a real implementation, you'd have a URL endpoint to serve files
        # For now, we'll return the file path which your frontend can use
        return {
            "filename": file_path.name,
            "download_url": f"/download/{file_path.name}",
            "file_path": str(file_path)
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating fart sound: {str(e)}")


@app.get("/download/{filename}")
async def download_file(filename: str):
    """
    Download endpoint for generated files.
    """
    file_path = Path("uploads") / filename
    if not file_path.exists():
        raise HTTPException(status_code=404, detail="File not found")
    
    return FileResponse(
        path=file_path,
        media_type="audio/mpeg",
        filename=filename
    )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)