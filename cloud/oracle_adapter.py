
import hmac
import hashlib
import base64
import logging

logger = logging.getLogger(__name__)

# =========================
# MARKET PROFILE ENGINE
# =========================
class MarketProfile:
    """ለአልፋ ኮይኖች እና ለፎሬክስ ገበያዎች የሊኩዲቲ እና መዋዠቅ መለኪያ።"""
    
    def get(self, symbol: str):
        # የቦትህ 11ኛ መርህ (Liquidity & Volatility Guard)
        # ከፍተኛ መዋዠቅ ያላቸው 'አልፋ' ኮይኖች ተለይተው ይታወቃሉ
        high_liquidity_pairs = ["EURUSD", "GBPUSD", "USDJPY", "XAUUSD", "BTCUSDT", "ETHUSDT"]

        if symbol in high_liquidity_pairs:
            return {
                "leverage_limit": 35, # ከፍ ያለ ሌቨሬጅ ለአልፋ ኮይኖች
                "volatility_target": 15, 
                "scan_interval": 180 # 3 ደቂቃ (መርህ #6)
            }

        return {
            "leverage_limit": 20,
            "volatility_target": 25,
            "scan_interval": 300
        }

# =========================
# API SECURITY MANAGER
# =========================
class APISecurityManager:
    def __init__(self, secret: str):
        if not secret:
            raise ValueError("❌ APISecurityManager: Missing API secret!")
        self.secret = secret.encode()

    def sign(self, payload: str) -> str:
        """የደህንነት ፊርማ ለመፍጠር።"""
        self.validate_secret()
        signature = hmac.new(
            self.secret,
            payload.encode(),
            hashlib.sha256
        ).digest()
        return base64.b64encode(signature).decode()

    def verify(self, payload: str, signature: str) -> bool:
        expected = self.sign(payload)
        return hmac.compare_digest(expected, signature)

    def validate_secret(self):
        """የደህንነት ማረጋገጫ።"""
        if not self.secret:
            raise ValueError("🚨 Security Alert: Attempted to sign with empty secret.")

    def get_profile(self, symbol: str):
        return MarketProfile().get(symbol)
