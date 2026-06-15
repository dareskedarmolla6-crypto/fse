
# fse/brain/inference_engine.py
import time
import logging
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field

logger = logging.getLogger("FSE.InferenceEngine")

# ==========================================================
# CORE INTELLIGENCE LAYERS
# ==========================================================

class InferenceController:
    """መርህ #10: ዋናው የአዕምሮ አስተባባሪ (Central Brain Coordinator)።"""
    def __init__(self):
        self.memory = MemoryEngine()
        self.volatility = VolatilityEngine()
        self.market_intelligence = MarketIntelligence()
        self.fusion = AIFusionEngine()
        self.decision = FSEDecisionEngine(self.volatility)
        self.signal_engine = SignalEngine()
        self.reliability = ReliabilityEngine()

    def process(self, market: MarketSnapshot, candles: List[Candle]) -> Optional[Dict[str, Any]]:
        try:
            # 1. Market Analysis (Structure + Liquidity + FVG)
            packet = self.market_intelligence.evaluate(candles)
            
            # 2. AI Confidence Scoring
            ai_result = self.fusion.evaluate(packet)
            
            # 3. FSE Philosophy Decision (Hedge + Grid Logic)
            decision = self.decision.decide(market, ai_result)
            
            # 4. Signal Generation
            signal = self.signal_engine.generate(market.symbol, decision)
            
            # 5. Reliability Checkpoint
            self.reliability.save_state({"symbol": market.symbol, "decision": decision, "ts": time.time()})
            
            return signal
        except Exception as e:
            logger.error(f"Inference process failed: {e}")
            return None
