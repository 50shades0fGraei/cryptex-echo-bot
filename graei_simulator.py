import random
import numpy as np
from typing import Dict, Any, List
from datetime import datetime, timedelta
from graei_strategy import trade_overlap_zones
from currency import Currency
from graei_constants import *

class GraeiSimulator:
    def __init__(self, initial_capital: Dict[str, float] = None, initial_prices: Dict[str, float] = None):
        self.initial_capital = initial_capital or starting_capital.copy()
        self.capital = self.initial_capital.copy()
        self.initial_prices = initial_prices or initial_prices.copy()
        self.current_prices = self.initial_prices.copy()
        self.monthly_pool = 0
        self.month_profits = [0]
        self.day = 0
        self.month = 1
        self.trades = []
        self.equity_curve = []
        
        self.currencies = {name: Currency(name, price) for name, price in self.initial_prices.items()}

    def update_prices(self):
        """Update prices for all currencies based on fluctuation rules."""
        self.current_prices["in_passer1"] *= (1 + daily_fluctuation_in_passer1)
        self.current_prices["in_passer2"] *= (1 + daily_fluctuation_in_passer2)
        direction = random.choice([-1, 1])
        self.current_prices["runner"] *= (1 + daily_fluctuation_runner * direction)
        self.current_prices["runner"] = max(1000, min(15000, self.current_prices["runner"]))

    def apply_profit_boost(self):
        """Apply profit boost to currencies with positive daily profit."""
        for curr_name in ["runner", "in_passer1", "in_passer2"]:
            daily_profit = self.capital[curr_name] - (initial_investment * self.initial_capital[curr_name] / initial_investment)
            if daily_profit > 0:
                self.capital[curr_name] *= (1 + profit_boost)

    def apply_monthly_boost(self):
        """Apply monthly boost based on previous month's profits."""
        if self.month_profits:
            monthly_boost = sum(self.month_profits[-1] * 0.5 for _ in range(3))
            for curr_name in self.initial_capital:
                self.capital[curr_name] += monthly_boost * (self.initial_capital[curr_name] / initial_investment)

    def calculate_monthly_profit(self):
        """Calculate and store monthly profit."""
        month_profit = sum(
            self.capital[curr] - (initial_investment * self.initial_capital[curr] / initial_investment)
            for curr in self.initial_capital
        )
        self.month_profits.append(month_profit)

    def calculate_performance_metrics(self) -> Dict[str, Any]:
        """Calculate final performance metrics."""
        total = sum(self.capital.values()) + self.monthly_pool
        quarterly_roi = (total / initial_investment - 1) * 100

        # Calculate max drawdown using equity curve
        if self.equity_curve:
            equity_array = np.array(self.equity_curve)
            peak = np.maximum.accumulate(equity_array)
            drawdown = (peak - equity_array) / peak * 100
            max_drawdown = np.max(drawdown)
        else:
            max_drawdown = 0

        return {
            "capital": self.capital,
            "monthly_pool": self.monthly_pool,
            "total": total,
            "quarterly_roi": quarterly_roi,
            "max_drawdown": max_drawdown,
            "trades": len(self.trades),
            "monthly_profits": self.month_profits,
            "equity_curve": self.equity_curve
        }

    def simulate(self, days: int = days_in_quarter) -> Dict[str, Any]:
        """Run the simulation for specified number of days."""
        for self.day in range(days):
            # Update prices
            self.update_prices()

            # Perform daily trades
            daily_equity = sum(self.capital.values()) + self.monthly_pool
            self.equity_curve.append(daily_equity)

            for _ in range(3):  # 3 trades per day
                self.monthly_pool = trade_overlap_zones(
                    self.current_prices,
                    self.capital,
                    self.currencies,
                    self.monthly_pool
                )

            # Apply profit boost
            self.apply_profit_boost()

            # Monthly processing
            if self.day % 30 == 0 and self.day > 0:
                self.apply_monthly_boost()
                self.month += 1

            # Track monthly profits
            if self.day % 30 == 29:
                self.calculate_monthly_profit()

        return self.calculate_performance_metrics()

def run_simulation(days: int = days_in_quarter) -> Dict[str, Any]:
    """Convenience function to run simulation with default parameters."""
    simulator = GraeiSimulator()
    return simulator.simulate(days)
