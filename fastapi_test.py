import requests

# Define the URL of the API endpoint
url = "http://127.0.0.1:8000/sum"

# Define the payload with the two numbers
payload = {
    "number_1": 5,
    "number_2": 7
}

try:
    # Send a POST request with the JSON payload
    response = requests.post(url, json=payload)

    # Check if the request was successful
    if response.status_code == 200:
        # Parse the JSON response
        result = response.json()
        print("Sum:", result.get("result"))
    else:
        print(f"Request failed with status code {response.status_code}: {response.text}")
except requests.exceptions.RequestException as e:
    print(f"An error occurred: {e}")
