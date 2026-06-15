
# fse/execution/mean_reversion.py
import time
import uuid
import hashlib
import logging

logger = logging.getLogger(__name__)

# =========================
# ID EMPOTENCY KEY
# =========================
def generate_idempotency_key(symbol, side, qty, strategy_id, bucket):
    raw = f"{symbol}:{side}:{qty}:{strategy_id}:{bucket}"
    return hashlib.sha256(raw.encode()).hexdigest()

# =========================
# EXECUTION COORDINATOR
# =========================
class ExecutionCoordinator:
    """ሲግናሎችን በሪስክ ኢንጂን በማረጋገጥ የሚፈጽም አስተባባሪ።"""
    
    def __init__(self, risk_engine, gateway, store, verifier, lock_mgr):
        self.risk = risk_engine
        self.gateway = gateway
        self.store = store
        self.verifier = verifier
        self.lock = lock_mgr

    def execute_signal(self, signal):
        """የሲግናል አፈጻጸም መቆጣጠሪያ።"""
        if self.store.get("system_status") in ["STOP", "EMERGENCY"]:
            logger.critical("🚨 SYSTEM HALTED: Emergency block active.")
            raise Exception("SYSTEM HALTED")

        with self.lock.acquire(signal["portfolio_id"]):
            if not self.risk.validate_new_position(signal):
                logger.warning(f"⚠️ Signal rejected for {signal['symbol']}.")
                return None

            trade_id = f"BOT_{uuid.uuid4().hex[:16]}"
            trade = self._create_trade(trade_id, signal)
            self.store.save(trade)

            key = generate_idempotency_key(
                signal["symbol"], signal["side"], signal["qty"],
                signal["strategy_id"], int(time.time() // 60)
            )

            resp = self.gateway.place_order(signal, idempotency_key=key)
            
            if resp:
                return self.verifier.verify_order(trade_id, signal["symbol"], resp["orderId"])
            return None

    def _create_trade(self, trade_id, signal):
        return {
            "trade_id": trade_id, "symbol": signal["symbol"],
            "side": signal["side"], "status": "CREATED",
            "ts": int(time.time()), "retries": 0
        }

# =========================
# EXECUTION ENGINE
# =========================
class ExecutionEngine:
    """የትዕዛዝ መፈጸሚያ (Live/Paper)።"""
    def __init__(self, client):
        self.client = client

    def open_long(self, symbol, qty):
        logger.info(f"📈 LONG OPENED: {symbol} | Qty: {qty}")

    def open_short(self, symbol, qty):
        logger.info(f"📉 SHORT OPENED: {symbol} | Qty: {qty}")

# =========================
# HEDGE ENGINE
# =========================
class HedgeEngine:
    """የመከላከያ ስልት (Hedge Mode) ማስተዳደሪያ።"""
    def open_hedge(self, executor, symbol, qty):
        logger.warning(f"⚖️ HEDGE MODE ACTIVE for {symbol}")
        long_trade = executor.open_long(symbol, qty)
        short_trade = executor.open_short(symbol, qty)
        return {"symbol": symbol, "status": "HEDGE_ACTIVE"}

# =========================
# STRATEGY (SIGNAL DECISION)
# =========================
class Strategy:
    """ስልታዊ ውሳኔ ሰጪ (Mean Reversion Logic)።"""
    def build(self, signal, confidence):
        # 60% በታች ከሆነ ሪስክን ለመቀነስ Hedge እናደርጋለን
        if confidence < 60:
            logger.info("🛡 Confidence < 60%. Triggering Full Hedge.")
            return "FULL_HEDGE"
        return "NORMAL_EXECUTION"
