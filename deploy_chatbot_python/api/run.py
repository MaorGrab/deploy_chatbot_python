import uvicorn

from deploy_chatbot_python.api.server import api  # pylint: disable=unused-import
import deploy_chatbot_python.config.constants as constants 

if __name__ == "__main__":
    uvicorn.run(
        "run:api",
        host=constants.API_HOST_ADDRESS,
        port=constants.API_HOST_PORT,
        reload=True
    )
