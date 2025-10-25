import requests
import json

# Test the FastAPI endpoints
BASE_URL = "http://localhost:8000"

def test_generate_fart():
    """Test the generate-fart endpoint"""
    url = f"{BASE_URL}/generate-fart/"
    
    # Test data
    payload = {
        "fart_type": "human",
        "user_input": "Hello! How are you?"
    }
    
    
    print("Testing /generate-fart/ endpoint...")
    try:
        response = requests.post(url, json=payload)
        print(f"Status Code: {response.status_code}")
        print(f"Response Headers: {response.headers}")
        
        if response.status_code == 200:
            # Save the audio file
            with open("test_output.mp3", "wb") as f:
                f.write(response.content)
            print("Audio file saved as test_output.mp3")
        else:
            print(f"Error Response: {response.text}")
    
    except Exception as e:
        print(f"Error occurred: {e}")

def test_generate_fart_url():
    """Test the generate-fart-url endpoint"""
    url = f"{BASE_URL}/generate-fart-url/"
    
    # Test data
    payload = {
        "fart_type": "dog",
        "user_input": "Testing dog fart"
    }
    
    print("\nTesting /generate-fart-url/ endpoint...")
    try:
        response = requests.post(url, json=payload)
        print(f"Status Code: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
    
    except Exception as e:
        print(f"Error occurred: {e}")

if __name__ == "__main__":
    test_generate_fart()
    test_generate_fart_url()