from websea.common import *


def exchange():
    data = marketData24(data={'symbol': 'BTC-USDT'})
    print(data)
    depth = marketDepth(data={'symbol': 'BTC-USDT', 'size': 1000})
    order = addOrder(data={'symbol': 'BTC-USDT', 'type': 'buy-limit', 'amount': 0.00010, 'price': 60000.00})
    if order is None:
        print("下订单失败")
    else:
        print(order.order_sn)
    accounts = walletList(timeout=1)
    print(accounts)
    data = currentList()
    cancelOrder(data={'order_ids': data[0].order_sn, 'symbol': 'BTC-USDT'})
    marketTradeMessage({'symbol': 'BTC-USDT'})
    marketList24({'symbol': 'BTC-USDT'})


exchange()
