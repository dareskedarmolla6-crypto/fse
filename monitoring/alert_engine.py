
# fse/monitoring/alert_engine.py
import logging

logger = logging.getLogger(__name__)

# =========================
# MEMORY ANALYTICS
# =========================
class MemoryAnalytics:
    """የቦቱን የንግድ ታሪክ የሚተነትን ክፍል (መርህ #1)።"""
    
    def __init__(self, memory):
        self.memory = memory

    def summary(self):
        history = getattr(self.memory, 'history', [])
        total = len(history)
        wins = len([t for t in history if t.get("pnl", 0) > 0])
        losses = total - wins
        win_rate = (wins / total) if total > 0 else 0

        return {
            "total_trades": total,
            "wins": wins,
            "losses": losses,
            "win_rate": round(win_rate, 3)
        }

# =========================
# ALERT ENGINE
# =========================
class AlertEngine:
    """የስራ አፈጻጸም መለኪያዎች እና የደህንነት ማስጠንቀቂያዎች (መርህ #11)።"""
    
    def __init__(self, memory, telegram=None):
        self.analytics = MemoryAnalytics(memory)
        self.telegram = telegram

    def check_health(self):
        stats = self.analytics.summary()
        alerts = []

        if stats["win_rate"] < 0.4 and stats["total_trades"] > 10:
            alerts.append("LOW_WIN_RATE")
        if stats["total_trades"] == 0:
            alerts.append("NO_TRADES_EXECUTED")
        if stats["losses"] > (stats["wins"] * 2 + 1):
            alerts.append("HIGH_RISK_DRAWDOWN")

        return stats, alerts

    def notify(self):
        stats, alerts = self.check_health()
        if not alerts:
            return {"status": "OK", "stats": stats}

        message = f"🚨 FSE ALERT\nStats: {stats}\nIssues: {', '.join(alerts)}"
        logger.warning(message)

        if self.telegram:
            try:
                self.telegram.send_message(message)
            except Exception as e:
                logger.error(f"❌ Alert notification failed: {e}")

        return {"status": "ALERT", "stats": stats, "alerts": alerts}
