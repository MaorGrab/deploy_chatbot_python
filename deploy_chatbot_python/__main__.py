from dotenv import load_dotenv
from deploy_chatbot_python.launcher import Launcher

load_dotenv()  # load OpenAI API key from .env file


def main() -> None:
    launcher = Launcher()
    launcher.run()

if __name__ == "__main__":
    main()
