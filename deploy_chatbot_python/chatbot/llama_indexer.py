from typing import Union
from dataclasses import dataclass, field

from deploy_chatbot_python.chatbot.openai_params import OpenAIParams
import deploy_chatbot_python.config.constants as constants

from llama_index.core import VectorStoreIndex, SimpleDirectoryReader
from llama_index.core.base.base_query_engine import BaseQueryEngine
from llama_index.embeddings.openai import OpenAIEmbedding
from llama_index.llms.openai import OpenAI


@dataclass
class LlamaIndexer:
    index: Union[VectorStoreIndex, None] = field(default=None, init=False)
    query_engine: Union[BaseQueryEngine, None] = field(default=None, init=False)
    llm: Union[OpenAI, None] = field(default=None, init=False)
    embedding_model: Union[OpenAIEmbedding, None] = field(default=None, init=False)

    def __post_init__(self):
        openai_params = OpenAIParams.from_config_yaml()
        self._initialize_models_from_params(openai_params)
    
    def _initialize_models_from_params(self, params: OpenAIParams) -> None:
        self.llm = OpenAI(model=params.model, temperature=params.temperature)
        self.embedding_model = OpenAIEmbedding(model=params.embedding_model)

    def build_query_pipeline(self) -> None:
        self._build_index()
        self.set_query_engine()

    def _build_index(self) -> None:
        documents = SimpleDirectoryReader(
            constants.TRAINING_DATA_PATH,
            recursive=True
        ).load_data()
        self.index = VectorStoreIndex.from_documents(
            documents=documents,
            embed_model=self.embedding_model,
        )

    def set_query_engine(self) -> None:
        if self.index is None:
            raise ValueError("Index is invalid.")
        if self.query_engine is not None:
            raise ValueError("Query engine is already set.")  # TODO: log warning
        self.query_engine = self.index.as_query_engine(llm=self.llm)


if __name__ == "__main__":
    llama_indexer = LlamaIndexer()
    llama_indexer.build_query_pipeline()
