
# fse/execution/order_executor.py
import time
import uuid
import hashlib
import logging

logger = logging.getLogger(__name__)

# =========================================================
# IDEMPOTENCY KEY (የተባዙ ትዕዛዞችን ለመከላከል)
# =========================================================
def generate_idempotency_key(symbol, side, qty, strategy_id, bucket):
    raw = f"{symbol}:{side}:{qty}:{strategy_id}:{bucket}"
    return hashlib.sha256(raw.encode()).hexdigest()

# =========================================================
# LIVE EXECUTOR (DIRECT EXECUTION LAYER)
# =========================================================
class LiveExecutor:
    """የትዕዛዝ ውሳኔዎችን ወደ ተግባር የሚቀይር ክፍል (መርህ #6)።"""
    
    def __init__(self, exchange):
        self.exchange = exchange

    def execute_trade(self, decision, symbol, size):
        try:
            if decision == "LONG":
                return self.exchange.place_order(symbol, "BUY", size)
            elif decision == "SHORT":
                return self.exchange.place_order(symbol, "SELL", size)
            elif decision == "GRID":
                orders = [self.exchange.place_order(symbol, "BUY", size / 3) for _ in range(3)]
                return orders
            elif decision == "HEDGE":
                return {
                    "LONG": self.exchange.place_order(symbol, "BUY", size / 2),
                    "SHORT": self.exchange.place_order(symbol, "SELL", size / 2)
                }
        except Exception as e:
            logger.error(f"❌ Execution error: {e}")
        return None

# =========================================================
# EXCHANGE EXECUTOR (LOW-LEVEL API WRAPPER)
# =========================================================
class ExchangeExecutor:
    """ከኤፒአይ ጋር የሚገናኝ መሰረታዊ አፈጻጸም ክፍል (Safety Wrapper)።"""
    
    def __init__(self, api):
        self.api = api

    def open_order(self, symbol, side, quantity):
        try:
            order = self.api.create_order(symbol=symbol, side=side, type="MARKET", quantity=quantity)
            logger.info(f"✅ Order opened: {symbol} {side} {quantity}")
            return {"status": "OPENED", "order": order}
        except Exception as e:
            logger.error(f"❌ Order failed: {e}")
            return {"status": "ERROR", "message": str(e)}

# =========================================================
# POSITION MANAGER
# =========================================================
class PositionManager:
    """ክፍት የሆኑ ቦታዎችን (Positions) የሚያስተዳድር ክፍል (መርህ #7)።"""
    
    def __init__(self):
        self.positions = []

    def add_position(self, order):
        self.positions.append(order)

    def close_position(self, position_id):
        for p in self.positions:
            if p.get("id") == position_id:
                p["status"] = "CLOSED"
                return p
        return None
