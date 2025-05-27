import uvicorn

from deploy_chatbot_python.backend.server import api  # pylint: disable=unused-import
from deploy_chatbot_python.config import constants


def main() -> None:
    uvicorn.run(
        "run:api",
        host=constants.API_HOST_ADDRESS,
        port=constants.API_HOST_PORT,
        reload=True
    )

if __name__ == "__main__":
    main()
