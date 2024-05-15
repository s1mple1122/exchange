import hashlib
import json
import random
import string
import time

import requests

from websea.classes import *

TOKEN = ""
SECRET = ""
HOST = "https://oapi.websea.com"


# HTTP Request Methods
def request(args, name):
    if not 'headers' in args:
        args['headers'] = {}
    if not 'user-agent' in args['headers']:
        args['headers'][
            'user-agent'] = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36"
    if not 'data' in args:
        args['data'] = {}
    args['headers'].update(mkHeader(args['data']))
    suc = False
    result = {}
    r = None
    try:
        if args['method'] == 'GET':
            r = requests.get(args['url'], params=args['data'], cookies=None, headers=args['headers'],
                             timeout=int(args['timeout']), verify=True)
            suc = True
        elif args['method'] == 'POST':
            r = requests.post(args['url'], data=args['data'], cookies=None, headers=args['headers'],
                              timeout=int(args['timeout']), verify=True)
            suc = True
        result = {'code': r.status_code, 'headers': r.headers, 'content': r.content}
    except:
        print("从websea交易所操作 -{}- 失败,请求参数 -{}-".format(name, args['data']))

    return suc, result


# Method of Generating HTTP Headers with Signature
def mkHeader(data=None):
    if data is None:
        data = dict()
    ran_str = ''.join(random.sample(string.ascii_letters + string.digits, 5))
    nonce = "%d_%s" % (int(time.time()), ran_str)
    header = dict()
    header['Token'] = TOKEN
    header['Nonce'] = nonce
    header['Signature'] = sign(nonce, data)
    return header


# Signature Generation Method
def sign(nonce, data=None):
    if data is None:
        data = dict()
    tmp = list()
    tmp.append(TOKEN)
    tmp.append(SECRET)
    tmp.append(nonce)
    for d, x in data.items():
        tmp.append(str(d) + "=" + str(x))
    return hashlib.sha1(''.join(sorted(tmp)).encode("utf8")).hexdigest()


# 市场行情
def marketDepth(data=None, timeout=3) -> MarketBook | None:
    """
    获取交易对的市场行情
    :param timeout: 超时时间
    :param data: 是一个字典 {'symbol': 'BTC-USDT', 'size': 1000}  size最大值1000
    :return: 返回一个市场行情,里面包含两个数组 asks 和 bids  还有请求时的时间戳
    """
    if data is None:
        data = dict()
    args = dict()
    args['url'] = HOST + '/openApi/market/depth'
    args['method'] = 'GET'
    args['timeout'] = timeout
    args['data'] = data
    suc, result = request(args, "获取市场行情")
    if not suc:
        return None
    else:
        if result['code'] == 200:
            data = json.loads(result['content'])
            if "result" in data:
                marketDepthBook = MarketBook()
                asks = data["result"]["asks"]
                bids = data["result"]["bids"]
                ts = data["result"]["ts"]
                marketDepthBook.asks = asks
                marketDepthBook.bids = bids
                marketDepthBook.timestamp = ts
                return marketDepthBook
            else:
                print("获取市场行情错误", data)
    return None


# 订单薄
def currentList(data=None, timeout=3) -> list[OrderBook] | None:
    """
    获取用户的交易订单
    :param timeout: 超时时间,,默认3秒
    :param data: 是一个字典 {'symbol': 'BTC-USDT', 'limit': 100} limit最大值100,symbol不建议为空,其他参数不建议使用
    :return: 返回一个订单薄数组,里面是每个订单
    """
    if data is None:
        data = dict()
    args = dict()
    args['url'] = HOST + '/openApi/entrust/currentList'
    args['method'] = 'GET'
    args['timeout'] = timeout
    args['data'] = data
    suc, result = request(args, "获取用户订单")
    if not suc:
        return None
    else:
        if result['code'] == 200:
            data = json.loads(result['content'])
            if "result" in data:
                orderBooks = []
                for order_data in data["result"]:
                    order_book = OrderBook(
                        order_data["order_sn"],
                        order_data["symbol"],
                        order_data["ctime"],
                        order_data["type"],
                        order_data["side"],
                        order_data["price"],
                        order_data["number"],
                        order_data["total_price"],
                        order_data["deal_number"],
                        order_data["deal_price"],
                        order_data["status"]
                    )
                    orderBooks.append(order_book)
                return orderBooks
            else:
                print("获取用户订单列表错误", data)
    return None


