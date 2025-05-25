from pathlib import Path
from dataclasses import dataclass
from deploy_chatbot_python import ROOT_DIR, PKG_DIR

class Data:
    _DATA_PATH: Path = ROOT_DIR / 'data'
    TRAINING_DATA_PATH: Path = _DATA_PATH / 'training'
    TRAINING_DATA_HASH_PATH: Path = _DATA_PATH / 'training_data_hash.txt'
    INDEX_STORE_PATH: Path = _DATA_PATH / 'index_storage'

class Config:
    _NAME: str = 'config.yaml'
    PATH: Path = PKG_DIR / 'config' / _NAME

# @dataclass
# class Directory:
#     NAME: str

    
#     def __post_init__(self):
#         self.PATH: Path = 
