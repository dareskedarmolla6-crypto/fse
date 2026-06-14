# FSE API REFERENCE - LEVERAGE SYSTEM

## Overview
This document defines the confidence-based leverage system used in the FSE trading engine.

---

## 📊 Confidence → Leverage Mapping

The system determines leverage based on AI confidence level:

| Confidence Range | Leverage |
|-----------------|----------|
| < 15%           | NO TRADE |
| 15 - 25%        | 5x       |
| 26 - 35%        | 8x       |
| 36 - 55%        | 10x      |
| 56 - 75%        | 15x      |
| 76 - 85%        | 20x      |
| 86%+            | 30x      |

---

## 🌪 Volatility Adjustment Rules

Leverage is dynamically adjusted based on market volatility:

- High volatility (≥ 0.8)
  → Reduce leverage (risk protection)

- Low volatility (≤ 0.3)
  → Slight leverage increase (opportunity boost)

---

## 🛡 Hedge Mode Rules

When hedge mode is active:

- Leverage is reduced by safety factor
- Purpose: reduce liquidation risk while maintaining dual positions

---

## ⚠️ Risk Control Rules

- Confidence below 15% → NO TRADE
- Maximum leverage cap → 30x
- All trades must pass risk engine validation before execution

---

## 🌍 Supported Markets (FSE Scope)

### Crypto Exchanges
- Binance
- Bybit
- OKX
- KuCoin
- Gate.io
- MEXC
- Bitget

### Forex Brokers
- MT5
- OANDA
- IC Markets
- Pepperstone
- Exness

### Future Expansion
- Indices
- Commodities (Gold, Silver, Oil)
- Stocks

---

## 🧠 System Behavior Summary

FSE uses a hybrid model:

- AI Confidence → determines trade strength
- Volatility → adjusts risk exposure
- Hedge mode → reduces leverage exposure
- Risk engine → final execution approval layer

---

## 🔐 Safety Note

This system is designed for:
- High-frequency crypto trading
- Alpha coin volatility exploitation
- Risk-controlled leverage scaling

Use caution: high leverage increases liquidation risk.