# 下订单
def addOrder(data=None, timeout=3) -> Order | None:
    """
    :param timeout: 超时时间,默认3秒
    :param data: data是一个字典
        {'symbol': 'BTC-USDT', 'type': 'buy-limit', 'amount': 1.25354, 'price': 3504.76}
        amount: 对于限价订单，它代表订单数量。对于市价买单，它表示购买多少钱（usdt）。对于市价卖单，表示卖出多少币（btc）
        price: 委托价格，市价委托不传此参数
        type: buy-market sell-market buy-limit sell-limit
    :return:
    """
    if data is None:
        data = dict()
    args = dict()
    args['url'] = HOST + '/openApi/entrust/add'
    args['method'] = 'POST'
    args['timeout'] = timeout
    args['data'] = data
    suc, result = request(args, "下订单")

    if not suc:
        return None
    else:
        if result['code'] == 200:
            data = json.loads(result['content'])
            if "result" in data:
                order = Order(data["result"]["order_sn"])
                return order
            else:
                print("下订单发生错误", data)
    return None


# 资金列表
def walletList(data=None, timeout=3) -> list[Account] | None:
    if data is None:
        data = dict()
    args = dict()
    args['url'] = HOST + '/openApi/wallet/list'
    args['method'] = 'GET'
    args['timeout'] = timeout
    args['data'] = data
    suc, result = request(args, "查询钱包余额")
    if not suc:
        return None
    else:
        if result['code'] == 200:
            data = json.loads(result['content'])
            if "result" in data:
                accounts = []
                for account_data in data["result"]:
                    account = Account(
                        account_data["currency"],
                        account_data["available"],
                        account_data["frozen"]
                    )
                    accounts.append(account)
                    return accounts
            else:
                print("获取资金列表错误", data)
    return None


# 取消订单
def cancelOrder(data=None, timeout=3) -> list[str] | None:
    """
    :param timeout: 超时时间,默认3秒
    :param data:{'order_ids':'sn1,sn2','symbol':'BTC-USDT'}
    :return: 取消成功的订单号集合
    """
    if data is None:
        data = dict()
    args = dict()
    args['url'] = HOST + '/openApi/entrust/cancel'
    args['method'] = 'POST'
    args['timeout'] = timeout
    args['data'] = data
    suc, result = request(args, "取消订单")
    if not suc:
        return None
    else:
        if result['code'] == 200:
            data = json.loads(result['content'])
            if "result" in data:
                success = data["result"]["success"]
                return success
            else:
                print("取消订单错误", data)
    return None


# 订单详情
def orderDetails(data=None, timeout=3) -> OrderMessage | None:
    """
    :param data: {'order_sn':'bs12315151215121'}
    :param timeout:
    :return:订单详情或者None
    """
    if data is None:
        data = dict()
    args = dict()
    args['url'] = HOST + '/openApi/entrust/status'
    args['method'] = 'GET'
    args['timeout'] = timeout
    args['data'] = data
    suc, result = request(args, "查询订单详情")
    if not suc:
        return None
    else:
        if result['code'] == 200:
            data = json.loads(result['content'])
            if "result" in data:
                om = OrderMessage()
                order_data = data['result']
                om.order_sn = order_data['order_sn']
                om.symbol = order_data['symbol']
                om.ctime = order_data['ctime']
                om.type = order_data['type']
                om.side = order_data['side']
                om.price = order_data['price']
                om.number = order_data['number']
                om.total_price = order_data['total_price']
                om.deal_number = order_data['deal_number']
                om.deal_price = order_data['deal_price']
                om.status = order_data['status']
                return om
            else:
                print("获取订单详情错误", data)
    return None


