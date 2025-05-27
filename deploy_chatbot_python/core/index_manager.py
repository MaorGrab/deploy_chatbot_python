import os
import json
import hashlib
from typing import Union
from dataclasses import dataclass, field
from llama_index.core import StorageContext, load_index_from_storage
from llama_index.core.base.response.schema import Response

from deploy_chatbot_python.core.llama_indexer import LlamaIndexer
from deploy_chatbot_python.config import constants
from deploy_chatbot_python.logging.logger_instance import log


@dataclass
class IndexManager:
    llama_indexer: LlamaIndexer = field(default_factory=LlamaIndexer, init=False)
    _current_data_hash: Union[str, None] = field(default=None, init=False)

    def __post_init__(self):
        self._initialize()

    def _initialize(self):
        log.debug('Initializing IndexManager')
        self._compute_data_hash()
        if self._is_index_outdated():
            self._save_data_hash()
            self._rebuild_index()
            self._save_index()
        else:
            self._load_index()

    def _is_index_outdated(self) -> bool:
        saved_data_hash = self._load_data_hash()
        is_outdated: bool = self._current_data_hash != saved_data_hash
        log.debug('Index storage is outdated' if is_outdated else 'Index storage is up-to-date')
        return is_outdated

    def _get_files_in_training_data_dir(self) -> dict:
        return {
            entry.path: entry.stat().st_mtime
            for entry in os.scandir(constants.TRAINING_DATA_PATH)
            if entry.is_file()
        }

    def _compute_data_hash(self) -> None:
        training_files: dict = self._get_files_in_training_data_dir()
        # Serialize dictionary with sorted keys to ensure consistency
        serialized: str = json.dumps(training_files, sort_keys=True)
        self._current_data_hash = hashlib.sha256(serialized.encode()).hexdigest()
        log.debug('Current data hash computed')

    def _load_data_hash(self) -> str:
        if not os.path.exists(constants.TRAINING_DATA_HASH_PATH):
            log.debug('No stored data hash found at: \n%s\n', constants.TRAINING_DATA_HASH_PATH)
            return ""
        with open(constants.TRAINING_DATA_HASH_PATH, "r", encoding='utf-8') as file:
            log.debug('Stored data hash found at: \n%s\n', constants.TRAINING_DATA_HASH_PATH)
            return file.read().strip()

    def _save_data_hash(self) -> None:
        with open(constants.TRAINING_DATA_HASH_PATH, "w", encoding='utf-8') as file:
            file.write(self._current_data_hash)
        log.debug('Data hash saved at: \n%s\n', constants.TRAINING_DATA_HASH_PATH)

    def _rebuild_index(self):
        self.llama_indexer.build_query_pipeline()

    def _save_index(self):
        self.llama_indexer.index.storage_context.persist(constants.INDEX_STORE_PATH)
        log.debug('Saved index storage')

    def _load_index(self):
        storage_context = StorageContext.from_defaults(persist_dir=constants.INDEX_STORE_PATH)
        self.llama_indexer.index = load_index_from_storage(storage_context)
        self.llama_indexer.set_query_engine()
        log.debug('Loaded index storage')

    def query(self, question: str) -> str:
        log.debug('Queried engine')
        if self.llama_indexer.query_engine is None:
            raise ValueError("Query engine is not set.")
        response: Response = self.llama_indexer.query_engine.query(question)
        return str(response)


if __name__ == '__main__':
    index_manager = IndexManager()
    print(index_manager.query("What types of dogs do you know?"))
    print(index_manager.query("What is a cabbage? Elaborate."))
