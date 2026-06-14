import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


class EnvConfig:
    """
    FSE Environment Configuration
    Secure API and system credentials
    """

    # Exchange API
    API_KEY = os.getenv("API_KEY")
    SECRET_KEY = os.getenv("SECRET_KEY")

    # Telegram Bot
    TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
    AUTHORIZED_USER = os.getenv("AUTHORIZED_USER")

    @classmethod
    def validate(cls):
        """
        Check required environment variables
        """
        required = [
            "API_KEY",
            "SECRET_KEY",
            "TELEGRAM_TOKEN",
            "AUTHORIZED_USER"
        ]

        missing = [
            key for key in required
            if not os.getenv(key)
        ]

        if missing:
            raise EnvironmentError(
                f"Missing environment variables: {', '.join(missing)}"
            )

        return True
# Validate environment variables on startup (recommended for safety)
EnvConfig.validate()
