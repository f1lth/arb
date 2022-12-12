import json
from web3 import Web3
from eth_abi import decode_abi
from web3._utils.request import make_post_request
from web3 import HTTPProvider

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
                   FILE: getPairs.py
                   PURPOSE: return a graph of pairs to search

############################################################

#1) generate a json with all pairs

#2) filter the coins by volume > 300

#3) get the reserve prices and format into graph

'''
pairABI = json.load(open('../abi/IUniswapV2Pair.json'))['abi']
qsPairABI = json.load(open('../abi/IUniswapQSPair.json'))['abi']

POLYGON_RPC = "https://polygon-mainnet.g.alchemy.com/v2/CgqAh4Ifjhpq7TBIzigvS1-x9gqfAqCI"
w3 = Web3(Web3.HTTPProvider(POLYGON_RPC))

pairs = json.load(open('../files/pairs.json'))

qs_addy = '0x5757371414417b8C6CAad45bAeF941aBc7d3Ab32'
qs = w3.eth.contract(abi=qsPairABI)

# format the http request and pull the data out of it
def generate_polygon_pairs(blockNumber='latest'):
    pairs = list()
    d = w3.eth.contract(abi=qsPairABI, address=qs_addy)
    total_length_pairs = d.functions.allPairsLength().call()
    print(total_length_pairs)

    TRIAL_LENGTH = 

    for i in range(TRIAL_LENGTH):
        # want reserves amount for each pair in the pairs in factory
        pool_i = d.functions.allPairs(i).call()

        c1 = w3.eth.contract(abi=pairABI, address=pool_i)

        #data = c1.functions.getReserves().call()

        pairs.append(pool_i)

        yield generate_json_rpc(
                method='eth_call',
                params=[{
                    'to': pool_i,
                    'data': c1.encodeABI(fn_name='getReserves', args=[]),
                    },
                    blockNumber ,
                    ]
                )

