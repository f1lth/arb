# import somethings from somewhere

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
                   FILE: search.py
                   PURPOSE: methods to search for arbitrage opportunities
'''


class Search:

    # searhch psudocode:
    #
    # loop through pairs
    #   if (token0 or token1 is tokenIn) skip pair
    #   if (reserve0 or reserve1 is less than 1)  skip pair
    #
    #    set the tempOut to the other token (either token0 or token1) (like if we start in dai and the first pair happens to be a dai pair then start with the other one)
    #    add tempOut to the path 
    #
    #    if we find a pair that has the tokenOut as the tempOut then we have a path and pathlength > 2
    #        calculate Ea and Eb
    #        if Ea and Eb and Ea < Eb (arbitrage opp!!!)
    #            calculate optimalAmount
    #            if optimalAmount > 0
    #                calculate outputAmount
    #                calculate profit
    #                add the trade to the list of bestTrades
    #
    #                sort the list of bestTrades by profit (we should use a different mechanism that is more efficnet than sorting the whole list)
    # 
    #         elif maxHops > 1 and len(pairs) > 1
    #             pairsExcludingThisPair = pairs[:i] + pairs[i+1:]
    #             keep searching for more trades
    #
    #     return bestTrades

    @staticmethod
    def dfs(pairs, tokenIn, tokenOut, maxHops, currentPairs, path, bestTrades, count=5):
        for i in range(len(pairs)):
            newPath = path.copy()
            pair = pairs[i]
            if not pair['token0']['address'] == tokenIn['address'] and not pair['token1']['address'] == tokenIn['address']:
                continue
            if pair['reserve0']/pow(10, pair['token0']['decimal']) < 1 or pair['reserve1']/pow(10, pair['token1']['decimal']) < 1:
                continue
            if tokenIn['address'] == pair['token0']['address']:
                tempOut = pair['token1']
            else:
                tempOut = pair['token0']
            newPath.append(tempOut)
            if tempOut['address'] == tokenOut['address'] and len(path) > 2:
                Ea, Eb = getEaEb(tokenOut, currentPairs + [pair])
                newTrade = { 'route': currentPairs + [pair], 'path': newPath, 'Ea': Ea, 'Eb': Eb }
                if Ea and Eb and Ea < Eb:
                    newTrade['optimalAmount'] = getOptimalAmount(Ea, Eb)
                    if newTrade['optimalAmount'] > 0:
                        newTrade['outputAmount'] = getAmountOut(newTrade['optimalAmount'], Ea, Eb)
                        newTrade['profit'] = newTrade['outputAmount']-newTrade['optimalAmount']
                        newTrade['p'] = int(newTrade['profit'])/pow(10, tokenOut['decimal'])
                    else:
                        continue
                    bestTrades = sortTrades(bestTrades, newTrade)
                    bestTrades.reverse()
                    bestTrades = bestTrades[:count]
            elif maxHops > 1 and len(pairs) > 1:
                pairsExcludingThisPair = pairs[:i] + pairs[i+1:]
                bestTrades = dfs(pairsExcludingThisPair, tempOut, tokenOut, maxHops-1, currentPairs + [pair], newPath, bestTrades, count)
        return bestTrades


    # write psudocode for the function below
    


    @staticmethod
    def astar():
        pass