# 订单成交详情
def orderTradeDetails(data=None, timeout=3) -> list[Trade] | None:
    """
    :param data: {'order_sn':'bs33312351321'}
    :param timeout:
    :return: 如果订单未成交返回[],成交返回记录,发生错误时返回Node
    """
    if data is None:
        data = dict()
    args = dict()
    args['url'] = HOST + '/openApi/entrust/deal'
    args['method'] = 'GET'
    args['timeout'] = timeout
    args['data'] = data
    suc, result = request(args, "查询订单执行情况")
    if not suc:
        return None
    else:
        if result['code'] == 200:
            data = json.loads(result['content'])
            if "result" in data:
                TradeBooks = []
                for trade_data in data["result"]:
                    trade = Trade()
                    trade.ctime = trade_data["ctime"]
                    trade.price = trade_data["price"]
                    trade.number = trade_data["number"]
                    trade.total_price = trade_data["total_price"]
                    trade.fee = trade_data["fee"]
                    TradeBooks.append(trade)
                return TradeBooks
            else:
                print("获取订单成交详情错误", data)
    return None


# 获取24小时行情列表
def marketList24(data=None, timeout=3) -> list[MarketList] | None:
    """
    不传递symbol会返回所有代币,否则只返回symbol
    :param data: {'symbol':'BTC-USDT'}
    :param timeout:
    :return:
    """
    if data is None:
        data = dict()
    args = dict()
    args['url'] = HOST + '/openApi/market/24kline'
    args['method'] = 'GET'
    args['timeout'] = timeout
    args['data'] = data
    suc, result = request(args, "查询24小时行情列表")
    if not suc:
        return None
    else:
        if result['code'] == 200:
            data = json.loads(result['content'])
            if "result" in data:
                list24 = []
                for ls in data["result"]:
                    msg = MarketList()
                    msg.symbol = ls['symbol']
                    msg.ask = ls['ask']
                    msg.bid = ls['bid']
                    msg.id = ls['data']['id']
                    msg.amount = ls['data']['amount']
                    msg.count = ls['data']['count']
                    msg.open = ls['data']['open']
                    msg.close = ls['data']['close']
                    msg.low = ls['data']['low']
                    msg.high = ls['data']['high']
                    msg.vol = ls['data']['vol']
                    list24.append(msg)
                return list24
        else:
            print("获取24小时行情失败", data)
    return None


# 获取24小时行情数据
def marketData24(data=None, timeout=3) -> MarketData or None:
    """
    获取24小时行情数据
    :param data: {'symbol':'BTC-USDT'}
    :param timeout:
    :return:
    """
    if data is None:
        print("参数必须使用symbol,data = ", data)
        return None
    args = dict()
    args['url'] = HOST + '/openApi/market/detail'
    args['method'] = 'GET'
    args['timeout'] = timeout
    args['data'] = data
    suc, result = request(args, "查询24小时行情数据")
    if not suc:
        return None
    else:
        if result['code'] == 200:
            data = json.loads(result['content'])
            if "result" in data:
                market_data = data['result']
                ms = MarketData()
                ms.open = market_data.get('open')
                ms.close = market_data.get('close')
                ms.low = market_data.get('low')
                ms.high = market_data.get('high')
                ms.amount = market_data.get('amount')
                ms.count = market_data.get('count')
                ms.vol = market_data.get('vol')
                ms.id = market_data.get('id')
                return ms
        else:
            print("获取23小时行情数据失败", data)
    return None


# 查询市场交易
def marketTradeMessage(data=None, timeout=3) -> TradeData | None:
    if data is None:
        print("参数必须使用symbol,data = ", data)
        return None
    args = dict()
    args['url'] = HOST + '/openApi/market/trade'
    args['method'] = 'GET'
    args['timeout'] = timeout
    args['data'] = data
    suc, result = request(args, "查询24小时行情数据")
    if not suc:
        return None
    else:
        if result['code'] == 200:
            data = json.loads(result['content'])

            if "result" in data:
                tradeList = []
                for ls in data["result"]['data']:
                    trade = TradeMessage()
                    trade.id = ls['id'],
                    trade.amount = ls['amount'],
                    trade.price = ls['price'],
                    trade.vol = ls['vol'],
                    trade.direction = ls['direction'],
                    trade.ts = ls['ts']
                    tradeList.append(trade)
                buy = []
                sell = []
                for msg in tradeList:
                    if msg.direction == "buy":
                        buy.append(msg)
                    else:
                        sell.append(msg)
                tradeData = TradeData(sell=sell, buy=buy)
                return tradeData
            else:
                print("获取市场交易信息失败", data)
    return None
