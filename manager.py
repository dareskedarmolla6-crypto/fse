class RiskManager:
    """የስጋት አስተዳደር ዋና ክፍል (Risk Manager)"""
    
    def __init__(self, balance):
        self.balance = balance
        self.max_risk_per_trade = 0.02  # በአንድ ትሬድ የሚፈቀድ 2% ስጋት
        
    def get_max_position(self):
        """ከካፒታል አቅም አንጻር የሚፈቀደውን ከፍተኛ የትሬዲንግ መጠን ይመልሳል"""
        return self.balance * self.max_risk_per_trade

    def check_risk_limits(self, trade_amount):
        """ትሬዱ በገደቡ ውስጥ መሆኑን ያረጋግጣል"""
        if trade_amount <= self.get_max_position():
            return True
        return False
