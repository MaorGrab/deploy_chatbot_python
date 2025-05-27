from pathlib import Path


PKG_DIR = Path(__file__).resolve().parent.parent
ROOT_DIR = PKG_DIR.parent

# Data paths
DATA_PATH = ROOT_DIR / 'data'
TRAINING_DATA_PATH = DATA_PATH / 'training'
TRAINING_DATA_HASH_PATH = DATA_PATH / 'training_data_hash.txt'
INDEX_STORE_PATH = DATA_PATH / 'index_storage'

# Config path
CONFIG_NAME = 'config.yaml'
CONFIG_PATH = PKG_DIR / 'config' / CONFIG_NAME

# API
API_HOST_ADDRESS = '127.0.0.1'
API_HOST_PORT = 8000
API_POST_ENDPOINT = 'query'
API_POST_ENDPOINT_URL = f"http://{API_HOST_ADDRESS}:{API_HOST_PORT}/{API_POST_ENDPOINT}"

# APP
APP_TITLE = "Chatbot Dashboard"
DASHBOARD_TITLE = "🤖 Chatbot Interface"
BOT_PLACEHOLDER_MESSAGE = 'Typing...'
USER_PLACEHOLDER_MESSAGE = "Type your message here..."
SEND_BUTTON_TEXT = 'Send'
POST_REQUEST_TIMEOUT = 60  # seconds
