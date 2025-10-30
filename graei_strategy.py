from typing import Dict, Any
from datetime import datetime

class GraeiStrategy:
    def __init__(self):
        self.name = "Graei Echo"
        self.description = "Price relationship analysis trading strategy"
        self.params = {
            "overlap_threshold": 0.05,  # 5% price overlap threshold
            "min_confidence": 0.7,      # Minimum confidence for trade signals
            "position_size": 0.2        # Use 20% of available capital per trade
        }

    def trade_overlap_zones(self, current_prices, capital, currencies, monthly_pool):
        """Original Graei trading logic."""
        runner_price = current_prices["runner"]
        in_passer1_price = current_prices["in_passer1"]
        in_passer2_price = current_prices["in_passer2"]

        # Buy Runner near In-Passer 1
        if abs(runner_price - in_passer1_price) / in_passer1_price <= self.params["overlap_threshold"] and runner_price < in_passer1_price:
            units_to_buy = capital["runner"] / runner_price
            cost = currencies["runner"].buy(runner_price, units_to_buy, capital["runner"])
            capital["runner"] -= cost

        # Sell Runner near In-Passer 2
        if abs(runner_price - in_passer2_price) / in_passer2_price <= self.params["overlap_threshold"] and runner_price >= in_passer2_price * 0.5:
            total_units = sum(units for _, units in currencies["runner"].positions)
            if total_units > 0:
                units_to_sell = min(1, total_units)
                proceeds = currencies["runner"].sell(runner_price, units_to_sell)
                capital["runner"] += proceeds
                profit = proceeds - (runner_price * units_to_sell * 0.9)
                if profit > 0:
                    pool_amount = profit * 0.5
                    reinvest_amount = profit * 0.5
                    capital["runner"] += reinvest_amount
                    monthly_pool += pool_amount

        return monthly_pool
    
    def analyze_prices(self, prices: list) -> Dict[str, Any]:
        """Analyze price data and generate trading signals."""
        if not prices or len(prices) < 2:
            return {
                "signal": "neutral",
                "confidence": 0.0,
                "reason": "Insufficient price data"
            }
        
        # Calculate basic metrics
        current_price = prices[-1]
        prev_price = prices[-2]
        price_change = (current_price - prev_price) / prev_price
        
        # Simple trend analysis
        if price_change > self.params["overlap_threshold"]:
            return {
                "signal": "buy",
                "confidence": min(abs(price_change) * 5, 1.0),
                "reason": "Strong upward movement"
            }
        elif price_change < -self.params["overlap_threshold"]:
            return {
                "signal": "sell",
                "confidence": min(abs(price_change) * 5, 1.0),
                "reason": "Strong downward movement"
            }
        
        return {
            "signal": "neutral",
            "confidence": 0.0,
            "reason": "No clear signal"
        }
    
    def calculate_position_size(self, capital: float, price: float) -> float:
        """Calculate the position size for a trade."""
        return capital * self.params["position_size"] / price
    
    def should_trade(self, analysis: Dict[str, Any]) -> bool:
        """Determine if we should trade based on the analysis."""
        return (
            analysis["signal"] in ["buy", "sell"] and 
            analysis["confidence"] >= self.params["min_confidence"]
        )


# Backwards-compatible module-level function expected by other modules
def trade_overlap_zones(current_prices, capital, currencies, monthly_pool):
    """Compatibility wrapper that uses GraeiStrategy's logic.

    Existing code imports `trade_overlap_zones` directly from this module.
    We keep that API by instantiating GraeiStrategy and delegating the call.
    """
    strategy = GraeiStrategy()
    return strategy.trade_overlap_zones(current_prices, capital, currencies, monthly_pool)
