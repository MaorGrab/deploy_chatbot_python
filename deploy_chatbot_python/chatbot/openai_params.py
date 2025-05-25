from dataclasses import dataclass
import os
import yaml

from deploy_chatbot_python.config.constants import Config


@dataclass
class OpenAIParams:
    model: str
    embedding_model: str
    temperature: float

    def __post_init__(self) -> None:
        self.validate_api_key()

    @classmethod
    def from_config_yaml(cls) -> "OpenAIParams":
        with open(Config.PATH, "r") as file:
            config = yaml.safe_load(file)
        return cls(**config['openai'])

    @staticmethod
    def validate_api_key() -> None:
        api_key = os.getenv("OPENAI_API_KEY")
        if api_key is None:
            raise ValueError("API key not found. Please set `OPENAI_API_KEY` env variable.")
