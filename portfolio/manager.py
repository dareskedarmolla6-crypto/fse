
# fse/portfolio/portfolio_manager.py
import logging

logger = logging.getLogger(__name__)

class PortfolioManager:
    """የፖርትፎሊዮ ካፒታልን የሚያከፋፍል እና አጠቃላይ አደጋን የሚቆጣጠር (መርህ #7)።"""
    
    def __init__(self, total_capital: float):
        self.total_capital = float(total_capital)
        self.reserve_ratio = 0.25  # 25% የጥሬ ገንዘብ መጠባበቂያ
        self.positions = []
        self.balance = float(total_capital)

    def allocate_capital(self, strategies):
        """በስልቶች ውጤት (Score) መሰረት ካፒታልን በስሜት የሚመድብ።"""
        if not strategies:
            return {}

        total_score = sum(s["score"] for s in strategies)
        available_capital = self.balance * (1.0 - self.reserve_ratio)
        allocations = {}

        for s in strategies:
            weight = s["score"] / total_score if total_score > 0 else 0
            allocations[s["symbol"]] = available_capital * weight

        return allocations

    def check_symbol_exposure(self, symbol, current_exposure):
        """ለእያንዳንዱ ምልክት የ20% የሪስክ ጣሪያ ማስቀመጥ።"""
        max_exposure = self.total_capital * 0.20
        if current_exposure >= max_exposure:
            logger.warning(f"⚠️ Exposure limit reached for {symbol}")
            return False, "EXPOSURE_LIMIT_REACHED"
        return True, "OK"

    def calculate_health_score(self):
        """የፖርትፎሊዮን አጠቃላይ ጤንነት መለኪያ (Health Score)።"""
        exposure_penalty = len(self.positions) * 2
        balance_factor = (self.balance / self.total_capital) * 100
        score = balance_factor - exposure_penalty
        return max(0.0, min(100.0, score))

    def update(self, trade_result):
        """የንግድ ውጤቶችን ተከትሎ ፖርትፎሊዮን ማዘመን።"""
        pnl = float(trade_result.get("pnl", 0))
        self.balance += pnl
        self.positions.append(trade_result)
        logger.info(f"📊 Portfolio Updated: PnL {pnl} | New Balance {self.balance}")

    def state(self):
        """የፖርትፎሊዮን ወቅታዊ ሁኔታ መመለስ።"""
        return {
            "balance": round(self.balance, 2),
            "open_positions": len(self.positions),
            "health_score": round(self.calculate_health_score(), 2)
        }
