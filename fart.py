import replicate
import datetime
from typing import Optional


def generate_fart_sound(fart_type: str, user_input: str = "Hello! how are you") -> str:
    """
    Generate a fart sound based on the specified type.
    
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

    elif fart_type == "ai":  # Changed to lowercase for consistency
        prompt = f"Create a sound for a AI/robot fart, the fart sound should have a robotic tone with electronic buzz, metallic echo, and synthetic processing like a computer-generated voice speaking through a robot. The fart must respond be to the length of {user_input}"

    elif fart_type == "you":  # Changed to lowercase for consistency
        prompt = f"Create a sound for a human fart, at first the fart sound the loudest like a bomb blast and the fart must respond be to the length of {user_input}"

    else:
        # Default case for any other input, including "robot"
        prompt = f"Create a sound for a human fart, at first the fart sound the loudest like a bomb blast and the fart must respond be to the length of {user_input}"

    def sound_gen(f_prompt):
        input_data = {
            "prompt": f_prompt,
            "duration": 5,
            "output_format": "mp3"
        }

        output = replicate.run(
            "sepal/audiogen:154b3e5141493cb1b8cec976d9aa90f2b691137e39ad906d2421b74c2a8c52b8",
            input=input_data
        )
        return output

    output_gen = sound_gen(prompt)
    
    # Generate unique filename with timestamp
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"output_{timestamp}.mp3"

    # To write the file to disk:
    with open(filename, "wb") as file:
        file.write(output_gen.read())
    
    return filename


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

