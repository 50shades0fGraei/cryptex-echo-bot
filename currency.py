class Currency:
    def __init__(self, name, price):
        self.name = name
        self.price = price
        self.positions = []

    def buy(self, price, units, capital):
        cost = price * units
        if capital >= cost:
            self.positions.append((price, units))
            return cost
        return 0

    def sell(self, price, units_to_sell):
        if not self.positions:
            return 0
        proceeds = 0
        sold_units = 0
        new_positions = []
        for buy_price, units in self.positions:
            if sold_units < units_to_sell:
                sell_units = min(units, units_to_sell - sold_units)
                sold_units += sell_units
                proceeds += sell_units * price
                remaining_units = units - sell_units
                if remaining_units > 0:
                    new_positions.append((buy_price, remaining_units))
            else:
                new_positions.append((buy_price, units))
        self.positions = new_positions
        return proceeds

    def portfolio_value(self):
        return sum(units * self.price for _, units in self.positions)

    def average_cost(self):
        if not self.positions:
            return 0
        total_cost = sum(price * units for price, units in self.positions)
        total_units = sum(units for _, units in self.positions)
        return total_cost / total_units if total_units > 0 else 0

