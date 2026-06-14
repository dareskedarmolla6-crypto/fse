# ==========================================================
# FSE MARKET ANALYSIS ENGINE (CORE)
# ==========================================================

class MarketAnalysisEngine:
    """
    Detects market regime:
    - Trend
    - Volatility
    - Liquidity pressure
    - Structure bias
    """

    def evaluate(self, market):
        trend = self._trend(market)
        volatility = self._volatility(market)
        liquidity = self._liquidity(market)

        structure = self._structure_bias(market)

        return {
            "trend": trend,
            "volatility": volatility,
            "liquidity": liquidity,
            "structure": structure
        }

    # --------------------------
    # TREND DETECTION
    # --------------------------
    def _trend(self, market):
        price_now = market.get("price_now", 0)
        price_avg = market.get("price_avg", 1)

        if price_now > price_avg * 1.002:
            return "UP"
        elif price_now < price_avg * 0.998:
            return "DOWN"
        return "SIDEWAYS"

    # --------------------------
    # VOLATILITY ENGINE
    # --------------------------
    def _volatility(self, market):
        high = market.get("high", 0)
        low = market.get("low", 0)
        price = market.get("price_now", 1)

        return abs(high - low) / price * 100

    # --------------------------
    # LIQUIDITY FILTER
    # --------------------------
    def _liquidity(self, market):
        volume = market.get("volume", 0)

        if volume > 100000:
            return "HIGH"
        elif volume > 50000:
            return "MEDIUM"
        return "LOW"

    # --------------------------
    # STRUCTURE (SIMPLIFIED BOS/CHOCH SIGNAL)
    # --------------------------
    def _structure_bias(self, market):
        if market.get("price_now", 0) > market.get("price_prev", 0):
            return "BULLISH"
        return "BEARISH"
