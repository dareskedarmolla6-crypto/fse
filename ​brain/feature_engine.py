
# fse/brain/feature_engine.py
from typing import Dict, Optional
import logging

logger = logging.getLogger("FSE.Brain.FeatureEngine")

# ==========================================================
# POSITION INTELLIGENCE
# ==========================================================

class PositionIntelligence:
    """መርህ #7: የካፒታል አያያዝ እና የሪስክ ቁጥጥር (Exposure Management)።"""
    def __init__(self, base_risk: float = 0.01, max_exposure: float = 0.20):
        self.base_risk = base_risk
        self.max_exposure = max_exposure
        self.current_exposure = 0.0

    def calculate_size(self, signal: Dict, wallet_balance: float) -> float:
        confidence = signal.get("confidence", 0.5)
        volatility = signal.get("volatility", 0)
        
        # መርህ #1: ከፍተኛ ቮላቲሊቲ ያላቸውን እድሎች መሸለም
        vol_bonus = min(volatility / 30, 1.0)
        risk_factor = (confidence * 0.6) + (vol_bonus * 0.4)
        
        size = wallet_balance * self.base_risk * (1 + risk_factor)
        available = (wallet_balance * self.max_exposure) - self.current_exposure
        
        return round(max(0, min(size, available)), 2)

# ==========================================================
# MARKET INTELLIGENCE (WHALE & VOLUME)
# ==========================================================

class WhaleSignalEngine:
    """መርህ #2: ትልልቅ ተጫዋቾችን (Whales) እንቅስቃሴ መለኪያ።"""
    def generate(self, whale_state: str, strength: float = 1.0) -> Optional[Dict]:
        states = {"ACCUMULATION": "LONG", "DISTRIBUTION": "SHORT"}
        side = states.get(whale_state)
        if not side: return None
        return {"signal": side, "confidence": min(1.0, 0.7 + strength * 0.3)}

class VolumeScoreEngine:
    """መርህ #11: የቮሊዩም ጥንካሬን (Quality) ወደ AI Score መቀየሪያ።"""
    def score(self, current_vol: float, avg_vol: float) -> float:
        if avg_vol <= 0: return 0.0
        return min(100, (current_vol / avg_vol) * 20)

# ==========================================================
# ALPHA FEATURE ENGINE (INTELLIGENCE)
# ==========================================================

class AlphaFeatureEngine:
    """መርህ #1: የገበያ መረጃን ወደ Alpha አምሳያዎች (Features) መቀየሪያ።"""
    def __init__(self):
        self.vol_score_engine = VolumeScoreEngine()

    def build(self, market: Dict) -> Dict:
        vol_score = self.vol_score_engine.score(market.get("volume", 0), market.get("average_volume", 1))
        volatility = market.get("volatility", 0)
        
        return {
            "volatility": volatility,
            "volume_score": vol_score,
            "high_volatility": (volatility >= 15),
            "alpha_quality": (volatility * 0.7 + vol_score * 0.3)
        }
