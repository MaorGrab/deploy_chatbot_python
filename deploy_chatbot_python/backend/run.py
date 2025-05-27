import uvicorn

from deploy_chatbot_python.backend.server import api  # pylint: disable=unused-import
from deploy_chatbot_python.config import constants

if __name__ == "__main__":
    uvicorn.run(
        "run:api",
        host=constants.API_HOST_ADDRESS,
        port=constants.API_HOST_PORT,
        reload=True
    )
