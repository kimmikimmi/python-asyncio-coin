from datetime import datetime
import pybithumb

##############################################################################################################################
con_key = ""
sec_key = ""

bithumb = pybithumb.Bithumb(con_key, sec_key)

coin_cache = bithumb.get_tickers()
#coin_cache.remove("BTC")
#change coin_cache if u wanna test it
bucket = {}

times_for_sell = 2
times_for_buy = 1.2


##############################################################################################################################

def check_new_coin():
    recent = get_all()

    if len(recent) > len(coin_cache):
        for coin in recent:
            if coin not in coin_cache:
                print("[%s] - there is a new coin !! .. from checking job \tcoin : %s" % (datetime.now(), coin))
                bucket[coin] = bithumb.get_current_price(coin)
                coin_cache.append(coin)  # 신규 코인 추가

    elif len(recent) == len(coin_cache):
        print("[%s] - nothing changed.. .. from checking job" % datetime.now())

    else:
        print("[%s] - a coin disappear... .. from checking job" % datetime.now())
        for coin in coin_cache:
            if coin not in recent:
                coin_cache.remove(coin)  # 사라진 코인 제거


##############################################################################################################################
def get_all():
    coins = bithumb.get_tickers()

    print("[%s] - # of remote : %d \t|\t # in Cache : %d" % (datetime.now(), len(coins), len(coin_cache)))
    return coins


##############################################################################################################################
def make_a_deal():
    if len(bucket) == 0:
        return

    for coin in list(bucket):  # thread - safe
        print("[%s] - there is a coin to deal \t bucket : %s" % (datetime.now(), bucket))
        balance = bithumb.get_balance(coin)

        if balance[0] == 0:  # 신규 coin 개수가 0 -> 아직 구입하지 않음.
            buy_if_possible(balance[2], coin)

        else:
            sell_if_possible(balance[0], coin)


## BUYING FUNCTION############################################################################################################################

def buy_if_possible(total_krw, coin):
    recent_price = bithumb.get_current_price(coin)
    price_to_buy = times_for_buy * bucket[coin]

    if recent_price >= price_to_buy and total_krw >= price_to_buy:
        unit = total_krw / recent_price
        print("[%s] - buy\tname: %s, unit %d" % (datetime.now(), coin, unit))
        return bithumb.buy_market_order(coin, unit)


## SELLING FUNCTIONS#####################################################################################################################
def sell_if_possible(unit, coin):
    recent_price = bithumb.get_current_price(coin)

    if recent_price >= times_for_sell * bucket[coin]:  # 코인 값이 상장가의 2배가 되는 경우 매도.
        print("[%s] - sell\tname : %s unit : %d" % (datetime.now(), coin, unit))
        bithumb.sell_market_order(coin, unit)
        bucket.clear()  # clear bucket after

##############################################################################################################################
