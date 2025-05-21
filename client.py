from dataclasses import dataclass
import requests

@dataclass
class ChatbotClient:
    url: str
    timeout: int = 60

    def ask(self, query: str) -> str:
        try:
            response = requests.post(self.url, json={'text': query}, timeout=self.timeout)
            response.raise_for_status()
            data = response.json()
            return data.get("response", {}).get("response", "No response found.")
        except requests.exceptions.RequestException as e:
            return f"Request error: {e}"
        except ValueError:
            return "Invalid JSON response."
        except Exception as e:
            raise RuntimeError(f"Unexpected error: {e}") from e

if __name__ == "__main__":
    client = ChatbotClient(url="http://localhost:8000/query")
    result = client.ask("What is the cabbage?")
    print("Response:", result)
