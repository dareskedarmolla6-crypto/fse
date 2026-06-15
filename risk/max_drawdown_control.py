
# fse/risk/max_drawdown_control.py
import logging

logger = logging.getLogger(__name__)

# =========================
# DRAWDOWN TRACKER
# =========================
class DrawdownControl:
    """የሒሳብ አናት (Equity Peak) መከታተያ።"""
    def __init__(self):
        self.peak_balance = 0.0

    def update_peak(self, balance):
        if balance > self.peak_balance:
            self.peak_balance = float(balance)

    def get_drawdown(self, balance):
        if self.peak_balance <= 0: return 0.0
        return (self.peak_balance - float(balance)) / self.peak_balance

# =========================
# MAX DRAWDOWN GUARD
# =========================
class MaxDrawdownControl:
    """የሪስክ ጣሪያን የሚከታተል የጥበቃ ክፍል (መርህ #9)።"""
    def __init__(self, max_drawdown=0.20):
        self.max_drawdown = float(max_drawdown)
        self.tracker = DrawdownControl()

    def allow_trade(self, balance):
        self.tracker.update_peak(balance)
        dd = self.tracker.get_drawdown(balance)
        
        if dd >= self.max_drawdown:
            logger.critical(f"🛑 TRADING HALTED: Drawdown reached {dd:.2%}")
            return False, dd
        return True, dd

# =========================
# KILL SWITCH (GLOBAL SAFETY)
# =========================
class KillSwitch:
    """ሲስተሙን በድንገተኛ አደጋ ሙሉ በሙሉ የሚያቆም (Hard Limit)።"""
    def __init__(self, hard_limit=0.25):
        self.hard_limit = float(hard_limit)

    def check(self, drawdown):
        return drawdown >= self.hard_limit

# =========================
# AUTONOMY SAFETY CORE
# =========================
class FullAutonomyCore:
    """የደህንነት መቆጣጠሪያ እና የንግድ ማስፈጸሚያ ማዕከል (Orchestrator)።"""
    def __init__(self, execution_engine, kill_switch: KillSwitch):
        self.execution = execution_engine
        self.kill = kill_switch

    def run(self, decision, drawdown):
        if self.kill.check(drawdown):
            logger.critical("🚨 CRITICAL: System Halted by Kill Switch!")
            return "SYSTEM_HALTED"
        return self.execution.execute_trade(decision)
