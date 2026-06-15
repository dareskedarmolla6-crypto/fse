
# fse/dashboard/websocket_feed.py
import asyncio
import json
import random
import time
import logging

logger = logging.getLogger(__name__)

# =========================
# MOCK MARKET DATA STREAM
# =========================
class MarketWebSocketFeed:
    """ሲሙሌት የተደረገ የገበያ መረጃ ማስተላለፊያ (ለወደፊቱ Binance/Bybit WS ይተካል)"""

    def __init__(self, symbol="BTCUSDT"):
        self.symbol = symbol
        self.running = False

    async def stream_price(self):
        """የገበያ ዋጋዎችን በየሰከንዱ ማመንጨት።"""
        while self.running:
            tick = {
                "symbol": self.symbol,
                "price": round(random.uniform(40000, 45000), 2),
                "volume": round(random.uniform(1, 10), 4),
                "timestamp": time.time()
            }
            yield tick
            await asyncio.sleep(1)

# =========================
# DASHBOARD FEED BROADCASTER
# =========================
class DashboardFeed:
    """ለዳሽቦርዱ መረጃን በWebSocket ማሰራጫ።"""

    def __init__(self):
        self.clients = set()

    def register(self, client):
        self.clients.add(client)

    def unregister(self, client):
        self.clients.discard(client)

    async def broadcast(self, message: dict):
        """ለሁሉም የተገናኙ ክሊየንቶች መረጃን ማስተላለፍ።"""
        if not self.clients: return
        payload = json.dumps(message)
        for client in list(self.clients):
            try:
                await client.send(payload)
            except Exception as e:
                logger.error(f"❌ Broadcast error: {e}")
                self.unregister(client)

# =========================
# BOT STATUS STREAM
# =========================
class BotStatus:
    def __init__(self):
        self.balance = 1000.0
        self.open_positions = 0
        self.last_signal = None
        self.last_confidence = 0

    def update(self, signal, confidence, balance_change=0):
        self.last_signal = signal
        self.last_confidence = confidence
        self.balance += balance_change

    def snapshot(self):
        return {
            "balance": round(self.balance, 2),
            "open_positions": self.open_positions,
            "last_signal": self.last_signal,
            "confidence": self.last_confidence,
            "timestamp": time.time()
        }

# =========================
# MAIN STREAM ENGINE
# =========================
class WebSocketFeedEngine:
    def __init__(self, feed: MarketWebSocketFeed, dashboard: DashboardFeed, status: BotStatus):
        self.feed = feed
        self.dashboard = dashboard
        self.status = status
        self.running = False

    async def run(self):
        """ዋናው የስትሪም አፈጻጸም ክፍል (መርህ #6)።"""
        self.running = True
        self.feed.running = True
        logger.info("🚀 WebSocket Feed Engine Started.")
        
        async for tick in self.feed.stream_price():
            if not self.running: break
            # የገበያ መረጃን እና የቦት ሁኔታን ማዋሃድ
            payload = {**tick, **self.status.snapshot()}
            await self.dashboard.broadcast(payload)
