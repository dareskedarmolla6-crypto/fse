import math


# =========================
# NORMALIZATION ENGINE
# =========================
class DataNormalizer:
    def __init__(self):
        self.min_max_cache = {}

    # -------------------------
    # SIMPLE MIN-MAX NORMALIZATION
    # -------------------------
    def min_max(self, value, min_val, max_val):
        if max_val == min_val:
            return 0.0
        return (value - min_val) / (max_val - min_val)

    # -------------------------
    # Z-SCORE NORMALIZATION
    # -------------------------
    def z_score(self, value, mean, std):
        if std == 0:
            return 0.0
        return (value - mean) / std

    # -------------------------
    # PRICE CHANGE NORMALIZATION
    # (IMPORTANT FOR FSE SIGNALS)
    # -------------------------
    def normalize_price_change(self, price_change):
        # clamp extreme values
        if price_change > 10:
            price_change = 10
        if price_change < -10:
            price_change = -10

        # scale to -1 to 1 range
        return price_change / 10

    # -------------------------
    # VOLUME NORMALIZATION
    # -------------------------
    def normalize_volume(self, volume, max_volume=1000):
        return min(volume / max_volume, 1.0)

    # -------------------------
    # VOLATILITY SCORE
    # -------------------------
    def volatility_score(self, price_changes):
        if not price_changes:
            return 0.0

        avg = sum(price_changes) / len(price_changes)

        variance = sum((x - avg) ** 2 for x in price_changes) / len(price_changes)

        return math.sqrt(variance) / 10  # scaled

    # -------------------------
    # FULL FEATURE PACK
    # -------------------------
    def build_features(self, market_data):
        """
        input:
            {
                "price_change": float,
                "volume": float,
                "history": [float]
            }
        """

        return {
            "price_change_norm": self.normalize_price_change(
                market_data.get("price_change", 0)
            ),
            "volume_norm": self.normalize_volume(
                market_data.get("volume", 0)
            ),
            "volatility": self.volatility_score(
                market_data.get("history", [])
            )
        }
