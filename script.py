from openai import OpenAI, RateLimitError
from dotenv import load_dotenv
import os


load_dotenv()

def validate_api_key(api_key):
    api_key = os.getenv("OPENAI_API_KEY")
    if api_key is None:
        raise ValueError("API key not found. Please set the OPENAI_API_KEY environment variable.")


def make_api_call():
    client = OpenAI()
    try:
        response = client.responses.create(
            model="gpt-4.1",
            input="Write a one-sentence bedtime story about a unicorn."
        )
        print(response.output_text)
    except RateLimitError as e:
        print("Rate limit exceeded. Please try again later.")
        print(f"Error details: {e}")

if __name__ == "__main__":
    validate_api_key(os.getenv("OPENAI_API_KEY"))
    make_api_call()