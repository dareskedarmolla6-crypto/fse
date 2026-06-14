# fse/dashboard/app.py

from flask import Flask, jsonify


# =========================
# FLASK APPLICATION
# =========================
app = Flask(__name__)


# =========================
# GLOBAL SYSTEM STATE
# =========================
system_state = {
    "status": "RUNNING",
    "balance": 0.0,
    "total_trades": 0,
    "profit": 0.0,
    "market_mode": "LIVE",
    "bot_status": "ACTIVE",
    "risk_status": "MANAGED"
}


# =========================
# API ENDPOINTS
# =========================
@app.route("/status")
def status():
    return jsonify(system_state)


@app.route("/live")
def live():
    return jsonify({
        "market": system_state["market_mode"],
        "bot": system_state["bot_status"],
        "risk": system_state["risk_status"]
    })


# =========================
# SYSTEM STATE UPDATE
# =========================
def update_state(
    balance,
    trades,
    profit,
    status="RUNNING"
):
    system_state.update({
        "status": status,
        "balance": balance,
        "total_trades": trades,
        "profit": profit
    })


# =========================
# LIVE DASHBOARD CONTROLLER
# =========================
class LiveDashboard:
    def __init__(self, core):
        self.core = core


    def get_system_status(self):
        return {
            "bot": "RUNNING" if self.core.running else "STOPPED",
            "balance": self.core.balance
        }


    def update_panels(self):
        return {
            "balance": self.core.balance,
            "positions": getattr(self.core, "positions", []),
            "risk": getattr(self.core, "last_risk", "UNKNOWN")
        }


    def control_panel(self, command):
        commands = {
            "START": "BOT_STARTED",
            "STOP": "BOT_STOPPED",
            "SAFE_MODE": "SAFE_MODE_ENABLED",
            "KILL_SWITCH": "EMERGENCY_STOP"
        }

        return commands.get(
            command,
            "INVALID_COMMAND"
        )


# =========================
# RUN DASHBOARD SERVER
# =========================
if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=5000,
        debug=False
    )
