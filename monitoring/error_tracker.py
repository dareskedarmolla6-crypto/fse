import logging
import time
import traceback


# =========================
# ERROR TRACKER / LOGGER
# =========================
class ErrorTracker:
    def __init__(self, store=None, alert_system=None):
        self.store = store
        self.alert_system = alert_system
        self.error_buffer = []

    def capture(self, error, context=None):
        error_data = {
            "timestamp": time.time(),
            "error": str(error),
            "context": context or {},
            "trace": traceback.format_exc()
        }

        self.error_buffer.append(error_data)

        logging.error(f"[FSE ERROR] {error_data['error']}")

        # store persistent log if available
        if self.store:
            self.store.save_error(error_data)

        # optional alert system (Telegram / webhook)
        if self.alert_system:
            try:
                self.alert_system.send_message(
                    f"🚨 ERROR: {error_data['error']}"
                )
            except Exception as e:
                logging.error(f"Alert system failed: {e}")

    def get_recent_errors(self, limit=20):
        return self.error_buffer[-limit:]

    def clear(self):
        self.error_buffer = []


# =========================
# SYSTEM HEALTH TRACKER
# =========================
class SystemHealthTracker:
    def __init__(self):
        self.start_time = time.time()
        self.error_count = 0
        self.last_heartbeat = time.time()

    def heartbeat(self):
        self.last_heartbeat = time.time()

    def record_error(self):
        self.error_count += 1

    def uptime(self):
        return time.time() - self.start_time

    def status(self):
        uptime = self.uptime()

        if self.error_count > 10:
            state = "UNSTABLE"
        elif uptime < 60:
            state = "WARMING_UP"
        else:
            state = "STABLE"

        return {
            "state": state,
            "uptime": uptime,
            "errors": self.error_count,
            "last_heartbeat": self.last_heartbeat
        }


# =========================
# SAFE EXECUTION WRAPPER
# =========================
class SafeExecutor:
    def __init__(self, error_tracker):
        self.error_tracker = error_tracker

    def run(self, fn, *args, **kwargs):
        try:
            return fn(*args, **kwargs)
        except Exception as e:
            self.error_tracker.capture(
                e,
                context={"fn": fn.__name__}
            )
            return None
