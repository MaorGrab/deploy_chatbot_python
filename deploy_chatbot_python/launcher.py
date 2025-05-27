import subprocess
import os
import signal
import sys
import time
import platform

from deploy_chatbot_python.config import constants


class Launcher:
    def __init__(self) -> None:
        self.processes = {}
        self.is_windows_os: bool = platform.system() == "Windows"

    @property
    def _new_process_kwarg(self) -> dict:
        if self.is_windows_os:
            return {"creationflags": subprocess.CREATE_NEW_PROCESS_GROUP}
        return {"start_new_session": True}

    def _launch_subprocess(self, cmd: list, name: str) -> None:
        print(f"[INFO] Launching {name}: {' '.join(cmd)}")
        try:
            process = subprocess.Popen(  # pylint: disable=consider-using-with
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                **self._new_process_kwarg,
            )
            self.processes[name] = process
        except Exception as e:  # pylint: disable=W0718 # critical on any exception
            print(f"[ERROR] Failed to launch {name}: {e}")
            self.stop_all()  # or any custom cleanup
            raise

    def start_api(self) -> None:
        cmd = [
            sys.executable, "-m", "uvicorn",
            "deploy_chatbot_python.backend.run:api",
            "--host", constants.API_HOST_ADDRESS,
            "--port", str(constants.API_HOST_PORT),
            "--reload"
        ]
        self._launch_subprocess(cmd, "FastAPI")

    def start_dash(self) -> None:
        cmd = [
            sys.executable, "-m", "deploy_chatbot_python.frontend.run"
        ]
        self._launch_subprocess(cmd, "Dash")

    def start_all(self) -> None:
        print("[INFO] Starting all servers...")
        self.start_api()
        self.start_dash()

    def stop_all(self) -> None:
        print("[INFO] Stopping all servers...")
        for name, process in self.processes.items():
            if process.poll() is None:  # Still running
                print(f"[INFO] Terminating {name} (PID {process.pid})...")
                try:
                    self._graceful_stop_process(process)
                except Exception as e:  # pylint: disable=W0718 # critical on any exception
                    print(f"[WARN] Could not terminate {name}: {e}")
                    try:
                        process.kill()
                    except Exception as e_:  # pylint: disable=W0718 # critical on any exception
                        print(f"[WARN] Could not terminate {name} with `.kill()` fallback: {e_}")
            else:
                print(f"[INFO] {name} already exited.")

    def _graceful_stop_process(self, process: subprocess.Popen) -> None:
        # pylint: disable=no-member  # available at either on Win or Unix systems, not both
        if self.is_windows_os:
            process.send_signal(signal.CTRL_BREAK_EVENT)
        else:
            os.killpg(os.getpgid(process.pid), signal.SIGTERM)
        process.wait(timeout=5)

    def _monitor(self) -> None:
        """Monitor subprocesses for failure."""
        while True:
            for name, proc in self.processes.items():
                retcode = proc.poll()
                if retcode is not None:
                    raise RuntimeError(f"[ERROR] {name} exited unexpectedly with code {retcode}")
            time.sleep(1)

    def run(self) -> None:
        try:
            self.start_all()
            self._monitor()
        except KeyboardInterrupt:
            print("\n[INFO] KeyboardInterrupt received. Shutting down...")
        except (OSError,ValueError,subprocess.SubprocessError,TimeoutError,PermissionError) as e:
            print(f"[ERROR] Process management error: {e}")
        except Exception as e:  # pylint: disable=W0718 # critical on any exception
            print(f"[ERROR] Exception occurred: {e}")
        finally:
            self.stop_all()
