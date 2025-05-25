import os
import json
import hashlib
from typing import Union
from dataclasses import dataclass, field
from llama_index.core import StorageContext, load_index_from_storage

from deploy_chatbot_python.chatbot.llama_indexer import LlamaIndexer
import deploy_chatbot_python.config.constants as constants

@dataclass
class IndexManager:
    llama_indexer: LlamaIndexer = field(default_factory=LlamaIndexer, init=False)
    _current_data_hash: Union[str, None] = field(default=None, init=False)

    def __post_init__(self):
        self._initialize()
    
    def _initialize(self):
        self._compute_data_hash()
        if self._is_index_valid():
            self._load_index()
        else:
            self._save_data_hash()
            self._rebuild_index()
            self._save_index()

    def _is_index_valid(self) -> bool:
        saved_data_hash = self._load_data_hash()
        return self._current_data_hash == saved_data_hash
    
    def _get_files_in_training_data_dir(self) -> dict:
        return {
            entry.path: entry.stat().st_mtime
            for entry in os.scandir(constants.Data.TRAINING_DATA_PATH)
            if entry.is_file()
        }

    def _compute_data_hash(self) -> None:
        training_files: dict = self._get_files_in_training_data_dir()
        # Serialize dictionary with sorted keys to ensure consistency
        serialized: str = json.dumps(training_files, sort_keys=True)
        self._current_data_hash = hashlib.sha256(serialized.encode()).hexdigest()
    
    def _load_data_hash(self) -> str:
        if not os.path.exists(constants.Data.TRAINING_DATA_HASH_PATH):
            return ""
        with open(constants.Data.TRAINING_DATA_HASH_PATH, "r") as file:
            return file.read().strip()
    
    def _save_data_hash(self) -> None:
        with open(constants.Data.TRAINING_DATA_HASH_PATH, "w") as file:
            file.write(self._current_data_hash)

    def _rebuild_index(self):
        self.llama_indexer.build_index()

    def _save_index(self):
        self.llama_indexer.index.storage_context.persist(constants.Data.INDEX_STORE_PATH)

    def _load_index(self):
        storage_context = StorageContext.from_defaults(persist_dir=constants.Data.INDEX_STORE_PATH)
        self.llama_indexer.index = load_index_from_storage(storage_context)

if __name__ == '__main__':
    mgr = IndexManager()
