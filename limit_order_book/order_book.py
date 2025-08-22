import itertools
import heapq
from collections import deque
from datetime import datetime
from dataclasses import dataclass


@dataclass
class Order:
    id: int
    side: str  # 'buy' or 'sell'
    price: float
    quantity: int
    timestamp: datetime


class LimitOrderBook:

    def __init__(self):
        self.order_counter = itertools.count()  # generate order id
        self.buy_heap = []  # max-heap for buy price
        self.sell_heap = []  # min-heap for sell price
        self.price_levels = {
            "buy": {},
            "sell": {},
        }  # order queue per price level for each side
        self.orders = {}  # order dict for cancel/modify lookup

    def match_orders(self):
        while self.buy_heap and self.sell_heap:
            highest_buy_price = -self.buy_heap[0]
            lowest_sell_price = self.sell_heap[0]

            if highest_buy_price >= lowest_sell_price:
                # Match found
                buy_order = self.price_levels["buy"][highest_buy_price].popleft()
                sell_order = self.price_levels["sell"][lowest_sell_price].popleft()
                print(f"Matching {buy_order} with {sell_order}")

                trade_price = lowest_sell_price
                trade_quantity = min(buy_order.quantity, sell_order.quantity)
                buy_order.quantity -= trade_quantity
                sell_order.quantity -= trade_quantity
                print(f"Trade executed: {trade_quantity} at {trade_price}")

                if buy_order.quantity == 0:
                    self.price_levels["buy"][highest_buy_price].popleft()
                    del self.orders[buy_order.id]
                    if not self.price_levels["buy"][highest_buy_price]:
                        del self.price_levels["buy"][highest_buy_price]
                        heapq.heappop(self.buy_heap)
                if sell_order.quantity == 0:
                    self.price_levels["sell"][lowest_sell_price].popleft()
                    del self.orders[sell_order.id]
                    if not self.price_levels["sell"][lowest_sell_price]:
                        del self.price_levels["sell"][lowest_sell_price]
                        heapq.heappop(self.sell_heap)
            else:
                break

    def add_order(self, side: str, price: float, quantity: int) -> int:
        order_id = next(self.order_counter)
        order = Order(id=order_id, side=side, price=price, quantity=quantity, timestamp=datetime.now())
        self.orders[order_id] = order

        if price not in self.price_levels[side]:
            self.price_levels[side][price] = deque()
            if side == "buy":
                heapq.heappush(self.buy_heap, -price)
            else:
                heapq.heappush(self.sell_heap, price)

        self.price_levels[side][price].append(order)
        self.match_orders()
        return order_id

    def cancel_order(self, order_id: int):
        order = self.orders.pop(order_id, None)
        if order:
            self.price_levels[order.side][order.price].remove(order)
            if not self.price_levels[order.side][order.price]:
                del self.price_levels[order.side][order.price]


    def modify_order(self, order_id: int, new_price: float = None, new_quantity: int = None):
        order = self.orders.get(order_id)
        if order:
            self.cancel_order(order_id)
            quantity = new_quantity if new_quantity is not None else order.quantity
            price = new_price if new_price is not None else order.price
            return self.add_order(order.side, price, quantity)


if __name__ == "__main__":
    books = {}
    books["AAPL"] = LimitOrderBook()
    books["TSLA"] = LimitOrderBook()
    books["BTC/USDT"] = LimitOrderBook()
    books["ETH/USDT"] = LimitOrderBook()
