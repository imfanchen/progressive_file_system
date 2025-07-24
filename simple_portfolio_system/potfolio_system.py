

from dataclasses import dataclass
from decimal import Decimal
from typing import List

class Portfolio:

    def __init__(self, initial_balance: Decimal):
        self.balance = initial_balance
        self.positions = {} # {ticker: quantity}

    def buy(self, ticker: str, quantity: int, price_per_share: Decimal):
        cost = quantity * price_per_share
        if (cost > self.balance):
            print(f"Insufficient cash: {self.balance}. Cost: {cost}.")
            return
        self.balance -= cost
        if ticker not in self.positions:
            self.positions[ticker] = 0
        self.positions[ticker] += quantity
    
    def sell(self, ticker: str, quantity: int, price_per_share: Decimal):
        cost = quantity * price_per_share
        if quantity > self.positions.get(ticker, 0):
            print(f"Do not have {quantity} of {ticker} to sell")
            return
        self.balance += cost
        self.positions[ticker] -= quantity

    def get_cash_balance(self) -> Decimal:
        return self.balance

    def get_quantity_of_shares(self, ticker: str) -> int:
        return self.positions.get(ticker, 0)

    def __repr__(self):
        return f"Portfolio Balance {self.balance}, Positions {self.positions}"


@dataclass
class Action:
    day: int # 0-index of the price action
    action_type: str  # BUY or SELL or HOLD
    ticker: str
    quantity: int
    today_price: Decimal
    tomorrow_price: Decimal


def maximize_gains(prices: List[Decimal], initial_cash: Decimal, ticker: str):
    portfolio = Portfolio(initial_cash)
    actions: List[Action] = []
    for i in range(len(prices)):
        today_price = prices[i]
        is_last_day = (i == len(prices) - 1)
        if is_last_day:
            quantity_to_liquidate = portfolio.get_quantity_of_shares(ticker)
            if quantity_to_liquidate > 0:
                portfolio.sell(ticker, quantity_to_liquidate, today_price)
                actions.append(Action(i, "SELL", ticker, quantity_to_liquidate, today_price, Decimal(0)))
            else:
                actions.append(Action(i, "HOLD", ticker, 0, today_price, Decimal(0)))
            break
        tomorrow_price = prices[i + 1]
        if tomorrow_price > today_price:
            quantity_to_buy = int(portfolio.get_cash_balance() // today_price)
            if quantity_to_buy > 0:
                portfolio.buy(ticker, quantity_to_buy, today_price)
                actions.append(Action(i, "BUY", ticker, quantity_to_buy, today_price, tomorrow_price))
            else:
                actions.append(Action(i, "HOLD", ticker, 0, today_price, tomorrow_price))
        elif tomorrow_price < today_price:
            quantity_to_sell = portfolio.get_quantity_of_shares(ticker)
            if quantity_to_sell > 0:
                portfolio.sell(ticker, quantity_to_sell, today_price)
                actions.append(Action(i, "SELL", ticker, quantity_to_sell, today_price, tomorrow_price))
            else:
                actions.append(Action(i, "HOLD", ticker, 0, today_price, tomorrow_price))
        else:
            actions.append(Action(i, "HOLD", ticker, 0, today_price, Decimal(0)))
    return actions

