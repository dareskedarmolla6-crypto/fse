import hmac
import hashlib
import base64


# =========================
# MARKET PROFILE ENGINE
# =========================
class MarketProfile:
    def get(self, symbol):
        high_liquidity_pairs = [
            "EURUSD", "GBPUSD", "USDJPY", "XAUUSD"
        ]

        if symbol in high_liquidity_pairs:
            return {
                "leverage_limit": 100,
                "volatility_target": 3,
                "scan_interval": 300
            }

        return {
            "leverage_limit": 20,
            "volatility_target": 15,
            "scan_interval": 180
        }


# =========================
# API SECURITY MANAGER
# =========================
class APISecurityManager:
    def __init__(self, secret: str):
        self.secret = secret.encode()

    def sign(self, payload: str) -> str:
        signature = hmac.new(
            self.secret,
            payload.encode(),
            hashlib.sha256
        ).digest()

        return base64.b64encode(signature).decode()

    def verify(self, payload: str, signature: str) -> bool:
        expected = self.sign(payload)
        return hmac.compare_digest(expected, signature)
# Safety improvement: prevent signing with empty secret (runtime protection)
def validate_secret(self):
    if not self.secret:
        raise ValueError("Missing API secret for signing")

# Optional helper: quick market profile shortcut
def get_profile(self, symbol):
    return self.get(symbol)
