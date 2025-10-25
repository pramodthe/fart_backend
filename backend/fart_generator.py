import replicate
import datetime
import os
from typing import Optional
from pathlib import Path
from utils.file_manager import ensure_directory_exists
import requests
from dotenv import load_dotenv
import io

# Load environment variables
load_dotenv()

# Create uploads directory if it doesn't exist
UPLOADS_DIR = ensure_directory_exists(Path("uploads"))

# Create a mock MP3 file for testing purposes (since the Replicate API has rate limits)
def create_mock_mp3():
    """
    Create a simple mock MP3 file for testing.
    In a real implementation, you might want to use a library like `pydub` to generate actual audio.
    For now, this is just a placeholder to test the backend functionality.
    """
    # This creates a small file that has the appearance of an MP3 but is just placeholder data
    # The actual content would be a real MP3 file in production
    mock_mp3_content = (
        b'\x49\x44\x33\x03\x00\x00\x00\x00\x00' +  # Basic ID3 tag
        b'MOCK_FAKE_MP3_CONTENT_FOR_TESTING' * 100  # Placeholder content
    )
    return io.BytesIO(mock_mp3_content)


def generate_fart_sound(fart_type: str, user_input: str = "Hello! how are you") -> str:
    """
    Generate a fart sound based on the specified type.
    In production, this will use the Replicate API.
    For testing, this creates a mock MP3 file.
    
    Args:
        fart_type (str): Type of fart to generate ('human', 'dog', 'ai', etc.)
        user_input (str): User input to determine length of fart sound
    
    Returns:
        str: Path to the generated MP3 file
    """
    
    if fart_type == "human":
        prompt = f"Create a sound for a human fart, the fart must respond be to the length of {user_input}"

    elif fart_type == "dog":
        prompt = f"Create a sound for a dog fart, just a random fart sound like dog bark, the fart must respond be to the length of {user_input}"

    elif fart_type == "ai":
        prompt = f"Create a sound for a AI/robot fart, the fart sound should have a robotic tone with electronic buzz, metallic echo, and synthetic processing like a computer-generated voice speaking through a robot. The fart must respond be to the length of {user_input}"

    elif fart_type == "you":
        prompt = f"Create a sound for a human fart, at first the fart sound the loudest like a bomb blast and the fart must respond be to the length of {user_input}"

    else:
        # Default case for any other input, including "robot"
        prompt = f"Create a sound for a human fart, at first the fart sound the loudest like a bomb blast and the fart must respond be to the length of {user_input}"

    def sound_gen(f_prompt):
        # Check if we should use the actual Replicate API or mock for testing
        use_mock = os.getenv("USE_MOCK_AUDIO", "true").lower() == "true"
        
        if use_mock:
            # Return mock audio for testing to avoid API rate limits
            return create_mock_mp3()
        else:
            # Use the actual Replicate API (production)
            input_data = {
                "prompt": f_prompt,
                "duration": 5,
                "output_format": "mp3"
            }

            output = replicate.run(
                "sepal/audiogen:154b3e5141493cb1b8cec976d9aa90f2b691137e39ad906d2421b74c2a8c52b8",
                input=input_data
            )
            
            # Check the type of output from replicate.run
            if isinstance(output, list) and len(output) > 0:
                # If it's a list of URLs, get the first one
                url = output[0]
                response = requests.get(url)
                return response
            elif hasattr(output, 'read'):  # If it's already a file-like object
                return output
            elif isinstance(output, str):  # If it's a single URL string
                response = requests.get(output)
                return response
            else:
                # If we can't handle the output type, raise an error
                raise ValueError(f"Unexpected output type from replicate: {type(output)} - {output}")

    output_gen = sound_gen(prompt)
    
    # Generate unique filename with timestamp
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"output_{timestamp}.mp3"
    
    # Save to uploads directory
    file_path = UPLOADS_DIR / filename

    # To write the file to disk:
    with open(file_path, "wb") as file:
        file.write(output_gen.read())
    
    return str(file_path)


# Keep the original command-line functionality for backward compatibility
if __name__ == "__main__":
    try:
        fart_type = input("fart type (human/dog/AI/You): ").lower()
    except EOFError:
        # If no input is provided (like when running from command line), use default
        fart_type = "human"
        print("Using default fart type: human")
    
    user_input = "Hello! how are you"
    filename = generate_fart_sound(fart_type, user_input)
    print(f"=> {filename} written to disk")