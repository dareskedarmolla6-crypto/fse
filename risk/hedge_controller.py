
# fse/risk/hedge_controller.py
import uuid
import time
import logging

logger = logging.getLogger(__name__)

# =========================
# POSITION MODEL
# =========================
class HedgePosition:
    """የሄጅንግ ፖዚሽን መረጃ ሞዴል (መርህ #2)።"""
    def __init__(self, symbol, side, qty, entry_price):
        self.id = str(uuid.uuid4())
        self.symbol = symbol
        self.side = side  # BUY / SELL
        self.qty = float(qty)
        self.entry_price = float(entry_price)
        self.created_at = time.time()
        self.status = "OPEN"
        self.realized_pnl = 0.0

# =========================
# HEDGE BOOK (STATE)
# =========================
class HedgeBook:
    """በአሁኑ ሰአት ያሉ ፖዚሽኖችን የሚከታተል መዝገብ።"""
    def __init__(self):
        self.long_positions = {}
        self.short_positions = {}

    def add(self, position: HedgePosition):
        if position.side == "BUY": self.long_positions[position.id] = position
        else: self.short_positions[position.id] = position

    def get_symbol_positions(self, symbol):
        longs = [p for p in self.long_positions.values() if p.symbol == symbol]
        shorts = [p for p in self.short_positions.values() if p.symbol == symbol]
        return longs, shorts

# =========================
# HEDGE CONTROLLER & EXPOSURE
# =========================
class HedgeController:
    def __init__(self, book: HedgeBook):
        self.book = book

    def open_long(self, symbol, qty, price):
        pos = HedgePosition(symbol, "BUY", qty, price)
        self.book.add(pos)
        logger.info(f"📈 LONG HEDGE OPENED: {symbol} | Qty: {qty}")
        return pos

    def open_short(self, symbol, qty, price):
        pos = HedgePosition(symbol, "SELL", qty, price)
        self.book.add(pos)
        logger.info(f"📉 SHORT HEDGE OPENED: {symbol} | Qty: {qty}")
        return pos

class ExposureEngine:
    """የተጣራ አደጋ (Net Exposure) መለኪያ።"""
    def calculate(self, book: HedgeBook):
        long_qty = sum(p.qty for p in book.long_positions.values())
        short_qty = sum(p.qty for p in book.short_positions.values())
        return {"long": long_qty, "short": short_qty, "net": long_qty - short_qty}

# =========================
# RISK GUARD & EXIT ENGINE
# =========================
class HedgeRiskEngine:
    def __init__(self, max_net_exposure=100.0):
        self.max_net_exposure = float(max_net_exposure)

    def validate(self, book: HedgeBook):
        exposure = ExposureEngine().calculate(book)
        if abs(exposure["net"]) > self.max_net_exposure:
            logger.warning(f"⚠️ HEDGE EXPOSURE LIMIT REACHED: {exposure['net']}")
            return False, "EXPOSURE_LIMIT"
        return True, "OK"

class HedgeExitEngine:
    """የፖዚሽን መዝጊያ እና የ PnL ስሌት።"""
    def close_position(self, position: HedgePosition, exit_price):
        if position.status != "OPEN": return 0.0
        pnl = (exit_price - position.entry_price) * position.qty if position.side == "BUY" else (position.entry_price - exit_price) * position.qty
        position.realized_pnl = float(pnl)
        position.status = "CLOSED"
        logger.info(f"🔴 HEDGE POSITION CLOSED: {position.symbol} | PnL: {pnl}")
        return pnl

# =========================
# MAIN MANAGER
# =========================
class HedgeModeManager:
    """የሄጅንግ ስልት ማስተባበሪያ ማዕከል (መርህ #3)።"""
    def __init__(self):
        self.book = HedgeBook()
        self.controller = HedgeController(self.book)
        self.risk = HedgeRiskEngine()
        self.exit_engine = HedgeExitEngine()

    def is_hedged(self, symbol):
        longs, shorts = self.book.get_symbol_positions(symbol)
        return len(longs) > 0 and len(shorts) > 0
