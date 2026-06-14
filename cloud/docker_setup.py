import os
import subprocess


class DockerSetup:
    """
    FSE Cloud Docker Setup
    - builds image
    - runs container
    - handles environment variables
    """

    def __init__(self, image_name="fse-bot", container_name="fse-container"):
        self.image_name = image_name
        self.container_name = container_name

    # =========================
    # BUILD IMAGE
    # =========================
    def build_image(self):
        print("🐳 Building Docker Image...")

        cmd = [
            "docker",
            "build",
            "-t",
            self.image_name,
            "."
        ]

        result = subprocess.run(cmd, capture_output=True, text=True)

        if result.returncode == 0:
            print("✅ Docker Image Built Successfully")
        else:
            print("❌ Build Failed")
            print(result.stderr)

    # =========================
    # RUN CONTAINER
    # =========================
    def run_container(self):
        print("🚀 Starting FSE Container...")

        env_vars = {
            "BINANCE_API_KEY": os.getenv("BINANCE_API_KEY", ""),
            "BINANCE_API_SECRET": os.getenv("BINANCE_API_SECRET", ""),
            "TELEGRAM_TOKEN": os.getenv("TELEGRAM_TOKEN", "")
        }

        env_flags = []
        for k, v in env_vars.items():
            env_flags += ["-e", f"{k}={v}"]

        cmd = [
            "docker",
            "run",
            "-d",
            "--name",
            self.container_name,
            *env_flags,
            self.image_name
        ]

        result = subprocess.run(cmd, capture_output=True, text=True)

        if result.returncode == 0:
            print("✅ Container Started Successfully")
            print("Container ID:", result.stdout.strip())
        else:
            print("❌ Container Failed to Start")
            print(result.stderr)

    # =========================
    # STOP CONTAINER
    # =========================
    def stop_container(self):
        print("🛑 Stopping Container...")

        cmd = ["docker", "stop", self.container_name]
        subprocess.run(cmd)

        cmd = ["docker", "rm", self.container_name]
        subprocess.run(cmd)

        print("✅ Container Stopped & Removed")


# =========================
# SIMPLE TEST RUN
# =========================
if __name__ == "__main__":
    setup = DockerSetup()

    setup.build_image()
    setup.run_container()
