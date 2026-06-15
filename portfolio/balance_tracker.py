
# fse/portfolio/balance_tracker.py
import time
import logging

logger = logging.getLogger(__name__)

# =========================
# BALANCE TRACKER CORE
# =========================
class BalanceTracker:
    """የካፒታል እና የሪስክ ሁኔታን (Drawdown) የሚከታተል ክፍል (መርህ #7)።"""
    
    def __init__(self, initial_balance=1000.0):
        self.initial_balance = float(initial_balance)
        self.balance = float(initial_balance)
        self.equity_peak = float(initial_balance)
        self.drawdown = 0.0
        self.history = []

    def update(self, pnl, metadata=None):
        """ትርፍ ወይም ኪሳራን ተከትሎ ሂሳብን ማዘመን።"""
        self.balance += float(pnl)

        if self.balance > self.equity_peak:
            self.equity_peak = self.balance

        self.drawdown = self.equity_peak - self.balance

        record = {
            "time": time.time(),
            "pnl": float(pnl),
            "balance": round(self.balance, 2),
            "drawdown": round(self.drawdown, 2),
            "metadata": metadata or {}
        }

        self.history.append(record)
        return record

    def status(self):
        """የአሁኑን የፋይናንስ ሁኔታ መመለስ።"""
        dd_percent = (self.drawdown / self.equity_peak) * 100 if self.equity_peak > 0 else 0
        return {
            "balance": round(self.balance, 2),
            "equity_peak": round(self.equity_peak, 2),
            "drawdown": round(self.drawdown, 2),
            "drawdown_percent": round(dd_percent, 2)
        }

    def risk_flag(self, max_drawdown_percent=20.0):
        """የሪስክ ጣሪያ (Drawdown limit) መጣሱን ማረጋገጥ።"""
        stats = self.status()
        if stats["drawdown_percent"] >= max_drawdown_percent:
            logger.critical(f"⚠️ RISK BREACH: Drawdown at {stats['drawdown_percent']}%")
            return {"status": "RISK_BREACH", "drawdown_percent": stats["drawdown_percent"]}
        
        return {"status": "OK", "drawdown_percent": stats["drawdown_percent"]}

    def reset(self):
        """ለBacktesting ሲባል ሂሳብን ወደነበረበት መመለስ።"""
        self.balance = self.initial_balance
        self.equity_peak = self.initial_balance
        self.drawdown = 0.0
        self.history.clear()
        logger.info("🔄 Balance tracker reset to initial state.")
