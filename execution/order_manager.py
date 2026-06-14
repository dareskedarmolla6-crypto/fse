
# fse/execution/order_manager.py

import uuid
import time
import hashlib


# =========================
# IDEMPOTENCY KEY GENERATOR
# =========================
def generate_idempotency_key(symbol, side, qty, strategy_id, bucket):
    raw = f"{symbol}:{side}:{qty}:{strategy_id}:{bucket}"
    return hashlib.sha256(raw.encode()).hexdigest()


# =========================
# BASIC EXECUTION ENGINE (PAPER / DEBUG)
# =========================
class ExecutionEngine:
    def __init__(self, client=None):
        self.client = client

    def open_long(self, symbol, qty):
        print(f"📈 LONG OPENED: {symbol} | Qty: {qty}")
        return {"symbol": symbol, "side": "LONG", "qty": qty, "status": "OPENED"}

    def open_short(self, symbol, qty):
        print(f"📉 SHORT OPENED: {symbol} | Qty: {qty}")
        return {"symbol": symbol, "side": "SHORT", "qty": qty, "status": "OPENED"}


# =========================
# HEDGE ENGINE
# =========================
class HedgeEngine:
    def __init__(self):
        self.registry = {}

    def open_hedge(self, executor, symbol, qty):
        print("⚖️ HEDGE MODE ACTIVATED")

        long_trade = executor.open_long(symbol, qty / 2)
        short_trade = executor.open_short(symbol, qty / 2)

        hedge_id = str(uuid.uuid4())

        hedge_position = {
            "hedge_id": hedge_id,
            "symbol": symbol,
            "long": long_trade,
            "short": short_trade,
            "status": "ACTIVE",
            "ts": int(time.time())
        }

        self.registry[hedge_id] = hedge_position
        return hedge_position


# =========================
# POSITION TRACKER
# =========================
class PositionManager:
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
    def __init__(self, execution_engine, hedge_engine, position_manager, gateway=None, store=None):
        self.execution = execution_engine
        self.hedge = hedge_engine
        self.pm = position_manager
        self.gateway = gateway
        self.store = store

    def execute(self, signal):
        """
        signal format:
        {
            "symbol": "BTCUSDT",
            "side": "LONG | SHORT | HEDGE",
            "qty": 0.01,
            "strategy_id": "mean_reversion"
        }
        """

        symbol = signal["symbol"]
        side = signal["side"]
        qty = signal["qty"]

        # =========================
        # LONG
        # =========================
        if side == "LONG":
            order = self.execution.open_long(symbol, qty)
            return self.pm.add_position(order)

        # =========================
        # SHORT
        # =========================
        if side == "SHORT":
            order = self.execution.open_short(symbol, qty)
            return self.pm.add_position(order)

        # =========================
        # HEDGE
        # =========================
        if side == "HEDGE":
            hedge = self.hedge.open_hedge(self.execution, symbol, qty)
            return self.pm.add_position(hedge)

        return {"status": "NO_ACTION", "reason": f"Unknown side: {side}"}


# =========================
# SIMPLE EXECUTION LOGGER (OPTIONAL)
# =========================
class ExecutionLogger:
    def log(self, message):
        print(f"[ORDER_LOG] {message}")
