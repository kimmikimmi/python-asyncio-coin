from datetime import datetime
import pybithumb

con_key = ""
sec_key = ""

bithumb = pybithumb.Bithumb(con_key, sec_key)

coin_dic = bithumb.get_tickers()
price = bithumb.get_current_price("BTC")
print(price)
bucket = {}
balance2 = bithumb.get_balance("TRX")

print(balance2[2])


def check_new_coin():
    recent = get_all()

    if len(recent) < len(coin_dic):
        for coin in coin_dic:
            if coin not in recent:
                print("신규 상장 코인이 있습니다" + coin)
                bucket[coin] = bithumb.get_current_price(coin)
                coin_dic.append(coin)  # 신규 코인 추가
                return coin
    elif len(recent) == len(coin_dic):
        print("신규 상장 코인이 없습니다")
    else:
        print("사라진 코인이 있습니다")
        for coin in recent:
            if coin not in coin_dic:
                coin_dic.pop(coin)  # 사라진 코인 제거

    return "NONE"


def buy_coin_in_bucket():
    if len(bucket) > 0:
        print("매수 합니다")
        buy_if_possible()

    else:
        print("매도할 코인이 없습니다")


def sell_coin_in_bucket():
    if len(bucket) > 0:
        print("매도합니다")
        sell_if_possible()
    else:
        print("매도할 코인이 없습니디")


def buy_if_possible():
    for coin in bucket:
        recent_price = bithumb.get_current_price(coin)
        total_krw = bithumb.get_balance(coin)[2]

        lower_bound = 1.2 * bucket[coin]
        if recent_price >= lower_bound:
            if total_krw >= lower_bound:
                buy(total_krw, recent_price)


def buy(total_krw, recent_price):
    for coin in bucket:
        unit = total_krw / recent_price
        bithumb.buy_market_order(coin, unit)


def sell_if_possible():
    for coin in bucket:
        recent_price = bithumb.get_current_price(coin)
        if recent_price >= 2.0 * bucket[coin]:
            unit = bithumb.get_balance(coin)[0]
            sell(unit)


def sell(unit):
    for coin in bucket:
        bithumb.sell_market_order(coin, unit)


def get_all():
    print('Tick! The time is: %s' % datetime.now())

    coins = bithumb.get_tickers()
    print(coins)
    return coins
