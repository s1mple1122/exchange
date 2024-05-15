class MarketBook:
    def __init__(self, asks=None, bids=None, timestamp=None):
        self.asks = asks if asks is not None else []
        self.bids = bids if bids is not None else []
        self.timestamp = timestamp


class OrderBook:
    def __init__(self, order_sn=None, symbol=None, ctime=None, type=None,
                 side=None, price=None, number=None, total_price=None, deal_number=None, deal_price=None, status=None):
        self.order_sn = order_sn
        self.symbol = symbol
        self.ctime = ctime
        self.type = type
        self.side = side
        self.price = price
        self.number = number
        self.total_price = total_price
        self.deal_number = deal_number
        self.deal_price = deal_price
        self.status = status


class Order:
    def __init__(self, order_sn=None):
        self.order_sn = order_sn


class Account:
    def __init__(self, currency=None, available=None, frozen=None):
        self.currency = currency
        self.available = available
        self.frozen = frozen


class OrderMessage:
    def __init__(self, order_sn=None, symbol=None, ctime=None, type=None, side=None, price=None, number=None,
                 total_price=None, deal_number=None, deal_price=None, status=None):
        self.order_sn = order_sn
        self.symbol = symbol
        self.ctime = ctime
        self.type = type
        self.side = side
        self.price = price
        self.number = number
        self.total_price = total_price
        self.deal_number = deal_number
        self.deal_price = deal_price
        self.status = status


class Trade:
    def __init__(self, id=None, ctime=None, price=None, number=None, total_price=None, fee=None):
        self.id = id
        self.ctime = ctime
        self.price = price
        self.number = number
        self.total_price = total_price
        self.fee = fee


class MarketList:
    def __init__(self, symbol=None, id=None, amount=None, count=None, open=None, close=None, low=None, high=None, vol=None, ask=None, bid=None):
        self.symbol = symbol
        self.id = id
        self.amount = amount
        self.count = count
        self.open = open
        self.close = close
        self.low = low
        self.high = high
        self.vol = vol
        self.ask = ask
        self.bid = bid


class MarketData:
    def __init__(self, id=None, amount=None, count=None, open=None, close=None, low=None, high=None, vol=None):
        self.id = id
        self.amount = amount
        self.count = count
        self.open = open
        self.close = close
        self.low = low
        self.high = high
        self.vol = vol


class TradeMessage:
    def __init__(self, id=None, amount=None, price=None, vol=None, direction=None, ts=None):
        self.id = id
        self.amount = amount
        self.price = price
        self.vol = vol
        self.direction = direction
        self.ts = ts


class TradeData:
    def __init__(self, buy=None, sell=None):
        self.buy = buy if buy is not None else []
        self.sell = sell if sell is not None else []