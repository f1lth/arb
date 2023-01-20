import json
import time
from quickswap import *
from utils import *

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

currentPairs = list()
bestTrades = list()
path = [tokenIn]



def main():
    global pairs, pairsDict # prolly some more...
    start = time.time()
    
    # 1) select relevant pairs


    # 2) get reserves for each pair
    try:
        reserves = get_reserves(pairs)
        end = time.time()
        delta = "{:.3f}".format(end - start)
        bot_print(f"Time to get reserves {delta}s", 'INFO')
    except Exception as e:
        bot_print(f"error: {e}", 'FAIL')
        return
    

    # format time to 3 decimal places

    input()

    # 3) find arb with A *

    # 4) pop the head to see the best trade

    # 5) if trade > min profit , executre


if __name__ == "__main__":
    while True:
        try:
            main()
        except Exception as e:
            print("error in main", e)

