
import time
import logging

# Logger setup
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# =========================
# BACKUP SYSTEM
# =========================
class BackupManager:
    def __init__(self, storage):
        self.storage = storage 

    def perform_daily_backup(self, state):
        logger.info("💾 Daily backup started...")
        self.storage.save("daily_backup", state)

    def perform_weekly_full_backup(self, state):
        logger.info("☁️ Full system backup started...")
        self.storage.save("weekly_full_backup", state)

    def restore_from_disaster(self):
        logger.info("🚨 Restoring system state...")
        return self.storage.load("weekly_full_backup")


# =========================
# CLOUD MONITOR + RESILIENCE
# =========================
class CloudMonitor:
    MAX_RECONNECT_ATTEMPTS = 5

    def __init__(self, api_client):
        self.api_client = api_client
        self.reconnect_attempts = 0

    def safe_loop(self, fetch_data, symbol):
        """የገበያ መረጃን በጥንቃቄ ለመቀበል የሚያገለግል ሜተድ"""
        while self.reconnect_attempts < self.MAX_RECONNECT_ATTEMPTS:
            try:
                data = fetch_data(symbol)
                self.reset_reconnect_counter()
                return data

            except Exception as e:
                self.reconnect_attempts += 1
                logger.error(f"⚠️ API ERROR: {e} | Attempt: {self.reconnect_attempts}")
                
                self.recovery_system()
                time.sleep(5)
        
        logger.critical("🚨 SYSTEM SHUTDOWN: MAX RECONNECT ATTEMPTS REACHED")
        raise ConnectionError("Could not establish connection to market data after max retries.")

    def heartbeat(self):
        try:
            return self.api_client.get_price("BTCUSDT") is not None
        except Exception:
            return False

    def recovery_system(self):
        logger.info("🔁 ATTEMPTING RECOVERY...")
        # እዚህ ጋር እንደ አስፈላጊነቱ የAPI Client ዳግም ማስጀመሪያ ኮድ ይጨመራል
        time.sleep(2)

    def reset_reconnect_counter(self):
        self.reconnect_attempts = 0
