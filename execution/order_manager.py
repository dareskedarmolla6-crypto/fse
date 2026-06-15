
# fse/execution/order_manager.py

import uuid
import time
import hashlib
import logging

logger = logging.getLogger(__name__)

# =========================
# IDEMPOTENCY KEY GENERATOR
# =========================
def generate_idempotency_key(symbol, side, qty, strategy_id, bucket):
    raw = f"{symbol}:{side}:{qty}:{strategy_id}:{bucket}"
    return hashlib.sha256(raw.encode()).hexdigest()

# =========================
# BASIC EXECUTION ENGINE
# =========================
class ExecutionEngine:
    """የመሰረታዊ ትዕዛዝ ፈጻሚ ክፍል (Paper/Debug Mode)።"""
    
    def __init__(self, client=None):
        self.client = client

    def open_long(self, symbol, qty):
        logger.info(f"📈 LONG OPENED: {symbol} | Qty: {qty}")
        return {"symbol": symbol, "side": "LONG", "qty": qty, "status": "OPENED", "order_id": str(uuid.uuid4())}

    def open_short(self, symbol, qty):
        logger.info(f"📉 SHORT OPENED: {symbol} | Qty: {qty}")
        return {"symbol": symbol, "side": "SHORT", "qty": qty, "status": "OPENED", "order_id": str(uuid.uuid4())}

# =========================
# HEDGE ENGINE
# =========================
class HedgeEngine:
    def __init__(self):
        self.registry = {}

    def open_hedge(self, executor, symbol, qty):
        logger.warning(f"⚖️ HEDGE MODE ACTIVATED for {symbol}")
        
        long_trade = executor.open_long(symbol, qty / 2)
        short_trade = executor.open_short(symbol, qty / 2)

        hedge_id = str(uuid.uuid4())
        hedge_position = {
            "hedge_id": hedge_id, "symbol": symbol,
            "long": long_trade, "short": short_trade,
            "status": "ACTIVE", "ts": int(time.time()), "order_id": hedge_id
        }

        self.registry[hedge_id] = hedge_position
        return hedge_position

# =========================
# POSITION TRACKER
# =========================
class PositionManager:
    """ክፍት የሆኑ ቦታዎችን የሚያስተዳድር።"""
    
    def __init__(self):
        self.positions = []

    def add_position(self, order):
        self.positions.append(order)
        return order

    def close_position(self, position_id):
        for p in self.positions:
            if p.get("order_id") == position_id:
                p["status"] = "CLOSED"
                p["closed_ts"] = int(time.time())
                return p
        return {"status": "NOT_FOUND"}

# =========================
# ORDER ROUTER (MAIN BRAIN)
# =========================
class OrderManager:
    """ሲግናሎችን ተቀብሎ ወደ ተግባር የሚቀይር ማዕከል (Orchestrator)።"""
    
    def __init__(self, execution_engine, hedge_engine, position_manager, gateway=None, store=None):
        self.execution = execution_engine
        self.hedge = hedge_engine
        self.pm = position_manager
        self.gateway = gateway
        self.store = store

    def execute(self, signal):
        try:
            symbol = signal.get("symbol")
            side = signal.get("side")
            qty = signal.get("qty")

            if side == "LONG":
                order = self.execution.open_long(symbol, qty)
            elif side == "SHORT":
                order = self.execution.open_short(symbol, qty)
            elif side == "HEDGE":
                order = self.hedge.open_hedge(self.execution, symbol, qty)
            else:
                return {"status": "NO_ACTION", "reason": f"Unknown side: {side}"}

            return self.pm.add_position(order)
        
        except Exception as e:
            logger.error(f"❌ Order Execution Error: {e}")
            return {"status": "ERROR", "reason": str(e)}
