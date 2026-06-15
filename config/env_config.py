
import os
import logging
from dotenv import load_dotenv

# Logger setup
logger = logging.getLogger(__name__)

# Load .env file safely
load_dotenv()

class EnvConfig:
    """
    FSE Environment Configuration
    ለደህንነቱ የተጠበቀ የኤፒአይ እና የስርዓት ምስክርነቶች (Credentials)።
    """

    # Exchange API
    BINANCE_API_KEY = os.getenv("BINANCE_API_KEY")
    BINANCE_API_SECRET = os.getenv("BINANCE_API_SECRET")

    # Telegram Bot
    TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
    AUTHORIZED_USER = os.getenv("AUTHORIZED_USER")
    
    # Environment mode (Production/Development)
    ENV = os.getenv("ENV", "production")

    @classmethod
    def validate(cls):
        """የሚያስፈልጉ የኤንቫይሮመንት ቫሪያብሎች መኖራቸውን ማረጋገጥ።"""
        required = [
            "BINANCE_API_KEY",
            "BINANCE_API_SECRET",
            "TELEGRAM_TOKEN",
            "AUTHORIZED_USER"
        ]

        missing = [key for key in required if not os.getenv(key)]

        if missing:
            error_msg = f"❌ Missing required environment variables: {', '.join(missing)}"
            logger.critical(error_msg)
            raise EnvironmentError(error_msg)

        logger.info("✅ All environment variables validated successfully.")
        return True

# ቦቱ ሲነሳ በራስ-ሰር ደህንነትን ማረጋገጥ
EnvConfig.validate()
