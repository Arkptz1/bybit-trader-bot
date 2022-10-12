
from pybit import spot
import time
import requests
from pybit import usdt_perpetual
session_auth = usdt_perpetual.HTTP(
    endpoint="https://api.bybit.com",
    api_key="",
    api_secret=""
)
def cancel_orders():
    print(session_auth.closed_profit_and_loss(
    symbol="BTCUSDT"
))
znach = 10
leverage = 10
try:
    print(session_auth.set_leverage(
        symbol="BTCUSDT",
        buy_leverage=leverage,
        sell_leverage=leverage
    ))
except:
    pass
def kline():
    l = time.time()
    g = l %1800
    r = (l - g - 1800) * 1000
    resp = requests.get(f'https://api2.bybit.com/public/linear/market/kline?symbol=BTCUSDT&resolution=30&from={int(l-g-1800)}&to={int(l-g)}&timeStamp={int(l*1000)}&showOrigin=true')
    return resp.json()['result']['list'][0]
while True:
    klin = kline()
    open = float(klin['open'])
    close = float(klin['close'])
    high = float(klin['high'])
    low = float(klin['low'])
    if 0 <= high - open < 10:
        print(session_auth.place_active_order(
            symbol="BTCUSDT",
            side="Sell",
            order_type="Limit",
            price =close+100,
            qty=znach*leverage/close,
            time_in_force="GoodTillCancel",
            reduce_only=False,
            close_on_trigger=False,
            position_idx =0,
            take_profit = close-400
        ))
        orders = session_auth.my_position(symbol="BTCUSDT")['result'][0]['side'] == 'None'
        while orders:
            orders = session_auth.my_position(symbol="BTCUSDT")['result'][0]['side'] == 'None'
            time.sleep(5)
        liq = session_auth.my_position(symbol="BTCUSDT")['result'][0]['liq_price']
        entry = session_auth.my_position(symbol="BTCUSDT")['result'][0]['entry_price']
        print(session_auth.place_active_order(
            symbol="BTCUSDT",
            side="Sell",
            order_type="Limit",
            price = liq-100,
            qty=round(znach*leverage/liq,3),
            time_in_force="GoodTillCancel",
            reduce_only=False,
            close_on_trigger=False,
            position_idx =0,
        ))
        entry_2 = session_auth.my_position(symbol="BTCUSDT")['result'][0]['entry_price']
        while (entry_2 == entry) and orders:
            orders = session_auth.my_position(symbol="BTCUSDT")['result'][0]['side'] == 'None'
            entry_2 = session_auth.my_position(symbol="BTCUSDT")['result'][0]['entry_price']
            time.sleep(3)
        if entry_2 != entry:
            print(session_auth.set_trading_stop(
                symbol="BTCUSDT",
                side="Sell",
                take_profit=entry_2-300,
                position_idx=0
            ))
            while (entry_2 == entry) and orders:
                orders = session_auth.my_position(symbol="BTCUSDT")['result'][0]['side'] == 'None'
                time.sleep(5)
            cancel_orders()
        else:
            cancel_orders()
    time.sleep(time.time() - time.time()%3600 + 5)