from deploy_chatbot_python.launcher import Launcher
from deploy_chatbot_python.logger_instance import logger_

def main() -> None:
    logger_.info('main run')
    launcher = Launcher()
    launcher.run()

if __name__ == "__main__":
    main()
