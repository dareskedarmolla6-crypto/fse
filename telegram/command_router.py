# fse/telegram/command_router.py


# =========================
# CONTROL CENTER (DASHBOARD UPDATES)
# =========================
class ControlCenter:
    def __init__(self, telegram):
        self.telegram = telegram

    async def update_all(self, state):
        msg = (
            f"📊 FSE DASHBOARD UPDATE\n\n"
            f"Balance: {state.get('balance', 0)}\n"
            f"Trades: {state.get('trades', 0)}\n"
            f"Profit: {state.get('profit', 0)}\n"
            f"Status: {state.get('status', 'UNKNOWN')}"
        )

        await self.telegram.send_message(msg)


# =========================
# SIGNAL DISTRIBUTOR (MULTI CHANNEL BROADCAST)
# =========================
class SignalDistributor:
    def __init__(self, telegram=None, discord=None, email=None):
        self.telegram = telegram
        self.discord = discord
        self.email = email

    async def broadcast(self, signal):
        msg = self._format(signal)

        if self.telegram:
            await self.telegram.send_message(msg)

        if self.discord:
            await self.discord.send(msg)

        if self.email:
            self.email.send(
                subject="FSE Trading Signal",
                body=msg
            )

    def _format(self, signal):
        return (
            "📡 FSE SIGNAL ALERT\n\n"
            f"{signal}"
        )
