# =====================================================
# FSE GLOBAL CONSTANTS
# =====================================================

# =========================
# SYSTEM SETTINGS
# =========================

BOT_NAME = "FSE"
BOT_VERSION = "1.0"

SCAN_INTERVAL_SECONDS = 180   # 3 minutes


# =========================
# MARKET SETTINGS
# =========================

MIN_CONFIDENCE = 15
MIN_VOLATILITY_PERCENT = 15

DEFAULT_SYMBOL = "DOGEUSDT"


# =========================
# CONFIDENCE → LEVERAGE MAP
# =========================

LEVERAGE_LEVELS = {
    (15, 25): 5,
    (26, 35): 8,
    (36, 55): 10,
    (56, 75): 15,
    (76, 85): 20,
    (86, 100): 30
}

MAX_LEVERAGE = 30


# =========================
# TRADING MODES
# =========================

LONG = "LONG"
SHORT = "SHORT"
HEDGE = "HEDGE"
GRID = "GRID"

NO_TRADE = "NO_TRADE"


# =========================
# RISK MANAGEMENT
# =========================

STOP_LOSS_ENABLED = True

TRAILING_STOP_ENABLED = True
TRAILING_ACTIVATION_PERCENT = 0.05
TRAILING_DISTANCE_PERCENT = 0.02

PARTIAL_TAKE_PROFIT_ENABLED = True
PARTIAL_TP_PERCENT = 0.10

PROFIT_LOCK_ENABLED = True
PROFIT_LOCK_PERCENT = 0.25


# =========================
# EXCHANGE SUPPORT
# =========================

CRYPTO_EXCHANGES = [
    "BINANCE",
    "BYBIT",
    "OKX",
    "KUCOIN",
    "GATE_IO",
    "MEXC",
    "BITGET"
]


FOREX_BROKERS = [
    "MT5",
    "OANDA",
    "IC_MARKETS",
    "PEPPERSTONE",
    "EXNESS"
]


# =========================
# FUTURE MARKET EXPANSION
# =========================

COMMODITIES = [
    "GOLD",
    "SILVER",
    "OIL"
]

INDICES_ENABLED = True
STOCKS_ENABLED = True


# =========================
# SYSTEM STATES
# =========================

SYSTEM_RUNNING = "RUNNING"
SYSTEM_STOPPED = "STOPPED"
SYSTEM_EMERGENCY = "EMERGENCY"


# =========================
# ORDER STATES
# =========================

ORDER_CREATED = "CREATED"
ORDER_OPEN = "OPEN"
ORDER_FILLED = "FILLED"
ORDER_CLOSED = "CLOSED"
ORDER_FAILED = "FAILED"


# =========================
# LOG LEVELS
# =========================

LOG_INFO = "INFO"
LOG_WARNING = "WARNING"
LOG_ERROR = "ERROR"
