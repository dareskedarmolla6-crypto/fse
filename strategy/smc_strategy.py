# fse/strategy/smc_strategy.py
from dataclasses import dataclass
import logging

logger = logging.getLogger(__name__)

# =========================
# CANDLE MODEL
# =========================
@dataclass
class Candle:
    open: float
    high: float
    low: float
    close: float

# =========================
# SMC STRATEGY ENGINE
# =========================
class SMCStrategy:
    """Smart Money Concepts ላይ የተመሰረተ የንግድ ስልት (መርህ #3)።"""

    def __init__(self):
        self.last_high = None
        self.last_low = None

    def detect_structure(self, candles):
        """የገበያ መዋቅር ለውጥ (BOS) መለየት።"""
        if len(candles) < 3: return "NO_DATA"

        current_high = max(c.high for c in candles)
        current_low = min(c.low for c in candles)

        if self.last_high is None:
            self.last_high, self.last_low = current_high, current_low
            return "INITIALIZED"

        if current_high > self.last_high:
            self.last_high = current_high
            return "BULLISH_BOS"

        if current_low < self.last_low:
            self.last_low = current_low
            return "BEARISH_BOS"

        return "RANGE"

    def liquidity_sweep(self, candles):
        """የሊኩዲቲ ወጥመድን (Liquidity Sweep) መለየት።"""
        last = candles[-1]
        if self.last_high and last.high > self.last_high and last.close < self.last_high:
            return "SELL_SIDE_SWEEP"
        if self.last_low and last.low < self.last_low and last.close > self.last_low:
            return "BUY_SIDE_SWEEP"
        return None

    def zone(self, candles):
        """Premium/Discount የዋጋ ቀጠናዎችን ማስላት።"""
        high = max(c.high for c in candles)
        low = min(c.low for c in candles)
        eq = (high + low) / 2.0
        
        last_close = candles[-1].close
        
        if last_close > eq:
            return "PREMIUM_ZONE" # የመሸጫ ቀጠና
        return "DISCOUNT_ZONE"    # የመግዣ ቀጠና

    def execute(self, candles):
        """የSMC ስልትን የሚያስፈጽም ዋና ተግባር።"""
        struct = self.detect_structure(candles)
        sweep = self.liquidity_sweep(candles)
        zone = self.zone(candles)
        
        logger.info(f"🧠 SMC Analysis: {struct} | {sweep} | {zone}")
        return {"structure": struct, "sweep": sweep, "zone": zone}

