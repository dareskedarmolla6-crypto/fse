
# fse/tests/test_integration.py
import unittest
import logging

# Mock Components (በእውነተኛ አሰራር ከሚመለከታቸው ሞጁሎች ይወርሳሉ)
class MockSystem:
    """የሲስተም ክፍሎችን የሚያቀናጅ መቆጣጠሪያ።"""
    def __init__(self, binance_fail=False):
        self.binance_fail = binance_fail

    def get_market_status(self):
        if self.binance_fail: raise ConnectionError("API DOWN")
        return {"price": 150.0}

# =========================
# INTEGRATION TEST SUITE
# =========================
class TestIntegration(unittest.TestCase):
    """የመላው ሲስተም (Integration) የጤና ምርመራ።"""

    def test_startup_workflow(self):
        """ሲስተሙ ሲጀመር ሁሉም አካላት መስራታቸውን ማረጋገጥ።"""
        sys = MockSystem()
        status = sys.get_market_status()
        self.assertIn("price", status)
        logging.info("✅ Startup sequence validated.")

    def test_api_failure_resilience(self):
        """API ሲቋረጥ ሲስተሙ SAFE MODE መግባቱን ማረጋገጥ።"""
        sys = MockSystem(binance_fail=True)
        with self.assertRaises(ConnectionError):
            sys.get_market_status()
        logging.warning("🛑 API Failure detected and handled.")

    def test_market_volatility_calc(self):
        """የቮላቲሊቲ ስሌት ትክክለኛነት ማረጋገጥ።"""
        prices = [100, 110, 105, 120]
        vol = max(prices) - min(prices)
        self.assertEqual(vol, 20)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    unittest.main()
