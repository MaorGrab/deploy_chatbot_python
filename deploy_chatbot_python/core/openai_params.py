from dataclasses import dataclass
import os
import yaml

from deploy_chatbot_python.config.constants import CONFIG_PATH
from deploy_chatbot_python.logging.logger_instance import log


@dataclass
class OpenAIParams:
    model: str
    embedding_model: str
    temperature: float

    def __post_init__(self) -> None:
        self.validate_api_key()

    @classmethod
    def from_config_yaml(cls) -> "OpenAIParams":
        with open(CONFIG_PATH, "r", encoding='utf-8') as file:
            config = yaml.safe_load(file)
        return cls(**config['openai'])

    @staticmethod
    def validate_api_key() -> None:
        api_key = os.getenv("OPENAI_API_KEY")
        if api_key is None:
            raise ValueError("API key not found. Please set `OPENAI_API_KEY` env variable.")
        log.debug('OPENAI_API_KEY was fetched from environment variables.')
