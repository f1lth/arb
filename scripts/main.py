import json
import time
from quickswap import *

'''
                        $$\                 $$\    
                        \__|                $$ |   
 $$$$$$\  $$$$$$\$$$$\  $$\ $$$$$$$\   $$$$$$$ |   
$$  __$$\ $$  _$$  _$$\ $$ |$$  __$$\ $$  __$$ |   
$$ /  $$ |$$ / $$ / $$ |$$ |$$ |  $$ |$$ /  $$ |   
$$ |  $$ |$$ | $$ | $$ |$$ |$$ |  $$ |$$ |  $$ |   
\$$$$$$$ |$$ | $$ | $$ |$$ |$$ |  $$ |\$$$$$$$ |   
 \____$$ |\__| \__| \__|\__|\__|  \__| \_______|   
      $$ |                                         
      $$ |         2022  -  2023  season                               
      \__|         DISRUPTIVE TECHNOLOGY 
                   FILE: main.py
                   PURPOSE: main loop execution 
'''

pairs = json.load(open('../files/polygon_pairs.json'))
pairDict = toDict(pairs)

tokenIn = ['USDC', 'DAI', "USDT","FRAX", "WETH", "ETH"]
tokenIn = ['USDC', 'DAI', "USDT","FRAX", "WETH", "ETH"]

currentPairs = list()
bestTrades = list()
path = [tokenIn]



def main():
    global pairs, pairsDict # prolly some more...
    start = int(time.time())
    
    # 1) select relevant pairs

    # @@@ !!!! Plzzz someone figure this out :)))
    # @@@ 1!!! i want to sort our pairs by liquidity or volume kthx

    # 2) get reserves for each pair
    try:
        reserves = get_reserves(pairs)
    except Exception as e:
        print("error getting reserves", e)
        return
    end = int(time.time())

    print("time to get reserves", end - start)
    print(reserves)
    # 3) find arb with A *

    # 4) pop the head to see the best trade

    # 5) if trade > min profit , executre


main()