
# fse/portfolio/allocation_engine.py
import time
import logging

logger = logging.getLogger(__name__)

# =========================
# PORTFOLIO ALLOCATION ENGINE
# =========================
class AllocationEngine:
    """በConfidence ደረጃ መሰረት ካፒታልን የሚያከፋፍል ክፍል (መርህ #7)።"""
    
    def __init__(self, initial_balance=1000.0):
        self.initial_balance = float(initial_balance)
        self.available_balance = float(initial_balance)
        self.used_margin = 0.0
        self.allocations = []
        self.max_risk_per_trade = 0.1  # 10% የካፒታል መቆጣጠሪያ ጣሪያ

    def calculate_position_size(self, confidence, balance=None):
        """በConfidence ደረጃ የንግድ መጠኑን ማስላት።"""
        bal = float(balance or self.available_balance)
        # confidence 0-100 ወደ መቶኛ መቀየር
        risk_factor = max(0.0, min(float(confidence) / 100.0, 1.0))
        position_size = bal * self.max_risk_per_trade * risk_factor
        return round(position_size, 4)

    def allocate(self, symbol, signal, confidence):
        """ካፒታልን መመደብ እና የሒሳብ መዝገብን ማዘመን።"""
        size = self.calculate_position_size(confidence)
        
        if size > self.available_balance:
            logger.warning(f"⚠️ Insufficient balance for {symbol}. Size: {size}")
            return None

        allocation = {
            "time": time.time(), "symbol": symbol, "signal": signal,
            "confidence": confidence, "allocated_size": size
        }

        self.allocations.append(allocation)
        self.available_balance -= size
        self.used_margin += size

        logger.info(f"💰 ALLOCATION: {symbol} | Size: {size} | Remaining: {self.available_balance}")
        return allocation

    def release(self, size):
        """ንግድ ሲዘጋ ካፒታልን መልቀቅ።"""
        s = float(size)
        self.available_balance += s
        self.used_margin = max(0.0, self.used_margin - s)
        logger.info(f"🔓 CAPITAL RELEASED: {s} | Available: {self.available_balance}")

    def status(self):
        """የፖርትፎሊዮ አጠቃላይ ሁኔታ።"""
        return {
            "available_balance": round(self.available_balance, 2),
            "used_margin": round(self.used_margin, 2),
            "total_allocations": len(self.allocations)
        }

    def can_allocate(self, confidence):
        """ንግድ ከመከፈቱ በፊት የካፒታል ብቃት ማረጋገጫ።"""
        return self.calculate_position_size(confidence) <= self.available_balance

    def reset(self):
        """ለBacktesting ሲባል ሂሳብን ወደነበረበት መመለስ።"""
        self.available_balance = self.initial_balance
        self.used_margin = 0.0
        self.allocations.clear()
        logger.info("🔄 Allocation Engine reset.")
