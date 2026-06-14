# fse/strategy/mean_reversion.py


class ReversalConfirmationEngine:
    """
    Confirms if market reversal is valid based on:
    trend + volume + momentum
    """

    def confirm_reversal(self, trend: bool, volume: bool, momentum: bool) -> bool:
        return all([trend, volume, momentum])


# =========================
# SMART HEDGE CONTROLLER
# =========================
class SmartHedgeController:
    """
    Manages hedge positions during reversal scenarios
    """

    def manage_position(self, long_position, short_position, reversal_confirmed: bool):

        if not reversal_confirmed:
            return "KEEP_BOTH"

        long_profit = long_position.get("profit", 0)
        short_profit = short_position.get("profit", 0)

        # If reversal confirmed → close weaker side
        if long_profit > short_profit:
            return "CLOSE_SHORT"
        else:
            return "CLOSE_LONG"
