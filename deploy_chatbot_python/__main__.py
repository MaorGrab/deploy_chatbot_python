from deploy_chatbot_python.launcher import Launcher
import deploy_chatbot_python.utils.load_env  # pylint: disable=unused-import


def main() -> None:
    launcher = Launcher()
    launcher.run()

if __name__ == "__main__":
    main()
