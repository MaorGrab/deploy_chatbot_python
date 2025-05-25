from typing import Union
from dataclasses import dataclass, field

from src.chatbot.openai_params import OpenAIParams
import src.config.constants as constants

from llama_index.core.base.response.schema import Response
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader
from llama_index.embeddings.openai import OpenAIEmbedding
from llama_index.llms.openai import OpenAI


@dataclass
class LlamaIndexer:
    index: Union[VectorStoreIndex, None] = field(default=None, init=False)
    llm: Union[OpenAI, None] = field(default=None, init=False)
    embedding_model: Union[OpenAIEmbedding, None] = field(default=None, init=False)

    def __post_init__(self):
        openai_params = OpenAIParams.from_config_yaml()
        self._initialize_models_from_params(openai_params)
    
    def _initialize_models_from_params(self, params: OpenAIParams) -> None:
        self.llm = OpenAI(model=params.model, temperature=params.temperature)
        self.embedding_model = OpenAIEmbedding(model=params.embedding_model)

    def build_index(self) -> None:
        documents = SimpleDirectoryReader(
            constants.Data.TRAINING_DATA_PATH,
            recursive=True
        ).load_data()
        self.index = VectorStoreIndex.from_documents(
            documents=documents,
            llm=self.llm,
            embed_model=self.embedding_model,
        )

    def _query(self, question: str) -> Response:
        response: Response = self.index.as_query_engine().query(question)
        return response
    
    def _verbose_query(self, question: str) -> None:
        response: Response = self._query(question)
        print('-' * 50)
        print(f"Question: {question}")
        print(f"Response: {response}")
        print('-' * 50)


if __name__ == "__main__":
    llama_indexer = LlamaIndexer()
    llama_indexer.build_index()
    llama_indexer._verbose_query("What types of dogs do you know?")
    llama_indexer._verbose_query("What is a cabbage? Elaborate.")

    # --------------------------------------------------
    # Question: What types of dogs do you know?
    # Response: Cabbage is a type of dog mentioned in the provided context.
    # --------------------------------------------------
    # --------------------------------------------------
    # Question: What is a cabbage? Elaborate.
    # Response: A cabbage is described as a type of dog in the provided context.
    # It is characterized by having five legs and two tails,
    # and is known to be very friendly and smart.
    # --------------------------------------------------
