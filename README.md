# Fart Sound Generator API

This is a FastAPI backend for generating fart sounds based on type and user input. It integrates with a Next.js frontend to provide audio generation capabilities.

## Features

- Generate different types of fart sounds (human, dog, AI/robot)
- Accepts user input to customize the fart sound
- File management and cleanup
- CORS configured for Next.js integration
- Support for both mock audio (for testing) and real audio generation (production)

## Requirements

- Python 3.7+
- FastAPI
- Uvicorn
- Replicate (for production audio generation)

## Installation

1. Install dependencies:

```bash
pip install -r backend/requirements.txt
```

2. Set up your environment variables in a `.env` file:

```
REPLICATE_API_TOKEN="your_replicate_api_token_here"
USE_MOCK_AUDIO="true"  # Set to "false" for production
```

## Running the Server

To run in development mode with mock audio (to avoid API rate limits):

```bash
cd backend
USE_MOCK_AUDIO=true uvicorn main:app --reload
```

For production with real audio generation:

```bash
cd backend
USE_MOCK_AUDIO=false uvicorn main:app --host 0.0.0.0 --port 8000
```

## API Endpoints

### POST /generate-fart/

Generate a fart sound based on the specified type and user input.

**Request Body:**
```json
{
  "fart_type": "human",
  "user_input": "Hello! how are you"
}
```

**Valid fart types:** `human`, `dog`, `ai`, `you`

**Response:** Returns the generated MP3 file directly.

### POST /generate-fart-url/

Generate a fart sound and return a URL to download it.

**Request Body:**
```json
{
  "fart_type": "dog",
  "user_input": "Testing dog fart"
}
```

**Response:**
```json
{
  "filename": "output_20251025_160423.mp3",
  "download_url": "/download/output_20251025_160423.mp3",
  "file_path": "uploads/output_20251025_160423.mp3"
}
```

### GET /download/{filename}

Download a previously generated audio file.

## Next.js Frontend Integration

To integrate with your Next.js frontend:

1. Make POST requests to `http://localhost:8000/generate-fart/` with the fart_type and user_input
2. Handle the returned MP3 file as needed in your frontend

Example:
```javascript
const response = await fetch('http://localhost:8000/generate-fart/', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({
    fart_type: 'human',
    user_input: 'Hello world'
  })
});

const audioBlob = await response.blob();
const audioUrl = URL.createObjectURL(audioBlob);
```

## File Management

Generated audio files are stored in the `uploads/` directory. Old files are automatically cleaned up to prevent disk space issues.