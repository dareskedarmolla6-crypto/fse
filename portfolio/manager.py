class PortfolioManager:
    def __init__(self, initial_capital):
        self.total_balance = initial_capital
        self.assets = {}

    def update_balance(self, new_balance):
        self.total_balance = new_balance
        print(f"Portfolio balance updated: {self.total_balance}")

    def track_allocation(self, asset_name, amount):
        """
        Updates the amount held for a specific asset.
        """
        self.assets[asset_name] = amount
        return self.assets

    def get_portfolio_summary(self):
        return {
            "Total": self.total_balance,
            "Holdings": self.assets
        }
