# Level 1

Build a class / object that can track your portfolio.  You do not need to track individual trades or tax lots, but it should capture the net impact of the trade on the portfolio (+/- cash and +/- quantity of shares).  

It should have methods:
    * Buy(ticker: string, quantity: integer, pricePerShare: decimal) : void : exception
       - Must have sufficient cash
    * Sell(ticker: string, quantity: integer, pricePerShare: decimal) : void : exception
       - Must have sufficient quantity
    * GetCashBalance() : decimal
    * GetQuantityOfShares(ticker: string) : integer

# Level 2

Given a list of predicted daily prices for a stock, write code that generates trades to maximize gains in that stock.

Instructions:
You may trade at most once per day, but are not required to trade every day.
Shares must be purchased as whole numbers (no fractional shares).
Shares and cash cannot be negative.
The position should be liquidated when there is no remaining price data.
Log what actions are taken each day (see “Output” below).

Starting Cash: 100000
Ticker: ABCD

Predicted Daily Prices for ABCD:
```python
 [
  170, // Day 1
  175, // Day 2
  172, // Day 3
  170, // Day 4
  180 // Day 5
 ]
```
