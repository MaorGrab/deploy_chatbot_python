import os
from dataclasses import dataclass

from llama_index.core.base.response.schema import Response
from llama_index.core.query_engine.retriever_query_engine import RetrieverQueryEngine
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader, Settings
from llama_index.embeddings.openai import OpenAIEmbedding
from llama_index.llms.openai import OpenAI
from dotenv import load_dotenv
from typing import Optional

load_dotenv()


@dataclass
class OpenAIConfig:
    model: str = "gpt-4o-mini"
    embbedding_model: str = "text-embedding-3-small"
    temperature: float = 0.1

    def __post_init__(self) -> None:
        # Set custom LLM and embedding models
        Settings.llm = OpenAI(model=OpenAIConfig.model, temperature=OpenAIConfig.temperature)
        Settings.embed_model = OpenAIEmbedding(model=OpenAIConfig.embbedding_model)

@dataclass
class LlamaIndexer:
    data_dir: Optional[str] = "data"
    index_storage: Optional[str] = "index_storage"
    index: Optional[VectorStoreIndex] = None
    query_engine: Optional[RetrieverQueryEngine] = None

    def __post_init__(self) -> None:
        self.validate_api_key()
        self.build_index()

    @staticmethod
    def validate_api_key() -> None:
        api_key = os.getenv("OPENAI_API_KEY")
        if api_key is None:
            raise ValueError("API key not found. Please set the OPENAI_API_KEY environment variable.")

    def build_index(self) -> None:
        documents = SimpleDirectoryReader(self.data_dir, recursive=True).load_data()
        self.index = VectorStoreIndex.from_documents(documents)
        self.query_engine = self.index.as_query_engine()

    def query(self, question: str) -> Response:
        if not self.query_engine:
            raise RuntimeError("Index not built. Call build_index() first.")
        response: Response = self.query_engine.query(question)
        return response

    def save_index(self):
        if not self.index:
            raise RuntimeError("Index not built. Call build_index() first.")
        self.index.storage_context.persist(self.index_storage)

    def verbose_query(self, question: str) -> None:
        response: Response = self.query(question)
        print('-' * 50)
        print(f"Question: {question}")
        print(f"Response: {response}")
        print('-' * 50)



if __name__ == "__main__":
    llama_indexer = LlamaIndexer()
    llama_indexer.verbose_query("What types of dogs do you know?")
    llama_indexer.verbose_query("What is a cabbage? Elaborate.")

    '''
    --------------------------------------------------
    Question: What types of dogs do you know?
    Response: Cabbage is a type of dog mentioned in the provided context.
    --------------------------------------------------
    --------------------------------------------------
    Question: What is a cabbage? Elaborate.
    Response: A cabbage is described as a type of dog in the provided context. It is characterized by having five legs and two tails, and is known to be very friendly and smart.
    --------------------------------------------------
    '''
