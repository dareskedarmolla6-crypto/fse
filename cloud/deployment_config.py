import time
import psutil
import os
import logging


# =========================
# PRODUCTION MONITOR
# =========================
class ProductionMonitor:
    def __init__(self, restart_callback=None):
        self.restart_callback = restart_callback
        self.last_heartbeat = time.time()

    # -------------------------
    # SYSTEM HEALTH TRACKING
    # -------------------------
    def track_system_health(self):
        health = {
            "cpu": psutil.cpu_percent(interval=1),
            "memory": psutil.virtual_memory().percent,
            "disk": psutil.disk_usage("/").percent,
            "uptime": time.time() - self.last_heartbeat
        }

        print(f"[HEALTH] CPU:{health['cpu']}% MEM:{health['memory']}% DISK:{health['disk']}%")
        return health

    # -------------------------
    # BOT LOOP MONITORING
    # -------------------------
    def monitor_bot_loop(self, last_trade_ts, timeout=30):
        now = time.time()

        if now - last_trade_ts > timeout:
            print("⚠️ BOT STALLED DETECTED")

            if self.restart_callback:
                print("♻️ Triggering auto recovery...")
                self.restart_callback()

            return False

        return True

    # -------------------------
    # AUTO RECOVERY HANDLER
    # -------------------------
    def trigger_auto_recovery(self):
        print("🔁 Auto recovery triggered")

        try:
            os.system("pkill -f main.py")
            os.system("python3 main.py &")
        except Exception as e:
            logging.error(f"Recovery failed: {e}")


# =========================
# CLOUD SYSTEM CORE STATE
# =========================
class F44Core:
    def __init__(self):
        self.running = False
        self.balance = 1000
        self.positions = {}
        self.last_risk = "LOW_RISK"
        self.last_trade_ts = time.time()

    def update_trade_time(self):
        self.last_trade_ts = time.time()

    def risk_state(self):
        return self.last_risk

    def set_risk(self, level):
        self.last_risk = level
