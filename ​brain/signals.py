
# fse/brain/signal_generator.py
import time
import random
import logging
from typing import Dict, List, Optional

logger = logging.getLogger("FSE.Brain.SignalGen")

# ==========================================================
# FUSION & CONSENSUS LAYERS
# ==========================================================

class BrainSignalGenerator:
    """መርህ #1 እና #4: የተለያዩ ሞዴሎችን በማዋሃድ የሲግናል ጥራትን ማረጋገጫ።"""
    def __init__(self, predictor, inference_engine, feature_engine):
        self.predictor = predictor
        self.inference_engine = inference_engine
        self.feature_engine = feature_engine

    def generate(self, data: Dict) -> Dict:
        pred, conf1 = self.predictor.predict(data)
        inf, conf2 = self.inference_engine.analyze(data)
        mode = self.feature_engine.adjust(data.get("win_rate", 0.5))

        if pred == inf:
            return {"symbol": data.get("symbol"), "side": pred, "confidence": int((conf1 + conf2) / 2), "mode": mode}
        return {"symbol": data.get("symbol"), "side": "HEDGE", "confidence": 50, "mode": mode}

# ==========================================================
# REGIME & DECISION ENGINES
# ==========================================================

class MarketRegimeAI:
    """መርህ #3 እና #11: የገበያ ሁኔታን (Regime) በመለየት ሪስክ መቆጣጠሪያ።"""
    def classify(self, data: Dict) -> str:
        vol = data.get("volatility", 0)
        mom = data.get("momentum", 0)
        if vol > 0.7: return "CHAOTIC"
        if mom > 0.2: return "TRENDING_UP"
        if mom < -0.2: return "TRENDING_DOWN"
        return "SIDEWAYS"

class AIDecisionEngine:
    """መርህ #4, #7 እና #8: የመጨረሻ ውሳኔ ሰጪ (Filter + Size + Regime)."""
    def __init__(self, filter_layer, position_engine, regime_ai):
        self.filter = filter_layer
        self.position_engine = position_engine
        self.regime_ai = regime_ai

    def decide(self, symbol: str, structure: Dict, market_data: Dict, wallet: float) -> Optional[Dict]:
        regime = self.regime_ai.classify(market_data)
        if regime == "CHAOTIC": return None # መርህ #11

        signal = {"symbol": symbol, "side": random.choice(["BUY", "SELL"]), "score": random.randint(60, 95)}
        
        if not self.filter.validate(structure, signal): return None

        signal["qty"] = self.position_engine.adjust_size(signal, wallet)
        signal["regime"] = regime
        return signal

# ==========================================================
# CORE BOT ORCHESTRATION
# ==========================================================

class TradingBotCore:
    """የሲስተሙ ዋና የልብ ምት (Orchestration Brain)።"""
    def __init__(self, data_engine, strategy_engine, risk_engine, execution_engine, portfolio_engine, monitor, telegram=None):
        self.data, self.strategy = data_engine, strategy_engine
        self.risk, self.execution = risk_engine, execution_engine
        self.portfolio, self.monitor, self.telegram = portfolio_engine, monitor, telegram
        self.running = False

    def run_once(self):
        market_data = self.data.get_snapshot()
        for signal in self.strategy.generate(market_data):
            if not self.risk.validate(signal, self.portfolio.state()): continue
            
            result = self.execution.execute_signal(signal)
            self.portfolio.update(result)
            self.monitor.record_trade()
            
            if self.telegram:
                self.telegram.notify_trade(signal["symbol"], signal["side"], result.get("pnl", 0))

    def start(self, interval: int = 3):
        self.running = True
        logger.info("🚀 FSE BOT STARTED")
        while self.running:
            try:
                self.run_once()
                time.sleep(interval)
            except Exception as e:
                logger.error(f"FATAL ERROR: {e}")
