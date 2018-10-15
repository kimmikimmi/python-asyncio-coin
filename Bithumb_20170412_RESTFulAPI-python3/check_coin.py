#! /usr/bin/env python

import sys
from xcoin_api_client import *
import pprint
import time

api_key = sys.argv[0];
api_secret = sys.argv[1];

api = XCoinAPI(api_key, api_secret);

rgParams = {
	"order_currency" : "BTC",
	"payment_currency" : "KRW"
};

#coin_dic = api.xcoinApiCall("/public/ticker/ALL", rgParams)["data"];
coin_dic = {}

#
# public api
#
# /public/ticker
# /public/recent_ticker
# /public/orderbook
# /public/recent_transactions

result = api.xcoinApiCall("/public/ticker/ALL", rgParams);
print(len(result["data"]));
keys = result["data"].keys();
print(keys);
while True:
    result = api.xcoinApiCall("/public/ticker/ALL", rgParams)
    print(result["data"].keys())
    if len(coin_dic) == len(result["data"]):
        print("새로 추가된 코인이 없습니다")
    else:
        print("새로 추가된 코인이 있습니다")
        bucket = {}
        for key in keys:
            if key not in coin_dic:
                bucket[key] = result["data"][key]
        #purchase all items in bucket
        for item in bucket:
            print(item + '을 구매합니다')

    time.sleep(3)

# private api
#
# endpoint		=> parameters
# /info/current
# /info/account
# /info/balance
# /info/wallet_address

#result = api.xcoinApiCall("/info/account", rgParams);
#print("status: " + result["status"]);
#print("created: " + result["data"]["created"]);
#print("account id: " + result["data"]["account_id"]);
#print("trade fee: " + result["data"]["trade_fee"]);
#print("balance: " + result["data"]["balance"]);

sys.exit(0);

